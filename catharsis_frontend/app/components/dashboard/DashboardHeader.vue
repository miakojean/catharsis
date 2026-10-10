<template>
  <header class="dashboard-header">
    <div class="header-titles">
      <h1 class="header-title">Dashboard</h1>
      <p v-if="authStore.user?.email" class="header-subtitle">Bienvenue, {{ authStore.user.email }}</p>
    </div>

    <div class="header-actions">
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

      <!-- User Avatar -->
      <div class="user-avatar-btn">
        <img
          src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=face"
          alt="User Profile"
          class="user-avatar-img"
          :title="authStore.user?.email"
        />
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/stores/authStore'
const authStore = useAuthStore()
// Top Dashboard Header with Search, Notifications and Avatar
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

/* User avatar */
.user-avatar-btn {
  width: 38px;
  height: 38px;
  border-radius: 9999px;
  overflow: hidden;
  cursor: pointer;
  border: 1.5px solid var(--border-color, #e2e8f0);
  transition: transform 0.15s ease;
}

.user-avatar-btn:hover {
  transform: scale(1.05);
}

.user-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@media (max-width: 640px) {
  .search-input {
    width: 180px;
  }
}
</style>
