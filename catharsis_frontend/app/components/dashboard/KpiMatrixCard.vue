<template>
  <div class="kpi-matrix-card">
    <!-- Quadrant 1: Users -->
    <div class="kpi-quadrant">
      <div class="quadrant-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      </div>
      <span class="quadrant-label">Users</span>
      <span class="quadrant-value">284</span>
      <div class="quadrant-trend">
        <svg class="trend-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="7" y1="17" x2="17" y2="7"></line>
          <polyline points="7 7 17 7 17 17"></polyline>
        </svg>
        <span class="trend-pct">1,02%</span>
        <span class="trend-period">from last week</span>
      </div>
    </div>

    <!-- Quadrant 2: Revenue -->
    <div class="kpi-quadrant">
      <div class="quadrant-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="4" width="20" height="16" rx="3"></rect>
          <path d="M6 10h12"></path>
          <circle cx="16" cy="14" r="1.5" fill="#2563eb"></circle>
        </svg>
      </div>
      <span class="quadrant-label">Revenue</span>
      <span class="quadrant-value">$3194,24</span>
      <div class="quadrant-trend">
        <svg class="trend-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="7" y1="17" x2="17" y2="7"></line>
          <polyline points="7 7 17 7 17 17"></polyline>
        </svg>
        <span class="trend-pct">2,75%</span>
        <span class="trend-period">from last week</span>
      </div>
    </div>

    <!-- Quadrant 3: Conv Rate -->
    <div class="kpi-quadrant">
      <div class="quadrant-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <line x1="18" y1="20" x2="18" y2="10"></line>
          <line x1="12" y1="20" x2="12" y2="4"></line>
          <line x1="6" y1="20" x2="6" y2="14"></line>
        </svg>
      </div>
      <span class="quadrant-label">Conv Rate</span>
      <span class="quadrant-value">2.85%</span>
      <div class="quadrant-trend">
        <svg class="trend-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="7" y1="17" x2="17" y2="7"></line>
          <polyline points="7 7 17 7 17 17"></polyline>
        </svg>
        <span class="trend-pct">3,44%</span>
        <span class="trend-period">from last week</span>
      </div>
    </div>

    <!-- Quadrant 4: Session -->
    <div class="kpi-quadrant">
      <div class="quadrant-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#2563eb" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="7" r="4"></circle>
          <path d="M5.5 21a6.5 6.5 0 0 1 13 0"></path>
        </svg>
      </div>
      <span class="quadrant-label">Session</span>
      <span class="quadrant-value">5.638</span>
      <div class="quadrant-trend">
        <svg class="trend-arrow" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="7" y1="17" x2="17" y2="7"></line>
          <polyline points="7 7 17 7 17 17"></polyline>
        </svg>
        <span class="trend-pct">1,89%</span>
        <span class="trend-period">from last week</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// 4-Quadrant KPI Card matching the top-left widget of the dashboard
</script>

<style scoped>
.kpi-matrix-card {
  background-color: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 1.25rem;
  padding: 1.75rem 1.5rem;
  display: grid;
  grid-template-columns: 1fr 1fr;
  position: relative;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

/* Quadrant layout */
.kpi-quadrant {
  display: flex;
  flex-direction: column;
  padding: 0.75rem 1rem;
}

/* Divider lines */
.kpi-quadrant:nth-child(1) {
  border-right: 1px solid var(--border-color, #f1f5f9);
  border-bottom: 1px solid var(--border-color, #f1f5f9);
  padding-bottom: 1.5rem;
}

.kpi-quadrant:nth-child(2) {
  border-bottom: 1px solid var(--border-color, #f1f5f9);
  padding-bottom: 1.5rem;
  padding-left: 1.5rem;
}

.kpi-quadrant:nth-child(3) {
  border-right: 1px solid var(--border-color, #f1f5f9);
  padding-top: 1.5rem;
}

.kpi-quadrant:nth-child(4) {
  padding-top: 1.5rem;
  padding-left: 1.5rem;
}

.quadrant-icon {
  width: 36px;
  height: 36px;
  border-radius: 9999px;
  background-color: var(--icon-bg, #eff6ff);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.75rem;
}

.quadrant-label {
  font-size: 0.8125rem;
  color: var(--text-muted, #64748b);
  font-weight: 500;
  margin-bottom: 0.25rem;
}

.quadrant-value {
  font-size: 1.625rem;
  font-weight: 700;
  color: var(--text-heading, #0f172a);
  letter-spacing: -0.02em;
  margin-bottom: 0.4rem;
  line-height: 1.2;
}

.quadrant-trend {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.75rem;
  color: #10b981;
  font-weight: 600;
}

.trend-arrow {
  flex-shrink: 0;
}

.trend-pct {
  color: #10b981;
}

.trend-period {
  color: var(--text-muted, #94a3b8);
  font-weight: 400;
  font-size: 0.6875rem;
}
</style>
