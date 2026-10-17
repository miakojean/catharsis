<template>
  <div class="active-users-card" :class="{ 'is-loading': analyticsStore.isLoading }">
    <!-- Header -->
    <div class="card-header">
      <h2 class="card-title">Active Users</h2>
      <button type="button" class="more-btn" aria-label="Refresh chart" @click="analyticsStore.fetchAnalytics()">
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
        <span>{{ formatK(yTicks[5]) }}</span>
        <span>{{ formatK(yTicks[4]) }}</span>
        <span>{{ formatK(yTicks[3]) }}</span>
        <span>{{ formatK(yTicks[2]) }}</span>
        <span>{{ formatK(yTicks[1]) }}</span>
        <span>0</span>
      </div>

      <!-- Graph Area -->
      <div class="graph-plot-area">
        <svg class="plot-svg" viewBox="0 0 550 180" preserveAspectRatio="none">
          <defs>
            <linearGradient id="activeUsersGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#22941a" stop-opacity="0.25" />
              <stop offset="70%" stop-color="#22941a" stop-opacity="0.05" />
              <stop offset="100%" stop-color="#22941a" stop-opacity="0.0" />
            </linearGradient>

            <linearGradient id="tooltipColumnGlow" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stop-color="#22941a" stop-opacity="0.18" />
              <stop offset="100%" stop-color="#22941a" stop-opacity="0.01" />
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
          <rect
            v-if="peakPoint.val > 0"
            :x="peakPoint.x - 15"
            y="25"
            width="30"
            height="145"
            fill="url(#tooltipColumnGlow)"
            rx="4"
          />
          <line
            v-if="peakPoint.val > 0"
            :x1="peakPoint.x"
            y1="25"
            :x2="peakPoint.x"
            y2="170"
            stroke="#bbf7d0"
            stroke-dasharray="3 3"
            stroke-width="1.2"
          />

          <!-- Area fill -->
          <path :d="areaPath" fill="url(#activeUsersGradient)" />

          <!-- Main curve line -->
          <path
            :d="linePath"
            fill="none"
            stroke="var(--green, #22941a)"
            stroke-width="2.5"
            stroke-linecap="round"
            stroke-linejoin="round"
          />

          <!-- Apex peak data dot -->
          <circle
            v-if="peakPoint.val > 0"
            :cx="peakPoint.x"
            :cy="peakPoint.y"
            r="5"
            fill="var(--black-forest, #293f14)"
            stroke="#ffffff"
            stroke-width="2"
          />
        </svg>

        <!-- Floating Tooltip Card -->
        <div
          v-if="peakPoint.val > 0"
          class="apex-tooltip"
          :style="{ left: `${(peakPoint.x / 550) * 100}%`, top: `${Math.max(4, peakPoint.y - 32)}px` }"
        >
          <span class="tooltip-date">{{ timeline.peak_label }}</span>
          <span class="tooltip-val">
            <strong>{{ formattedPeakVal }}</strong> active users
          </span>
        </div>


        <!-- X-Axis Labels -->
        <div class="x-axis">
          <span v-for="lbl in timeline.labels" :key="lbl">{{ lbl }}</span>
        </div>
      </div>
    </div>

    <!-- Footer Controls (Day/Month/Year) -->
    <div class="card-footer">
      <div class="filter-segmented-pill">
        <button
          type="button"
          class="filter-opt"
          :class="{ 'active': analyticsStore.selectedPeriod === 'day' }"
          @click="analyticsStore.setPeriod('day')"
        >
          Day
        </button>
        <button
          type="button"
          class="filter-opt"
          :class="{ 'active': analyticsStore.selectedPeriod === 'month' }"
          @click="analyticsStore.setPeriod('month')"
        >
          Month
        </button>
        <button
          type="button"
          class="filter-opt"
          :class="{ 'active': analyticsStore.selectedPeriod === 'year' }"
          @click="analyticsStore.setPeriod('year')"
        >
          Year
        </button>
      </div>

      <button type="button" class="view-report-btn" @click="analyticsStore.fetchAnalytics()">
        <span>Rafraîchir</span>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <polyline points="9 18 15 12 9 6"></polyline>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAnalyticsStore } from '~/stores/analyticsStore'

const analyticsStore = useAnalyticsStore()

const timeline = computed(() => analyticsStore.activeUsers)

const dataPoints = computed(() => timeline.value.data || [0])

const maxVal = computed(() => {
  const m = Math.max(...dataPoints.value, 1)
  return Math.ceil(m / 1000) * 1000 || 25000
})

const yTicks = computed(() => {
  const step = maxVal.value / 5
  return [0, step, step * 2, step * 3, step * 4, maxVal.value]
})

function formatK(num: number): string {
  if (num >= 1000000) return `${(num / 1000000).toFixed(1)}M`
  if (num >= 1000) return `${Math.round(num / 1000)}K`
  return `${Math.round(num)}`
}

const points = computed(() => {
  const data = dataPoints.value
  const len = data.length
  if (len === 0) return []

  const width = 550
  const startX = 25
  const endX = 525
  const usableW = endX - startX
  const topY = 30
  const bottomY = 168
  const usableH = bottomY - topY

  return data.map((val, idx) => {
    const x = len === 1 ? width / 2 : startX + (idx / (len - 1)) * usableW
    const ratio = Math.min(1, Math.max(0, val / maxVal.value))
    const y = bottomY - ratio * usableH
    return { x: Math.round(x), y: Math.round(y), val }
  })
})

const peakPoint = computed(() => {
  if (points.value.length === 0) return { x: 275, y: 50, val: 0 }
  let maxIdx = 0
  for (let i = 1; i < points.value.length; i++) {
    if (points.value[i].val > points.value[maxIdx].val) {
      maxIdx = i
    }
  }
  return points.value[maxIdx]
})

const formattedPeakVal = computed(() => {
  const val = timeline.value.peak_value || peakPoint.value.val || 0
  return val.toLocaleString('fr-FR').replace(/[\s\u202F\u00A0]/g, ' ')
})


const linePath = computed(() => {
  const pts = points.value
  if (pts.length === 0) return ''
  return pts.reduce((acc, pt, i) => {
    return i === 0 ? `M ${pt.x} ${pt.y}` : `${acc} L ${pt.x} ${pt.y}`
  }, '')
})

const areaPath = computed(() => {
  const pts = points.value
  if (pts.length === 0) return ''
  const first = pts[0]
  const last = pts[pts.length - 1]
  const line = linePath.value
  return `${line} L ${last.x} 170 L ${first.x} 170 Z`
})
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
  transition: opacity 0.2s ease;
}

.active-users-card.is-loading {
  opacity: 0.7;
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
  white-space: nowrap;
}

.tooltip-date {
  font-size: 0.5625rem;
  color: var(--text-muted, #94a3b8);
  font-weight: 500;
}

.tooltip-val {
  font-size: 0.6875rem;
  color: var(--black-forest, #293f14);
  font-weight: 500;
}

.tooltip-val strong {
  font-weight: 700;
  color: var(--green, #22941a);
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
  color: var(--black-forest, #293f14);
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
