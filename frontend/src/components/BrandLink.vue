<template>
  <RouterLink class="brand" :to="{ name: 'home' }" aria-label="ACT7 Confeitaria, início">
    <span class="brand-mark" aria-hidden="true"><span></span></span>
    <span class="brand-name">ACT7 <span>Confeitaria</span></span>
  </RouterLink>
</template>

<style scoped>
.brand {
  display: inline-flex;
  width: fit-content;
  align-items: center;
  gap: 0.65rem;
  color: var(--text);
  font-family: var(--font-display);
  font-size: 1.04rem;
  font-weight: 800;
  letter-spacing: -0.04em;
  text-decoration: none;
  white-space: nowrap;
}

.brand-name span {
  margin-left: 0.12em;
  font-weight: 620;
}

.brand-mark {
  display: grid;
  width: 2.4rem;
  height: 2.4rem;
  place-items: center;
  border: 1px solid #634880;
  border-radius: 0.7rem;
  color: var(--accent);
  background: #2e2040;
}

.brand-mark span {
  position: relative;
  width: 1.04rem;
  height: 0.69rem;
  margin-top: 0.21rem;
  border: 1.5px solid currentColor;
  border-radius: 0.24rem 0.24rem 0.14rem 0.14rem;
}

.brand-mark span::before,
.brand-mark span::after {
  position: absolute;
  content: '';
}

.brand-mark span::before {
  inset: 0.2rem 0 auto;
  border-top: 1px solid currentColor;
}

.brand-mark span::after {
  width: 2px;
  height: 5px;
  inset: -6px 50% auto auto;
  border-radius: 100% 100% 0 0;
  background: currentColor;
  transform: translateX(50%);
}
</style>
