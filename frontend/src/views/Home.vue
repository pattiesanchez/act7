<script setup>
import { onMounted, ref } from 'vue'
import RecipeCard from '@/components/RecipeCard.vue'
import { getDadosHome } from '@/services/homeService'
import { useAuthStore } from '@/stores/authStore'

defineOptions({ name: 'PaginaHome' })

const auth = useAuthStore()
const recipes = ref([])
const loading = ref(true)
const loadError = ref(false)

async function loadRecipes() {
  loading.value = true
  loadError.value = false

  try {
    recipes.value = await getDadosHome()
  } catch {
    loadError.value = true
  } finally {
    loading.value = false
  }
}

onMounted(loadRecipes)
</script>

<template>
  <section class="home-hero" aria-labelledby="home-title">
    <div class="page-shell hero-inner">
      <div class="hero-copy">
        <p class="eyebrow hero-kicker">Receitas da comunidade</p>
        <h1 id="home-title">Confeitaria<br /><span>feita em casa</span></h1>
        <p class="hero-description">
          Descubra bolos, doces e sobremesas para o café da tarde e para ocasiões especiais
        </p>
        <div class="hero-actions">
          <RouterLink class="button button--primary" :to="{ name: 'receitas' }">
            Explorar receitas
            <span class="action-arrow" aria-hidden="true">→</span>
          </RouterLink>
          <RouterLink class="button button--secondary" :to="{ name: 'sobreNos' }">
            Sobre a ACT7
          </RouterLink>
        </div>
      </div>
      <figure class="hero-photo">
        <img
          src="/img/bg-img/act7-bolo-framboesa.jpg"
          width="1122"
          height="1402"
          fetchpriority="high"
          alt="Fatia de bolo red velvet com camadas de creme e framboesas em um prato roxo"
        />
      </figure>
    </div>
  </section>

  <section class="page-shell featured-section" aria-labelledby="featured-title">
    <div class="section-heading">
      <h2 id="featured-title">Receitas em destaque</h2>
      <RouterLink class="section-link" :to="{ name: 'receitas' }">
        Ver todas <span aria-hidden="true">→</span>
      </RouterLink>
    </div>

    <div v-if="loading" class="featured-grid" role="status" aria-label="Carregando receitas">
      <div v-for="card in 3" :key="card" class="recipe-skeleton" aria-hidden="true"></div>
    </div>
    <div v-else-if="loadError" class="featured-state" role="status">
      <p>Não foi possível carregar os destaques</p>
      <button class="button button--secondary" type="button" @click="loadRecipes">Tentar novamente</button>
    </div>
    <div v-else-if="recipes.length" class="featured-grid">
      <RecipeCard v-for="recipe in recipes" :key="recipe.id ?? recipe.slug" :recipe="recipe" />
    </div>
    <div v-else class="featured-state">
      <p>As receitas publicadas pela comunidade aparecerão aqui</p>
      <RouterLink class="section-link" :to="{ name: 'receitas' }">Abrir catálogo <span aria-hidden="true">→</span></RouterLink>
    </div>
  </section>

  <div class="page-shell share-section">
    <section class="share-card" aria-labelledby="share-title">
      <div>
        <h2 id="share-title">Compartilhe sua receita</h2>
        <p>Publique uma criação da sua cozinha no catálogo da ACT7</p>
      </div>
      <RouterLink class="button button--primary" :to="{ name: auth.authId ? 'painel' : 'cadastro' }">
        {{ auth.authId ? 'Acessar meu painel' : 'Criar minha conta' }} <span aria-hidden="true">→</span>
      </RouterLink>
    </section>
  </div>
</template>

<style scoped>
.home-hero {
  border-bottom: 1px solid var(--line);
  background:
    radial-gradient(ellipse at 83% 42%, rgb(96 51 126 / 24%), transparent 57%),
    var(--bg);
}

.hero-inner {
  display: grid;
  grid-template-columns: 1.05fr 1fr;
  align-items: center;
  gap: clamp(1.75rem, 4.4vw, 4.5rem);
  padding-block: clamp(3rem, 5.5vw, 5.25rem);
}

.hero-copy {
  padding-block: 0.75rem;
}

.hero-kicker {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  margin-bottom: 1.2rem;
}

.hero-kicker::before {
  width: 1.3rem;
  height: 1px;
  background: currentColor;
  content: '';
}

.hero-copy h1 {
  font-size: clamp(3rem, 6.85vw, 6.15rem);
  font-weight: 780;
  line-height: 0.97;
  letter-spacing: -0.075em;
}

.hero-copy h1 span {
  color: var(--accent);
}

.hero-description {
  max-width: 39ch;
  margin-top: 1.45rem;
  color: var(--muted);
  font-size: clamp(1rem, 1.45vw, 1.18rem);
  line-height: 1.65;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.7rem;
  margin-top: 1.75rem;
}

.hero-actions .button {
  min-height: 3rem;
  padding-inline: 1.25rem;
}

.action-arrow {
  font-size: 1.2em;
  line-height: 1;
}

.hero-photo {
  overflow: hidden;
  aspect-ratio: 1.04;
  margin: 0;
  border: 1px solid #57405e;
  border-radius: 1.75rem;
  background: var(--surface);
  box-shadow: 0 2rem 5rem rgb(5 1 10 / 45%);
}

.hero-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center 55%;
}

.featured-section {
  padding-block: clamp(3rem, 5.3vw, 5.15rem);
}

.section-heading,
.share-card {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.9rem 2rem;
}

.section-heading {
  margin-bottom: 1.6rem;
}

.section-heading h2,
.share-card h2 {
  font-size: clamp(1.85rem, 3.6vw, 3rem);
}

.share-card p {
  margin-top: 0.45rem;
  color: var(--muted);
}

.section-link {
  display: inline-flex;
  width: fit-content;
  align-items: center;
  gap: 0.45rem;
  color: var(--accent);
  font-weight: 700;
  text-decoration: none;
}

.section-link:hover {
  text-decoration: underline;
}

.featured-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: clamp(0.85rem, 2vw, 1.45rem);
}

.featured-state,
.recipe-skeleton {
  border: 1px solid var(--line);
  border-radius: 1rem;
  background: var(--surface);
}

.featured-state {
  display: grid;
  justify-items: start;
  gap: 1rem;
  padding: 1.45rem;
  color: var(--muted);
}

.recipe-skeleton {
  aspect-ratio: 1.2;
  background: linear-gradient(145deg, var(--surface-raised), var(--surface));
}

.share-section {
  padding-bottom: clamp(3rem, 6vw, 5.6rem);
}

.share-card {
  padding: clamp(1.45rem, 4vw, 3.35rem);
  border: 1px solid #553f6b;
  border-radius: 1.3rem;
  background:
    radial-gradient(ellipse at 96% 60%, rgb(118 75 167 / 24%), transparent 59%),
    var(--surface);
}

@media (max-width: 760px) {
  .hero-inner {
    grid-template-columns: 1fr;
    gap: 1.85rem;
    padding-block: 2.45rem 2rem;
  }

  .hero-copy {
    padding: 0;
  }

  .hero-copy h1 {
    font-size: clamp(2.85rem, 10.6vw, 5rem);
  }

  .hero-photo {
    aspect-ratio: 1.22;
    border-radius: 1.15rem;
  }

  .featured-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 480px) {
  .featured-grid {
    grid-template-columns: 1fr;
  }

  .recipe-skeleton:nth-child(n + 2) {
    display: none;
  }
}
</style>
