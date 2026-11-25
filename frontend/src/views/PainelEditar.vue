<script setup>
import { onBeforeUnmount, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { apiUrl } from '@/services/apiUrl'
import { useAuthStore } from '@/stores/authStore'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const receita = ref(null)
const foto = ref(null)
const previa = ref('')
const carregando = ref(true)
const salvando = ref(false)
const erroCarga = ref('')
const erroEnvio = ref('')
let requisicao

function limparSelecao() {
  if (previa.value) {
    URL.revokeObjectURL(previa.value)
  }
  previa.value = ''
  foto.value = null
}

async function carregarReceita(id = route.params.id) {
  requisicao?.abort()
  requisicao = new AbortController()
  const { signal } = requisicao
  carregando.value = true
  erroCarga.value = ''
  erroEnvio.value = ''
  limparSelecao()

  try {
    const resposta = await axios.get(apiUrl(`receitas/${id}`), { signal })
    receita.value = resposta.data.data
  } catch {
    if (!signal.aborted) {
      erroCarga.value = 'Não foi possível carregar esta receita.'
    }
  } finally {
    if (!signal.aborted) {
      carregando.value = false
    }
  }
}

watch(() => route.params.id, carregarReceita, { immediate: true })

onBeforeUnmount(() => {
  requisicao?.abort()
  limparSelecao()
})

function selecionarFoto(event) {
  limparSelecao()
  erroEnvio.value = ''
  const arquivo = event.target.files[0]
  if (!arquivo) {
    return
  }

  if (!['image/jpeg', 'image/png'].includes(arquivo.type)) {
    event.target.value = ''
    erroEnvio.value = 'Selecione uma foto JPG ou PNG.'
    return
  }

  foto.value = arquivo
  previa.value = URL.createObjectURL(arquivo)
}

async function salvarFoto() {
  if (!foto.value || salvando.value) {
    return
  }

  const id = route.params.id
  const corpo = new FormData()
  corpo.append('foto', foto.value)
  corpo.append('id', id)

  salvando.value = true
  erroEnvio.value = ''

  try {
    await axios.post(apiUrl('receitas/editar/foto'), corpo, {
      headers: { Authorization: `Bearer ${auth.authToken}` },
    })

    if (route.name === 'painel_editar' && route.params.id === id) {
      await router.push({ name: 'painel' })
    }
  } catch (erro) {
    erroEnvio.value = erro.response?.data?.error || 'Não foi possível salvar a foto.'
  } finally {
    salvando.value = false
  }
}
</script>

<template>
  <section class="page-shell photo-editor" aria-labelledby="photo-editor-title">
    <RouterLink class="back-link" :to="{ name: 'painel' }">
      <span aria-hidden="true">←</span> Minhas receitas
    </RouterLink>
    <h1 id="photo-editor-title">Editar foto</h1>

    <div v-if="carregando" class="photo-editor-state" role="status">Carregando receita…</div>
    <div v-else-if="erroCarga" class="photo-editor-state">
      <p role="alert">{{ erroCarga }}</p>
      <button class="button button--secondary" type="button" @click="carregarReceita()">
        Tentar novamente
      </button>
    </div>

    <div v-else class="photo-editor-card">
      <figure class="photo-preview">
        <img :src="previa || receita.imagem" :alt="receita.nome" />
        <figcaption>{{ previa ? 'Prévia da nova foto' : 'Foto atual' }}</figcaption>
      </figure>

      <form class="photo-form" @submit.prevent="salvarFoto">
        <h2>{{ receita.nome }}</h2>
        <label class="field">
          <span>Nova foto</span>
          <input
            type="file"
            name="foto"
            accept="image/jpeg,image/png"
            aria-describedby="photo-format"
            :disabled="salvando"
            @change="selecionarFoto"
          />
        </label>
        <p id="photo-format" class="photo-hint">Formatos aceitos: JPG e PNG.</p>

        <p v-if="erroEnvio" class="photo-error" role="alert">{{ erroEnvio }}</p>
        <div class="photo-actions">
          <RouterLink class="button button--secondary" :to="{ name: 'painel' }">
            Cancelar
          </RouterLink>
          <button class="button button--primary" type="submit" :disabled="salvando || !foto">
            {{ salvando ? 'Salvando…' : 'Salvar foto' }}
          </button>
        </div>
      </form>
    </div>
  </section>
</template>

<style scoped>
.photo-editor {
  padding-block: clamp(3rem, 7vw, 6.25rem);
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  color: var(--accent);
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: none;
}

.back-link:hover {
  text-decoration: underline;
}

.photo-editor h1 {
  margin: 0.8rem 0 1.75rem;
  font-family: var(--font-display);
  font-size: clamp(2.55rem, 6.2vw, 5.25rem);
  font-weight: 700;
  line-height: 1.05;
  letter-spacing: -0.07em;
}

.photo-editor-card,
.photo-editor-state {
  max-width: 58rem;
  border: 1px solid var(--line);
  border-radius: 22px;
  background: var(--surface);
}

.photo-editor-card {
  display: grid;
  grid-template-columns: 1fr minmax(0, 1.1fr);
  align-items: center;
  gap: clamp(1rem, 4vw, 2.5rem);
  padding: clamp(1rem, 4vw, 2rem);
}

.photo-editor-state {
  padding: clamp(1.75rem, 6vw, 4rem) 1rem;
  text-align: center;
  color: var(--muted);
}

.photo-editor-state p {
  margin: 0 0 0.75rem;
}

.photo-preview {
  position: relative;
  display: grid;
  margin: 0;
}

.photo-preview img {
  display: block;
  width: 100%;
  aspect-ratio: 4 / 3;
  border-radius: 14px;
  object-fit: cover;
  color: var(--muted);
  background: var(--surface-raised);
}

.photo-preview figcaption {
  position: absolute;
  bottom: 0.7rem;
  left: 0.7rem;
  padding: 0.25rem 0.7rem;
  border: 1px solid rgb(248 245 252 / 0.18);
  border-radius: 999px;
  color: #f8f5fc;
  background: rgb(17 14 23 / 0.88);
  font-size: 0.77rem;
}

.photo-form {
  min-width: 0;
}

.photo-form h2 {
  margin: 0 0 1.25rem;
  font-family: var(--font-display);
  font-size: clamp(1.35rem, 4vw, 2.1rem);
  line-height: 1.1;
  letter-spacing: -0.035em;
  overflow-wrap: anywhere;
}

.photo-form input[type='file'] {
  width: 100%;
}

.photo-form input::file-selector-button {
  margin-right: 0.6rem;
  padding: 0.35rem 0.55rem;
  border: 0;
  border-radius: 6px;
  color: var(--text);
  background: var(--surface-raised);
  font: inherit;
  cursor: pointer;
}

.photo-hint,
.photo-error {
  margin: 0.45rem 0 0;
  color: var(--muted);
  font-size: 0.85rem;
}

.photo-error {
  color: #ffb3c2;
}

.photo-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.55rem;
  margin-top: 1.25rem;
}

@media (max-width: 700px) {
  .photo-editor-card {
    grid-template-columns: minmax(0, 1fr);
    gap: 1.2rem;
  }
}
</style>
