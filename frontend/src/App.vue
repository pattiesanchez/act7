<script setup>
import { RouterView } from 'vue-router'
import Header from '@/components/Header.vue'
import Footer from '@/components/Footer.vue'
</script>

<template>
  <a class="skip-link" href="#conteudo">Ir para o conteúdo</a>
  <Header />
  <main id="conteudo" tabindex="-1">
    <RouterView />
  </main>
  <Footer />
</template>
