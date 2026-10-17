<template>
  <header class="dashboard-header">
    <div class="header-titles">
      <h1 class="header-title">Dashboard</h1>
      <p v-if="authStore.user?.email" class="header-subtitle">Bienvenue, {{ authStore.user.email }}</p>
    </div>

    <div class="header-actions">
      <!-- Site selector dropdown if multiple projects exist -->
      <div v-if="projectStore.projects.length > 0" class="site-picker">
        <svg class="site-icon" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="2" y1="12" x2="22" y2="12"></line>
          <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
        </svg>
        <select
          id="dashboard-site-select"
          class="site-select"
          :value="analyticsStore.selectedSiteId || projectStore.projects[0]?.site_id"
          @change="onSiteSelect"
          aria-label="Sélectionner un site web"
        >
          <option v-for="p in projectStore.projects" :key="p.id" :value="p.site_id">
            {{ p.name }}
          </option>
        </select>
      </div>

      <button type="button" class="add-site-btn" @click="$emit('add-site')">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path stroke-linecap="round" d="M12 5v14M5 12h14"></path>
        </svg>
        <span>Enregistrer un site</span>
      </button>

      <!-- Search input -->
      <div class="search-bar">
        <svg class="search-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8"></circle>
          <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
        </svg>
        <input
          type="text"
          class="search-input"
          placeholder="Search here ..."
        />
      </div>

      <!-- Notification Bell -->
      <button type="button" class="notif-btn" aria-label="Notifications">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
          <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"></path>
          <path d="M13.73 21a2 2 0 0 1-3.46 0"></path>
        </svg>
        <span class="unread-dot"></span>
      </button>

      <ProfileButton />
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/authStore'
import { useProjectSiteStore } from '~/stores/projectSiteStore'
import { useAnalyticsStore } from '~/stores/analyticsStore'
import ProfileButton from '~/components/buttons/profileButton.vue'

const authStore = useAuthStore()
const projectStore = useProjectSiteStore()
const analyticsStore = useAnalyticsStore()

defineEmits<{
  (event: 'add-site'): void
}>()

function onSiteSelect(e: Event) {
  const target = e.target as HTMLSelectElement
  if (target && target.value) {
    analyticsStore.setSite(target.value)
  }
}
</script>


<style scoped>
.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 1.5rem;
}

.header-titles {
  display: flex;
  flex-direction: column;
}

.header-title {
  font-size: 1.625rem;
  font-weight: 700;
  color: var(--text-heading, #0f172a);
  letter-spacing: -0.02em;
  margin: 0;
}

.header-subtitle {
  font-size: 0.875rem;
  color: var(--text-muted, #64748b);
  margin: 0.25rem 0 0 0;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

/* Site Picker */
.site-picker {
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  background-color: var(--input-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 9999px;
  padding: 0 0.85rem;
  height: 40px;
  color: var(--text-heading, #0f172a);
  transition: all 0.15s ease;
}

.site-picker:hover {
  border-color: var(--green, #22941a);
}

.site-icon {
  color: var(--green, #22941a);
  flex-shrink: 0;
}

.site-select {
  border: none;
  background: transparent;
  color: var(--text-heading, #0f172a);
  font-family: inherit;
  font-size: 0.8125rem;
  font-weight: 600;
  outline: none;
  cursor: pointer;
  padding-right: 0.25rem;
}


.add-site-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  min-height: 40px;
  padding: 0 1rem;
  border: 1px solid var(--black-forest, #293f14);
  border-radius: 9999px;
  background: var(--black-forest, #293f14);
  color: #fff;
  font: inherit;
  font-size: 0.8125rem;
  font-weight: 600;
  white-space: nowrap;
  cursor: pointer;
  transition: background-color 0.18s ease, border-color 0.18s ease, transform 0.18s ease;
}

.add-site-btn:hover {
  transform: translateY(-1px);
  background: var(--green, #22941a);
  border-color: var(--green, #22941a);
}

.add-site-btn:focus-visible {
  outline: 3px solid rgb(34 148 26 / 22%);
  outline-offset: 2px;
}

.add-site-btn svg {
  width: 16px;
  height: 16px;
  flex: 0 0 auto;
}

/* Search bar */
.search-bar {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 0.95rem;
  color: #94a3b8;
  pointer-events: none;
}

.search-input {
  width: 260px;
  height: 40px;
  padding: 0 1rem 0 2.5rem;
  border-radius: 9999px;
  background-color: var(--input-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  font-size: 0.84375rem;
  color: var(--text-heading, #0f172a);
  outline: none;
  transition: all 0.15s ease;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
}

/* Notification */
.notif-btn {
  position: relative;
  background: none;
  border: none;
  padding: 0.5rem;
  color: var(--nav-text, #64748b);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  transition: all 0.15s ease;
}

.notif-btn:hover {
  background-color: var(--nav-hover-bg, #f1f5f9);
  color: var(--text-heading, #0f172a);
}

.unread-dot {
  position: absolute;
  top: 7px;
  right: 7px;
  width: 7px;
  height: 7px;
  border-radius: 9999px;
  background-color: #ef4444;
  border: 1.5px solid var(--card-bg, #ffffff);
}

@media (max-width: 640px) {
  .search-input {
    width: 140px;
  }

  .header-actions {
    gap: 0.5rem;
  }

  .add-site-btn {
    width: 40px;
    padding: 0;
  }

  .add-site-btn span {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
  }
}
</style>
