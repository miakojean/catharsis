<template>
  <div class="heatmap-card" :class="{ 'is-loading': analyticsStore.isLoading }">
    <!-- Header -->
    <div class="card-header">
      <h2 class="card-title">User by time of day</h2>
      <button type="button" class="more-btn" aria-label="More options" @click="analyticsStore.fetchAnalytics()">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
          <circle cx="5" cy="12" r="2" />
          <circle cx="12" cy="12" r="2" />
          <circle cx="19" cy="12" r="2" />
        </svg>
      </button>
    </div>

    <!-- Heatmap Grid -->
    <div class="heatmap-body">
      <div class="heatmap-grid-table">
        <!-- Day rows -->
        <div v-for="(day, dIdx) in days" :key="day" class="heatmap-row">
          <span class="day-label">{{ day }}</span>
          
          <div class="cells-row">
            <div
              v-for="(val, hIdx) in (heatmapMatrix[dIdx] || [])"
              :key="hIdx"
              class="heatmap-cell"
              :class="getCellClass(val)"
              :title="`${day} - ${hours[hIdx] || ''}: ${val} users`"
            ></div>
          </div>
        </div>
      </div>

      <!-- Hours labels -->
      <div class="hours-row">
        <span class="spacer"></span>
        <div class="hours-labels">
          <span v-for="hour in hours" :key="hour" class="hour-label">{{ hour }}</span>
        </div>
      </div>

      <!-- Color Intensity Scale Bar -->
      <div class="scale-section">
        <div class="scale-bar"></div>
        <div class="scale-ticks">
          <span>0</span>
          <span>{{ Math.round(maxVal * 0.25) }}</span>
          <span>{{ Math.round(maxVal * 0.5) }}</span>
          <span>{{ Math.round(maxVal * 0.75) }}</span>
          <span>{{ maxVal }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useAnalyticsStore } from '~/stores/analyticsStore'

const analyticsStore = useAnalyticsStore()

const days = computed(() => analyticsStore.heatmap.days || ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])
const hours = computed(() => analyticsStore.heatmap.hours || ['12 am', '2 am', '4 am', '6 am', '8 am', '10 am', '12 am', '12 am', '2 pm', '4 pm', '6 pm'])
const heatmapMatrix = computed(() => analyticsStore.heatmap.matrix || [])

const maxVal = computed(() => {
  let highest = 0
  for (const row of heatmapMatrix.value) {
    for (const v of row) {
      if (v > highest) highest = v
    }
  }
  return highest
})

function getCellClass(val: number) {
  if (val <= 0 || maxVal.value <= 0) return 'heat-empty'
  const ratio = val / maxVal.value
  if (ratio >= 0.8) return 'heat-level-5'
  if (ratio >= 0.55) return 'heat-level-4'
  if (ratio >= 0.35) return 'heat-level-3'
  if (ratio >= 0.15) return 'heat-level-2'
  return 'heat-level-1'
}

</script>

<style scoped>
.heatmap-card {
  background-color: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e2e8f0);
  border-radius: 1.25rem;
  padding: 1.5rem 1.5rem 1.25rem;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
  transition: opacity 0.2s ease;
}

.heatmap-card.is-loading {
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

.heatmap-body {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.heatmap-grid-table {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.heatmap-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.day-label {
  font-size: 0.6875rem;
  color: var(--text-muted, #94a3b8);
  width: 26px;
  text-align: right;
  flex-shrink: 0;
}

.cells-row {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(11, 1fr);
  gap: 0.35rem;
}

.heatmap-cell {
  height: 20px;
  border-radius: 4px;
  transition: transform 0.15s ease, filter 0.15s ease;
  cursor: pointer;
}

.heatmap-cell:hover {
  transform: scale(1.15);
  z-index: 5;
}

/* Heat levels matching brand green and cobalt blue */
.heat-empty {
  background-color: var(--icon-bg, #f8fafc);
}

.heat-level-1 {
  background-color: #dcfce7;
}

.heat-level-2 {
  background-color: #86efac;
}

.heat-level-3 {
  background-color: var(--malachite, #31d843);
}

.heat-level-4 {
  background-color: var(--green, #22941a);
}

.heat-level-5 {
  background-color: var(--black-forest, #293f14);
}

/* Hours row */
.hours-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0.25rem;
}

.spacer {
  width: 26px;
  flex-shrink: 0;
}

.hours-labels {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(11, 1fr);
  gap: 0.35rem;
}

.hour-label {
  font-size: 0.5625rem;
  color: var(--text-muted, #94a3b8);
  text-align: center;
  white-space: nowrap;
}

/* Scale section */
.scale-section {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  margin-top: 1rem;
  padding-left: 2rem;
}

.scale-bar {
  width: 100%;
  height: 6px;
  border-radius: 9999px;
  background: linear-gradient(
    to right,
    #dcfce7 0%,
    #86efac 25%,
    var(--malachite, #31d843) 50%,
    var(--green, #22941a) 75%,
    var(--black-forest, #293f14) 100%
  );
}

.scale-ticks {
  display: flex;
  justify-content: space-between;
  font-size: 0.625rem;
  color: var(--text-muted, #94a3b8);
  font-weight: 500;
}
</style>
