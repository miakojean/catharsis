<template>
  <aside class="dashboard-sidebar">
    <!-- Brand Logo -->
    <div class="sidebar-brand">
      <NuxtLink to="/dashboard" class="brand-link">
        <div class="brand-logo-icon">
          <!-- Blue circular icon with white curve arrow / lightning -->
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="12" fill="#2563eb" />
            <path
              d="M7 13.5L12 8.5M12 8.5L17 13.5M12 8.5V17"
              stroke="#ffffff"
              stroke-width="2.2"
              stroke-linecap="round"
              stroke-linejoin="round"
              transform="rotate(45 12 12)"
            />
          </svg>
        </div>
        <span class="brand-name">Catharsis</span>
      </NuxtLink>
    </div>

    <!-- Main Navigation List -->
    <nav class="sidebar-nav">
      <ul class="nav-list">
        <!-- Dashboard (Active) -->
        <li class="nav-item">
          <NuxtLink to="/dashboard" class="nav-link active">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
            <span class="nav-label">Dashboard</span>
          </NuxtLink>
        </li>

        <!-- Customization -->
        <li class="nav-item">
          <button type="button" class="nav-link nav-btn" @click="activeMenu = activeMenu === 'customization' ? '' : 'customization'">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            <span class="nav-label">Customization</span>
            <svg class="chevron-icon" :class="{ 'rotated': activeMenu === 'customization' }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </li>

        <!-- Realtime -->
        <li class="nav-item">
          <button type="button" class="nav-link nav-btn" @click="activeMenu = activeMenu === 'realtime' ? '' : 'realtime'">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <span class="nav-label">Realtime</span>
            <svg class="chevron-icon" :class="{ 'rotated': activeMenu === 'realtime' }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </li>

        <!-- Audience with Badge -->
        <li class="nav-item">
          <a href="#" class="nav-link" @click.prevent>
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <span class="nav-label">Audience</span>
            <span class="nav-badge">10</span>
          </a>
        </li>

        <!-- Behavior -->
        <li class="nav-item">
          <button type="button" class="nav-link nav-btn" @click="activeMenu = activeMenu === 'behavior' ? '' : 'behavior'">
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span class="nav-label">Behavior</span>
            <svg class="chevron-icon" :class="{ 'rotated': activeMenu === 'behavior' }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </button>
        </li>

        <!-- Conversion -->
        <li class="nav-item">
          <a href="#" class="nav-link" @click.prevent>
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="20" x2="18" y2="10"></line>
              <line x1="12" y1="20" x2="12" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
            <span class="nav-label">Conversion</span>
          </a>
        </li>
      </ul>

      <!-- Section "OTHERS" -->
      <div class="nav-section-title">OTHERS</div>
      <ul class="nav-list">
        <li class="nav-item">
          <a href="#" class="nav-link" @click.prevent>
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span class="nav-label">Settings</span>
          </a>
        </li>

        <li class="nav-item">
          <a href="#" class="nav-link" @click.prevent>
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 18v-6a9 9 0 0 1 18 0v6"></path>
              <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z"></path>
            </svg>
            <span class="nav-label">Help Center</span>
          </a>
        </li>
      </ul>
    </nav>

    <!-- Bottom Appearance Switcher (Light / Dark) -->
    <div class="sidebar-appearance">
      <span class="appearance-title">APPEARANCE</span>
      <div class="appearance-toggle">
        <button
          type="button"
          class="toggle-opt"
          :class="{ 'active': !isDark }"
          @click="$emit('theme-change', false)"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
          </svg>
          <span>Light</span>
        </button>

        <button
          type="button"
          class="toggle-opt"
          :class="{ 'active': isDark }"
          @click="$emit('theme-change', true)"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
          <span>Dark</span>
        </button>
      </div>
    </div>
    
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  isDark?: boolean
}>()

defineEmits<{
  (e: 'theme-change', isDark: boolean): void
}>()

const activeMenu = ref('')
</script>

<style scoped>
.dashboard-sidebar {
  position:sticky;
  top: 0px;
  width: 240px;
  min-width: 240px;
  height: 100vh;
  background-color: var(--sidebar-bg, #ffffff);
  border-right: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 1.25rem ;
  box-sizing: border-box;
  user-select: none;
}

/* Brand */
.sidebar-brand {
  margin-bottom: 2rem;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  text-decoration: none;
}

.brand-logo-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-heading, #0f172a);
  letter-spacing: -0.02em;
}

/* Nav */
.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.nav-item {
  width: 100%;
}

.nav-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.65rem 0.85rem;
  border-radius: 0.65rem;
  text-decoration: none;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--nav-text, #64748b);
  transition: all 0.15s ease;
  width: 100%;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
}

.nav-btn {
  justify-content: flex-start;
}

.nav-link:hover {
  background-color: var(--nav-hover-bg, #f8fafc);
  color: var(--text-heading, #0f172a);
}

.nav-link.active {
  background-color: var(--nav-active-bg, #eff6ff);
  color: #2563eb;
  font-weight: 600;
}

.nav-icon {
  flex-shrink: 0;
}

.nav-label {
  flex: 1;
}

.nav-badge {
  background-color: #f97316;
  color: #ffffff;
  font-size: 0.6875rem;
  font-weight: 700;
  padding: 0.1rem 0.45rem;
  border-radius: 9999px;
  line-height: 1.2;
}

.chevron-icon {
  transition: transform 0.2s ease;
  color: #94a3b8;
}

.chevron-icon.rotated {
  transform: rotate(180deg);
}

.nav-section-title {
  font-size: 0.6875rem;
  font-weight: 600;
  color: #94a3b8;
  letter-spacing: 0.05em;
  margin: 1.75rem 0 0.65rem 0.5rem;
}

/* Appearance Switcher */
.sidebar-appearance {
  margin-top: 2rem;
  padding-top: 1rem;
}

.appearance-title {
  display: block;
  font-size: 0.6875rem;
  font-weight: 600;
  color: #94a3b8;
  letter-spacing: 0.05em;
  margin-bottom: 0.65rem;
  margin-left: 0.25rem;
}

.appearance-toggle {
  display: flex;
  background-color: var(--toggle-bg, #f1f5f9);
  padding: 3px;
  border-radius: 0.6rem;
  gap: 3px;
}

.toggle-opt {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.35rem;
  padding: 0.45rem 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--nav-text, #64748b);
  border: none;
  background: none;
  border-radius: 0.45rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.toggle-opt.active {
  background-color: var(--card-bg, #ffffff);
  color: var(--text-heading, #0f172a);
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}
</style>
