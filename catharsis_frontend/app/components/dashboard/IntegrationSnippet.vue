<template>
  <div class="integration-snippet-card" :class="{ 'is-compact': compact }">
    <!-- Header avec onglets de formats -->
    <div class="snippet-header">
      <div class="snippet-tabs" role="tablist" aria-label="Format d'intégration">
        <button
          type="button"
          role="tab"
          class="tab-btn"
          :class="{ active: activeTab === 'html' }"
          :aria-selected="activeTab === 'html'"
          @click="activeTab = 'html'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tab-icon">
            <polyline points="16 18 22 12 16 6"></polyline>
            <polyline points="8 6 2 12 8 18"></polyline>
          </svg>
          <span>HTML Standard</span>
        </button>

        <button
          type="button"
          role="tab"
          class="tab-btn"
          :class="{ active: activeTab === 'spa' }"
          :aria-selected="activeTab === 'spa'"
          @click="activeTab = 'spa'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tab-icon">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="9" y1="3" x2="9" y2="21"></line>
          </svg>
          <span>SPA / Nuxt / React</span>
        </button>

        <button
          type="button"
          role="tab"
          class="tab-btn"
          :class="{ active: activeTab === 'custom' }"
          :aria-selected="activeTab === 'custom'"
          @click="activeTab = 'custom'"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="tab-icon">
            <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"></path>
          </svg>
          <span>Événement Custom</span>
        </button>
      </div>

      <div class="site-id-badge" title="Identifiant unique de votre site">
        <span class="badge-label">Site ID:</span>
        <code class="badge-code">{{ siteId }}</code>
      </div>
    </div>

    <!-- Instructions contextuelles -->
    <p class="snippet-instruction">
      <template v-if="activeTab === 'html'">
        Insérez ce script dans la balise <code>&lt;head&gt;</code> de toutes les pages à analyser.
      </template>
      <template v-else-if="activeTab === 'spa'">
        Ajoutez la balise via votre gestionnaire de balises d'en-tête (ex: <code>useHead</code> dans Nuxt ou <code>next/script</code>).
      </template>
      <template v-else>
        Déclenchez vos propres conversions manuellement n'importe où dans votre code JavaScript.
      </template>
    </p>

    <!-- Zone de code avec bouton Copier -->
    <div class="code-box">
      <div class="code-box-top">
        <span class="code-lang">
          {{ activeTab === 'html' ? 'HTML' : activeTab === 'spa' ? 'TypeScript / Vue' : 'JavaScript' }}
        </span>
        <button
          type="button"
          class="copy-code-btn"
          :class="{ copied: isCopied }"
          :aria-label="isCopied ? 'Code copié dans le presse-papier' : 'Copier le code'"
          @click="copySnippet"
        >
          <svg v-if="!isCopied" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="copy-icon">
            <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
            <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
          </svg>
          <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" class="copy-icon check-icon">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
          <span>{{ isCopied ? 'Copié !' : 'Copier le code' }}</span>
        </button>
      </div>

      <pre class="code-content"><code>{{ currentSnippet }}</code></pre>
    </div>

    <!-- Alertes ou erreurs de copie -->
    <p v-if="copyError" class="copy-error-msg" role="alert">
      {{ copyError }}
    </p>

    <!-- Guide de démarrage rapide -->
    <div class="onboarding-steps">
      <div class="step-item">
        <div class="step-num">1</div>
        <div class="step-text">
          <strong>Intégration</strong>
          <span>Copiez le script et collez-le sur votre site web.</span>
        </div>
      </div>

      <div class="step-divider" aria-hidden="true"></div>

      <div class="step-item">
        <div class="step-num">2</div>
        <div class="step-text">
          <strong>Publication</strong>
          <span>Mettez votre site en ligne ou visitez une page en local.</span>
        </div>
      </div>

      <div class="step-divider" aria-hidden="true"></div>

      <div class="step-item">
        <div class="step-num">3</div>
        <div class="step-text">
          <strong>Visualisation</strong>
          <span>Les visites remonteront automatiquement sur votre tableau de bord.</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useProjectSiteStore } from '~/stores/projectSiteStore'

const props = withDefaults(
  defineProps<{
    siteId: string
    siteName?: string
    compact?: boolean
  }>(),
  {
    siteName: '',
    compact: false,
  }
)

const projectStore = useProjectSiteStore()

type TabKey = 'html' | 'spa' | 'custom'
const activeTab = ref<TabKey>('html')
const isCopied = ref(false)
const copyError = ref('')

const currentSnippet = computed(() => {
  if (activeTab.value === 'html') {
    return projectStore.getScriptSnippet(props.siteId)
  }
  if (activeTab.value === 'spa') {
    return projectStore.getFrameworkSnippet(props.siteId)
  }
  return projectStore.getManualEventSnippet()
})

async function copySnippet() {
  try {
    await navigator.clipboard.writeText(currentSnippet.value)
    isCopied.value = true
    copyError.value = ''
    setTimeout(() => {
      isCopied.value = false
    }, 2200)
  } catch {
    copyError.value = 'La copie automatique a échoué. Veuillez sélectionner le code manuellement.'
  }
}
</script>

<style scoped>
.integration-snippet-card {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 0.9rem;
  background: transparent;
}

.snippet-header {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 0.75rem;
}

.snippet-tabs {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.25rem;
  background: #f1f5f9;
  border-radius: 9999px;
  border: 1px solid #e2e8f0;
}

.tab-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  padding: 0.35rem 0.85rem;
  border: none;
  border-radius: 9999px;
  background: transparent;
  color: #64748b;
  font-size: 0.78rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.16s ease;
}

.tab-btn:hover {
  color: #0f172a;
}

.tab-btn.active {
  background: #ffffff;
  color: var(--black-forest, #293f14);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.tab-icon {
  width: 14px;
  height: 14px;
}

.site-id-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.25rem 0.65rem;
  background: #f0fdf4;
  border: 1px solid rgb(34 148 26 / 20%);
  border-radius: 9999px;
  font-size: 0.75rem;
}

.badge-label {
  color: #166534;
  font-weight: 600;
}

.badge-code {
  color: var(--black-forest, #293f14);
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-weight: 700;
}

.snippet-instruction {
  font-size: 0.84rem;
  color: #475569;
  line-height: 1.5;
  margin: 0;
}

.snippet-instruction code {
  padding: 0.15rem 0.35rem;
  background: #f1f5f9;
  border-radius: 4px;
  font-family: ui-monospace, monospace;
  font-size: 0.82rem;
  color: var(--black-forest, #293f14);
}

/* Code box container */
.code-box {
  position: relative;
  display: flex;
  flex-direction: column;
  border-radius: 0.85rem;
  background: #0f172a;
  border: 1px solid #1e293b;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.12);
}

.code-box-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.5rem 0.9rem;
  background: #1e293b;
  border-bottom: 1px solid #334155;
}

.code-lang {
  color: #94a3b8;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.copy-code-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  padding: 0.3rem 0.75rem;
  background: #334155;
  border: 1px solid #475569;
  border-radius: 6px;
  color: #f8fafc;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.18s ease;
}

.copy-code-btn:hover {
  background: #475569;
  color: #ffffff;
}

.copy-code-btn.copied {
  background: var(--green, #22941a);
  border-color: var(--bright-fern, #38a700);
  color: #ffffff;
}

.copy-icon {
  width: 14px;
  height: 14px;
}

.check-icon {
  stroke-width: 3;
}

.code-content {
  margin: 0;
  padding: 1rem 1.1rem;
  overflow-x: auto;
  color: #f1f5f9;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.82rem;
  line-height: 1.6;
  white-space: pre;
}

.code-content code {
  color: inherit;
  font-family: inherit;
  font-size: inherit;
}

.copy-error-msg {
  color: #dc2626;
  font-size: 0.78rem;
  margin: 0;
}

/* Onboarding steps list */
.onboarding-steps {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 0.85rem 1rem;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 0.85rem;
}

.step-item {
  display: flex;
  align-items: flex-start;
  gap: 0.55rem;
  flex: 1;
}

.step-num {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  flex-shrink: 0;
  background: #dcfce7;
  color: var(--green, #22941a);
  font-weight: 700;
  font-size: 0.75rem;
  border-radius: 50%;
}

.step-text {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.step-text strong {
  font-size: 0.78rem;
  color: #0f172a;
}

.step-text span {
  font-size: 0.72rem;
  color: #64748b;
  line-height: 1.35;
}

.step-divider {
  width: 1px;
  height: 34px;
  background: #e2e8f0;
  flex-shrink: 0;
  align-self: center;
}

@media (max-width: 640px) {
  .onboarding-steps {
    flex-direction: column;
  }
  .step-divider {
    display: none;
  }
}
</style>
