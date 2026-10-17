<template>
  <form class="project-form" @submit.prevent="handleSubmit">
    <div class="form-intro">
      <span class="form-eyebrow">NOUVEAU PROJET</span>
      <h3>Enregistrez votre site</h3>
      <p>Donnez un nom à votre site ou application pour le retrouver facilement dans votre espace.</p>
    </div>

    <BaseInput
      v-model="name"
      label="Nom du site ou de l’application"
      placeholder="Ex. Ma boutique en ligne"
      :error-message="nameError"
      hint="Vous pourrez retrouver ce nom dans votre tableau de bord."
      autocomplete="organization"
      :maxlength="200"
      required
    >
      <template #prepend>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true">
          <circle cx="12" cy="12" r="9"></circle>
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.6 9h16.8M3.6 15h16.8M12 3c2.1 2.4 3.2 5.4 3.2 9s-1.1 6.6-3.2 9c-2.1-2.4-3.2-5.4-3.2-9S9.9 5.4 12 3Z"></path>
        </svg>
      </template>
    </BaseInput>

    <p v-if="errorMessage" class="form-error" role="alert">
      {{ errorMessage }}
    </p>

    <div class="form-actions">
      <button class="cancel-button" type="button" :disabled="isLoading" @click="$emit('cancel')">
        Annuler
      </button>
      <mainButton
        class="submit-button"
        type="submit"
        label="Enregistrer le site"
        :is-loading="isLoading"
        :disabled="isLoading"
      />
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseInput from '~/components/BaseInput/BaseInput.vue'
import mainButton from '~/components/buttons/mainButton.vue'

withDefaults(
  defineProps<{
    isLoading?: boolean
    errorMessage?: string
  }>(),
  {
    isLoading: false,
    errorMessage: ''
  }
)

const emit = defineEmits<{
  (event: 'submit', payload: { name: string }): void
  (event: 'cancel'): void
}>()

const name = ref('')
const nameError = ref('')

function handleSubmit() {
  const trimmedName = name.value.trim()
  nameError.value = ''

  if (!trimmedName) {
    nameError.value = 'Veuillez saisir le nom de votre site.'
    return
  }

  emit('submit', { name: trimmedName })
}
</script>

<style scoped>
.project-form {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 1.5rem;
  width: 100%;
  max-width: none;
  padding: 0;
}

.form-intro {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.form-eyebrow {
  color: var(--green, #22941a);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.form-intro h3 {
  color: #171717;
  font-size: 1.35rem;
  font-weight: 650;
  letter-spacing: -0.035em;
}

.form-intro p {
  color: #737373;
  font-size: 0.875rem;
  line-height: 1.55;
}

.project-form :deep(.input-label) {
  color: #293f14;
  font-weight: 600;
}

.project-form :deep(.form-input:focus) {
  border-color: var(--green, #22941a);
  box-shadow: 0 0 0 3px rgb(34 148 26 / 12%);
}

.project-form :deep(.input-icon-left) {
  color: var(--green, #22941a);
}

.project-form :deep(.input-icon-left svg) {
  width: 18px;
  height: 18px;
}

.form-error {
  margin-top: -0.9rem;
  color: #b42318;
  font-size: 0.8125rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 0.75rem;
  padding-top: 0.25rem;
}

.cancel-button {
  min-height: 44px;
  padding: 0 1.15rem;
  border: 1px solid #e5e7eb;
  border-radius: 9999px;
  background: #fff;
  color: #525252;
  font: inherit;
  font-size: 0.875rem;
  font-weight: 550;
  cursor: pointer;
  transition: border-color 0.18s ease, background-color 0.18s ease;
}

.cancel-button:hover:not(:disabled) {
  border-color: #cbd5c0;
  background: #f7faf5;
}

.cancel-button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.submit-button {
  width: auto;
  min-width: 175px;
  background-color: var(--black-forest, #293f14);
  border-color: var(--black-forest, #293f14);
}

.submit-button:hover:not(:disabled) {
  background-color: var(--green, #22941a);
  border-color: var(--green, #22941a);
}

@media (max-width: 480px) {
  .form-actions {
    flex-direction: column-reverse;
    align-items: stretch;
  }

  .cancel-button,
  .submit-button {
    width: 100%;
  }
}
</style>
