<script setup>
import BrandLink from '@/components/BrandLink.vue'

defineOptions({ name: 'AppFooter' })

const year = new Date().getFullYear()
</script>

<template>
  <footer class="site-footer">
    <div class="page-shell">
      <div class="footer-top">
        <BrandLink />
        <nav aria-label="Rodapé">
          <RouterLink :to="{ name: 'receitas' }">Receitas</RouterLink>
          <RouterLink :to="{ name: 'sobreNos' }">Sobre nós</RouterLink>
          <RouterLink :to="{ name: 'contato' }">Contato</RouterLink>
        </nav>
      </div>
      <div class="footer-bottom">
        <p>© {{ year }} ACT7 Confeitaria</p>
        <p>Desenvolvido por <a href="https://github.com/pattiesanchez" target="_blank" rel="noopener">PSanx</a></p>
      </div>
    </div>
  </footer>
</template>

<style scoped>
.site-footer {
  margin-top: auto;
  border-top: 1px solid var(--line);
  background: #15101c;
}

.footer-top,
.footer-bottom,
nav {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem 1.6rem;
}

.footer-top {
  padding-block: 2.1rem;
  border-bottom: 1px solid var(--line);
}

nav a {
  text-decoration: none;
}

nav a,
.footer-bottom {
  color: var(--muted);
  font-size: 0.87rem;
}

.footer-bottom {
  padding-block: 1.15rem;
  gap: 0.35rem 1rem;
}

.footer-bottom a {
  color: var(--accent);
}

nav a:hover,
.footer-bottom a:hover {
  color: var(--text);
}
</style>
