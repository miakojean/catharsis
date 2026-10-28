<template>
  <Teleport to="body">
    <dialog
      ref="dialog"
      class="tracking-snippet-dialog"
      aria-labelledby="tracking-snippet-title"
      @close="$emit('close')"
      @cancel="handleCancel"
    >
      <div class="dialog-shell">
        <div class="dialog-accent" aria-hidden="true">
          <div class="accent-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="16 18 22 12 16 6"></polyline>
              <polyline points="8 6 2 12 8 18"></polyline>
            </svg>
          </div>
          <button
            class="close-button"
            type="button"
            aria-label="Fermer la fenêtre"
            @click="close"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" d="m6 6 12 12M18 6 6 18"></path>
            </svg>
          </button>
        </div>

        <div class="dialog-content">
          <header class="dialog-header-text">
            <span class="dialog-eyebrow">INSTALLATION DU TRACKER</span>
            <h2 id="tracking-snippet-title">
              Instructions pour {{ siteName || 'votre site' }}
            </h2>
            <p class="dialog-description">
              Le tracker Catharsis est conçu pour être ultra-léger (&lt; 2 KB), respectueux de la vie privée et sans cookie tiers.
            </p>
          </header>

          <IntegrationSnippet
            :site-id="siteId"
            :site-name="siteName"
          />

          <div class="dialog-footer">
            <button class="close-action-button" type="button" @click="close">
              Fermer
            </button>
          </div>
        </div>
      </div>
    </dialog>
  </Teleport>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import IntegrationSnippet from '~/components/dashboard/IntegrationSnippet.vue'

withDefaults(
  defineProps<{
    siteId: string
    siteName?: string
  }>(),
  {
    siteName: '',
  }
)

const emit = defineEmits<{
  (event: 'close'): void
}>()

const dialog = ref<HTMLDialogElement | null>(null)

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
</script>

<style scoped>
.tracking-snippet-dialog {
  position: fixed;
  inset: 50% auto auto 50%;
  transform: translate(-50%, -50%);
  margin: 0;
  width: min(100% - 2rem, 640px);
  max-width: 640px;
  max-height: min(92vh, 800px);
  padding: 0;
  overflow: auto;
  border: 1px solid rgb(41 63 20 / 10%);
  border-radius: 1.35rem;
  background: #fff;
  color: #171717;
  box-shadow: 0 24px 80px rgb(15 23 42 / 24%);
}

.tracking-snippet-dialog::backdrop {
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
  width: 44px;
  height: 44px;
  place-items: center;
  border: 1px solid rgb(34 148 26 / 14%);
  border-radius: 14px;
  background: #f0f8ed;
  color: var(--green, #22941a);
}

.accent-icon svg {
  width: 22px;
  height: 22px;
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

.close-button:hover {
  background: #f3f4f6;
  color: #171717;
}

.close-button svg {
  width: 19px;
  height: 19px;
}

.dialog-content {
  padding: 0.75rem 1.75rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.dialog-header-text {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.dialog-eyebrow {
  color: var(--green, #22941a);
  font-size: 0.68rem;
  font-weight: 700;
  letter-spacing: 0.12em;
}

.dialog-header-text h2 {
  color: #0f172a;
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  margin: 0;
}

.dialog-description {
  color: #64748b;
  font-size: 0.85rem;
  line-height: 1.5;
  margin: 0;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.close-action-button {
  min-height: 40px;
  padding: 0 1.35rem;
  border: 1px solid var(--black-forest, #293f14);
  border-radius: 9999px;
  background: var(--black-forest, #293f14);
  color: #fff;
  font: inherit;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.16s ease;
}

.close-action-button:hover {
  background: var(--green, #22941a);
  border-color: var(--green, #22941a);
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
