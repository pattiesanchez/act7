<script setup>
import { nextTick, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import BrandLink from '@/components/BrandLink.vue'
import { useAuthStore } from '@/stores/authStore'

defineOptions({ name: 'AppHeader' })

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()
const menuOpen = ref(false)
const menuButton = ref(null)

const links = [
  { to: { name: 'home' }, label: 'Início' },
  { to: { name: 'receitas' }, label: 'Receitas' },
  { to: { name: 'sobreNos' }, label: 'Sobre nós' },
  { to: { name: 'contato' }, label: 'Contato' },
]

watch(() => route.fullPath, () => {
  menuOpen.value = false
})

async function closeMenu() {
  if (!menuOpen.value) return
  menuOpen.value = false
  await nextTick()
  menuButton.value?.focus()
}

async function signOut() {
  if (auth.encerrarSecao()) {
    menuOpen.value = false
    await router.push({ name: 'login' })
  }
}
</script>

<template>
  <header class="site-header" @keydown.esc="closeMenu">
    <div class="page-shell header-inner">
      <BrandLink @click="menuOpen = false" />

      <button
        ref="menuButton"
        class="menu-toggle"
        type="button"
        aria-controls="navigation"
        :aria-expanded="menuOpen"
        :aria-label="menuOpen ? 'Fechar menu' : 'Abrir menu'"
        @click="menuOpen = !menuOpen"
      >
        <span aria-hidden="true"></span>
        <span aria-hidden="true"></span>
      </button>

      <nav id="navigation" class="header-nav" :class="{ 'is-open': menuOpen }" aria-label="Menu principal">
        <div class="nav-links">
          <RouterLink
            v-for="link in links"
            :key="link.to.name"
            :to="link.to"
            class="nav-link"
            :class="{ 'is-current': link.to.name === 'receitas' && route.path.startsWith('/receitas/') }"
            @click="menuOpen = false"
          >
            {{ link.label }}
          </RouterLink>
        </div>
        <div class="account-links">
          <template v-if="auth.authId">
            <RouterLink class="nav-link" :to="{ name: 'painel' }" @click="menuOpen = false">Meu painel</RouterLink>
            <button class="button button--secondary" type="button" @click="signOut">Sair</button>
          </template>
          <template v-else>
            <RouterLink class="nav-link" :to="{ name: 'login' }" @click="menuOpen = false">Entrar</RouterLink>
            <RouterLink class="button button--secondary signup-link" :to="{ name: 'cadastro' }" @click="menuOpen = false">
              Criar conta
            </RouterLink>
          </template>
        </div>
      </nav>
    </div>
  </header>
</template>

<style scoped>
.site-header {
  position: sticky;
  z-index: 10;
  top: 0;
  border-bottom: 1px solid var(--line);
  background: rgb(17 14 23 / 94%);
  backdrop-filter: blur(16px);
}

.header-inner {
  display: flex;
  min-height: 4.8rem;
  align-items: center;
  justify-content: space-between;
  gap: clamp(1.5rem, 3vw, 3rem);
}

.header-nav {
  display: flex;
  flex: 1;
  align-items: center;
  gap: 1.5rem;
}

.nav-links,
.account-links {
  display: flex;
  align-items: center;
  gap: clamp(0.9rem, 2.2vw, 1.8rem);
}

.nav-links {
  margin-inline: auto;
}

.account-links {
  flex-shrink: 0;
  gap: 0.75rem;
}

.nav-link {
  padding: 0.55rem 0.3rem;
  color: var(--muted);
  font-size: 0.91rem;
  font-weight: 600;
  text-decoration: none;
  white-space: nowrap;
  transition: color 150ms;
}

.nav-link:hover,
.nav-link.router-link-exact-active,
.nav-link.is-current {
  color: var(--accent);
}

.account-links .button {
  min-height: 2.45rem;
  padding-inline: 0.9rem;
  font-size: 0.85rem;
}

.signup-link {
  border-color: #59436b;
  color: var(--accent);
  background: #251b32;
}

.menu-toggle {
  display: none;
}

@media (max-width: 760px) {
  .header-inner {
    min-height: 4.15rem;
  }

  .menu-toggle {
    display: grid;
    width: 2.65rem;
    height: 2.65rem;
    place-content: center;
    gap: 0.31rem;
    border: 1px solid var(--line);
    border-radius: 0.65rem;
    color: var(--text);
    background: var(--surface);
  }

  .menu-toggle span {
    width: 1.02rem;
    height: 2px;
    border-radius: 1rem;
    background: currentColor;
    transition: transform 150ms;
  }

  .menu-toggle[aria-expanded='true'] span:first-child {
    transform: translateY(3.5px) rotate(45deg);
  }

  .menu-toggle[aria-expanded='true'] span:last-child {
    transform: translateY(-3.5px) rotate(-45deg);
  }

  .header-nav {
    display: none;
    position: absolute;
    inset: calc(100% + 0.6rem) var(--page-gutter) auto;
    padding: 1rem;
    border: 1px solid var(--line);
    border-radius: 1rem;
    background: var(--surface);
    box-shadow: 0 1.25rem 3rem rgb(0 0 0 / 45%);
  }

  .header-nav.is-open,
  .nav-links {
    display: grid;
    margin: 0;
    gap: 0.15rem;
  }

  .nav-link {
    padding: 0.65rem;
  }

  .account-links {
    flex-wrap: wrap;
    margin-top: 0.55rem;
    padding-top: 0.55rem;
    border-top: 1px solid var(--line);
  }
}
</style>
