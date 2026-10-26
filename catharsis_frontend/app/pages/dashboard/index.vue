<template>
  <div class="dashboard-root" :class="{ 'dark-theme': isDark }">
    <Head>
      <Title>Dashboard — Catharsis Analytics</Title>
      <Meta name="description" content="Gotics Business & Web Analytics Dashboard" />
    </Head>

    <div class="dashboard-app-layout">
      <!-- Left Sidebar -->
      <DashboardSidebar
        :is-dark="isDark"
        @theme-change="handleThemeChange"
      />

      <!-- Main Dashboard Content Area -->
      <main class="dashboard-main-area">
        <!-- Top Header (Search, Notifications, Profile) -->
          <DashboardHeader
            @add-site="isRegisterSiteModalOpen = true"
            @view-snippet="isTrackingSnippetModalOpen = true"
          />

        <!-- Grid of Dashboard Widgets -->
        <div v-if="projectStore.projects.length > 0" class="dashboard-grid">
          
          <!-- Row 1: Top Widgets -->
          <div class="grid-row row-top">
            <!-- Widget 1: 4-Quadrant KPI Stats Matrix -->
            <div class="grid-col col-kpi">
              <KpiMatrixCard />
            </div>

            <!-- Widget 2: User by time of day Heatmap -->
            <div class="grid-col col-heatmap">
              <HeatmapCard />
            </div>
          </div>

          <!-- Row 2: Bottom Widgets -->
          <div class="grid-row row-bottom">
            <!-- Widget 3: Active Users Step Area Chart -->
            <div class="grid-col col-active-users">
              <ActiveUsersChart />
            </div>

            <!-- Widget 4: Sessions by device Radial Gauge -->
            <div class="grid-col col-sessions-device">
              <SessionsDeviceCard />
            </div>
          </div>

        </div>

        <div v-else>
          <emptyChartState
            v-if="projectStore.projects.length === 0"
            title="Aucun site enregistré"
            description="Enregistrez votre premier site pour préparer le suivi de son activité."
            actionText="Enregistrer un site"
            @action="isRegisterSiteModalOpen = true"
          />
        </div>
      </main>
    </div>

    <RegisterSiteModal
      v-if="isRegisterSiteModalOpen"
      :is-loading="projectStore.isLoading"
      :error-message="projectStore.message.errorMessage"
      :created-project="createdProject"
      @close="handleCloseRegisterSiteModal"
      @submit="handleCreateProject"
    />

    <TrackingSnippetModal
      v-if="isTrackingSnippetModalOpen && activeProject"
      :site-id="activeProject.site_id"
      :site-name="activeProject.name"
      @close="isTrackingSnippetModalOpen = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useProjectSiteStore } from '~/stores/projectSiteStore'
import { useAnalyticsStore } from '~/stores/analyticsStore'
import DashboardSidebar from '~/components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '~/components/dashboard/DashboardHeader.vue'
import KpiMatrixCard from '~/components/dashboard/KpiMatrixCard.vue'
import HeatmapCard from '~/components/dashboard/HeatmapCard.vue'
import ActiveUsersChart from '~/components/dashboard/ActiveUsersChart.vue'
import SessionsDeviceCard from '~/components/dashboard/SessionsDeviceCard.vue'
import emptyChartState from '~/components/dashboard/emptyChartState.vue'
import RegisterSiteModal from '~/components/dashboard/RegisterSiteModal.vue'
import TrackingSnippetModal from '~/components/dashboard/TrackingSnippetModal.vue'

const projectStore = useProjectSiteStore()
const analyticsStore = useAnalyticsStore()
const isRegisterSiteModalOpen = ref(false)
const isTrackingSnippetModalOpen = ref(false)
const createdProject = ref<import('~/stores/projectSiteStore').Project | null>(null)

const activeProject = computed(() => {
  if (analyticsStore.selectedSiteId) {
    return projectStore.projects.find(p => p.site_id === analyticsStore.selectedSiteId) || projectStore.projects[0] || null
  }
  return projectStore.projects[0] || null
})

onMounted(async () => {
  await projectStore.getProjects()
  if (projectStore.projects.length > 0) {
    const defaultSiteId = projectStore.projects[0]?.site_id
    await analyticsStore.fetchAnalytics({ site_id: defaultSiteId })
  }
})

async function handleCreateProject(payload: { name: string }) {
  const project = await projectStore.createProject(payload)
  if (project) {
    createdProject.value = project
    await analyticsStore.fetchAnalytics({ site_id: project.site_id })
  }
}


function handleCloseRegisterSiteModal() {
  isRegisterSiteModalOpen.value = false
  createdProject.value = null
  projectStore.clearMessages()
}

// Theme toggle state (default light matching the screenshot)
const isDark = ref(false)

const handleThemeChange = (dark: boolean) => {
  isDark.value = dark
}
</script>

<style scoped>
/* CSS Variables for Light / Dark themes */
.dashboard-root {
  --bg-main: #f8fafc;
  --card-bg: #ffffff;
  --sidebar-bg: #ffffff;
  --border-color: #e2e8f0;
  --text-heading: #0f172a;
  --text-muted: #64748b;
  --input-bg: #ffffff;
  --icon-bg: #eff6ff;
  --toggle-bg: #f1f5f9;
  --nav-text: #64748b;
  --nav-hover-bg: #f8fafc;
  --nav-active-bg: #eff6ff;
  --grid-color: #f1f5f9;
  --gauge-track: #f1f5f9;

  min-height: 100vh;
  width: 100%;
  background-color: var(--bg-main);
  color: var(--text-heading);
  font-family: 'Inter Tight', 'Inter', -apple-system, sans-serif;
  transition: background-color 0.2s ease, color 0.2s ease;
}

/* Dark theme overrides */
.dashboard-root.dark-theme {
  --bg-main: #0b0f19;
  --card-bg: #111827;
  --sidebar-bg: #0f172a;
  --border-color: #1e293b;
  --text-heading: #f8fafc;
  --text-muted: #94a3b8;
  --input-bg: #1e293b;
  --icon-bg: #1e293b;
  --toggle-bg: #1e293b;
  --nav-text: #94a3b8;
  --nav-hover-bg: #1e293b;
  --nav-active-bg: #1e3a8a;
  --grid-color: #1e293b;
  --gauge-track: #1e293b;
}

.dashboard-app-layout {
  display: flex;
  min-height: 100vh;
  width: 100%;
}

.dashboard-main-area {
  flex: 1;
  padding: 1.75rem 2rem 2.5rem;
  overflow-y: auto;
  box-sizing: border-box;
}

@media (max-width: 768px) {
  .dashboard-app-layout {
    flex-direction: column;
  }

  .dashboard-main-area {
    padding: 1.25rem 1rem;
  }
}

/* Dashboard Grid Layout */
.dashboard-grid {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.grid-row {
  display: grid;
  gap: 1.5rem;
}

/* Row 1: KPI (4.5 cols) + Heatmap (5.5 cols) */
.row-top {
  grid-template-columns: 1fr;
}

@media (min-width: 1100px) {
  .row-top {
    grid-template-columns: 4.8fr 5.2fr;
  }
}

/* Row 2: Active Users (6.8 cols) + Sessions Device (3.2 cols) */
.row-bottom {
  grid-template-columns: 1fr;
}

@media (min-width: 1100px) {
  .row-bottom {
    grid-template-columns: 6.5fr 3.5fr;
  }
}

.grid-col {
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>
