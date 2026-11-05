<template>
  <aside
    class="dashboard-sidebar"
    :class="{
      'is-collapsed': isCollapsed,
      'is-dark': currentIsDark
    }"
  >
    <!-- Brand Logo & Collapse Toggle -->
    <div class="sidebar-brand">
      <NuxtLink
        to="/dashboard"
        class="brand-link"
        :title="isCollapsed ? 'Catharsis Analytics' : undefined"
      >
        <CatharsisLogo
          :variant="isCollapsed ? 'mark' : 'full'"
          :size="isCollapsed ? 'sm' : 'md'"
          :show-subtitle="!isCollapsed"
        />
      </NuxtLink>

      <button
        type="button"
        class="collapse-toggle-btn"
        :title="isCollapsed ? 'Déplier la barre latérale' : 'Réduire la barre latérale'"
        :aria-label="isCollapsed ? 'Déplier la barre latérale' : 'Réduire la barre latérale'"
        @click="toggleSidebarCollapse"
      >
        <svg
          class="collapse-icon"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
          <line x1="9" y1="3" x2="9" y2="21"></line>
          <polyline v-if="!isCollapsed" points="15 9 12 12 15 15"></polyline>
          <polyline v-else points="12 9 15 12 12 15"></polyline>
        </svg>
      </button>
    </div>

    <!-- Main Navigation List (Scrollable Area) -->
    <nav class="sidebar-nav" aria-label="Menu principal">
      <ul class="nav-list">
        <!-- Dashboard -->
        <li class="nav-item">
          <NuxtLink
            to="/dashboard"
            class="nav-link"
            :class="{ 'active': route.path === '/dashboard' }"
            :title="isCollapsed ? 'Dashboard' : undefined"
          >
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
            <span class="nav-label">Dashboard</span>
          </NuxtLink>
        </li>

        <!-- Mes utilisateurs (Expandable) -->
        <li class="nav-item">
          <button
            type="button"
            class="nav-link nav-btn"
            :class="{ 'active': route.path.startsWith('/dashboard/myusers') }"
            aria-controls="users-submenu"
            :aria-expanded="activeMenu === 'users'"
            :title="isCollapsed ? 'Mes utilisateurs' : undefined"
            @click="handleUsersClick"
          >
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="3" width="7" height="7"></rect>
              <rect x="14" y="3" width="7" height="7"></rect>
              <rect x="14" y="14" width="7" height="7"></rect>
              <rect x="3" y="14" width="7" height="7"></rect>
            </svg>
            <span class="nav-label">Mes utilisateurs</span>
            <span
              class="chevron-wrapper"
              :title="activeMenu === 'users' ? 'Replier' : 'Déplier'"
              @click.stop.prevent="toggleSubmenu('users')"
            >
              <svg
                class="chevron-icon"
                :class="{ 'rotated': activeMenu === 'users' }"
                width="14"
                height="14"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>
          </button>

          <!-- Submenu -->
          <Transition name="submenu-slide">
            <ul v-if="activeMenu === 'users' && !isCollapsed" id="users-submenu" class="nav-submenu">
              <li v-for="item in userRoutes" :key="item.path">
                <NuxtLink
                  :to="item.path"
                  class="nav-sublink"
                  :class="{ active: route.path === item.path }"
                  :aria-current="route.path === item.path ? 'page' : undefined"
                >
                  {{ item.label }}
                </NuxtLink>
              </li>
            </ul>
          </Transition>
        </li>

        <!-- Evènements (Realtime) -->
        <li class="nav-item">
          <button
            type="button"
            class="nav-link nav-btn"
            :title="isCollapsed ? 'Evènements' : undefined"
            @click="toggleSubmenu('realtime')"
          >
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            <span class="nav-label">Evènements</span>
            <span class="chevron-wrapper" @click.stop.prevent="toggleSubmenu('realtime')">
              <svg class="chevron-icon" :class="{ 'rotated': activeMenu === 'realtime' }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>
          </button>
        </li>

        <!-- Audience with Badge -->
        <li class="nav-item">
          <a
            href="#"
            class="nav-link"
            :title="isCollapsed ? 'Audience (10)' : undefined"
            @click.prevent
          >
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
          <button
            type="button"
            class="nav-link nav-btn"
            :title="isCollapsed ? 'Behavior' : undefined"
            @click="toggleSubmenu('behavior')"
          >
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="12"></line>
              <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span class="nav-label">Behavior</span>
            <span class="chevron-wrapper" @click.stop.prevent="toggleSubmenu('behavior')">
              <svg class="chevron-icon" :class="{ 'rotated': activeMenu === 'behavior' }" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="6 9 12 15 18 9"></polyline>
              </svg>
            </span>
          </button>
        </li>

        <!-- Conversion -->
        <li class="nav-item">
          <NuxtLink
            to="/dashboard/conversions"
            class="nav-link"
            :class="{ active: route.path.startsWith('/dashboard/conversions') }"
            :title="isCollapsed ? 'Conversion' : undefined"
          >
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="18" y1="20" x2="18" y2="10"></line>
              <line x1="12" y1="20" x2="12" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
            <span class="nav-label">Conversion</span>
          </NuxtLink>
        </li>
      </ul>

      <!-- Section "OTHERS" -->
      <div class="nav-section-title">OTHERS</div>
      <ul class="nav-list">
        <li class="nav-item">
          <a
            href="#"
            class="nav-link"
            :title="isCollapsed ? 'Settings' : undefined"
            @click.prevent
          >
            <svg class="nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <span class="nav-label">Settings</span>
          </a>
        </li>

        <li class="nav-item">
          <a
            href="#"
            class="nav-link"
            :title="isCollapsed ? 'Help Center' : undefined"
            @click.prevent
          >
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
          :class="{ 'active': !currentIsDark }"
          :title="isCollapsed ? 'Mode clair' : undefined"
          @click="handleThemeToggle(false)"
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
          <span class="toggle-text">Light</span>
        </button>

        <button
          type="button"
          class="toggle-opt"
          :class="{ 'active': currentIsDark }"
          :title="isCollapsed ? 'Mode sombre' : undefined"
          @click="handleThemeToggle(true)"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
          </svg>
          <span class="toggle-text">Dark</span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import CatharsisLogo from '~/components/brand/CatharsisLogo.vue'
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useThemeStore } from '~/stores/themeStore'

const props = defineProps<{
  isDark?: boolean
}>()

const emit = defineEmits<{
  (e: 'theme-change', isDark: boolean): void
}>()

const themeStore = useThemeStore()

const currentIsDark = computed(() => {
  return props.isDark !== undefined ? props.isDark : themeStore.isDark
})

function handleThemeToggle(dark: boolean) {
  themeStore.setTheme(dark)
  emit('theme-change', dark)
}

const route = useRoute()
const router = useRouter()

const isCollapsed = ref(false)
const activeMenu = ref(route.path.startsWith('/dashboard/myusers') ? 'users' : '')

const userRoutes = [
  { label: 'Pays d’origine', path: '/dashboard/myusers/countries' },
  { label: 'Sources d’acquisition', path: '/dashboard/myusers/sources' },
  { label: 'Appareils', path: '/dashboard/myusers/devices' },
  { label: 'Navigateurs', path: '/dashboard/myusers/browsers' },
  { label: 'Systèmes d’exploitation', path: '/dashboard/myusers/operating-systems' },
  { label: 'Pages visitées', path: '/dashboard/myusers/pages' },
]

function toggleSidebarCollapse() {
  isCollapsed.value = !isCollapsed.value
  try {
    localStorage.setItem('catharsis_sidebar_collapsed', String(isCollapsed.value))
  } catch {}
}

function handleUsersClick() {
  if (isCollapsed.value) {
    isCollapsed.value = false
    activeMenu.value = 'users'
  } else if (activeMenu.value !== 'users') {
    activeMenu.value = 'users'
  }
  if (!route.path.startsWith('/dashboard/myusers')) {
    router.push('/dashboard/myusers')
  }
}

function toggleSubmenu(menu: string) {
  if (isCollapsed.value) {
    isCollapsed.value = false
  }
  activeMenu.value = activeMenu.value === menu ? '' : menu
}

// Adaptation responsive au montage et au redimensionnement
function checkResponsiveLayout() {
  if (typeof window === 'undefined') return
  const savedState = localStorage.getItem('catharsis_sidebar_collapsed')
  if (savedState !== null) {
    isCollapsed.value = savedState === 'true'
  } else if (window.innerWidth <= 1080) {
    // Sur écrans d'ordinateurs plus étroits (ou fenêtres fenêtrées côte à côte)
    isCollapsed.value = true
  }
}

onMounted(() => {
  checkResponsiveLayout()
  window.addEventListener('resize', onWindowResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onWindowResize)
})

let resizeTimeout: any = null
function onWindowResize() {
  clearTimeout(resizeTimeout)
  resizeTimeout = setTimeout(() => {
    // Si l'utilisateur n'a pas explicitement fixé un choix, on adapte automatiquement
    if (localStorage.getItem('catharsis_sidebar_collapsed') === null) {
      if (window.innerWidth <= 1080 && !isCollapsed.value) {
        isCollapsed.value = true
      } else if (window.innerWidth > 1080 && isCollapsed.value) {
        isCollapsed.value = false
      }
    }
  }, 150)
}

watch(() => route.path, (path) => {
  if (path.startsWith('/dashboard/myusers')) {
    activeMenu.value = 'users'
  }
})
</script>

<style scoped>
.dashboard-sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  max-height: 100vh;
  width: 250px;
  min-width: 250px;
  background-color: var(--sidebar-bg, #ffffff);
  border-right: 1px solid var(--border-color, #e2e8f0);
  display: flex;
  flex-direction: column;
  padding: 1.25rem 1rem;
  box-sizing: border-box;
  user-select: none;
  z-index: 40;
  overflow: hidden;
  transition: width 0.25s cubic-bezier(0.4, 0, 0.2, 1),
              min-width 0.25s cubic-bezier(0.4, 0, 0.2, 1),
              padding 0.25s ease;
}

/* Mode replié (collapsed) */
.dashboard-sidebar.is-collapsed {
  width: 72px;
  min-width: 72px;
  padding: 1.25rem 0.5rem;
}

/* Thème sombre spécifique à la sidebar */
.dashboard-sidebar.is-dark {
  --sidebar-bg: #0f172a;
  --border-color: #1e293b;
  --text-heading: #f8fafc;
  --text-muted: #94a3b8;
  --input-bg: #1e293b;
  --card-bg: #111827;
  --icon-bg: #1e293b;
  --toggle-bg: #1e293b;
  --nav-text: #94a3b8;
  --nav-hover-bg: #1e293b;
  --nav-active-bg: #1e3a8a;
  background-color: var(--sidebar-bg);
  border-right-color: var(--border-color);
  color: var(--text-heading);
}

/* Brand Header */
.sidebar-brand {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 1.75rem;
  flex-shrink: 0;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  text-decoration: none;
  min-width: 0;
  overflow: hidden;
}

/* Bouton de collapse / expand */
.collapse-toggle-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 0.45rem;
  border: 1px solid var(--border-color, #e2e8f0);
  background: var(--card-bg, #ffffff);
  color: var(--nav-text, #64748b);
  cursor: pointer;
  flex-shrink: 0;
  transition: all 0.15s ease;
  padding: 0;
}

.collapse-toggle-btn:hover {
  background-color: var(--nav-hover-bg, #f8fafc);
  color: var(--text-heading, #0f172a);
  border-color: #cbd5e1;
}

.is-collapsed .sidebar-brand {
  flex-direction: column;
  justify-content: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.is-collapsed .collapse-toggle-btn {
  width: 24px;
  height: 24px;
}

/* Navigation principale avec SCROLL */
.sidebar-nav {
  flex: 1 1 auto;
  min-height: 0; /* CRUCIAL pour activer le scroll flexbox */
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  padding-right: 0.25rem;
  margin-right: -0.25rem;
  overscroll-behavior: contain;
  scrollbar-width: thin;
  scrollbar-color: var(--border-color, #cbd5e1) transparent;
}

/* Scrollbar personnalisée discrète */
.sidebar-nav::-webkit-scrollbar {
  width: 5px;
}

.sidebar-nav::-webkit-scrollbar-track {
  background: transparent;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background-color: var(--border-color, #cbd5e1);
  border-radius: 9999px;
  transition: background-color 0.2s ease;
}

.sidebar-nav::-webkit-scrollbar-thumb:hover {
  background-color: var(--nav-text, #94a3b8);
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
  box-sizing: border-box;
}

.nav-btn {
  justify-content: flex-start;
}

.nav-link:hover {
  background-color: var(--nav-hover-bg, #f8fafc);
  color: var(--text-heading, #0f172a);
}

.nav-link.active {
  background-color: var(--bright-fern, #38a700);
  color: #ffffff;
  font-weight: 600;
}

.nav-icon {
  flex-shrink: 0;
}

.nav-label {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.nav-badge {
  background-color: #f97316;
  color: #ffffff;
  font-size: 0.6875rem;
  font-weight: 700;
  padding: 0.1rem 0.45rem;
  border-radius: 9999px;
  line-height: 1.2;
  flex-shrink: 0;
}

.chevron-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.2rem;
  border-radius: 0.25rem;
  transition: background-color 0.15s ease;
  flex-shrink: 0;
}

.chevron-wrapper:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.chevron-icon {
  transition: transform 0.2s ease;
  color: #94a3b8;
}

.nav-link.active .chevron-icon {
  color: #ffffff;
}

.chevron-icon.rotated {
  transform: rotate(180deg);
}

/* Submenu */
.nav-submenu {
  list-style: none;
  margin: 0.25rem 0 0.35rem 1.4rem;
  padding: 0 0 0 0.65rem;
  border-left: 2px solid var(--border-color, #e2e8f0);
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.nav-sublink {
  display: block;
  padding: 0.45rem 0.65rem;
  border-radius: 0.45rem;
  color: var(--nav-text, #64748b);
  font-size: 0.8125rem;
  line-height: 1.3;
  text-decoration: none;
  transition: all 0.15s ease;
  word-break: break-word;
}

.nav-sublink:hover {
  background-color: var(--nav-hover-bg, #f8fafc);
  color: var(--text-heading, #0f172a);
}

.nav-sublink.active {
  background-color: var(--bright-fern, #38a700);
  color: #ffffff;
  font-weight: 600;
}

/* Animation d'ouverture du sous-menu */
.submenu-slide-enter-active,
.submenu-slide-leave-active {
  transition: all 0.2s ease;
  max-height: 300px;
  overflow: hidden;
}

.submenu-slide-enter-from,
.submenu-slide-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-4px);
}

.nav-section-title {
  font-size: 0.6875rem;
  font-weight: 600;
  color: #94a3b8;
  letter-spacing: 0.05em;
  margin: 1.5rem 0 0.5rem 0.5rem;
  flex-shrink: 0;
}

/* Appearance Switcher */
.sidebar-appearance {
  flex-shrink: 0;
  margin-top: auto;
  padding-top: 1rem;
  border-top: 1px solid var(--border-color, #f1f5f9);
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
  white-space: nowrap;
}

.toggle-opt.active {
  background-color: var(--card-bg, #ffffff);
  color: var(--text-heading, #0f172a);
  font-weight: 600;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

/* Styles spécifiques au mode replié (.is-collapsed) */
.is-collapsed .nav-label,
.is-collapsed .chevron-wrapper,
.is-collapsed .nav-badge,
.is-collapsed .nav-section-title,
.is-collapsed .appearance-title,
.is-collapsed .toggle-text,
.is-collapsed .nav-submenu {
  display: none !important;
}

.is-collapsed .nav-link {
  justify-content: center;
  padding: 0.65rem 0;
}

.is-collapsed .appearance-toggle {
  flex-direction: column;
  padding: 4px;
}

.is-collapsed .toggle-opt {
  padding: 0.5rem 0;
  justify-content: center;
}

/* RESPONSIVE : Hauteur écran réduite (ex: ordinateurs portables 1366x768, zoom 125%) */
@media (max-height: 800px) {
  .dashboard-sidebar {
    padding: 0.85rem 0.75rem;
  }

  .sidebar-brand {
    margin-bottom: 1rem;
  }

  .nav-list {
    gap: 0.2rem;
  }

  .nav-link {
    padding: 0.5rem 0.65rem;
  }

  .nav-section-title {
    margin: 1rem 0 0.35rem 0.5rem;
  }

  .sidebar-appearance {
    padding-top: 0.5rem;
  }

  .appearance-title {
    margin-bottom: 0.35rem;
  }

  .nav-sublink {
    padding: 0.35rem 0.5rem;
  }
}

/* RESPONSIVE : Mobile & tablettes portrait (< 768px) */
@media (max-width: 768px) {
  .dashboard-sidebar {
    position: static;
    width: 100%;
    min-width: 100%;
    height: auto;
    max-height: none;
    border-right: none;
    border-bottom: 1px solid var(--border-color, #e2e8f0);
    padding: 1rem;
  }

  .dashboard-sidebar.is-collapsed {
    width: 100%;
    min-width: 100%;
    padding: 1rem;
  }

  .collapse-toggle-btn {
    display: none;
  }

  .is-collapsed .nav-label,
  .is-collapsed .chevron-wrapper,
  .is-collapsed .nav-badge,
  .is-collapsed .nav-section-title,
  .is-collapsed .appearance-title,
  .is-collapsed .toggle-text {
    display: inline-block !important;
  }

  .is-collapsed .nav-link {
    justify-content: flex-start;
    padding: 0.65rem 0.85rem;
  }

  .is-collapsed .appearance-toggle {
    flex-direction: row;
  }

  .sidebar-nav {
    max-height: 400px;
  }
}
</style>
