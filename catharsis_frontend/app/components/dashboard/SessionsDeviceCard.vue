<template>
  <div class="sessions-device-card" :class="{ 'is-loading': analyticsStore.isLoading }">
    <!-- Header -->
    <div class="card-header">
      <h2 class="card-title">Sessions by device</h2>
      <button type="button" class="more-btn" aria-label="Refresh devices" @click="analyticsStore.fetchAnalytics()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
          <circle cx="5" cy="12" r="2" />
          <circle cx="12" cy="12" r="2" />
          <circle cx="19" cy="12" r="2" />
        </svg>
      </button>
    </div>

    <!-- Radial Donut Gauge -->
    <div class="gauge-container">
      <div class="gauge-ring-wrapper">
        <svg class="gauge-svg" viewBox="0 0 160 160">
          <!-- Background Track (open arc at bottom) -->
          <circle
            cx="80"
            cy="80"
            r="62"
            fill="none"
            stroke="var(--gauge-track, #f1f5f9)"
            stroke-width="12"
            stroke-linecap="round"
            stroke-dasharray="320"
            stroke-dashoffset="64"
            transform="rotate(126 80 80)"
          />

          <!-- Mobile Arc (Cyan / Bright Fern) -->
          <circle
            v-if="mobilePct > 0"
            cx="80"
            cy="80"
            r="62"
            fill="none"
            stroke="var(--malachite, #31d843)"
            stroke-width="12"
            stroke-linecap="round"
            :stroke-dasharray="320"
            :stroke-dashoffset="mobileDashOffset"
            transform="rotate(130 80 80)"
          />

          <!-- Desktop Arc (Brand Green) -->
          <circle
            v-if="desktopPct > 0"
            cx="80"
            cy="80"
            r="62"
            fill="none"
            stroke="var(--green, #22941a)"
            stroke-width="12"
            stroke-linecap="round"
            :stroke-dasharray="320"
            :stroke-dashoffset="desktopDashOffset"
            transform="rotate(195 80 80)"
          />

        </svg>

        <!-- Center Visitor Count -->
        <div class="gauge-center-content">
          <div class="user-badge-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <span class="visitor-count">{{ devicesData.formatted_total }}</span>
          <span class="visitor-label">Total visitor</span>
        </div>
      </div>
    </div>

    <!-- Device Breakdown Legend -->
    <div class="device-legend">
      <div
        v-for="item in devicesData.breakdown"
        :key="item.name"
        class="legend-row"
      >
        <div class="device-name-group">
          <!-- Laptop icon for Desktop -->
          <svg
            v-if="item.name.toLowerCase().includes('desktop')"
            class="device-icon"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="var(--green, #22941a)"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="3" y="4" width="18" height="12" rx="2"></rect>
            <line x1="2" y1="20" x2="22" y2="20"></line>
          </svg>

          <!-- Phone icon for Mobile -->
          <svg
            v-else-if="item.name.toLowerCase().includes('mobile')"
            class="device-icon"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="var(--malachite, #31d843)"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="5" y="2" width="14" height="20" rx="2"></rect>
            <line x1="12" y1="18" x2="12.01" y2="18"></line>
          </svg>

          <!-- Tablet icon for Tablet -->
          <svg
            v-else
            class="device-icon"
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="#94a3b8"
            stroke-width="2"
            stroke-linecap="round"
            stroke-linejoin="round"
          >
            <rect x="4" y="2" width="16" height="20" rx="2"></rect>
            <line x1="12" y1="18" x2="12.01" y2="18"></line>
          </svg>

          <span class="device-label">{{ item.name }}</span>
        </div>
        <span class="device-pct">{{ item.percentage }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAnalyticsStore } from '~/stores/analyticsStore'

const analyticsStore = useAnalyticsStore()

const devicesData = computed(() => analyticsStore.devices)

const desktopPct = computed(() => {
  const d = devicesData.value.breakdown.find(b => b.name.toLowerCase().includes('desktop'))
  return d ? d.percentage : 0
})

const mobilePct = computed(() => {
  const m = devicesData.value.breakdown.find(b => b.name.toLowerCase().includes('mobile'))
  return m ? m.percentage : 0
})


// Gauge arc calculation: total arc length ~256 out of 320 perimeter
const desktopDashOffset = computed(() => {
  const arcLength = (desktopPct.value / 100) * 256
  return Math.round(320 - arcLength)
})

const mobileDashOffset = computed(() => {
  const arcLength = (mobilePct.value / 100) * 256
  return Math.round(320 - arcLength)
})
</script>

<style scoped>
.sessions-device-card {
  background-color: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 1.25rem;
  padding: 1.5rem 1.5rem 1.25rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  transition: opacity 0.2s ease;
}

.sessions-device-card.is-loading {
  opacity: 0.7;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.card-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--text-heading, #0f172a);
  letter-spacing: -0.01em;
  margin: 0;
}

.more-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 0.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.15s ease;
}

.more-btn:hover {
  color: var(--text-heading, #0f172a);
}

/* Gauge container */
.gauge-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.75rem 0 0.5rem;
}

.gauge-ring-wrapper {
  position: relative;
  width: 140px;
  height: 140px;
}

.gauge-svg {
  width: 100%;
  height: 100%;
}

.gauge-center-content {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 4px;
}

.user-badge-icon {
  width: 26px;
  height: 26px;
  border-radius: 9999px;
  background-color: var(--icon-bg, #eff6ff);
  color: var(--green, #22941a);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 2px;
}

.visitor-count {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-heading, #0f172a);
  letter-spacing: -0.02em;
  line-height: 1.15;
}

.visitor-label {
  font-size: 0.625rem;
  color: var(--text-muted, #94a3b8);
  font-weight: 500;
}

/* Device Legend */
.device-legend {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-color, #f1f5f9);
}

.legend-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 0.78125rem;
}

.device-name-group {
  display: flex;
  align-items: center;
  gap: 0.55rem;
}

.device-icon {
  flex-shrink: 0;
}

.device-label {
  color: var(--text-heading, #334155);
  font-weight: 500;
}

.device-pct {
  color: var(--text-heading, #0f172a);
  font-weight: 600;
}
</style>
