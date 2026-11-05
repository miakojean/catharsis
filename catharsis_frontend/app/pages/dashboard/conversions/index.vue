<template>
  <div class="dashboard-root" :class="{ 'dark-theme': isDark }">
    <Head>
      <Title>Conversions — Catharsis Analytics</Title>
      <Meta name="description" content="Configurez et suivez vos objectifs de conversion personnalisés." />
    </Head>

    <div class="dashboard-app-layout">
      <DashboardSidebar
        :is-dark="isDark"
        @theme-change="handleThemeChange"
      />

      <main class="dashboard-main-area">
        <DashboardHeader
          title="conversions"
          @add-site="isRegisterSiteModalOpen = true"
          @view-snippet="isTrackingSnippetModalOpen = true"
        />

        <ConversionsOverview />
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
import { ref, computed } from 'vue'
import { useProjectSiteStore, type Project } from '~/stores/projectSiteStore'
import { useAnalyticsStore } from '~/stores/analyticsStore'
import DashboardSidebar from '~/components/dashboard/DashboardSidebar.vue'
import DashboardHeader from '~/components/dashboard/DashboardHeader.vue'
import ConversionsOverview from '~/components/conversions/ConversionsOverview.vue'
import RegisterSiteModal from '~/components/modale/RegisterSiteModal.vue'
import TrackingSnippetModal from '~/components/dashboard/TrackingSnippetModal.vue'
import { useThemeStore } from '~/stores/themeStore'

const projectStore = useProjectSiteStore()
const analyticsStore = useAnalyticsStore()
const themeStore = useThemeStore()

const isDark = computed(() => themeStore.isDark)
const isRegisterSiteModalOpen = ref(false)
const isTrackingSnippetModalOpen = ref(false)
const createdProject = ref<Project | null>(null)

const activeProject = computed(() => {
  if (analyticsStore.selectedSiteId) {
    return (
      projectStore.projects.find((p) => p.site_id === analyticsStore.selectedSiteId) ||
      projectStore.projects[0] ||
      null
    )
  }
  return projectStore.projects[0] || null
})

function handleThemeChange(dark: boolean) {
  themeStore.setTheme(dark)
}

async function handleCreateProject(payload: { name: string }) {
  const project = await projectStore.createProject(payload)
  if (project) {
    createdProject.value = project
    analyticsStore.setSite(project.site_id)
  }
}

function handleCloseRegisterSiteModal() {
  isRegisterSiteModalOpen.value = false
  createdProject.value = null
  projectStore.clearMessages()
}
</script>

<style scoped>
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
  min-width: 0;
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
</style>

