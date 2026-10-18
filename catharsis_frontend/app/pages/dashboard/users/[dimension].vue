<template>
  <div class="users-page">
    <Head>
      <Title>{{ reportTitle }} — Catharsis Analytics</Title>
      <Meta name="description" content="Analysez l’origine et les caractéristiques de votre audience." />
    </Head>

    <div class="users-layout">
      <DashboardSidebar :is-dark="false" />

      <main class="users-main">
        <header class="page-header">
          <div>
            <NuxtLink to="/dashboard" class="back-link">← Tableau de bord</NuxtLink>
            <h1>{{ reportTitle }}</h1>
            <p>Répartition des visiteurs uniques par {{ reportDescription }}.</p>
          </div>
          <label v-if="projects.length" class="site-picker">
            <span>Site</span>
            <select v-model="selectedSiteId" aria-label="Sélectionner un site" @change="loadReport">
              <option v-for="project in projects" :key="project.site_id" :value="project.site_id">
                {{ project.name }}
              </option>
            </select>
          </label>
        </header>

        <div class="summary-card">
          <span class="summary-label">Visiteurs suivis</span>
          <strong>{{ report?.total_visitors ?? 0 }}</strong>
        </div>

        <p v-if="errorMessage" class="notice error" role="alert">{{ errorMessage }}</p>
        <p v-else-if="report?.message" class="notice" role="status">{{ report.message }}</p>

        <section class="report-card" aria-live="polite">
          <div class="report-heading">
            <h2>{{ reportTitle }}</h2>
            <span v-if="isLoading" class="loading-label">Chargement…</span>
          </div>

          <p v-if="!isLoading && report?.available && report.results.length === 0" class="empty-state">
            Aucune donnée disponible pour cette période.
          </p>

          <ol v-else-if="report?.results.length" class="result-list">
            <li v-for="(item, index) in report.results" :key="item.label" class="result-row">
              <span class="rank">{{ index + 1 }}</span>
              <span class="result-label">{{ item.label }}</span>
              <span class="result-count">{{ item.visitors }}</span>
              <div class="bar-track">
                <span
                  class="bar-fill"
                  :style="{ width: `${Math.max(2, (item.visitors / maxVisitors) * 100)}%` }"
                />
              </div>
            </li>
          </ol>
        </section>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DashboardSidebar from '~/components/dashboard/DashboardSidebar.vue'
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

const route = useRoute()
const { $api } = useNuxtApp()
const projectStore = useProjectSiteStore()
const projects = computed(() => projectStore.projects)
const selectedSiteId = ref('')
const report = ref<AudienceReport | null>(null)
const isLoading = ref(false)
const errorMessage = ref('')

const reportConfig: Record<string, { title: string; description: string }> = {
  countries: { title: 'Pays d’origine', description: 'pays' },
  sources: { title: 'Sources d’acquisition', description: 'source' },
  devices: { title: 'Appareils', description: 'appareil' },
  browsers: { title: 'Navigateurs', description: 'navigateur' },
  'operating-systems': { title: 'Systèmes d’exploitation', description: 'système d’exploitation' },
  pages: { title: 'Pages visitées', description: 'page' },
}

const dimension = computed(() => String(route.params.dimension || ''))
const reportTitle = computed(() => reportConfig[dimension.value]?.title || 'Audience')
const reportDescription = computed(() => reportConfig[dimension.value]?.description || 'catégorie')
const maxVisitors = computed(() => Math.max(1, ...(report.value?.results.map(item => item.visitors) || [1])))

async function loadReport() {
  if (!reportConfig[dimension.value] || !selectedSiteId.value) return

  isLoading.value = true
  errorMessage.value = ''
  try {
    report.value = await $api<AudienceReport>('/event/audience/', {
      query: { dimension: dimension.value, site_id: selectedSiteId.value },
    })
  } catch (error: any) {
    errorMessage.value = error?.data?.error || error?.message || 'Impossible de charger ces données.'
    report.value = null
  } finally {
    isLoading.value = false
  }
}

onMounted(async () => {
  await projectStore.getProjects()
  selectedSiteId.value = projectStore.projects[0]?.site_id || ''
  if (!selectedSiteId.value) {
    errorMessage.value = 'Enregistrez un site pour consulter les données de votre audience.'
  }
  await loadReport()
})

watch(dimension, () => {
  if (selectedSiteId.value) void loadReport()
})
</script>

<style scoped>
.users-page {
  min-height: 100vh;
  background: #f8fafc;
  color: #0f172a;
  font-family: 'Inter Tight', 'Inter', sans-serif;
}

.users-layout {
  display: flex;
  min-height: 100vh;
}

.users-main {
  flex: 1;
  min-width: 0;
  padding: 2rem;
}

.page-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.back-link {
  color: #2563eb;
  font-size: 0.85rem;
  text-decoration: none;
}

h1 {
  margin-top: 0.5rem;
  font-size: 1.7rem;
}

.page-header p {
  margin-top: 0.4rem;
  color: #64748b;
}

.site-picker,
.summary-card,
.report-card {
  border: 1px solid #e2e8f0;
  border-radius: 0.9rem;
  background: white;
}

.site-picker {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  padding: 0.6rem 0.8rem;
  color: #64748b;
  font-size: 0.85rem;
}

.site-picker select {
  max-width: 14rem;
  border: 0;
  color: #0f172a;
  background: transparent;
  font: inherit;
}

.summary-card {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  width: min(100%, 18rem);
  padding: 1.1rem 1.25rem;
  margin-bottom: 1rem;
}

.summary-label {
  color: #64748b;
  font-size: 0.85rem;
}

.summary-card strong {
  font-size: 1.75rem;
}

.report-card {
  padding: 1.4rem;
}

.report-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.report-heading h2 {
  font-size: 1rem;
}

.loading-label,
.empty-state {
  color: #64748b;
  font-size: 0.9rem;
}

.empty-state {
  padding: 2rem 0;
  text-align: center;
}

.notice {
  padding: 0.9rem 1rem;
  margin-bottom: 1rem;
  border: 1px solid #bfdbfe;
  border-radius: 0.75rem;
  background: #eff6ff;
  color: #1e40af;
  font-size: 0.9rem;
}

.notice.error {
  border-color: #fecaca;
  background: #fef2f2;
  color: #b91c1c;
}

.result-list {
  list-style: none;
}

.result-row {
  display: grid;
  grid-template-columns: 2rem minmax(8rem, 1fr) 4rem minmax(6rem, 1fr);
  align-items: center;
  gap: 0.8rem;
  min-height: 3.25rem;
  border-bottom: 1px solid #f1f5f9;
}

.rank {
  color: #94a3b8;
  font-size: 0.8rem;
}

.result-label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-size: 0.9rem;
}

.result-count {
  text-align: right;
  font-variant-numeric: tabular-nums;
  font-weight: 600;
}

.bar-track {
  height: 0.45rem;
  overflow: hidden;
  border-radius: 999px;
  background: #f1f5f9;
}

.bar-fill {
  display: block;
  height: 100%;
  border-radius: inherit;
  background: #2563eb;
}

@media (max-width: 768px) {
  .users-layout {
    flex-direction: column;
  }

  .users-main {
    padding: 1.25rem 1rem;
  }

  .page-header {
    align-items: stretch;
    flex-direction: column;
  }

  .result-row {
    grid-template-columns: 1.5rem minmax(5rem, 1fr) 3rem;
  }

  .bar-track {
    display: none;
  }
}
</style>
