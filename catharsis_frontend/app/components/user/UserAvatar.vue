<template>
  <div
    class="user-avatar-root"
    :class="[
      `avatar-${size}`,
      `avatar-${variant}`,
      { 'is-interactive': interactive }
    ]"
    :title="tooltipText"
    role="img"
    :aria-label="tooltipText"
  >
    <span class="avatar-initials">{{ displayInitials }}</span>
    <span
      v-if="showStatus"
      class="avatar-status-dot"
      :class="`status-${status}`"
      aria-hidden="true"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAuthStore, computeUserInitials } from '~/stores/authStore'

interface Props {
  initials?: string
  email?: string
  name?: string
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'gradient' | 'forest' | 'subtle'
  showStatus?: boolean
  status?: 'online' | 'offline' | 'busy'
  interactive?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  initials: '',
  email: '',
  name: '',
  size: 'md',
  variant: 'gradient',
  showStatus: false,
  status: 'online',
  interactive: false
})

const authStore = useAuthStore()

const displayInitials = computed(() => {
  if (props.initials && props.initials.trim()) {
    return props.initials.trim().slice(0, 2).toUpperCase()
  }
  if (props.email || props.name) {
    return computeUserInitials({
      email: props.email,
      username: props.name
    })
  }
  return authStore.initials || '??'
})

const tooltipText = computed(() => {
  const currentEmail = props.email || authStore.user?.email
  const currentName = props.name || authStore.user?.username
  if (currentName && currentEmail) return `${currentName} (${currentEmail})`
  if (currentEmail) return currentEmail
  if (currentName) return currentName
  return 'Utilisateur connecté'
})
</script>

<style scoped>
.user-avatar-root {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  user-select: none;
  font-family: 'Inter Tight', -apple-system, sans-serif;
  font-weight: 700;
  text-transform: uppercase;
  color: #ffffff;
  flex-shrink: 0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease;
}

.user-avatar-root.is-interactive:hover {
  transform: translateY(-1px) scale(1.02);
  box-shadow: 0 4px 12px rgba(41, 63, 20, 0.25);
}

/* Color Variants based on main.css design system */
.avatar-gradient {
  background: linear-gradient(135deg, var(--black-forest, #293f14) 0%, var(--green, #22941a) 100%);
  border: 1.5px solid rgba(255, 255, 255, 0.3);
}

.avatar-forest {
  background: var(--black-forest, #293f14);
  border: 1.5px solid rgba(255, 255, 255, 0.2);
}

.avatar-subtle {
  background: #f0fdf4;
  color: var(--black-forest, #293f14);
  border: 1.5px solid #bbf7d0;
}

/* Sizes */
.avatar-xs {
  width: 24px;
  height: 24px;
  font-size: 0.625rem;
  letter-spacing: -0.01em;
}

.avatar-sm {
  width: 32px;
  height: 32px;
  font-size: 0.75rem;
  letter-spacing: -0.01em;
}

.avatar-md {
  width: 40px;
  height: 40px;
  font-size: 0.875rem;
  letter-spacing: 0.02em;
}

.avatar-lg {
  width: 48px;
  height: 48px;
  font-size: 1.0625rem;
  letter-spacing: 0.02em;
}

.avatar-xl {
  width: 60px;
  height: 60px;
  font-size: 1.35rem;
  letter-spacing: 0.03em;
}

.avatar-initials {
  line-height: 1;
  display: inline-block;
}

/* Status indicator badge */
.avatar-status-dot {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 28%;
  height: 28%;
  min-width: 8px;
  min-height: 8px;
  border-radius: 9999px;
  border: 2px solid #ffffff;
  box-sizing: content-box;
}

.status-online {
  background-color: var(--malachite, #31d843);
  box-shadow: 0 0 0 1px rgba(34, 148, 26, 0.2);
}

.status-busy {
  background-color: #ef4444;
}

.status-offline {
  background-color: #94a3b8;
}
</style>
