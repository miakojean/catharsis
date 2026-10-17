<template>
  <div class="profile-wrapper" ref="wrapperRef">
    <!-- Trigger Button displaying User Avatar with dynamic initials -->
    <button
      class="profile-trigger-btn"
      type="button"
      :aria-label="triggerAriaLabel"
      :aria-expanded="isOpen"
      @click="toggleDropdown"
    >
      <UserAvatar
        size="md"
        :initials="authStore.initials"
        :email="authStore.user?.email"
        :show-status="true"
        status="online"
        :interactive="true"
      />
    </button>

    <!-- Dropdown Menu -->
    <Transition name="dropdown-pop">
      <div v-if="isOpen" class="dropdown-panel" role="menu">
        <!-- User identity header -->
        <div class="user-info-card">
          <UserAvatar
            size="lg"
            :initials="authStore.initials"
            :email="authStore.user?.email"
            :show-status="true"
            status="online"
          />
          <div class="user-text-details">
            <span class="user-name-title">{{ displayDisplayName }}</span>
            <span class="user-email-text" :title="authStore.user?.email || ''">
              {{ authStore.user?.email || 'Non connecté' }}
            </span>
            <span class="user-status-badge">
              <span class="status-pulse-dot" aria-hidden="true"></span>
              Connecté
            </span>
          </div>
        </div>

        <div class="dropdown-divider"></div>

        <!-- Navigation Links -->
        <ul class="dropdown-menu-list">
          <li>
            <NuxtLink to="/profile" class="menu-item" @click="closeDropdown">
              <svg class="menu-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                <circle cx="12" cy="7" r="4"></circle>
              </svg>
              <span>Mon profil</span>
            </NuxtLink>
          </li>
          <li>
            <NuxtLink to="/settings" class="menu-item" @click="closeDropdown">
              <svg class="menu-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
              <span>Paramètres</span>
            </NuxtLink>
          </li>
        </ul>

        <div class="dropdown-divider"></div>

        <!-- Logout Action -->
        <div class="logout-wrapper">
          <button
            type="button"
            class="logout-btn"
            :disabled="authStore.isLoading"
            @click="logout"
          >
            <svg class="logout-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
            <span>{{ authStore.isLoading ? 'Déconnexion…' : 'Déconnexion' }}</span>
          </button>
        </div>

        <div v-if="authStore.message.errorMessage" class="logout-error-alert" role="alert">
          {{ authStore.message.errorMessage }}
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '~/stores/authStore'
import UserAvatar from '~/components/user/UserAvatar.vue'

const isOpen = ref(false)
const wrapperRef = ref<HTMLElement | null>(null)
const authStore = useAuthStore()
const router = useRouter()

const triggerAriaLabel = computed(() => {
  if (authStore.user?.email) {
    return `Profil de ${authStore.user.email} (initiales ${authStore.initials})`
  }
  return 'Menu du profil utilisateur'
})

const displayDisplayName = computed(() => {
  if (authStore.user?.username && authStore.user.username.trim()) {
    return authStore.user.username
  }
  if (authStore.user?.email) {
    const namePart = authStore.user.email.split('@')[0]
    return namePart
      .replace(/[._-]+/g, ' ')
      .replace(/\b\w/g, (c) => c.toUpperCase())
  }
  return 'Compte Utilisateur'
})

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const handleClickOutside = (event: MouseEvent) => {
  if (wrapperRef.value && event.target instanceof Node && !wrapperRef.value.contains(event.target)) {
    closeDropdown()
  }
}

const handleKeyDown = (event: KeyboardEvent) => {
  if (event.key === 'Escape' && isOpen.value) {
    closeDropdown()
  }
}

const logout = async () => {
  closeDropdown()
  await authStore.logout()
  await router.replace('/auth/login')
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeyDown)

  // Fetch updated user info from backend if session token exists
  if (!authStore.user?.initials) {
    authStore.fetchCurrentUser()
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeyDown)
})
</script>

<style scoped>
.profile-wrapper {
  position: relative;
  display: inline-block;
}

.profile-trigger-btn {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  cursor: pointer;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.15s ease, filter 0.15s ease;
}

.profile-trigger-btn:focus-visible {
  outline: 3px solid rgba(34, 148, 26, 0.35);
  outline-offset: 3px;
}

.profile-trigger-btn:hover {
  filter: brightness(1.05);
}

/* Dropdown Panel */
.dropdown-panel {
  position: absolute;
  top: calc(100% + 0.65rem);
  right: 0;
  width: 260px;
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 14px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.12), 0 8px 10px -6px rgba(0, 0, 0, 0.05);
  z-index: 1000;
  padding: 0.75rem;
  box-sizing: border-box;
  transform-origin: top right;
}

/* User Identity Card */
.user-info-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem;
}

.user-text-details {
  display: flex;
  flex-direction: column;
  min-width: 0;
  flex: 1;
}

.user-name-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--text-heading, #0f172a);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-email-text {
  font-size: 0.75rem;
  color: var(--text-muted, #64748b);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 0.1rem;
}

.user-status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--green, #22941a);
  margin-top: 0.35rem;
}

.status-pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 9999px;
  background-color: var(--malachite, #31d843);
  box-shadow: 0 0 0 2px rgba(49, 216, 67, 0.2);
}

.dropdown-divider {
  height: 1px;
  background-color: var(--border-color, #f1f5f9);
  margin: 0.5rem 0;
}

/* Menu items */
.dropdown-menu-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  width: 100%;
  padding: 0.55rem 0.65rem;
  text-decoration: none;
  color: var(--nav-text, #475569);
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 500;
  transition: background-color 0.15s ease, color 0.15s ease;
  box-sizing: border-box;
}

.menu-icon {
  color: var(--text-muted, #94a3b8);
  flex-shrink: 0;
  transition: color 0.15s ease;
}

.menu-item:hover {
  background-color: var(--nav-hover-bg, #f0fdf4);
  color: var(--black-forest, #293f14);
}

.menu-item:hover .menu-icon {
  color: var(--green, #22941a);
}

/* Logout action */
.logout-wrapper {
  margin-top: 0.2rem;
}

.logout-btn {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  width: 100%;
  padding: 0.55rem 0.65rem;
  border: none;
  background: none;
  color: #ef4444;
  border-radius: 8px;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  text-align: left;
  transition: background-color 0.15s ease, color 0.15s ease;
}

.logout-icon {
  color: #ef4444;
  flex-shrink: 0;
}

.logout-btn:hover {
  background-color: #fef2f2;
  color: #dc2626;
}

.logout-btn:disabled {
  opacity: 0.6;
  cursor: wait;
}

.logout-error-alert {
  margin-top: 0.5rem;
  padding: 0.5rem;
  font-size: 0.75rem;
  color: #b91c1c;
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
}

/* Dropdown Animation */
.dropdown-pop-enter-active,
.dropdown-pop-leave-active {
  transition: opacity 0.18s cubic-bezier(0.16, 1, 0.3, 1), transform 0.18s cubic-bezier(0.16, 1, 0.3, 1);
}

.dropdown-pop-enter-from,
.dropdown-pop-leave-to {
  opacity: 0;
  transform: translateY(-6px) scale(0.97);
}
</style>