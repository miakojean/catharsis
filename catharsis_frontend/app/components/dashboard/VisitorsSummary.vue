<template>
  <section class="visitors-summary" aria-labelledby="visitors-summary-title">
    <header class="summary-header">
      <div>
        <h2 id="visitors-summary-title">Profil des visiteurs</h2>
        <p>Les principales caractéristiques de votre audience, en un coup d’œil.</p>
      </div>
      <div class="total-box">
        <span>Visiteurs uniques</span>
        <strong>{{ totalVisitors }}</strong>
      </div>
    </header>

    <p v-if="globalError" class="notice error" role="alert">{{ globalError }}</p>

    <div class="cards-grid" aria-live="polite">
      <article v-for="card in cards" :key="card.key" class="dimension-card">
        <div class="card-heading">
          <h3>{{ card.title }}</h3>
          <span v-if="isLoading" class="loading-label">Chargement…</span>
        </div>

        <p v-if="card.error" class="card-note error">{{ card.error }}</p>
        <p v-else-if="!isLoading && !card.available" class="card-note">{{ card.message }}</p>
        <p v-else-if="!isLoading && card.rows.length === 0" class="card-note">
          Aucune donnée pour le moment.
        </p>

        <ul v-else class="rows">
          <li v-for="row in card.rows" :key="row.label" class="row">
            <div class="row-text">
              <span class="row-label" :title="row.label">{{ row.label }}</span>
              <span class="row-value">
                {{ row.visitors }}
                <small>{{ row.percent.toFixed(1) }}%</small>
              </span>
            </div>
            <div class="bar" role="presentation">
              <div class="bar-fill" :style="{ width: `${row.percent}%` }" />
            </div>
          </li>
        </ul>

        <NuxtLink :to="card.to" class="detail-button">
          Voir le détail
          <span v-if="card.total > 0" class="detail-count">{{ card.total }}</span>
        </NuxtLink>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useProjectSiteStore } from '~/stores/projectSiteStore'

interface AudienceResult {
  label: string
  visitors: number
}

interface AudienceReport {
  dimension: string
  available: boolean
  message: string
  total_visitors: number
  results: AudienceResult[]
}

const props = withDefaults(
  defineProps<{
    /** Site à analyser. Par défaut : le premier site de l'utilisateur. */
    siteId?: string
    /** Nombre de lignes affichées par carte. */
    limit?: number
    /** Chemin de la page de détail (sans le slash final), suivi de /:dimension. */
    detailBasePath?: string
  }>(),
  { siteId: '', limit: 5, detailBasePath: '/dashboard/users' },
)

const DIMENSIONS = [
  { key: 'countries', title: 'Pays d’origine' },
  { key: 'sources', title: 'Sources d’acquisition' },
  { key: 'devices', title: 'Appareils' },
  { key: 'browsers', title: 'Navigateurs' },
  { key: 'operating-systems', title: 'Systèmes d’exploitation' },
  { key: 'pages', title: 'Pages visitées' },
]

const { $api } = useNuxtApp()
const projectStore = useProjectSiteStore()

const fallbackSiteId = ref('')
const reports = ref<Record<string, AudienceReport | null>>({})
const errors = ref<Record<string, string>>({})
const isLoading = ref(false)
const globalError = ref('')
let requestToken = 0 // ignore les réponses d'un chargement dépassé

const activeSiteId = computed(() => props.siteId || fallbackSiteId.value)

const totalVisitors = computed(
  () => Object.values(reports.value).find((report) => report)?.total_visitors ?? 0,
)

const cards = computed(() =>
  DIMENSIONS.map(({ key, title }) => {
    const report = reports.value[key]
    const total = report?.total_visitors || 0
    const results = report?.results ?? []
    return {
      key,
      title,
      available: report?.available ?? true,
      message: report?.message ?? '',
      error: errors.value[key] ?? '',
      total: results.length,
      rows: results.slice(0, props.limit).map((row) => ({
        ...row,
        percent: total ? (row.visitors / total) * 100 : 0,
      })),
      to: {
        path: `${props.detailBasePath}/${key}`,
        query: activeSiteId.value ? { site_id: activeSiteId.value } : undefined,
      },
    }
  }),
)

async function loadSummary() {
  if (!activeSiteId.value) return

  const token = ++requestToken
  isLoading.value = true
  globalError.value = ''

  const settled = await Promise.allSettled(
    DIMENSIONS.map(({ key }) =>
      $api<AudienceReport>('/event/audience/', {
        query: { dimension: key, site_id: activeSiteId.value },
      }),
    ),
  )
  if (token !== requestToken) return

  const nextReports: Record<string, AudienceReport | null> = {}
  const nextErrors: Record<string, string> = {}
  settled.forEach((result, index) => {
    const { key } = DIMENSIONS[index]
    if (result.status === 'fulfilled') {
      nextReports[key] = result.value
    } else {
      const error: any = result.reason
      nextReports[key] = null
      nextErrors[key] =
        error?.data?.detail || error?.data?.error || 'Impossible de charger ces données.'
    }
  })
  reports.value = nextReports
  errors.value = nextErrors
  isLoading.value = false
}

onMounted(async () => {
  if (!props.siteId) {
    await projectStore.getProjects()
    fallbackSiteId.value = projectStore.projects[0]?.site_id || ''
  }
  if (!activeSiteId.value) {
    globalError.value = 'Enregistrez un site pour consulter les données de votre audience.'
    return
  }
  await loadSummary()
})

watch(
  () => props.siteId,
  () => void loadSummary(),
)
</script>

<style scoped>
.visitors-summary {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  font-family: 'Inter Tight', 'Inter', sans-serif;
  color: #0f172a;
}

.summary-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem;
}

.summary-header h2 {
  font-size: 1.25rem;
}

.summary-header p {
  margin-top: 0.3rem;
  color: #64748b;
  font-size: 0.9rem;
}

.total-box {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 0.15rem;
  color: #64748b;
  font-size: 0.85rem;
}

.total-box strong {
  color: #0f172a;
  font-size: 1.75rem;
  line-height: 1;
}

.notice {
  padding: 0.75rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.75rem;
  background: white;
  color: #475569;
  font-size: 0.875rem;
}

.notice.error,
.card-note.error {
  color: #b91c1c;
}

.notice.error {
  border-color: #fecaca;
  background: #fef2f2;
}

.cards-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.25rem;
}

@media (min-width: 700px) {
  .cards-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1200px) {
  .cards-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

.dimension-card {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-width: 0;
  padding: 1.25rem;
  border: 1px solid #e2e8f0;
  border-radius: 0.9rem;
  background: white;
}

.card-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-heading h3 {
  font-size: 1rem;
}

.loading-label {
  color: #94a3b8;
  font-size: 0.8rem;
}

.card-note {
  flex: 1;
  color: #64748b;
  font-size: 0.875rem;
}

.rows {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.85rem;
  margin: 0;
  padding: 0;
  list-style: none;
}

.row-text {
  display: flex;
  justify-content: space-between;
  gap: 0.75rem;
  margin-bottom: 0.35rem;
  font-size: 0.875rem;
}

.row-label {
  min-width: 0;
  overflow: hidden;
  color: #1e293b;
  font-weight: 500;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.row-value {
  flex-shrink: 0;
  color: #475569;
  font-variant-numeric: tabular-nums;
}

.row-value small {
  margin-left: 0.4rem;
  color: #94a3b8;
  font-size: 0.75rem;
}

.bar {
  height: 0.375rem;
  border-radius: 999px;
  background: #eff6ff;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  min-width: 2px;
  border-radius: 999px;
  background: #2563eb;
}

.detail-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.6rem 1rem;
  border: 1px solid #bfdbfe;
  border-radius: 0.6rem;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 0.875rem;
  font-weight: 600;
  text-decoration: none;
  transition: background-color 0.15s, border-color 0.15s;
}

.detail-button:hover {
  border-color: #93c5fd;
  background: #dbeafe;
}

.detail-button:focus-visible {
  outline: 2px solid #2563eb;
  outline-offset: 2px;
}

.detail-count {
  padding: 0 0.5rem;
  border-radius: 999px;
  background: white;
  color: #2563eb;
  font-size: 0.75rem;
}

@media (max-width: 768px) {
  .summary-header {
    align-items: stretch;
    flex-direction: column;
    gap: 1rem;
  }

  .total-box {
    align-items: flex-start;
  }
}
</style>
