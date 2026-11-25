<script setup>
import { Field } from 'vee-validate'

defineProps({
  name: { type: String, required: true },
  label: { type: String, required: true },
  type: { type: String, default: 'text' },
  as: { type: String, default: 'input' },
  autocomplete: { type: String, default: undefined },
})
</script>

<template>
  <div class="field">
    <label :for="name">{{ label }}</label>
    <Field :name="name" v-slot="{ field, errorMessage }">
      <component
        :is="as"
        :id="name"
        v-bind="field"
        :type="as === 'input' ? type : undefined"
        :rows="as === 'textarea' ? 5 : undefined"
        :autocomplete="autocomplete"
        :aria-invalid="Boolean(errorMessage)"
        :aria-describedby="errorMessage ? `${name}-erro` : undefined"
        required
      />
      <span v-if="errorMessage" :id="`${name}-erro`" class="field-error">
        {{ errorMessage }}
      </span>
    </Field>
  </div>
</template>
