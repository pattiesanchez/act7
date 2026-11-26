<script setup>
import { Form } from 'vee-validate'
import { ref } from 'vue'
import CampoFormulario from '@/components/CampoFormulario.vue'
import CartaoAcesso from '@/components/CartaoAcesso.vue'
import { cadastroComposable } from '@/composables/useSegurancaComposable'
import { cadastroSchema } from '@/schemas/validacoesSchema'

defineOptions({ name: 'PaginaCadastro' })

const { sendData } = cadastroComposable()
const erroEnvio = ref('')
const cadastroConcluido = ref(false)

async function enviar(valores) {
  erroEnvio.value = ''
  try {
    await sendData(valores)
    cadastroConcluido.value = true
  } catch (error) {
    const mensagem = error.response?.data?.error
    erroEnvio.value = typeof mensagem === 'string'
      ? mensagem
      : 'Não foi possível criar a conta. Tente novamente'
  }
}
</script>

<template>
  <CartaoAcesso title="Crie sua conta" description="Publique e gerencie suas receitas no painel">
    <p v-if="cadastroConcluido" class="form-success" role="status">
      Cadastro concluído. Confira seu e-mail e siga o link para ativar sua conta
    </p>

    <Form
      v-else
      class="access-form"
      :validation-schema="cadastroSchema"
      v-slot="{ isSubmitting }"
      novalidate
      @submit="enviar"
    >
      <CampoFormulario name="nome" label="Nome" autocomplete="name" />
      <CampoFormulario name="email" label="E-mail" type="email" autocomplete="email" />
      <CampoFormulario name="password" label="Senha" type="password" autocomplete="new-password" />
      <p v-if="erroEnvio" class="form-error" role="alert">{{ erroEnvio }}</p>
      <button class="button button--primary" type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Criando conta…' : 'Criar conta' }}
      </button>
    </Form>

    <template #footer>
      Já tem uma conta? <RouterLink :to="{ name: 'login' }">Entrar</RouterLink>
    </template>
  </CartaoAcesso>
</template>
