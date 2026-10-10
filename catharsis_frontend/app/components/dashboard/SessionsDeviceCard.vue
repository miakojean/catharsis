<template>
  <div class="sessions-device-card">
    <!-- Header -->
    <div class="card-header">
      <h2 class="card-title">Sessions by device</h2>
      <button type="button" class="more-btn" aria-label="More options">
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

          <!-- Mobile Arc (Cyan / Light Blue ~19.7%) -->
          <circle
            cx="80"
            cy="80"
            r="62"
            fill="none"
            stroke="#38bdf8"
            stroke-width="12"
            stroke-linecap="round"
            stroke-dasharray="320"
            stroke-dashoffset="240"
            transform="rotate(130 80 80)"
          />

          <!-- Desktop Arc (Cobalt Blue ~78.5%) -->
          <circle
            cx="80"
            cy="80"
            r="62"
            fill="none"
            stroke="#2563eb"
            stroke-width="12"
            stroke-linecap="round"
            stroke-dasharray="320"
            stroke-dashoffset="110"
            transform="rotate(195 80 80)"
          />
        </svg>

        <!-- Center Visitor Count -->
        <div class="gauge-center-content">
          <div class="user-badge-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
              <circle cx="12" cy="7" r="4"></circle>
            </svg>
          </div>
          <span class="visitor-count">10,739</span>
          <span class="visitor-label">Total visitor</span>
        </div>
      </div>
    </div>

    <!-- Device Breakdown Legend -->
    <div class="device-legend">
      <!-- Desktop -->
      <div class="legend-row">
        <div class="device-name-group">
          <!-- Laptop icon -->
          <svg class="device-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="12" rx="2"></rect>
            <line x1="2" y1="20" x2="22" y2="20"></line>
          </svg>
          <span class="device-label">Desktop</span>
        </div>
        <span class="device-pct">78.5%</span>
      </div>

      <!-- Mobile -->
      <div class="legend-row">
        <div class="device-name-group">
          <!-- Phone icon -->
          <svg class="device-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="5" y="2" width="14" height="20" rx="2"></rect>
            <line x1="12" y1="18" x2="12.01" y2="18"></line>
          </svg>
          <span class="device-label">Mobile</span>
        </div>
        <span class="device-pct">19.7%</span>
      </div>

      <!-- Tablet -->
      <div class="legend-row">
        <div class="device-name-group">
          <!-- Tablet icon -->
          <svg class="device-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="4" y="2" width="16" height="20" rx="2"></rect>
            <line x1="12" y1="18" x2="12.01" y2="18"></line>
          </svg>
          <span class="device-label">Tablet</span>
        </div>
        <span class="device-pct">1.8%</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Sessions by device circular gauge and device breakdown legend
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
