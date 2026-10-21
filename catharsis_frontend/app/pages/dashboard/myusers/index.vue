<template>
  <div class="dashboard-root">
    <Head>
      <title>Dashboard - Catharsis Analytics</title>
      <meta name="description" content="Gotics Business & Web Analytics Dashboard" />
    </Head>

    <div class="dashboard-app-layout">
      <DashboardSidebar
        :is-dark="isDark"
        @theme-change="handleThemeChange"
      />

      <main class="dashboard-main-area">
        <!-- Top Header (Search, Notifications, Profile) -->
        <DashboardHeader 
          title="mes utilisateurs"
          @add-site="isRegisterUserModalOpen = true" 
        />

        <!-- Résumé des caractéristiques des visiteurs -->
        <VisitorsSummary />
      </main>
    </div>
  </div>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue';
import DashboardSidebar from '~/components/dashboard/DashboardSidebar.vue';
import VisitorsSummary from '~/components/dashboard/VisitorsSummary.vue';

export default{
  components:{
    DashboardSidebar,
    VisitorsSummary
  },
  setup(){
    const isDark = ref(false)

    const handleThemeChange = (dark: boolean) => {
      isDark.value = dark
    }

    const isRegisterUserModalOpen = ref(false)

    const openRegisterUserModal = () => {
      isRegisterUserModalOpen.value = true
    }

    const closeRegisterUserModal = () => {
      isRegisterUserModalOpen.value = false
    }

    return{
        isDark,
        handleThemeChange,
        isRegisterUserModalOpen,
        openRegisterUserModal,
        closeRegisterUserModal
    }
  }
}

</script>

<style scoped>
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