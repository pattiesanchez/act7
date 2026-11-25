<script setup>
defineProps({
  title: { type: String, required: true },
  description: { type: String, required: true },
})
</script>

<template>
  <section class="page-shell access-page" aria-labelledby="access-title">
    <div class="access-card">
      <div class="access-card__image" aria-hidden="true">
        <img src="/img/bg-img/bg2.jpg" alt="" />
      </div>
      <div class="access-card__body">
        <div>
          <h1 id="access-title">{{ title }}</h1>
          <p class="access-card__description">{{ description }}</p>
        </div>
        <slot />
        <p class="access-card__footer"><slot name="footer" /></p>
      </div>
    </div>
  </section>
</template>

<style scoped>
.access-page {
  padding-block: clamp(2rem, 7vw, 5.5rem);
}

.access-card {
  display: grid;
  grid-template-columns: 0.95fr 1fr;
  max-width: 61rem;
  margin-inline: auto;
  overflow: hidden;
  border: 1px solid var(--line);
  border-radius: 1.5rem;
  background: var(--surface);
}

.access-card__image {
  position: relative;
  min-height: 31rem;
  background: var(--surface-raised);
}

.access-card__image img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: 76% center;
}

.access-card__body {
  min-width: 0;
  align-self: center;
  display: grid;
  gap: 1.75rem;
  padding: clamp(1.5rem, 4vw, 3.5rem);
}

.access-card__body h1 {
  margin: 0;
  font: 650 clamp(2rem, 3.4vw, 3rem) / 1.05 var(--font-display);
  letter-spacing: -0.045em;
}

.access-card__description {
  margin: 0.75rem 0 0;
  color: var(--muted);
  line-height: 1.55;
}

.access-card__footer {
  margin: 0;
  padding-top: 1.25rem;
  border-top: 1px solid var(--line);
  color: var(--muted);
  font-size: 0.9rem;
}

.access-card__footer :deep(a) {
  color: var(--accent);
  font-weight: 650;
  text-underline-offset: 0.2em;
}

.access-card :deep(.access-form) {
  display: grid;
  gap: 1rem;
  margin: 0;
}

.access-card :deep(.access-form .button) {
  width: 100%;
  margin-top: 0.25rem;
}

.access-card :deep(.form-success) {
  margin: 0;
  border: 1px solid var(--line);
  border-radius: 0.75rem;
  padding: 1rem;
  color: var(--text);
  background: var(--surface-raised);
}

.access-card :deep(.access-form .form-error) {
  margin: 0;
  color: var(--danger, #ffc2d5);
  font-size: 0.9rem;
}

@media (max-width: 720px) {
  .access-card {
    grid-template-columns: minmax(0, 1fr);
    max-width: 29rem;
  }

  .access-card__image {
    display: none;
  }
}
</style>
