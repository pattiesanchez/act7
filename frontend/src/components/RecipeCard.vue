<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  recipe: { type: Object, required: true },
})

const failedImage = ref(null)
</script>

<template>
  <RouterLink class="recipe-card" :to="{ name: 'receitasDetalhes', params: { slug: recipe.slug } }">
    <div class="recipe-card__media">
      <img
        v-if="recipe.imagem && recipe.imagem !== failedImage"
        :src="recipe.imagem"
        alt=""
        width="640"
        height="440"
        loading="lazy"
        decoding="async"
        @error="failedImage = props.recipe.imagem"
      />
      <span v-else class="recipe-card__fallback">Foto indisponível</span>
      <span v-if="recipe.categoria" class="recipe-card__category">{{ recipe.categoria }}</span>
    </div>
    <div class="recipe-card__body">
      <div>
        <h3>{{ recipe.nome }}</h3>
        <p v-if="recipe.tempo">{{ recipe.tempo }}</p>
      </div>
      <span class="recipe-card__arrow" aria-hidden="true">↗</span>
    </div>
  </RouterLink>
</template>

<style scoped>
.recipe-card {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  height: 100%;
  border: 1px solid var(--line);
  border-radius: 20px;
  background: var(--surface);
  color: var(--text);
  text-decoration: none;
  transition: border-color 160ms ease, transform 160ms ease;
}

.recipe-card:hover {
  transform: translateY(-3px);
  border-color: var(--accent);
}

.recipe-card__media {
  position: relative;
  display: grid;
  place-items: center;
  overflow: hidden;
  aspect-ratio: 16 / 10;
  background: linear-gradient(140deg, var(--surface-raised), var(--surface));
}

.recipe-card__media img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.recipe-card__fallback {
  color: var(--muted);
  font-size: 0.85rem;
}

.recipe-card__category {
  position: absolute;
  inset-block-start: 0.9rem;
  inset-inline-start: 0.9rem;
  max-width: calc(100% - 1.8rem);
  padding: 0.35rem 0.7rem;
  border: 1px solid rgb(255 255 255 / 22%);
  border-radius: 999px;
  background: rgb(17 14 23 / 90%);
  color: var(--text);
  font-size: 0.76rem;
  font-weight: 650;
  overflow-wrap: anywhere;
}

.recipe-card__body {
  flex: 1;
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: center;
  gap: 1rem;
  padding: 1.1rem 1.15rem 1.2rem;
}

.recipe-card__body h3 {
  margin: 0;
  color: var(--text);
  font-family: var(--font-display);
  font-size: clamp(1.2rem, 2vw, 1.4rem);
  line-height: 1.2;
  overflow-wrap: anywhere;
}

.recipe-card__body p {
  margin: 0.45rem 0 0;
  color: var(--muted);
  font-size: 0.87rem;
  overflow-wrap: anywhere;
}

.recipe-card__arrow {
  display: grid;
  place-items: center;
  width: 2.55rem;
  height: 2.55rem;
  border: 1px solid var(--line);
  border-radius: 50%;
  color: var(--accent);
  font-size: 1.15rem;
  line-height: 1;
}

.recipe-card:hover .recipe-card__arrow,
.recipe-card:focus-visible .recipe-card__arrow {
  border-color: var(--accent);
  background: var(--accent);
  color: var(--bg);
}
</style>
