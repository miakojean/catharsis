<template>
  <div class="heatmap-card">
    <!-- Header -->
    <div class="card-header">
      <h2 class="card-title">User by time of day</h2>
      <button type="button" class="more-btn" aria-label="More options">
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
              v-for="(val, hIdx) in heatmapData[dIdx]"
              :key="hIdx"
              class="heatmap-cell"
              :class="getCellClass(val)"
              :title="`${day} - ${hours[hIdx]}: ${val} users`"
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
          <span>50</span>
          <span>200</span>
          <span>400</span>
          <span>600</span>
          <span>800</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
const hours = ['12 am', '2 am', '4 am', '6 am', '8 am', '10 am', '12 am', '12 am', '2 pm', '4 pm', '6 pm']

// Heatmap data matrix matching the screenshot visual distribution (higher around 10am-2pm)
const heatmapData = [
  // Sun: moderate mid-day
  [0, 0, 0, 0, 100, 250, 450, 350, 300, 200, 100],
  // Mon: higher weekday
  [0, 0, 0, 80, 280, 580, 820, 620, 420, 260, 120],
  // Tue: peak weekday
  [0, 0, 0, 120, 380, 750, 880, 720, 520, 340, 150],
  // Wed: strong mid-week
  [0, 0, 90, 180, 420, 800, 890, 740, 560, 360, 180],
  // Thu: high peak
  [0, 0, 80, 220, 480, 850, 890, 780, 580, 380, 200],
  // Fri: active afternoon
  [0, 0, 60, 160, 390, 700, 790, 680, 490, 310, 160],
  // Sat: weekend pattern
  [0, 0, 0, 0, 120, 320, 500, 420, 280, 160, 80]
]

function getCellClass(val: number) {
  if (val >= 750) return 'heat-level-5'
  if (val >= 500) return 'heat-level-4'
  if (val >= 300) return 'heat-level-3'
  if (val >= 150) return 'heat-level-2'
  if (val > 0) return 'heat-level-1'
  return 'heat-empty'
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

/* Heat levels */
.heat-empty {
  background-color: transparent;
}

.heat-level-1 {
  background-color: #eff6ff;
}

.heat-level-2 {
  background-color: #bfdbfe;
}

.heat-level-3 {
  background-color: #60a5fa;
}

.heat-level-4 {
  background-color: #2563eb;
}

.heat-level-5 {
  background-color: #1e40af;
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
    #bfdbfe 0%,
    #60a5fa 35%,
    #2563eb 65%,
    #1e40af 100%
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
