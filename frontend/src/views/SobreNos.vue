<template>
  <section class="page-shell about-page" aria-labelledby="about-title">
    <div class="about-page__copy">
      <p class="eyebrow">Sobre a ACT7</p>
      <h1 id="about-title">Receitas para descobrir e compartilhar</h1>
      <p class="about-page__description">
        A ACT7 Confeitaria é um espaço para quem gosta de preparar sobremesas. Explore o catálogo
        por categoria ou crie uma conta para publicar suas receitas e gerenciá-las no seu painel.
      </p>
      <div class="about-page__actions">
        <RouterLink class="button button--primary" :to="{ name: 'receitas' }">
          Explorar receitas
        </RouterLink>
        <RouterLink class="button button--secondary" :to="{ name: 'contato' }">
          Fale com a ACT7
        </RouterLink>
      </div>
    </div>

    <img
      class="about-page__image"
      src="/img/bg-img/r6.jpg"
      alt="Sobremesa com frutas frescas em uma tigela"
      width="1000"
      height="859"
    />
  </section>
</template>

<style scoped>
.about-page {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 0.9fr);
  align-items: center;
  gap: clamp(2rem, 7vw, 5.5rem);
  padding-block: clamp(2.5rem, 8vw, 6.5rem);
}

.about-page__copy h1 {
  max-width: 14ch;
  margin: 0.75rem 0 0;
  font: 650 clamp(2.5rem, 5vw, 4.5rem) / 1.02 var(--font-display);
  letter-spacing: -0.055em;
}

.about-page__description {
  max-width: 45ch;
  margin: 1.25rem 0 0;
  color: var(--muted);
  font-size: 1.05rem;
  line-height: 1.7;
}

.about-page__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.625rem;
  margin-top: 1.75rem;
}

.about-page__image {
  width: 100%;
  height: auto;
  aspect-ratio: 1.05;
  object-fit: cover;
  border: 1px solid var(--line);
  border-radius: 1.5rem;
}

@media (max-width: 760px) {
  .about-page {
    grid-template-columns: minmax(0, 1fr);
  }

  .about-page__image {
    aspect-ratio: 1.45;
  }
}
</style>
