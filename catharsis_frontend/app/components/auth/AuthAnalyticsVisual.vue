<template>
  <div class="market-share-container">
    <div class="content-centering-wrapper">
      
      <!-- The Main Market Share Card -->
      <div class="market-share-card">
        
        <!-- Card Header -->
        <div class="card-header">
          <span class="card-title">Market Share</span>
          <button type="button" class="more-options-btn" aria-label="More options">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <circle cx="5" cy="12" r="2" />
              <circle cx="12" cy="12" r="2" />
              <circle cx="19" cy="12" r="2" />
            </svg>
          </button>
        </div>

        <!-- Center Donut Chart Container -->
        <div class="donut-chart-wrapper">
          <svg class="donut-svg" viewBox="0 0 300 300">
            <!-- 6 Donut Slices (with 2.5px gap border) -->
            
            <!-- QuickSync (26%) - White -->
            <path
              d="M 150.00,88.00 L 150.00,35.00 A 115,115 0 0,1 264.77,157.22 L 211.88,153.89 A 62,62 0 0,0 150.00,88.00 Z"
              fill="#ffffff"
              stroke="#0b0b0d"
              stroke-width="2.5"
              class="donut-slice slice-quicksync"
            />
            <text x="214.5" y="93.4" fill="#000000" font-size="11" font-weight="600" text-anchor="middle">26%</text>

            <!-- TaskFlow (22%) - Light Silver Gray -->
            <path
              d="M 211.88,153.89 L 264.77,157.22 A 115,115 0 0,1 164.41,264.09 L 157.77,211.51 A 62,62 0 0,0 211.88,153.89 Z"
              fill="#8e8e93"
              stroke="#0b0b0d"
              stroke-width="2.5"
              class="donut-slice slice-taskflow"
            />
            <text x="214.5" y="214.6" fill="#ffffff" font-size="11" font-weight="600" text-anchor="middle">22%</text>

            <!-- CloudNest (12%) - Medium Gray -->
            <path
              d="M 157.77,211.51 L 164.41,264.09 A 115,115 0 0,1 82.40,243.04 L 113.56,200.16 A 62,62 0 0,0 157.77,211.51 Z"
              fill="#5e5e63"
              stroke="#0b0b0d"
              stroke-width="2.5"
              class="donut-slice slice-cloudnest"
            />
            <text x="128.0" y="239.7" fill="#ffffff" font-size="11" font-weight="600" text-anchor="middle">12%</text>

            <!-- DataPulse (22%) - Dark Medium Gray -->
            <path
              d="M 113.56,200.16 L 82.40,243.04 A 115,115 0 0,1 45.94,101.04 L 93.90,123.60 A 62,62 0 0,0 113.56,200.16 Z"
              fill="#424246"
              stroke="#0b0b0d"
              stroke-width="2.5"
              class="donut-slice slice-datapulse"
            />
            <text x="64.3" y="176.0" fill="#ffffff" font-size="11" font-weight="600" text-anchor="middle">22%</text>

            <!-- InsightHub (7%) - Dark Gray -->
            <path
              d="M 93.90,123.60 L 45.94,101.04 A 115,115 0 0,1 76.70,61.39 L 110.48,102.23 A 62,62 0 0,0 93.90,123.60 Z"
              fill="#2e2e32"
              stroke="#0b0b0d"
              stroke-width="2.5"
              class="donut-slice slice-insighthub"
            />
            <text x="80.1" y="99.8" fill="#ffffff" font-size="11" font-weight="600" text-anchor="middle">7%</text>

            <!-- StreamlinePro (11%) - Charcoal -->
            <path
              d="M 110.48,102.23 L 76.70,61.39 A 115,115 0 0,1 150.00,35.00 L 150.00,88.00 A 62,62 0 0,0 110.48,102.23 Z"
              fill="#1e1e22"
              stroke="#0b0b0d"
              stroke-width="2.5"
              class="donut-slice slice-streamline"
            />
            <text x="120.0" y="70.7" fill="#ffffff" font-size="11" font-weight="600" text-anchor="middle">11%</text>

            <!-- Center Cutout Hole (Black) -->
            <circle cx="150" cy="150" r="61" fill="#000000" />
            
            <!-- Center Text -->
            <text x="150" y="146" fill="#ffffff" font-size="20" font-weight="700" letter-spacing="-0.5px" text-anchor="middle" font-family="'Inter Tight', monospace, sans-serif">$100B</text>
            <text x="150" y="165" fill="#888888" font-size="9.5" font-weight="400" letter-spacing="-0.1px" text-anchor="middle">Globe Ecosystem</text>
          </svg>
        </div>

        <!-- Legend 2-Column Grid -->
        <div class="legend-grid">
          
          <!-- Column 1 (Left) -->
          <div class="legend-col">
            <!-- QuickSync (White) -->
            <div class="legend-item">
              <span class="swatch swatch-white"></span>
              <span class="item-name">QuickSync</span>
              <span class="item-stats">$26B</span>
              <span class="item-pct">(26%)</span>
            </div>

            <!-- DataPulse (Dark Medium Gray) -->
            <div class="legend-item">
              <span class="swatch swatch-datapulse"></span>
              <span class="item-name">DataPulse</span>
              <span class="item-stats">$22</span>
              <span class="item-pct">(22%)</span>
            </div>

            <!-- CloudNest (Medium Gray) -->
            <div class="legend-item">
              <span class="swatch swatch-cloudnest"></span>
              <span class="item-name">CloudNest</span>
              <span class="item-stats">$12B</span>
              <span class="item-pct">(12%)</span>
            </div>
          </div>

          <!-- Column 2 (Right) -->
          <div class="legend-col">
            <!-- TaskFlow (Light Silver Gray) -->
            <div class="legend-item">
              <span class="swatch swatch-taskflow"></span>
              <span class="item-name">TaskFlow</span>
              <span class="item-stats">$22B</span>
              <span class="item-pct">(22%)</span>
            </div>

            <!-- InsightHub (Dark Gray) -->
            <div class="legend-item">
              <span class="swatch swatch-insighthub"></span>
              <span class="item-name">InsightHub</span>
              <span class="item-stats">$7B</span>
              <span class="item-pct">(7%)</span>
            </div>

            <!-- StreamlinePro (Charcoal) -->
            <div class="legend-item">
              <span class="swatch swatch-streamline"></span>
              <span class="item-name">StreamlinePro</span>
              <span class="item-stats">$11B</span>
              <span class="item-pct">(11%)</span>
            </div>
          </div>

        </div>

      </div>

      <!-- Bottom Design System Attribution -->
      <footer class="system-attribution">
        <div class="attr-icon-box">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none">
            <rect x="2" y="5" width="20" height="14" rx="4" stroke="currentColor" stroke-width="2" />
            <line x1="8" y1="12" x2="16" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round" />
          </svg>
        </div>
        <div class="attr-text-box">
          <span class="attr-title">Interfaces Design System</span>
          <span class="attr-url">https://interfaces.supply</span>
        </div>
      </footer>

    </div>
  </div>
</template>

<script setup lang="ts">
// Market Share Donut Chart component matching the reference design exactly
</script>

<style scoped>
/* Main visual container: Deep dark carbon canvas */
.market-share-container {
  width: 100%;
  height: 100%;
  min-height: 100vh;
  background-color: #0f0f11;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1.5rem;
  box-sizing: border-box;
  user-select: none;
  font-family: 'Inter Tight', 'Inter', -apple-system, sans-serif;
}

.content-centering-wrapper {
  width: 100%;
  max-width: 410px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* The Market Share Card */
.market-share-card {
  width: 100%;
  background-color: #000000;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 1.25rem;
  padding: 1.35rem 1.4rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.15rem;
  box-shadow: 
    0 25px 50px -12px rgba(0, 0, 0, 0.8),
    0 0 0 1px rgba(255, 255, 255, 0.03);
}

/* Card Header */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.card-title {
  font-size: 0.9375rem;
  font-weight: 500;
  color: #ffffff;
  letter-spacing: -0.01em;
}

.more-options-btn {
  background: none;
  border: none;
  color: #52525b;
  cursor: pointer;
  padding: 0.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color 0.15s ease;
}

.more-options-btn:hover {
  color: #a1a1aa;
}

/* Donut Chart SVG Wrapper */
.donut-chart-wrapper {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.donut-svg {
  width: 100%;
  max-width: 270px;
  height: auto;
  display: block;
}

.donut-slice {
  transition: opacity 0.2s ease, transform 0.2s ease;
  cursor: pointer;
}

.donut-slice:hover {
  opacity: 0.9;
}

/* Legend 2-Column Grid */
.legend-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem 0.5rem;
  padding: 0.5rem 0.25rem 0;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

.legend-col {
  display: flex;
  flex-direction: column;
  gap: 0.65rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.6875rem;
  white-space: nowrap;
}

.swatch {
  width: 10px;
  height: 10px;
  border-radius: 2.5px;
  flex-shrink: 0;
}

.swatch-white {
  background-color: #ffffff;
}

.swatch-taskflow {
  background-color: #8e8e93;
}

.swatch-cloudnest {
  background-color: #5e5e63;
}

.swatch-datapulse {
  background-color: #424246;
}

.swatch-insighthub {
  background-color: #2e2e32;
}

.swatch-streamline {
  background-color: #1e1e22;
}

.item-name {
  color: #f4f4f5;
  font-weight: 500;
  letter-spacing: -0.01em;
}

.item-stats {
  color: #71717a;
  margin-left: auto;
}

.item-pct {
  color: #71717a;
}

/* Attribution Footer below Card */
.system-attribution {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  padding: 0 0.5rem;
  color: #71717a;
}

.attr-icon-box {
  display: flex;
  align-items: center;
  color: #a1a1aa;
}

.attr-text-box {
  display: flex;
  flex-direction: column;
  line-height: 1.25;
}

.attr-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: #f4f4f5;
  letter-spacing: -0.01em;
}

.attr-url {
  font-size: 0.6875rem;
  color: #71717a;
}
</style>
