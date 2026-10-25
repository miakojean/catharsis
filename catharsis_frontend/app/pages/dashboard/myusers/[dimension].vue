<template>
  <div class="users-page">
    <Head>
      <Title>{{ reportTitle }} — Catharsis Analytics</Title>
      <Meta name="description" content="Analysez l'origine et les caractéristiques de votre audience." />
    </Head>

    <div class="users-layout">
      <DashboardSidebar :is-dark="false" />

      <main class="users-main">

        <DashboardHeader :title="reportTitle"/>

        <div class="summary-card">
          <span class="summary-label">Visiteurs suivis</span>
          <strong>{{ report?.total_visitors ?? 0 }}</strong>
        </div>

        <p v-if="errorMessage" class="notice error" role="alert">{{ errorMessage }}</p>
        <p v-else-if="report?.message" class="notice" role="status">{{ report.message }}</p>

        <section class="report-card" aria-live="polite">
          <div class="report-heading">
            <h2>Tableau de {{ reportTitle }}</h2>
            <span v-if="isLoading" class="loading-label">Chargement…</span>
          </div>

          <p v-if="!isLoading && report?.available && report.results.length === 0" class="empty-state">
            Aucune donnée disponible pour cette période.
          </p>

          <!-- Tableau inspiré de la maquette -->
          <div v-else-if="report?.results.length" class="table-wrapper">
            <table class="data-table">
              <thead>
                <tr>
                  <th class="col-icon"></th>
                  <th>{{ reportDescription.charAt(0).toUpperCase() + reportDescription.slice(1) }}</th>
                  <th class="text-right">Visiteurs</th>
                  <th class="text-right">Proportion</th>
                  <th class="text-center">Statut</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(item, index) in report.results" :key="item.label">
                  <td class="col-icon">
                    <span class="row-icon">...</span>
                  </td>
                  <td class="font-medium">{{ item.label }}</td>
                  <td class="text-right font-mono">{{ item.visitors }}</td>
                  <td class="text-right font-mono">
                    {{ ((item.visitors / (report.total_visitors || 1)) * 100).toFixed(1) }}%
                  </td>
                  <td class="text-center">
                    <span class="status-pill" :class="getBadgeTheme(index)">
                      {{ getBadgeLabel(index) }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
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
import DashboardHeader from '~/components/dashboard/DashboardHeader.vue'

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

// Fonctions utilitaires pour simuler les badges de la maquette
const getBadgeTheme = (index: number) => {
  const themes = ['theme-pending', 'theme-ready', 'theme-arrived', 'theme-draft', 'theme-canceled']
  return themes[index % themes.length]
}

const getBadgeLabel = (index: number) => {
  const labels = ['En cours', 'Prêt', 'Terminé', 'Brouillon', 'Annulé']
  return labels[index % labels.length]
}

onMounted(async () => {
  await projectStore.getProjects()
  selectedSiteId.value = (route.query.site_id as string) || projectStore.projects[0]?.site_id || ''
  if (!selectedSiteId.value) {
    errorMessage.value = 'Enregistrez un site pour consulter les données de votre audience.'
  }
  await loadReport()
})

watch([dimension, () => route.query.site_id], () => {
  if (route.query.site_id) {
    selectedSiteId.value = String(route.query.site_id)
  }
  if (selectedSiteId.value) void loadReport()
})
</script>

<style scoped>
/* Conservez vos styles généraux existants ici... */
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
  background: none;
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

/* Nouveaux styles pour le tableau */
.table-wrapper {
  overflow-x: auto;
  border: 1px solid #f1f5f9;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.875rem;
  white-space: nowrap;
}

.data-table thead {
  background-color: #f8fafc;
  color: #475569;
  font-weight: 600;
}

.data-table th,
.data-table td {
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.data-table tbody tr:hover {
  background-color: #f8fafc;
}

.text-right {
  text-align: right;
}

.text-center {
  text-align: center;
}

.font-medium {
  font-weight: 500;
  color: #1e293b;
}

.font-mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  color: #64748b;
}

/* Icône de ligne factice (comme sur la maquette) */
.row-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 1.75rem;
  height: 1.25rem;
  background: #eff6ff;
  color: #60a5fa;
  border-radius: 0.25rem;
  font-weight: bold;
  letter-spacing: 1px;
  line-height: 1;
}

/* Badges de statut */
.status-pill {
  display: inline-block;
  padding: 0.25rem 0.75rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
}

.theme-pending { background: #fef9c3; color: #a16207; }
.theme-ready { background: #e0e7ff; color: #4338ca; }
.theme-arrived { background: #dcfce7; color: #15803d; }
.theme-draft { background: #f3e8ff; color: #7e22ce; }
.theme-canceled { background: #fee2e2; color: #b91c1c; }

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
}
</style>