<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { ErrorMessage, Field, Form } from 'vee-validate'
import axios from 'axios'
import { receitasSchema } from '@/schemas/validacoesSchema'
import { apiUrl } from '@/services/apiUrl'
import { useAuthStore } from '@/stores/authStore'

defineOptions({ name: 'PaginaPainel' })

const auth = useAuthStore()
const receitas = ref([])
const categorias = ref([])
const carregando = ref(true)
const erroPainel = ref('')
const aviso = ref('')

const dialogo = ref(null)
const modo = ref('')
const receitaSelecionada = ref(null)
const camposIniciais = ref(null)
const foto = ref(null)
const erroDialogo = ref('')
const carregandoEdicao = ref(false)
const salvando = ref(false)
let requisicaoEdicao

function configAutenticada() {
  return { headers: { Authorization: `Bearer ${auth.authToken}` } }
}

async function carregarPainel() {
  carregando.value = true
  erroPainel.value = ''

  try {
    const [receitasResposta, categoriasResposta] = await Promise.all([
      axios.get(apiUrl(`receitas-painel/${auth.authId}`), configAutenticada()),
      axios.get(apiUrl('categorias')),
    ])

    if (!Array.isArray(receitasResposta.data.data) || !Array.isArray(categoriasResposta.data.data)) {
      throw new Error('Resposta inesperada ao carregar o painel')
    }

    receitas.value = receitasResposta.data.data
    categorias.value = categoriasResposta.data.data
  } catch {
    erroPainel.value = 'Não foi possível carregar suas receitas'
  } finally {
    carregando.value = false
  }
}

onMounted(carregarPainel)
onBeforeUnmount(() => requisicaoEdicao?.abort())

async function abrirDialogo(acao, receita = null) {
  modo.value = acao
  receitaSelecionada.value = receita
  foto.value = null
  erroDialogo.value = ''
  camposIniciais.value = acao === 'criar'
    ? { categoria_id: '0', nome: '', tempo: '', descricao: '' }
    : null

  carregandoEdicao.value = acao === 'editar'
  await nextTick()
  dialogo.value?.showModal()

  if (acao === 'editar') {
    await carregarCampos()
  }
}

async function carregarCampos() {
  requisicaoEdicao = new AbortController()
  const { signal } = requisicaoEdicao
  carregandoEdicao.value = true
  erroDialogo.value = ''

  try {
    const resposta = await axios.get(apiUrl(`receitas/${receitaSelecionada.value.id}`), { signal })
    const { categoria_id, nome, tempo, descricao } = resposta.data.data
    camposIniciais.value = { categoria_id: String(categoria_id), nome, tempo, descricao }
  } catch {
    if (!signal.aborted) {
      erroDialogo.value = 'Não foi possível abrir os dados da receita'
    }
  } finally {
    if (!signal.aborted) {
      carregandoEdicao.value = false
    }
  }
}

function limparDialogo() {
  requisicaoEdicao?.abort()
  modo.value = ''
}

function fecharDialogo() {
  if (!salvando.value) {
    dialogo.value.close()
  }
}

function cancelarDialogo(event) {
  if (salvando.value) {
    event.preventDefault()
  }
}

async function salvarReceita(campos) {
  erroDialogo.value = ''

  if (modo.value === 'criar' && !foto.value) {
    erroDialogo.value = 'Selecione uma foto JPG ou PNG'
    return
  }

  salvando.value = true
  try {
    if (modo.value === 'criar') {
      const corpo = new FormData()
      for (const [campo, valor] of Object.entries(campos)) {
        corpo.append(campo, valor)
      }
      corpo.append('foto', foto.value)
      await axios.post(apiUrl('receitas'), corpo, configAutenticada())
      aviso.value = 'Receita publicada com sucesso'
    } else {
      await axios.put(apiUrl(`receitas/${receitaSelecionada.value.id}`), campos, configAutenticada())
      aviso.value = 'Receita atualizada com sucesso'
    }

    dialogo.value.close()
    await carregarPainel()
  } catch (erro) {
    erroDialogo.value = erro.response?.data?.error || 'Não foi possível salvar a receita'
  } finally {
    salvando.value = false
  }
}

async function excluirReceita() {
  erroDialogo.value = ''
  salvando.value = true

  try {
    await axios.delete(apiUrl(`receitas/${receitaSelecionada.value.id}`), configAutenticada())
    aviso.value = 'Receita excluída'
    dialogo.value.close()
    await carregarPainel()
  } catch (erro) {
    erroDialogo.value = erro.response?.data?.error || 'Não foi possível excluir a receita.'
  } finally {
    salvando.value = false
  }
}
</script>

<template>
  <section class="page-shell dashboard" aria-labelledby="dashboard-title">
    <header class="dashboard-heading">
      <div>
        <p class="eyebrow">Minha conta</p>
        <h1 id="dashboard-title">Minhas receitas</h1>
        <p v-if="!carregando && !erroPainel" class="recipe-count">
          {{ receitas.length }} {{ receitas.length === 1 ? 'receita publicada' : 'receitas publicadas' }}
        </p>
      </div>
      <button
        class="button button--primary"
        type="button"
        :disabled="carregando || !!erroPainel"
        @click="abrirDialogo('criar')"
      >
        <span aria-hidden="true">+</span> Nova receita
      </button>
    </header>

    <p v-if="aviso" class="dashboard-feedback" role="status">{{ aviso }}</p>

    <div v-if="carregando" class="dashboard-state" role="status">Carregando receitas…</div>
    <div v-else-if="erroPainel" class="dashboard-state">
      <p role="alert">{{ erroPainel }}</p>
      <button class="button button--secondary" type="button" @click="carregarPainel">
        Tentar novamente
      </button>
    </div>
    <div v-else-if="!receitas.length" class="dashboard-state">
      <h2>Sua primeira receita</h2>
      <p>Publique uma receita para encontrá-la aqui</p>
    </div>

    <ul v-else class="recipe-list" aria-label="Receitas publicadas">
      <li v-for="receita in receitas" :key="receita.id" class="recipe-row">
        <button
          class="recipe-photo"
          type="button"
          :aria-label="`Ampliar foto de ${receita.nome}`"
          @click="abrirDialogo('foto', receita)"
        >
          <img :src="receita.imagem" alt="" loading="lazy" />
        </button>
        <div class="recipe-info">
          <p class="recipe-category">{{ receita.categoria }}</p>
          <h2>
            <RouterLink :to="{ name: 'receitasDetalhes', params: { slug: receita.slug } }">
              {{ receita.nome }}
            </RouterLink>
          </h2>
          <p class="recipe-description">{{ receita.descricao }}</p>
          <p class="recipe-time">{{ receita.tempo }}</p>
        </div>
        <div class="recipe-actions">
          <button class="button button--secondary" type="button" @click="abrirDialogo('editar', receita)">
            Editar
          </button>
          <RouterLink
            class="button button--secondary"
            :to="{ name: 'painel_editar', params: { id: receita.id } }"
          >
            Trocar foto
          </RouterLink>
          <button class="button button--secondary danger-action" type="button" @click="abrirDialogo('excluir', receita)">
            Excluir
          </button>
        </div>
      </li>
    </ul>

    <dialog
      ref="dialogo"
      class="recipe-dialog"
      :class="{ 'recipe-dialog--photo': modo === 'foto' }"
      aria-labelledby="recipe-dialog-title"
      @cancel="cancelarDialogo"
      @close="limparDialogo"
    >
      <template v-if="modo === 'criar' || modo === 'editar'">
        <header class="dialog-heading">
          <h2 id="recipe-dialog-title">{{ modo === 'criar' ? 'Nova receita' : 'Editar receita' }}</h2>
          <button
            class="dialog-close"
            type="button"
            aria-label="Fechar"
            :disabled="salvando"
            @click="fecharDialogo"
          >×</button>
        </header>

        <p v-if="carregandoEdicao" role="status">Carregando dados da receita…</p>
        <div v-else-if="!camposIniciais" class="dialog-retry">
          <p class="form-error" role="alert">{{ erroDialogo }}</p>
          <button class="button button--secondary" type="button" @click="carregarCampos">
            Tentar novamente
          </button>
        </div>
        <Form
          v-else
          v-slot="{ errors }"
          :validation-schema="receitasSchema"
          :initial-values="camposIniciais"
          @submit="salvarReceita"
        >
          <fieldset class="recipe-fields" :disabled="salvando">
            <label class="field">
              <span>Categoria</span>
              <Field
                as="select"
                name="categoria_id"
                :aria-invalid="!!errors.categoria_id"
                :aria-describedby="errors.categoria_id ? 'recipe-category-error' : undefined"
              >
                <option value="0" disabled>Selecione uma categoria</option>
                <option v-for="categoria in categorias" :key="categoria.id" :value="String(categoria.id)">
                  {{ categoria.nome }}
                </option>
              </Field>
              <ErrorMessage id="recipe-category-error" name="categoria_id" class="form-error" />
            </label>
            <label class="field">
              <span>Nome da receita</span>
              <Field
                name="nome"
                :aria-invalid="!!errors.nome"
                :aria-describedby="errors.nome ? 'recipe-name-error' : undefined"
              />
              <ErrorMessage id="recipe-name-error" name="nome" class="form-error" />
            </label>
            <label class="field">
              <span>Tempo de preparo</span>
              <Field
                name="tempo"
                placeholder="Ex. 45 minutos"
                :aria-invalid="!!errors.tempo"
                :aria-describedby="errors.tempo ? 'recipe-time-error' : undefined"
              />
              <ErrorMessage id="recipe-time-error" name="tempo" class="form-error" />
            </label>
            <label class="field">
              <span>Descrição</span>
              <Field
                as="textarea"
                name="descricao"
                rows="4"
                :aria-invalid="!!errors.descricao"
                :aria-describedby="errors.descricao ? 'recipe-description-error' : undefined"
              />
              <ErrorMessage id="recipe-description-error" name="descricao" class="form-error" />
            </label>
            <label v-if="modo === 'criar'" class="field">
              <span>Foto (JPG ou PNG)</span>
              <input type="file" name="foto" accept="image/jpeg,image/png" @change="foto = $event.target.files[0]" />
            </label>
          </fieldset>

          <p v-if="erroDialogo" class="form-error" role="alert">{{ erroDialogo }}</p>
          <div class="dialog-actions">
            <button class="button button--secondary" type="button" :disabled="salvando" @click="fecharDialogo">
              Cancelar
            </button>
            <button class="button button--primary" type="submit" :disabled="salvando">
              {{ salvando ? 'Salvando…' : 'Salvar receita' }}
            </button>
          </div>
        </Form>
      </template>

      <template v-else-if="modo === 'excluir'">
        <h2 id="recipe-dialog-title">Excluir receita?</h2>
        <p>
          A receita <strong>{{ receitaSelecionada.nome }}</strong> será removida do catálogo
        </p>
        <p v-if="erroDialogo" class="form-error" role="alert">{{ erroDialogo }}</p>
        <div class="dialog-actions">
          <button class="button button--secondary" type="button" :disabled="salvando" @click="fecharDialogo">
            Cancelar
          </button>
          <button class="button danger-button" type="button" :disabled="salvando" @click="excluirReceita">
            {{ salvando ? 'Excluindo…' : 'Excluir receita' }}
          </button>
        </div>
      </template>

      <template v-else-if="modo === 'foto'">
        <header class="dialog-heading">
          <h2 id="recipe-dialog-title">{{ receitaSelecionada.nome }}</h2>
          <button class="dialog-close" type="button" aria-label="Fechar foto" @click="fecharDialogo">×</button>
        </header>
        <img class="enlarged-photo" :src="receitaSelecionada.imagem" :alt="receitaSelecionada.nome" />
      </template>
    </dialog>
  </section>
</template>

<style scoped>
.dashboard {
  padding-block: clamp(3rem, 7vw, 6.25rem);
}

.dashboard-heading {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem 2rem;
  margin-bottom: 2.2rem;
}

.dashboard-heading h1 {
  margin: 0.55rem 0 0;
  font-family: var(--font-display);
  font-size: clamp(2.55rem, 6.2vw, 5.25rem);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.07em;
}

.recipe-count {
  margin: 0.85rem 0 0;
  color: var(--muted);
}

.dashboard-feedback,
.dashboard-state {
  border: 1px solid var(--line);
  border-radius: 16px;
  background: var(--surface);
}

.dashboard-feedback {
  margin: 0 0 1rem;
  padding: 0.85rem 1rem;
  color: var(--accent);
}

.dashboard-state {
  padding: clamp(1.75rem, 6vw, 4rem) 1rem;
  text-align: center;
  color: var(--muted);
}

.dashboard-state h2 {
  margin: 0 0 0.4rem;
  color: var(--text);
  font-size: 1.35rem;
}

.dashboard-state p {
  margin: 0 0 0.75rem;
}

.recipe-list {
  display: grid;
  gap: 0.8rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.recipe-row {
  display: grid;
  grid-template-columns: 110px minmax(0, 1fr) auto;
  align-items: center;
  gap: 1.2rem;
  padding: 0.9rem;
  border: 1px solid var(--line);
  border-radius: 20px;
  background: var(--surface);
}

.recipe-photo {
  display: block;
  aspect-ratio: 1.12;
  overflow: hidden;
  padding: 0;
  border: 0;
  border-radius: 12px;
  background: var(--surface-raised);
  cursor: zoom-in;
}

.recipe-photo img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.recipe-info {
  min-width: 0;
}

.recipe-info h2 {
  margin: 0.15rem 0;
  font-family: var(--font-display);
  font-size: clamp(1.2rem, 2vw, 1.55rem);
  line-height: 1.2;
  overflow-wrap: anywhere;
}

.recipe-info a {
  color: var(--text);
  text-decoration: none;
}

.recipe-info a:hover {
  color: var(--accent);
}

.recipe-category,
.recipe-time,
.recipe-description {
  margin: 0;
  font-size: 0.85rem;
  color: var(--muted);
}

.recipe-category {
  color: var(--accent);
  font-weight: 600;
}

.recipe-description {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recipe-time {
  margin-top: 0.3rem;
}

.recipe-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
}

.recipe-actions .button {
  min-height: 2.65rem;
  padding: 0.45rem 0.8rem;
  font-size: 0.83rem;
}

.danger-action,
.form-error {
  color: #ffb3c2;
}

.recipe-dialog {
  box-sizing: border-box;
  width: min(100% - 2rem, 34rem);
  max-width: unset;
  max-height: calc(100dvh - 2rem);
  margin: auto;
  padding: clamp(1.15rem, 4vw, 1.8rem);
  overflow: auto;
  border: 1px solid var(--line);
  border-radius: 20px;
  color: var(--text);
  background: var(--surface);
}

.recipe-dialog::backdrop {
  background: rgb(8 5 13 / 0.78);
  backdrop-filter: blur(5px);
}

.recipe-dialog--photo {
  width: min(100% - 2rem, 52rem);
}

.recipe-dialog h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 4vw, 2rem);
  line-height: 1.1;
  letter-spacing: -0.04em;
  overflow-wrap: anywhere;
}

.dialog-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.25rem;
}

.dialog-close {
  display: grid;
  flex: 0 0 auto;
  width: 2.5rem;
  height: 2.5rem;
  place-items: center;
  padding: 0;
  border: 1px solid var(--line);
  border-radius: 50%;
  color: var(--text);
  background: var(--surface-raised);
  font-size: 1.35rem;
  cursor: pointer;
}

.recipe-fields {
  display: grid;
  gap: 0.8rem;
  min-width: 0;
  margin: 0;
  padding: 0;
  border: 0;
}

.recipe-fields textarea {
  resize: vertical;
}

.dialog-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 0.55rem;
  margin-top: 1.35rem;
}

.form-error {
  font-size: 0.85rem;
}

.danger-button {
  color: #2b0915;
  background: #ffb3c2;
}

.enlarged-photo {
  display: block;
  width: 100%;
  max-height: min(66dvh, 32rem);
  object-fit: contain;
  border-radius: 12px;
  background: var(--bg);
}

.recipe-fields input[type='file'] {
  max-width: 100%;
}

.recipe-fields input::file-selector-button {
  margin-right: 0.6rem;
  padding: 0.35rem 0.55rem;
  border: 0;
  border-radius: 6px;
  color: var(--text);
  background: var(--surface-raised);
  font: inherit;
  cursor: pointer;
}

@media (max-width: 760px) {
  .recipe-row {
    grid-template-columns: minmax(3.9rem, 24%) minmax(0, 1fr);
    gap: 0.7rem 0.9rem;
  }

  .recipe-actions {
    grid-column: 1 / -1;
    padding-top: 0.65rem;
    border-top: 1px solid var(--line);
  }
}
</style>
