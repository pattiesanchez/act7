<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { receitaComposable } from '@/composables/receitaCompos'

const route = useRoute()
const { receita, erro, naoEncontrada, carregando, recarregar } = receitaComposable(() => route.params.slug)
const failedImage = ref(null)
</script>

<template>
  <div class="recipe-detail page-shell">
    <RouterLink class="recipe-detail__back" :to="{ name: 'receitas' }">
      <span aria-hidden="true">←</span> Todas as receitas
    </RouterLink>

    <p v-if="carregando" class="recipe-detail__state" role="status">Carregando receita…</p>
    <div v-else-if="naoEncontrada" class="recipe-detail__state">
      <h1>Receita não encontrada</h1>
      <p>Explore o catálogo para encontrar outra receita.</p>
      <RouterLink class="button button--primary" :to="{ name: 'receitas' }">Ver receitas</RouterLink>
    </div>
    <div v-else-if="erro" class="recipe-detail__state">
      <h1>Não foi possível carregar a receita</h1>
      <button class="button button--secondary" type="button" @click="recarregar">
        Tentar novamente
      </button>
    </div>

    <article v-else-if="receita" class="recipe-detail__article">
      <div class="recipe-detail__hero">
        <header class="recipe-detail__header">
          <RouterLink
            v-if="receita.categoria && receita.categoria_id"
            class="eyebrow recipe-detail__category"
            :to="{ path: '/receitas/pesquisar', query: { categoria_id: receita.categoria_id } }"
          >
            {{ receita.categoria }}
          </RouterLink>
          <p v-else-if="receita.categoria" class="eyebrow recipe-detail__category">{{ receita.categoria }}</p>

          <h1>{{ receita.nome }}</h1>
          <dl v-if="receita.tempo || receita.user || receita.data" class="recipe-detail__metadata">
            <div v-if="receita.tempo">
              <dt>Tempo de preparo</dt>
              <dd>{{ receita.tempo }}</dd>
            </div>
            <div v-if="receita.user">
              <dt>Autoria</dt>
              <dd>{{ receita.user }}</dd>
            </div>
            <div v-if="receita.data">
              <dt>Publicação</dt>
              <dd>{{ receita.data.split(' ')[0] }}</dd>
            </div>
          </dl>
        </header>

        <figure class="recipe-detail__media">
          <img
            v-if="receita.imagem && receita.imagem !== failedImage"
            :src="receita.imagem"
            :alt="receita.nome"
            width="800"
            height="640"
            fetchpriority="high"
            @error="failedImage = receita.imagem"
          />
          <span v-else>Foto indisponível</span>
        </figure>
      </div>

      <section class="recipe-detail__preparation" aria-labelledby="preparation-title">
        <h2 id="preparation-title">Modo de preparo</h2>
        <p>{{ receita.descricao }}</p>
      </section>
    </article>
  </div>
</template>

<style scoped>
.recipe-detail {
  padding-block: clamp(1.8rem, 5vw, 4rem) clamp(4rem, 8vw, 7.5rem);
}

.recipe-detail__back {
  display: inline-flex;
  align-items: center;
  gap: 0.55rem;
  min-height: 44px;
  margin-bottom: clamp(1.25rem, 4vw, 2rem);
  color: var(--accent);
  font-size: 0.92rem;
  font-weight: 650;
  text-decoration: none;
}

.recipe-detail__back:hover,
a.recipe-detail__category:hover {
  text-decoration: underline;
}

.recipe-detail__hero {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1fr);
  align-items: center;
  gap: clamp(1.5rem, 5vw, 4.5rem);
}

.recipe-detail__category {
  display: inline-block;
  margin: 0 0 0.85rem;
  color: var(--accent);
  text-decoration: none;
}

.recipe-detail__header h1 {
  margin: 0;
  color: var(--text);
  font-family: var(--font-display);
  font-size: clamp(2.6rem, 5.4vw, 5.6rem);
  line-height: 0.99;
  letter-spacing: -0.055em;
  overflow-wrap: anywhere;
}

.recipe-detail__metadata {
  display: flex;
  flex-wrap: wrap;
  gap: 1.15rem clamp(1rem, 2.35vw, 2rem);
  margin: clamp(1.25rem, 3vw, 2.3rem) 0 0;
  padding-top: 1.2rem;
  border-top: 1px solid var(--line);
}

.recipe-detail__metadata div {
  min-width: 0;
}

.recipe-detail__metadata dt {
  color: var(--muted);
  font-size: 0.83rem;
}

.recipe-detail__metadata dd {
  margin: 0.35rem 0 0;
  color: var(--text);
  font-size: 0.95rem;
  font-weight: 650;
  overflow-wrap: anywhere;
}

.recipe-detail__media {
  display: grid;
  place-items: center;
  overflow: hidden;
  aspect-ratio: 5 / 4;
  margin: 0;
  border: 1px solid var(--line);
  border-radius: clamp(1rem, 3vw, 1.6rem);
  background: linear-gradient(140deg, var(--surface-raised), var(--surface));
  color: var(--muted);
}

.recipe-detail__media img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.recipe-detail__preparation {
  display: grid;
  grid-template-columns: minmax(0, 0.4fr) minmax(0, 1fr);
  gap: 1.25rem 2.25rem;
  margin-top: clamp(2rem, 6vw, 4.5rem);
  padding: clamp(1.25rem, 4vw, 2.8rem);
  border: 1px solid var(--line);
  border-radius: 20px;
  background: var(--surface);
}

.recipe-detail__preparation h2 {
  margin: 0;
  font-family: var(--font-display);
  font-size: clamp(1.4rem, 3vw, 2.35rem);
  line-height: 1.1;
  letter-spacing: -0.035em;
}

.recipe-detail__preparation p {
  max-width: 68ch;
  margin: 0;
  color: var(--muted);
  font-size: 1.05rem;
  line-height: 1.85;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
}

.recipe-detail__state {
  margin: 0;
  padding: clamp(1.75rem, 7vw, 3.5rem) 1rem;
  border: 1px solid var(--line);
  border-radius: 20px;
  background: var(--surface);
  color: var(--muted);
  text-align: center;
}

.recipe-detail__state h1 {
  margin: 0 0 0.8rem;
  color: var(--text);
  font-family: var(--font-display);
  font-size: clamp(1.45rem, 4vw, 2rem);
}

.recipe-detail__state p {
  margin: 0 0 1.25rem;
}

@media (max-width: 740px) {
  .recipe-detail__hero,
  .recipe-detail__preparation {
    grid-template-columns: minmax(0, 1fr);
  }

  .recipe-detail__media {
    max-height: 28rem;
  }
}
</style>
