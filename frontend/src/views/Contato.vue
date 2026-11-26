<script setup>
import { Form } from 'vee-validate'
import { ref } from 'vue'
import CampoFormulario from '@/components/CampoFormulario.vue'
import { useContatoComposable } from '@/composables/useContatoComposable'
import { contatoSchema } from '@/schemas/validacoesSchema'

defineOptions({ name: 'PaginaContato' })

const { sendData } = useContatoComposable()
const mensagemEnviada = ref(false)
const erroEnvio = ref('')

async function enviar(valores, { resetForm }) {
  erroEnvio.value = ''
  mensagemEnviada.value = false
  try {
    await sendData(valores)
    resetForm()
    mensagemEnviada.value = true
  } catch {
    erroEnvio.value = 'Não foi possível enviar sua mensagem. Tente novamente'
  }
}
</script>

<template>
  <section class="page-shell contact-page" aria-labelledby="contact-title">
    <div class="contact-page__intro">
      <h1 id="contact-title">Fale conosco</h1>
      <p>Tem uma dúvida ou sugestão sobre as receitas? Envie uma mensagem pelo formulário</p>
    </div>

    <Form
      class="contact-form"
      :validation-schema="contatoSchema"
      v-slot="{ isSubmitting }"
      novalidate
      @submit="enviar"
    >
      <div class="contact-form__row">
        <CampoFormulario name="nome" label="Nome" autocomplete="name" />
        <CampoFormulario name="email" label="Email" type="email" autocomplete="email" />
      </div>
      <CampoFormulario name="telefone" label="Telefone" type="tel" autocomplete="tel" />
      <CampoFormulario name="mensagem" label="Mensagem" as="textarea" />
      <p v-if="erroEnvio" class="contact-form__error" role="alert">{{ erroEnvio }}</p>
      <p v-if="mensagemEnviada" class="contact-form__success" role="status">
        Sua mensagem foi enviada com sucesso
      </p>
      <button class="button button--primary" type="submit" :disabled="isSubmitting">
        {{ isSubmitting ? 'Enviando…' : 'Enviar mensagem' }}
      </button>
    </Form>
  </section>
</template>

<style scoped>
.contact-page {
  display: grid;
  grid-template-columns: minmax(0, 0.75fr) minmax(0, 1.25fr);
  align-items: start;
  gap: clamp(1.75rem, 6vw, 5rem);
  padding-block: clamp(2.5rem, 8vw, 6.5rem);
}

.contact-page__intro {
  max-width: 24rem;
}

.contact-page__intro h1 {
  margin: 0;
  font: 650 clamp(2.5rem, 5vw, 4.25rem) / 1.03 var(--font-display);
  letter-spacing: -0.055em;
}

.contact-page__intro p {
  margin: 1rem 0 0;
  color: var(--muted);
  font-size: 1.05rem;
  line-height: 1.6;
}

.contact-email {
  display: inline-block;
  margin-top: 1rem;
  color: var(--accent);
}

.contact-form {
  display: grid;
  gap: 1.125rem;
  border: 1px solid var(--line);
  border-radius: 1.5rem;
  padding: clamp(1.25rem, 4vw, 2.5rem);
  background: var(--surface);
}

.contact-form__row {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.contact-form :deep(textarea) {
  min-height: 8rem;
  resize: vertical;
}

.contact-form button {
  justify-self: start;
}

.contact-form__error,
.contact-form__success {
  margin: 0;
  font-size: 0.95rem;
}

.contact-form__error {
  color: var(--danger, #ffc2d5);
}

.contact-form__success {
  padding: 0.75rem 1rem;
  border-radius: 0.75rem;
  color: var(--text);
  background: var(--surface-raised);
}

@media (max-width: 760px) {
  .contact-page {
    grid-template-columns: minmax(0, 1fr);
  }
}

@media (max-width: 480px) {
  .contact-form__row {
    grid-template-columns: minmax(0, 1fr);
  }

  .contact-form button {
    width: 100%;
  }
}
</style>
