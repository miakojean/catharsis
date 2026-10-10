<template>
  <div class="active-users-card">
    <!-- Header -->
    <div class="card-header">
      <h2 class="card-title">Active Users</h2>
      <button type="button" class="more-btn" aria-label="More options">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
          <circle cx="5" cy="12" r="2" />
          <circle cx="12" cy="12" r="2" />
          <circle cx="19" cy="12" r="2" />
        </svg>
      </button>
    </div>

    <!-- Chart Viewport -->
    <div class="chart-viewport">
      <!-- Y-Axis Ticks -->
      <div class="y-axis">
        <span>25K</span>
        <span>20K</span>
        <span>15K</span>
        <span>10K</span>
        <span>5K</span>
        <span>0</span>
      </div>

      <!-- Graph Area -->
      <div class="graph-plot-area">
        <svg class="plot-svg" viewBox="0 0 550 180" preserveAspectRatio="none">
          <defs>
            <linearGradient id="activeUsersGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#2563eb" stop-opacity="0.22" />
              <stop offset="70%" stop-color="#2563eb" stop-opacity="0.04" />
              <stop offset="100%" stop-color="#2563eb" stop-opacity="0.0" />
            </linearGradient>

            <!-- Column glow under tooltip -->
            <linearGradient id="tooltipColumnGlow" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#2563eb" stop-opacity="0.18" />
              <stop offset="100%" stop-color="#2563eb" stop-opacity="0.01" />
            </linearGradient>
          </defs>

          <!-- Horizontal Grid Lines -->
          <line x1="0" y1="10" x2="550" y2="10" stroke="var(--grid-color, #f1f5f9)" stroke-width="1" />
          <line x1="0" y1="42" x2="550" y2="42" stroke="var(--grid-color, #f1f5f9)" stroke-width="1" />
          <line x1="0" y1="74" x2="550" y2="74" stroke="var(--grid-color, #f1f5f9)" stroke-width="1" />
          <line x1="0" y1="106" x2="550" y2="106" stroke="var(--grid-color, #f1f5f9)" stroke-width="1" />
          <line x1="0" y1="138" x2="550" y2="138" stroke="var(--grid-color, #f1f5f9)" stroke-width="1" />
          <line x1="0" y1="170" x2="550" y2="170" stroke="var(--grid-color, #f1f5f9)" stroke-width="1" />

          <!-- Tooltip vertical highlight bar -->
          <rect x="340" y="38" width="30" height="132" fill="url(#tooltipColumnGlow)" rx="4" />
          <line x1="355" y1="38" x2="355" y2="170" stroke="#bfdbfe" stroke-dasharray="3 3" stroke-width="1.2" />

          <!-- Area fill -->
          <path
            d="M 20 120 
               L 80 90 
               L 135 90 
               L 170 125 
               L 205 105 
               L 260 105 
               L 315 85 
               L 355 38 
               L 395 85 
               L 440 120 
               L 485 120 
               L 520 145 
               L 520 170 
               L 20 170 Z"
            fill="url(#activeUsersGradient)"
          />

          <!-- Main blue curve line -->
          <path
            d="M 20 120 
               L 80 90 
               L 135 90 
               L 170 125 
               L 205 105 
               L 260 105 
               L 315 85 
               L 355 38 
               L 395 85 
               L 440 120 
               L 485 120 
               L 520 145"
            fill="none"
            stroke="#2563eb"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />

          <!-- Apex data dot on May 18 -->
          <circle cx="355" cy="38" r="4.5" fill="#2563eb" stroke="#ffffff" stroke-width="2" />
        </svg>

        <!-- Floating Tooltip Card (May 18, 2022 / 18,584 active users) -->
        <div class="apex-tooltip" style="left: 64.5%; top: 8px;">
          <span class="tooltip-date">May 18, 2022</span>
          <span class="tooltip-val"><strong>18,584</strong> active users</span>
        </div>

        <!-- X-Axis Labels -->
        <div class="x-axis">
          <span>Jan 2022</span>
          <span>Feb 2022</span>
          <span>Mar 2022</span>
          <span>Apr 2022</span>
          <span>May 2022</span>
          <span>Jun 2022</span>
          <span>Jul 2022</span>
          <span>Aug 2022</span>
        </div>
      </div>
    </div>

    <!-- Footer Controls (Day/Month/Year + View report button) -->
    <div class="card-footer">
      <!-- Time segment filters -->
      <div class="filter-segmented-pill">
        <button
          type="button"
          class="filter-opt"
          :class="{ 'active': activePeriod === 'day' }"
          @click="activePeriod = 'day'"
        >
          Day
        </button>
        <button
          type="button"
          class="filter-opt"
          :class="{ 'active': activePeriod === 'month' }"
          @click="activePeriod = 'month'"
        >
          Month
        </button>
        <button
          type="button"
          class="filter-opt"
          :class="{ 'active': activePeriod === 'year' }"
          @click="activePeriod = 'year'"
        >
          Year
        </button>
      </div>

      <!-- Action button -->
      <button type="button" class="view-report-btn">
        <span>View report</span>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const activePeriod = ref<'day' | 'month' | 'year'>('month')
</script>

<style scoped>
.active-users-card {
  background-color: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 1.25rem;
  padding: 1.5rem 1.5rem 1.25rem;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.25rem;
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

/* Chart Viewport */
.chart-viewport {
  display: flex;
  gap: 0.75rem;
  height: 205px;
  position: relative;
}

.y-axis {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-size: 0.625rem;
  color: var(--text-muted, #94a3b8);
  padding: 3px 0 22px 0;
  text-align: right;
  width: 26px;
  flex-shrink: 0;
}

.graph-plot-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  position: relative;
}

.plot-svg {
  width: 100%;
  height: 170px;
  overflow: visible;
}

/* Apex Tooltip */
.apex-tooltip {
  position: absolute;
  transform: translateX(-50%);
  background-color: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 0.5rem;
  padding: 0.35rem 0.65rem;
  box-shadow: 0 4px 12px -2px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 1px;
  pointer-events: none;
  z-index: 10;
}

.tooltip-date {
  font-size: 0.5625rem;
  color: var(--text-muted, #94a3b8);
  font-weight: 500;
}

.tooltip-val {
  font-size: 0.6875rem;
  color: #2563eb;
  font-weight: 500;
}

.tooltip-val strong {
  font-weight: 700;
}

/* X-Axis labels */
.x-axis {
  display: flex;
  justify-content: space-between;
  font-size: 0.625rem;
  color: var(--text-muted, #94a3b8);
  padding-top: 0.35rem;
}

/* Footer controls */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 1.25rem;
  padding-top: 0.75rem;
  border-top: 1px solid var(--border-color, #f1f5f9);
}

.filter-segmented-pill {
  display: flex;
  background-color: var(--input-bg, #f8fafc);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 0.5rem;
  padding: 2px;
  gap: 2px;
}

.filter-opt {
  background: none;
  border: none;
  padding: 0.35rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--text-muted, #64748b);
  border-radius: 0.375rem;
  cursor: pointer;
  transition: all 0.15s ease;
}

.filter-opt.active {
  background-color: var(--card-bg, #ffffff);
  color: var(--text-heading, #0f172a);
  font-weight: 600;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.view-report-btn {
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: none;
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 0.5rem;
  padding: 0.4rem 0.85rem;
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--text-heading, #0f172a);
  cursor: pointer;
  transition: all 0.15s ease;
}

.view-report-btn:hover {
  background-color: var(--nav-hover-bg, #f8fafc);
  border-color: #cbd5e1;
}
</style>
