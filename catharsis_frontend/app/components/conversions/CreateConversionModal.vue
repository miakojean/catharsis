<template>
  <Teleport to="body">
    <div
      class="conversion-modal-backdrop"
      role="dialog"
      aria-modal="true"
      aria-labelledby="create-conversion-title"
      @click.self="conversionStore.closeCreateModal()"
    >
      <div class="conversion-modal-card">
        <!-- En-tête de la modale -->
        <header class="modal-header">
          <div class="header-badge-group">
            <div class="icon-circle">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <circle cx="12" cy="12" r="6"></circle>
                <circle cx="12" cy="12" r="2"></circle>
              </svg>
            </div>
            <div>
              <span class="modal-eyebrow">NOUVEL OBJECTIF</span>
              <h2 id="create-conversion-title" class="modal-title">Configurer une conversion</h2>
            </div>
          </div>

          <button
            type="button"
            class="close-btn"
            aria-label="Fermer la fenêtre"
            :disabled="conversionStore.isSubmitting"
            @click="conversionStore.closeCreateModal()"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path stroke-linecap="round" d="M6 6l12 12M18 6L6 18"></path>
            </svg>
          </button>
        </header>

        <!-- Formulaire -->
        <form class="modal-form" @submit.prevent="handleSubmit">
          <!-- Choix du mode de capture -->
          <div class="field-group">
            <label class="field-label">Type de déclencheur</label>
            <div class="type-selector" role="radiogroup" aria-label="Type de conversion">
              <button
                type="button"
                class="type-option"
                :class="{ active: goalType === 'custom_event' }"
                @click="goalType = 'custom_event'"
              >
                <div class="type-option-head">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
                  </svg>
                  <span>Événement personnalisé</span>
                </div>
                <p>Déclenché via <code>trackEvent()</code> ou action JS</p>
              </button>

              <button
                type="button"
                class="type-option"
                :class="{ active: goalType === 'pageview_url' }"
                @click="goalType = 'pageview_url'"
              >
                <div class="type-option-head">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path>
                    <path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>
                  </svg>
                  <span>Visite d’URL</span>
                </div>
                <p>Automatique dès qu’une page cible est visitée</p>
              </button>
            </div>
          </div>

          <!-- Nom de l'objectif -->
          <div class="field-group">
            <label for="goal-name-input" class="field-label">Nom de l’objectif</label>
            <input
              id="goal-name-input"
              v-model="name"
              type="text"
              class="field-input"
              :placeholder="goalType === 'custom_event' ? 'Ex : Inscription terminée' : 'Ex : Visite de la page Tarifs'"
              required
            />
          </div>

          <!-- Valeur cible -->
          <div class="field-group">
            <label for="goal-target-input" class="field-label">
              {{ goalType === 'custom_event' ? 'Identifiant de l’événement (event_type)' : 'Chemin ou URL de la page cible' }}
            </label>
            <input
              id="goal-target-input"
              v-model="targetValue"
              type="text"
              class="field-input font-mono"
              :placeholder="goalType === 'custom_event' ? 'Ex : signup_completed ou form_submit' : 'Ex : /pricing ou /merci'"
              required
            />
            <span class="field-hint">
              <template v-if="goalType === 'custom_event'">
                Saisissez le nom exact passé à <code>window.Catharsis.trackEvent('...')</code> ou un événement standard (<code>form_submit</code>, <code>click</code>).
              </template>
              <template v-else>
                Toute visite de page dont l’URL correspond ou contient ce chemin sera comptabilisée comme une conversion.
              </template>
            </span>
          </div>

          <!-- Aperçu du snippet si Événement personnalisé -->
          <div v-if="goalType === 'custom_event'" class="snippet-preview-box">
            <div class="snippet-preview-header">
              <span>Code de déclenchement côté site</span>
              <button type="button" class="copy-mini-btn" @click="copyPreview">
                {{ copied ? 'Copié !' : 'Copier' }}
              </button>
            </div>
            <pre class="snippet-code"><code>{{ snippetPreview }}</code></pre>
          </div>

          <!-- Message d'erreur -->
          <p v-if="conversionStore.message.errorMessage" class="error-banner" role="alert">
            {{ conversionStore.message.errorMessage }}
          </p>

          <!-- Actions -->
          <div class="modal-actions">
            <button
              type="button"
              class="btn-cancel"
              :disabled="conversionStore.isSubmitting"
              @click="conversionStore.closeCreateModal()"
            >
              Annuler
            </button>
            <button
              type="submit"
              class="btn-submit"
              :disabled="conversionStore.isSubmitting || !name.trim() || !targetValue.trim()"
            >
              {{ conversionStore.isSubmitting ? 'Enregistrement…' : 'Créer l’objectif' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useConversionStore, type ConversionGoalType } from '~/stores/conversionStore'

const props = defineProps<{
  siteId?: string
  startDate?: string | null
  endDate?: string | null
}>()

const emit = defineEmits<{
  (e: 'created'): void
}>()

const conversionStore = useConversionStore()

const name = ref('')
const goalType = ref<ConversionGoalType>('custom_event')
const targetValue = ref('')
const copied = ref(false)

const snippetPreview = computed(() => {
  const evtName = targetValue.value.trim() || 'mon_evenement'
  return `window.Catharsis?.trackEvent('${evtName}')`
})

async function copyPreview() {
  try {
    await navigator.clipboard.writeText(snippetPreview.value)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 1800)
  } catch {
    copied.value = false
  }
}

async function handleSubmit() {
  const success = await conversionStore.createGoal(
    {
      site_id: props.siteId,
      name: name.value.trim(),
      goal_type: goalType.value,
      target_value: targetValue.value.trim(),
    },
    {
      start_date: props.startDate,
      end_date: props.endDate,
    }
  )

  if (success) {
    emit('created')
    conversionStore.closeCreateModal()
  }
}
</script>

<style scoped>
.conversion-modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  background: rgba(15, 23, 42, 0.55);
  backdrop-filter: blur(4px);
}

.conversion-modal-card {
  width: 100%;
  max-width: 540px;
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 16px;
  box-shadow: 0 24px 48px rgba(15, 23, 42, 0.2);
  overflow: hidden;
  animation: modalPop 0.2s ease-out;
}

@keyframes modalPop {
  from {
    opacity: 0;
    transform: translateY(8px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  background: linear-gradient(135deg, rgba(34, 148, 26, 0.08), rgba(56, 167, 0, 0.02));
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.header-badge-group {
  display: flex;
  align-items: center;
  gap: 0.85rem;
}

.icon-circle {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #dcfce7;
  color: var(--green, #22941a);
}

.modal-eyebrow {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  color: var(--green, #22941a);
}

.modal-title {
  margin: 0;
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--text-heading, #0f172a);
}

.close-btn {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  border: 1px solid var(--border-color, #e2e8f0);
  background: var(--card-bg, #ffffff);
  color: var(--text-muted, #64748b);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.close-btn:hover {
  color: var(--text-heading, #0f172a);
  background: var(--nav-hover-bg, #f8fafc);
}

.modal-form {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 0.45rem;
}

.field-label {
  font-size: 0.84rem;
  font-weight: 600;
  color: var(--text-heading, #0f172a);
}

.type-selector {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
}

.type-option {
  text-align: left;
  padding: 0.85rem;
  border-radius: 10px;
  border: 1.5px solid var(--border-color, #e2e8f0);
  background: var(--input-bg, #ffffff);
  cursor: pointer;
  transition: all 0.16s ease;
}

.type-option:hover {
  border-color: #94a3b8;
}

.type-option.active {
  border-color: var(--green, #22941a);
  background: rgba(34, 148, 26, 0.05);
  box-shadow: 0 0 0 3px rgba(34, 148, 26, 0.12);
}

.type-option-head {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--text-heading, #0f172a);
  margin-bottom: 0.25rem;
}

.type-option.active .type-option-head {
  color: var(--black-forest, #293f14);
}

.type-option p {
  margin: 0;
  font-size: 0.74rem;
  color: var(--text-muted, #64748b);
  line-height: 1.35;
}

.field-input {
  width: 100%;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  border: 1px solid var(--border-color, #e2e8f0);
  background: var(--input-bg, #ffffff);
  color: var(--text-heading, #0f172a);
  font-size: 0.88rem;
  outline: none;
  transition: border-color 0.16s ease, box-shadow 0.16s ease;
}

.field-input:focus {
  border-color: var(--green, #22941a);
  box-shadow: 0 0 0 3px rgba(34, 148, 26, 0.14);
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.field-hint {
  font-size: 0.75rem;
  color: var(--text-muted, #64748b);
  line-height: 1.4;
}

.field-hint code {
  padding: 0.1rem 0.3rem;
  background: #f1f5f9;
  border-radius: 4px;
  font-family: ui-monospace, monospace;
  color: var(--black-forest, #293f14);
}

.snippet-preview-box {
  background: #0f172a;
  border-radius: 10px;
  border: 1px solid #1e293b;
  overflow: hidden;
}

.snippet-preview-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.45rem 0.85rem;
  background: #1e293b;
  font-size: 0.72rem;
  font-weight: 600;
  color: #94a3b8;
}

.copy-mini-btn {
  padding: 0.2rem 0.55rem;
  border-radius: 5px;
  border: 1px solid #475569;
  background: #334155;
  color: #f8fafc;
  font-size: 0.7rem;
  font-weight: 600;
  cursor: pointer;
}

.copy-mini-btn:hover {
  background: var(--green, #22941a);
  border-color: var(--bright-fern, #38a700);
}

.snippet-code {
  margin: 0;
  padding: 0.75rem 0.85rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.8rem;
  color: var(--spring-green, #3eff8b);
  overflow-x: auto;
}

.error-banner {
  margin: 0;
  padding: 0.65rem 0.85rem;
  border-radius: 8px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
  font-size: 0.82rem;
  font-weight: 500;
}

.modal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 0.25rem;
}

.btn-cancel {
  padding: 0.6rem 1.1rem;
  border-radius: 8px;
  border: 1px solid var(--border-color, #e2e8f0);
  background: var(--card-bg, #ffffff);
  color: var(--text-muted, #64748b);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-cancel:hover {
  color: var(--text-heading, #0f172a);
  background: var(--nav-hover-bg, #f8fafc);
}

.btn-submit {
  padding: 0.6rem 1.25rem;
  border-radius: 8px;
  border: none;
  background: var(--green, #22941a);
  color: #ffffff;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.16s ease, transform 0.1s ease;
}

.btn-submit:hover:not(:disabled) {
  background: var(--bright-fern, #38a700);
}

.btn-submit:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

@media (max-width: 520px) {
  .type-selector {
    grid-template-columns: 1fr;
  }
}
</style>

