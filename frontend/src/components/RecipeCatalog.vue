<script setup>
import { computed, ref, watch } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import RecipeCard from '@/components/RecipeCard.vue'
import { receitasComposables } from '@/composables/receitasComposables'

defineProps({
  isSearch: Boolean,
})

const router = useRouter()
const {
  categoriaId,
  termo,
  receitas,
  categorias,
  erro,
  erroCategorias,
  carregando,
  carregandoCategorias,
  recarregarReceitas,
  recarregarCategorias,
} = receitasComposables()

const categoriaSelecionada = ref('')
const textoBusca = ref('')
const filtrosAtivos = computed(() => Boolean(categoriaId.value || termo.value))

watch([categoriaId, termo], ([categoria, busca]) => {
  categoriaSelecionada.value = categoria
  textoBusca.value = busca
}, { immediate: true })

function buscar() {
  const categoria = categoriaSelecionada.value
  const busca = textoBusca.value.trim()
  const query = {}

  if (categoria) query.categoria_id = categoria
  if (busca) query.search = busca
  if (!categoria && !busca) return router.push({ name: 'receitas' })

  return router.push({ path: '/receitas/pesquisar', query })
}
</script>

<template>
  <div class="recipe-catalog page-shell">
    <header class="recipe-catalog__header">
      <nav class="recipe-catalog__breadcrumbs" aria-label="Localização">
        <RouterLink :to="{ name: 'home' }">Início</RouterLink>
        <span aria-hidden="true">/</span>
        <template v-if="isSearch">
          <RouterLink :to="{ name: 'receitas' }">Receitas</RouterLink>
          <span aria-hidden="true">/</span>
          <span aria-current="page">Busca</span>
        </template>
        <span v-else aria-current="page">Receitas</span>
      </nav>
      <h1>{{ isSearch ? 'Buscar receitas' : 'Receitas' }}</h1>
      <p>Encontre sua próxima receita pelo nome ou pela categoria</p>
    </header>

    <form class="recipe-catalog__filter" role="search" aria-label="Filtrar receitas" @submit.prevent="buscar">
      <label class="field">
        <span>Nome da receita</span>
        <input v-model="textoBusca" type="search" name="search" placeholder="Ex. bolo de chocolate" />
      </label>

      <label class="field">
        <span>Categoria</span>
        <select v-model="categoriaSelecionada" name="categoria_id" :disabled="carregandoCategorias || Boolean(erroCategorias)">
          <option value="">{{ carregandoCategorias ? 'Carregando categorias…' : 'Todas as categorias' }}</option>
          <option v-for="categoria in categorias" :key="categoria.id" :value="String(categoria.id)">{{ categoria.nome }}</option>
        </select>
      </label>

      <button class="button button--primary recipe-catalog__submit" type="submit">Buscar</button>
      <p v-if="erroCategorias" class="recipe-catalog__filter-error" role="status">
        Não foi possível carregar as categorias.
        <button type="button" @click="recarregarCategorias">Tentar novamente</button>
      </p>
    </form>

    <section class="recipe-catalog__results" aria-labelledby="recipe-results-title" :aria-busy="carregando">
      <div class="recipe-catalog__heading">
        <div>
          <h2 id="recipe-results-title">{{ isSearch ? 'Resultados da busca' : 'Todas as receitas' }}</h2>
          <p v-if="!carregando && !erro" role="status">
            {{ receitas.length }} {{ receitas.length === 1 ? 'receita' : 'receitas' }}
          </p>
        </div>

        <RouterLink v-if="filtrosAtivos" class="recipe-catalog__clear" :to="{ name: 'receitas' }">
          Limpar filtros
        </RouterLink>
      </div>

      <p v-if="carregando" class="recipe-catalog__state" role="status">Carregando receitas…</p>
      <div v-else-if="erro" class="recipe-catalog__state" role="status">
        <h3>Não foi possível carregar as receitas</h3>
        <button class="button button--secondary" type="button" @click="recarregarReceitas">
          Tentar novamente
        </button>
      </div>
      <div v-else-if="!receitas.length" class="recipe-catalog__state">
        <h3>{{ filtrosAtivos ? 'Nenhuma receita encontrada' : 'Nenhuma receita publicada' }}</h3>
        <p v-if="filtrosAtivos">Tente buscar por outro nome ou escolher outra categoria.</p>
      </div>
      <ul v-else class="recipe-catalog__grid">
        <li v-for="receita in receitas" :key="receita.id ?? receita.slug">
          <RecipeCard :recipe="receita" />
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.recipe-catalog {
  padding-block: clamp(2rem, 6.5vw, 5.5rem) clamp(4rem, 8vw, 7.5rem);
}

.recipe-catalog__header {
  position: relative;
  isolation: isolate;
}

.recipe-catalog__header::after {
  position: absolute;
  z-index: -1;
  inset: -5rem 0 -1rem 0;
  background: radial-gradient(ellipse at 78% 22%, rgb(141 91 240 / 12%), transparent 65%);
  content: '';
  pointer-events: none;
}

.recipe-catalog__breadcrumbs {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.6rem;
  margin-bottom: clamp(1.35rem, 3vw, 2rem);
  color: var(--muted);
  font-size: 0.88rem;
}

.recipe-catalog__breadcrumbs a,
.recipe-catalog__clear {
  color: var(--accent);
  text-decoration: none;
}

.recipe-catalog__breadcrumbs a:hover,
.recipe-catalog__clear:hover {
  text-decoration: underline;
}

.recipe-catalog__header h1 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(3rem, 7vw, 6.2rem);
  line-height: 1;
  letter-spacing: -0.055em;
}

.recipe-catalog__header p {
  margin: 1rem 0 0;
  color: var(--muted);
  font-size: clamp(1rem, 2vw, 1.15rem);
}

.recipe-catalog__filter {
  display: grid;
  grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr) auto;
  align-items: end;
  gap: 1rem;
  margin-top: clamp(1.6rem, 5vw, 2.7rem);
  padding: clamp(1rem, 3vw, 1.55rem);
  border: 1px solid var(--line);
  border-radius: 20px;
  background: var(--surface);
}

.recipe-catalog__submit {
  min-width: 7rem;
  min-height: 48px;
}

.recipe-catalog__filter-error {
  grid-column: 1 / -1;
  margin: 0;
  color: var(--muted);
  font-size: 0.88rem;
}

.recipe-catalog__filter-error button {
  padding: 0;
  border: 0;
  background: none;
  color: var(--accent);
  font: inherit;
  text-decoration: underline;
  cursor: pointer;
}

.recipe-catalog__results {
  margin-top: clamp(2.8rem, 7vw, 5rem);
}

.recipe-catalog__heading {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.35rem;
}

.recipe-catalog__heading h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 3vw, 2.45rem);
  line-height: 1.1;
  letter-spacing: -0.04em;
}

.recipe-catalog__heading p {
  margin: 0.35rem 0 0;
  color: var(--muted);
  font-size: 0.88rem;
}

.recipe-catalog__clear {
  font-size: 0.94rem;
  font-weight: 600;
}

.recipe-catalog__grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1.25rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.recipe-catalog__state {
  margin: 0;
  padding: clamp(1.75rem, 7vw, 3.5rem) 1rem;
  border: 1px solid var(--line);
  border-radius: 20px;
  background: var(--surface);
  color: var(--muted);
  text-align: center;
}

.recipe-catalog__state h3 {
  margin: 0;
  color: var(--text);
  font-family: var(--font-display);
  font-size: clamp(1.1rem, 3vw, 1.45rem);
}

.recipe-catalog__state p,
.recipe-catalog__state button {
  margin-top: 0.9rem;
}

@media (max-width: 760px) {
  .recipe-catalog__filter,
  .recipe-catalog__grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .recipe-catalog__submit {
    grid-column: 1 / -1;
    justify-self: start;
  }
}

@media (max-width: 480px) {
  .recipe-catalog__filter,
  .recipe-catalog__grid {
    grid-template-columns: minmax(0, 1fr);
  }

  .recipe-catalog__submit {
    justify-self: stretch;
  }
}
</style>
