<script setup>
import { Form } from 'vee-validate'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import CampoFormulario from '@/components/CampoFormulario.vue'
import CartaoAcesso from '@/components/CartaoAcesso.vue'
import { loginComposable } from '@/composables/useSegurancaComposable'
import { loginSchema } from '@/schemas/validacoesSchema'

defineOptions({ name: 'PaginaLogin' })

const router = useRouter()
const { sendData } = loginComposable()
const erroEnvio = ref('')

async function enviar(valores) {
  erroEnvio.value = ''
  try {
    await sendData(valores)
    await router.push({ name: 'painel' })
  } catch (error) {
    const status = error.response?.status
    erroEnvio.value = status === 400 || status === 404
      ? 'Confira seu e-mail e senha e verifique se a conta foi ativada.'
      : 'Não foi possível entrar. Tente novamente.'
  }
}
</script>

<template>
  <CartaoAcesso title="Entrar na sua conta" description="Acesse o painel para publicar e editar suas receitas.">
    <Form
      class="access-form"
      :validation-schema="loginSchema"
      v-slot="{ isSubmitting }"
      novalidate
      @submit="enviar"
    >
      <CampoFormulario name="email" label="E-mail" type="email" autocomplete="email" />
      <CampoFormulario name="password" label="Senha" type="password" autocomplete="current-password" />
      <p v-if="erroEnvio" class="form-error" role="alert">{{ erroEnvio }}</p>
      <button class="button button--primary" type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Entrando…' : 'Entrar' }}
      </button>
    </Form>

    <template #footer>
      Ainda não tem conta? <RouterLink :to="{ name: 'cadastro' }">Cadastre-se</RouterLink>
    </template>
  </CartaoAcesso>
</template>
