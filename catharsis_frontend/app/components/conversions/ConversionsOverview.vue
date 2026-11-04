<template>
  <section class="conversions-overview" aria-labelledby="conversions-section-title">
    <!-- Barre d'outils supérieure -->
    <header class="overview-toolbar">
      <div class="toolbar-intro">
        <h2 id="conversions-section-title" class="sr-only">Objectifs de conversion</h2>
        <p class="toolbar-subtitle">
          Suivez vos événements clés et mesurez le taux de transformation de vos visiteurs.
        </p>
      </div>

      <div class="toolbar-actions">
        <periodFilter v-model="selectedPeriod" />

        <button
          type="button"
          class="create-goal-btn"
          :disabled="projectStore.projects.length === 0"
          @click="conversionStore.openCreateModal()"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2">
            <path stroke-linecap="round" d="M12 5v14M5 12h14"></path>
          </svg>
          <span>Configurer une conversion</span>
        </button>
      </div>
    </header>

    <!-- Message d'alerte ou succès -->
    <p v-if="conversionStore.message.errorMessage" class="alert-box error" role="alert">
      {{ conversionStore.message.errorMessage }}
    </p>

    <!-- Cartes de synthèse KPI -->
    <div class="kpi-summary-grid">
      <!-- Carte 1 : Taux de conversion global -->
      <div class="summary-metric-card highlight-card">
        <div class="metric-top">
          <span class="metric-label">Taux de conversion global</span>
          <div class="metric-icon green-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline>
              <polyline points="17 6 23 6 23 12"></polyline>
            </svg>
          </div>
        </div>
        <div class="metric-value-row">
          <strong class="metric-big-value">{{ conversionStore.globalConversionRate }}%</strong>
          <span class="metric-badge">
            {{ conversionStore.convertedSessions }} / {{ conversionStore.totalSessions }} sessions
          </span>
        </div>
        <p class="metric-caption">Proportion de sessions ayant atteint au moins un objectif</p>
      </div>

      <!-- Carte 2 : Nombre total de conversions -->
      <div class="summary-metric-card">
        <div class="metric-top">
          <span class="metric-label">Nombre de conversions</span>
          <div class="metric-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
        </div>
        <div class="metric-value-row">
          <strong class="metric-big-value">{{ conversionStore.totalConversions }}</strong>
          <span class="metric-sub">accomplissements</span>
        </div>
        <p class="metric-caption">Volume cumulé d’événements de conversion déclenchés</p>
      </div>

      <!-- Carte 3 : Objectifs actifs -->
      <div class="summary-metric-card">
        <div class="metric-top">
          <span class="metric-label">Objectifs configurés</span>
          <div class="metric-icon">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <circle cx="12" cy="12" r="6"></circle>
              <circle cx="12" cy="12" r="2"></circle>
            </svg>
          </div>
        </div>
        <div class="metric-value-row">
          <strong class="metric-big-value">{{ conversionStore.goals.length }}</strong>
          <span class="metric-sub">
            {{ conversionStore.customEventGoalsCount }} custom · {{ conversionStore.pageviewGoalsCount }} URL
          </span>
        </div>
        <p class="metric-caption">
          <template v-if="conversionStore.topPerformingGoal">
            Meilleur : <strong>{{ conversionStore.topPerformingGoal.name }}</strong> ({{ conversionStore.topPerformingGoal.conversion_rate }}%)
          </template>
          <template v-else>
            Aucun objectif actif pour le moment
          </template>
        </p>
      </div>
    </div>

    <!-- Tableau des objectifs ou État vide -->
    <div v-if="conversionStore.hasGoals" class="goals-table-card">
      <div class="card-heading">
        <div>
          <h3>Performance par objectif de conversion</h3>
          <p>Détail du nombre de conversions et du taux de transformation par objectif</p>
        </div>
        <span v-if="conversionStore.isLoading" class="loading-pill">Actualisation…</span>
      </div>

      <div class="table-responsive">
        <table class="goals-table">
          <thead>
            <tr>
              <th>Objectif</th>
              <th>Type de capture</th>
              <th>Cible / Déclencheur</th>
              <th class="text-right">Conversions</th>
              <th class="text-right">Sessions converties</th>
              <th class="col-rate">Taux de conversion (%)</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="goal in conversionStore.goals" :key="goal.id">
              <!-- Nom -->
              <td>
                <div class="goal-name-cell">
                  <span class="goal-dot"></span>
                  <strong>{{ goal.name }}</strong>
                </div>
              </td>

              <!-- Type -->
              <td>
                <span
                  class="type-pill"
                  :class="goal.goal_type === 'custom_event' ? 'pill-event' : 'pill-url'"
                >
                  <template v-if="goal.goal_type === 'custom_event'">
                    Événement personnalisé
                  </template>
                  <template v-else>
                    Visite d’URL
                  </template>
                </span>
              </td>

              <!-- Cible -->
              <td>
                <div class="target-cell">
                  <code class="target-code">{{ goal.target_value }}</code>
                  <button
                    v-if="goal.goal_type === 'custom_event'"
                    type="button"
                    class="copy-trigger-btn"
                    :title="`Copier window.Catharsis?.trackEvent('${goal.target_value}')`"
                    @click="copyTriggerSnippet(goal.id, goal.target_value)"
                  >
                    {{ copiedGoalId === goal.id ? 'Copié !' : 'Copier JS' }}
                  </button>
                </div>
              </td>

              <!-- Nombre total de conversions -->
              <td class="text-right font-mono font-bold">
                {{ goal.conversions_count }}
              </td>

              <!-- Sessions uniques converties -->
              <td class="text-right font-mono text-muted">
                {{ goal.converted_sessions }} / {{ conversionStore.totalSessions }}
              </td>

              <!-- Taux de conversion avec barre visuelle -->
              <td class="col-rate">
                <div class="rate-cell">
                  <div class="rate-bar-track">
                    <div
                      class="rate-bar-fill"
                      :style="{ width: `${Math.min(100, goal.conversion_rate)}%` }"
                    ></div>
                  </div>
                  <span class="rate-pct font-mono">{{ goal.conversion_rate.toFixed(1) }}%</span>
                </div>
              </td>

              <!-- Suppression -->
              <td class="text-center">
                <button
                  type="button"
                  class="delete-goal-btn"
                  title="Supprimer cet objectif"
                  :disabled="conversionStore.isSubmitting"
                  @click="handleDeleteGoal(goal.id)"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"></polyline>
                    <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                  </svg>
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- État vide lorsqu'aucun objectif n'est encore configuré -->
    <div v-else-if="!conversionStore.isLoading" class="empty-goals-wrapper">
      <emptyChartState
        title="Aucun objectif de conversion configuré"
        description="Définissez un événement personnalisé (ex: signup, purchase) ou une URL cible (ex: /merci) pour mesurer votre taux de conversion en %."
        actionText="Configurer ma première conversion"
        @action="conversionStore.openCreateModal()"
      />
    </div>

    <!-- Modale de création d'objectif -->
    <CreateConversionModal
      v-if="conversionStore.isCreateModalOpen"
      :site-id="activeSiteId"
      :start-date="selectedPeriod?.start"
      :end-date="selectedPeriod?.end"
      @created="handleGoalCreated"
    />
  </section>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useConversionStore } from '~/stores/conversionStore'
import { useProjectSiteStore } from '~/stores/projectSiteStore'
import { useAnalyticsStore } from '~/stores/analyticsStore'
import periodFilter, { type PeriodValue } from '~/components/Tools/periodFilter.vue'
import emptyChartState from '~/components/dashboard/emptyChartState.vue'
import CreateConversionModal from '~/components/conversions/CreateConversionModal.vue'

const conversionStore = useConversionStore()
const projectStore = useProjectSiteStore()
const analyticsStore = useAnalyticsStore()

const selectedPeriod = ref<PeriodValue | undefined>()
const copiedGoalId = ref<string>('')

const activeSiteId = computed(() => {
  return (
    analyticsStore.selectedSiteId ||
    conversionStore.selectedSiteId ||
    projectStore.projects[0]?.site_id ||
    ''
  )
})

async function loadConversions() {
  if (!activeSiteId.value) return
  await conversionStore.fetchConversions({
    site_id: activeSiteId.value,
    start_date: selectedPeriod.value?.start,
    end_date: selectedPeriod.value?.end,
  })
}

async function handleDeleteGoal(goalId: string) {
  await conversionStore.deleteGoal(goalId, {
    start_date: selectedPeriod.value?.start,
    end_date: selectedPeriod.value?.end,
  })
  // Synchronise aussi le KPI du dashboard principal
  if (activeSiteId.value) {
    await analyticsStore.fetchAnalytics({ site_id: activeSiteId.value })
  }
}

async function handleGoalCreated() {
  if (activeSiteId.value) {
    await analyticsStore.fetchAnalytics({ site_id: activeSiteId.value })
  }
}

async function copyTriggerSnippet(goalId: string, targetValue: string) {
  try {
    await navigator.clipboard.writeText(`window.Catharsis?.trackEvent('${targetValue}')`)
    copiedGoalId.value = goalId
    setTimeout(() => {
      if (copiedGoalId.value === goalId) {
        copiedGoalId.value = ''
      }
    }, 1800)
  } catch {
    copiedGoalId.value = ''
  }
}

onMounted(async () => {
  if (!projectStore.projects.length) {
    await projectStore.getProjects()
  }
  await loadConversions()
})

watch([activeSiteId, selectedPeriod], () => {
  loadConversions()
})
</script>

<style scoped>
.conversions-overview {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.overview-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 12px;
}

.toolbar-subtitle {
  margin: 0;
  font-size: 0.9rem;
  color: var(--text-muted, #64748b);
}

.toolbar-actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 0.75rem;
}

.create-goal-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.55rem 1rem;
  border-radius: 9999px;
  border: 1px solid var(--green, #22941a);
  background: var(--green, #22941a);
  color: #ffffff;
  font-size: 0.82rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.16s ease, transform 0.12s ease;
}

.create-goal-btn:hover:not(:disabled) {
  background: var(--bright-fern, #38a700);
  border-color: var(--bright-fern, #38a700);
}

.create-goal-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.alert-box.error {
  margin: 0;
  padding: 0.85rem 1rem;
  border-radius: 10px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
  font-size: 0.85rem;
}

/* Grille KPI */
.kpi-summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.25rem;
}

.summary-metric-card {
  padding: 1.25rem 1.4rem;
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.03);
}

.summary-metric-card.highlight-card {
  border-color: rgba(34, 148, 26, 0.35);
  background: linear-gradient(160deg, var(--card-bg, #ffffff) 65%, rgba(34, 148, 26, 0.05) 100%);
}

.metric-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.metric-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--text-muted, #64748b);
}

.metric-icon {
  width: 34px;
  height: 34px;
  border-radius: 8px;
  background: var(--icon-bg, #eff6ff);
  color: var(--text-heading, #0f172a);
  display: flex;
  align-items: center;
  justify-content: center;
}

.metric-icon.green-icon {
  background: #dcfce7;
  color: var(--green, #22941a);
}

.metric-value-row {
  display: flex;
  align-items: baseline;
  gap: 0.65rem;
}

.metric-big-value {
  font-size: 1.85rem;
  font-weight: 800;
  color: var(--text-heading, #0f172a);
  letter-spacing: -0.03em;
}

.metric-badge {
  padding: 0.2rem 0.55rem;
  border-radius: 9999px;
  background: #dcfce7;
  color: var(--black-forest, #293f14);
  font-size: 0.74rem;
  font-weight: 700;
}

.metric-sub {
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-muted, #64748b);
}

.metric-caption {
  margin: 0;
  font-size: 0.76rem;
  color: var(--text-muted, #64748b);
}

/* Tableau des objectifs */
.goals-table-card {
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 12px;
  overflow: hidden;
}

.card-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.card-heading h3 {
  margin: 0 0 0.2rem;
  font-size: 1.02rem;
  font-weight: 700;
  color: var(--text-heading, #0f172a);
}

.card-heading p {
  margin: 0;
  font-size: 0.8rem;
  color: var(--text-muted, #64748b);
}

.loading-pill {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--green, #22941a);
}

.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.goals-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
}

.goals-table th {
  padding: 0.85rem 1.25rem;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted, #64748b);
  background: var(--nav-hover-bg, #f8fafc);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
}

.goals-table td {
  padding: 1rem 1.25rem;
  font-size: 0.88rem;
  color: var(--text-heading, #0f172a);
  border-bottom: 1px solid var(--border-color, #e2e8f0);
  vertical-align: middle;
}

.goals-table tbody tr:last-child td {
  border-bottom: none;
}

.goals-table tbody tr:hover {
  background: var(--nav-hover-bg, #f8fafc);
}

.goal-name-cell {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.goal-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--green, #22941a);
  flex-shrink: 0;
}

.type-pill {
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.65rem;
  border-radius: 9999px;
  font-size: 0.74rem;
  font-weight: 600;
}

.pill-event {
  background: #dcfce7;
  color: var(--black-forest, #293f14);
}

.pill-url {
  background: #eff6ff;
  color: #1d4ed8;
}

.target-cell {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.target-code {
  padding: 0.2rem 0.5rem;
  background: #f1f5f9;
  border-radius: 6px;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.8rem;
  color: #0f172a;
}

.copy-trigger-btn {
  padding: 0.2rem 0.5rem;
  border-radius: 5px;
  border: 1px solid var(--border-color, #e2e8f0);
  background: var(--card-bg, #ffffff);
  color: var(--text-muted, #64748b);
  font-size: 0.7rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s ease;
}

.copy-trigger-btn:hover {
  border-color: var(--green, #22941a);
  color: var(--green, #22941a);
}

.text-right {
  text-align: right;
}

.text-center {
  text-align: center;
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

.font-bold {
  font-weight: 700;
}

.text-muted {
  color: var(--text-muted, #64748b);
}

.col-rate {
  min-width: 190px;
}

.rate-cell {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.rate-bar-track {
  flex: 1;
  height: 8px;
  background: var(--gauge-track, #f1f5f9);
  border-radius: 9999px;
  overflow: hidden;
}

.rate-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--green, #22941a), var(--malachite, #31d843));
  border-radius: 9999px;
  transition: width 0.35s ease;
}

.rate-pct {
  min-width: 48px;
  text-align: right;
  font-weight: 700;
  color: var(--black-forest, #293f14);
}

.delete-goal-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid transparent;
  background: transparent;
  color: var(--text-muted, #64748b);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.delete-goal-btn:hover:not(:disabled) {
  background: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}
</style>

