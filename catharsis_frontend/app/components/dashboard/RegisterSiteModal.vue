<template>
  <Teleport to="body">
    <dialog
      ref="dialog"
      class="register-site-dialog"
      aria-labelledby="register-site-title"
      @close="$emit('close')"
      @cancel="handleCancel"
    >
      <div class="dialog-shell">
        <div class="dialog-accent" aria-hidden="true">
          <div class="accent-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7">
              <circle cx="12" cy="12" r="9"></circle>
              <path stroke-linecap="round" stroke-linejoin="round" d="M3.6 9h16.8M3.6 15h16.8M12 3c2.1 2.4 3.2 5.4 3.2 9s-1.1 6.6-3.2 9c-2.1-2.4-3.2-5.4-3.2-9S9.9 5.4 12 3Z"></path>
            </svg>
          </div>
          <button
            class="close-button"
            type="button"
            aria-label="Fermer la fenêtre"
            :disabled="isLoading"
            @click="close"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" d="m6 6 12 12M18 6 6 18"></path>
            </svg>
          </button>
        </div>

        <div class="dialog-content">
          <h2 id="register-site-title" class="sr-only">
            {{ createdProject ? 'Site enregistré' : 'Enregistrer un site' }}
          </h2>
          <projectRegistrationForm
            v-if="!createdProject"
            :is-loading="isLoading"
            :error-message="errorMessage"
            @submit="$emit('submit', $event)"
            @cancel="close"
          />
          <section v-else class="project-created" aria-live="polite">
            <span class="success-icon" aria-hidden="true">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="m5 12 4 4L19 6"></path>
              </svg>
            </span>
            <span class="form-eyebrow">PROJET CRÉÉ</span>
            <h3>{{ createdProject.name }} est enregistré</h3>
            <p class="success-description">
              Installez le tracker ci-dessous sur votre site pour commencer à collecter des statistiques d'audience en temps réel.
            </p>

            <IntegrationSnippet
              :site-id="createdProject.site_id"
              :site-name="createdProject.name"
            />

            <button class="done-button" type="button" @click="close">Accéder au tableau de bord</button>
          </section>
        </div>
      </div>
    </dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import projectRegistrationForm from '~/components/forms/projectRegistrationForm.vue'
import IntegrationSnippet from '~/components/dashboard/IntegrationSnippet.vue'
import type { Project } from '~/stores/projectSiteStore'

withDefaults(
  defineProps<{
    isLoading?: boolean
    errorMessage?: string
    createdProject?: Project | null
  }>(),
  {
    isLoading: false,
    errorMessage: '',
    createdProject: null
  }
)

const emit = defineEmits<{
  (event: 'submit', payload: { name: string }): void
  (event: 'close'): void
}>()

const dialog = ref<HTMLDialogElement | null>(null)
const copied = ref(false)
const copyError = ref('')

onMounted(() => {
  dialog.value?.showModal()
})

function handleCancel(event: Event) {
  if (dialog.value && dialog.value.open) {
    event.preventDefault()
    close()
  }
}

function close() {
  if (dialog.value?.open) {
    dialog.value.close()
  } else {
    emit('close')
  }
}

async function copySiteId(projectId: string) {
  try {
    await navigator.clipboard.writeText(projectId)
    copied.value = true
    copyError.value = ''
  } catch {
    copyError.value = 'La copie automatique a échoué. Sélectionnez puis copiez l’identifiant.'
  }
}
</script>

<style scoped>
.register-site-dialog {
  position: fixed;
  inset: 50% auto auto 50%;
  transform: translate(-50%, -50%);
  margin: 0;
  width: min(100% - 2rem, 640px);
  max-width: 640px;
  max-height: min(90vh, 760px);
  padding: 0;
  overflow: auto;
  border: 1px solid rgb(41 63 20 / 10%);
  border-radius: 1.35rem;
  background: #fff;
  color: #171717;
  box-shadow: 0 24px 80px rgb(15 23 42 / 22%);
}

.register-site-dialog::backdrop {
  background: rgb(15 23 42 / 48%);
  backdrop-filter: blur(4px);
}

.dialog-shell {
  overflow: hidden;
  background:
    radial-gradient(ellipse at top right, rgb(62 255 139 / 12%), transparent 42%),
    #fff;
}

.dialog-accent {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.35rem 1.5rem 0;
}

.accent-icon {
  display: grid;
  width: 46px;
  height: 46px;
  place-items: center;
  border: 1px solid rgb(34 148 26 / 14%);
  border-radius: 15px;
  background: #f0f8ed;
  color: var(--green, #22941a);
}

.accent-icon svg {
  width: 23px;
  height: 23px;
}

.close-button {
  display: grid;
  width: 36px;
  height: 36px;
  place-items: center;
  border: 0;
  border-radius: 50%;
  background: transparent;
  color: #737373;
  cursor: pointer;
  transition: color 0.16s ease, background-color 0.16s ease;
}

.close-button:hover:not(:disabled) {
  background: #f3f4f6;
  color: #171717;
}

.close-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}

.close-button svg {
  width: 19px;
  height: 19px;
}

.dialog-content {
  padding: 1rem 1.75rem 1.75rem;
}

.project-created {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 0.7rem;
}

.success-icon {
  display: grid;
  width: 42px;
  height: 42px;
  margin-bottom: 0.25rem;
  place-items: center;
  border-radius: 50%;
  background: #edf8e9;
  color: var(--green, #22941a);
}

.success-icon svg {
  width: 21px;
  height: 21px;
}

.form-eyebrow {
  color: var(--green, #22941a);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.project-created h3 {
  color: #171717;
  font-size: 1.35rem;
  font-weight: 650;
  letter-spacing: -0.035em;
  overflow-wrap: anywhere;
}

.success-description,
.tracker-notice {
  color: #737373;
  font-size: 0.875rem;
  line-height: 1.55;
}

.site-id-card {
  width: 100%;
  margin-top: 0.35rem;
  padding: 1rem;
  border: 1px solid #e5e7eb;
  border-radius: 0.9rem;
  background: #fafcf9;
}

.site-id-label {
  display: block;
  margin-bottom: 0.55rem;
  color: #525252;
  font-size: 0.75rem;
  font-weight: 600;
}

.site-id-value {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.site-id-value code {
  min-width: 0;
  color: var(--black-forest, #293f14);
  font-size: 0.95rem;
  font-weight: 650;
  overflow-wrap: anywhere;
}

.copy-button {
  display: inline-flex;
  flex: 0 0 auto;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  min-height: 36px;
  padding: 0 0.75rem;
  border: 1px solid rgb(34 148 26 / 20%);
  border-radius: 9999px;
  background: #fff;
  color: var(--green, #22941a);
  font: inherit;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
}

.copy-button:hover {
  background: #f0f8ed;
}

.copy-button svg {
  width: 15px;
  height: 15px;
}

.copy-error {
  margin-top: 0.5rem;
  color: #b42318;
  font-size: 0.78rem;
}

.tracker-notice {
  padding: 0.75rem 0.9rem;
  border-left: 3px solid var(--bright-fern, #38a700);
  border-radius: 0.25rem 0.65rem 0.65rem 0.25rem;
  background: #f5faf2;
  color: #47543f;
  font-size: 0.8rem;
}

.done-button {
  align-self: flex-end;
  min-height: 42px;
  margin-top: 0.25rem;
  padding: 0 1.25rem;
  border: 1px solid var(--black-forest, #293f14);
  border-radius: 9999px;
  background: var(--black-forest, #293f14);
  color: #fff;
  font: inherit;
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
}

.done-button:hover {
  background: var(--green, #22941a);
  border-color: var(--green, #22941a);
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

@media (max-width: 480px) {
  .dialog-accent {
    padding: 1rem 1rem 0;
  }

  .dialog-content {
    padding: 0.75rem 1rem 1rem;
  }
}
</style>
