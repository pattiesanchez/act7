<script setup>
defineOptions({ name: 'PaginaErro404' })
</script>

<template>
  <section class="page-shell not-found-page" aria-labelledby="not-found-title">
    <div class="not-found-page__panel">
      <img class="not-found-page__image" src="/img/img/404.png" alt="erro 404"/>
      <!-- <p class="eyebrow">Erro 404</p> -->
      <!-- <h1 id="not-found-title">Página não encontrada</h1> -->
      <!-- <p class="not-found-page__description">Confira se o endereço está correto</p> -->
      <div class="not-found-page__actions">
        <RouterLink class="button button--primary" :to="{ name: 'home' }">
          Voltar ao início
        </RouterLink>
        <RouterLink class="button button--secondary" :to="{ name: 'receitas' }">
          Explorar receitas
        </RouterLink>
      </div>
    </div>
  </section>
</template>

<style scoped>
.not-found-page {
  padding-block: clamp(2.5rem, 8vw, 6.5rem);
}

.not-found-page__panel {
  display: grid;
  justify-items: center;
  text-align: center;
  min-height: 22rem;
  align-content: center;
  padding: clamp(1.25rem, 6vw, 4rem);
  border: 1px solid var(--line);
  border-radius: 1.5rem;
  background:
    radial-gradient(ellipse at left top, color-mix(in srgb, var(--accent) 18%, transparent), transparent 60%),
    var(--surface);
}

.not-found-page__panel h1 {
  margin: 0.75rem 0 0;
  font: 650 clamp(2.25rem, 5vw, 4rem) / 1.05 var(--font-display);
  letter-spacing: -0.05em;
}

.not-found-page__description {
  margin: 1rem 0 0;
  color: var(--muted);
}

.not-found-page__actions {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.625rem;
  margin-top: 1.5rem;
}

.not-found-page__image {
  display: block;
  width: 100%;
  max-width: 500px;
  height: auto;
  margin: 0 auto 16px;
  border-radius: 8vh;
}
</style>
