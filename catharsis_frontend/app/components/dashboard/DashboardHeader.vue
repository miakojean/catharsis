<template>
  <header class="dashboard-header">
    <div class="header-titles">
      <h1 class="header-title">{{title || 'Dashboard'}}</h1>
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

      <button
        v-if="projectStore.projects.length > 0"
        type="button"
        class="view-snippet-btn"
        title="Voir les instructions et le code d'installation"
        @click="$emit('view-snippet')"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <polyline points="16 18 22 12 16 6"></polyline>
          <polyline points="8 6 2 12 8 18"></polyline>
        </svg>
        <span class="btn-text">Code de suivi</span>
      </button>

      <button
        type="button"
        class="add-site-btn"
        title="Enregistrer un nouveau site"
        @click="$emit('add-site')"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true">
          <path stroke-linecap="round" d="M12 5v14M5 12h14"></path>
        </svg>
        <span class="btn-text">Enregistrer un site</span>
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

      <ProfileButton class="header-profile" />
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

defineProps<{
  title?: string,
}>()

defineEmits<{
  (event: 'add-site'): void
  (event: 'view-snippet'): void
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
  gap: 1rem;
  width: 100%;
  max-width: 100%;
  margin-bottom: 1.5rem;
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 8px 24px -12px rgba(15, 23, 42, 0.12);
  padding: 0.875rem 1.25rem;
  border-radius: 10px;
  box-sizing: border-box;
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.header-titles {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 0 1 auto;
}

.header-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-heading, #0f172a);
  letter-spacing: -0.02em;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  text-transform: capitalize;
}

.header-subtitle {
  font-size: 0.8125rem;
  color: var(--text-muted, #64748b);
  margin: 0.2rem 0 0 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 260px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1 1 auto;
  justify-content: flex-end;
  flex-wrap: nowrap;
  min-width: 0;
}

/* Site Picker */
.site-picker {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  background-color: var(--input-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 9999px;
  padding: 0 0.75rem;
  height: 38px;
  max-width: 175px;
  color: var(--text-heading, #0f172a);
  box-sizing: border-box;
  flex-shrink: 0;
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
  max-width: 125px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Tracking Snippet Button */
.view-snippet-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  height: 38px;
  padding: 0 0.85rem;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 9999px;
  background: var(--input-bg, #ffffff);
  color: var(--text-heading, #0f172a);
  font: inherit;
  font-size: 0.8125rem;
  font-weight: 600;
  white-space: nowrap;
  cursor: pointer;
  flex-shrink: 0;
  box-sizing: border-box;
  transition: all 0.18s ease;
}

.view-snippet-btn:hover {
  border-color: var(--green, #22941a);
  color: var(--green, #22941a);
  background: #f0fdf4;
}

.view-snippet-btn svg {
  width: 15px;
  height: 15px;
  color: var(--green, #22941a);
  flex: 0 0 auto;
}

/* Add Site Button */
.add-site-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.45rem;
  height: 38px;
  padding: 0 0.9rem;
  border: 1px solid var(--black-forest, #293f14);
  border-radius: 9999px;
  background: var(--black-forest, #293f14);
  color: #fff;
  font: inherit;
  font-size: 0.8125rem;
  font-weight: 600;
  white-space: nowrap;
  cursor: pointer;
  flex-shrink: 0;
  box-sizing: border-box;
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
  flex: 0 1 180px;
  min-width: 110px;
  max-width: 220px;
}

.search-icon {
  position: absolute;
  left: 0.85rem;
  color: #94a3b8;
  pointer-events: none;
}

.search-input {
  width: 100%;
  height: 38px;
  padding: 0 0.85rem 0 2.25rem;
  border-radius: 9999px;
  background-color: var(--input-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  font-size: 0.8125rem;
  color: var(--text-heading, #0f172a);
  outline: none;
  box-sizing: border-box;
  transition: all 0.15s ease;
}

.search-input::placeholder {
  color: #94a3b8;
}

.search-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
}

/* Notification Button */
.notif-btn {
  position: relative;
  background: none;
  border: none;
  width: 38px;
  height: 38px;
  color: var(--nav-text, #64748b);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  flex-shrink: 0;
  box-sizing: border-box;
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

/* User Avatar Profile Button: strictly prevent wrapping or squishing */
.header-profile,
:deep(.profile-wrapper) {
  flex-shrink: 0;
  display: flex;
  align-items: center;
}

/* Screen width <= 1260px: condense buttons so everything fits on one single line */
@media (max-width: 1260px) {
  .search-bar {
    flex: 0 1 140px;
    min-width: 80px;
  }

  .btn-text {
    display: none;
  }

  .view-snippet-btn,
  .add-site-btn {
    width: 38px;
    height: 38px;
    padding: 0;
    border-radius: 50%;
  }
}

/* Tablet & Smaller: titles on top, but ALL actions stay strictly on the SAME line below */
@media (max-width: 860px) {
  .dashboard-header {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
    padding: 0.75rem 1rem;
  }

  .header-titles {
    width: 100%;
  }

  .header-actions {
    width: 100%;
    justify-content: flex-start;
    gap: 0.45rem;
    flex-wrap: nowrap;
  }

  .search-bar {
    flex: 1 1 auto;
    min-width: 70px;
    max-width: none;
  }
}

/* Mobile: compact sizes, still strictly on ONE line */
@media (max-width: 520px) {
  .dashboard-header {
    padding: 0.65rem 0.75rem;
  }

  .header-actions {
    gap: 0.35rem;
    flex-wrap: nowrap;
  }

  .site-picker {
    max-width: 110px;
    padding: 0 0.45rem;
    height: 36px;
  }

  .site-select {
    max-width: 70px;
    font-size: 0.75rem;
  }

  .view-snippet-btn,
  .add-site-btn,
  .notif-btn {
    width: 36px;
    height: 36px;
  }

  .search-bar {
    flex: 1 1 60px;
    min-width: 60px;
  }

  .search-input {
    height: 36px;
    padding: 0 0.5rem 0 1.85rem;
    font-size: 0.75rem;
  }

  .search-icon {
    left: 0.55rem;
    width: 13px;
    height: 13px;
  }
}
</style>
