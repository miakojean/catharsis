<template>
  <div class="catharsis-brand" :class="[`variant-${variant}`, `size-${size}`]">
    <!-- Variante 1 : Icône compacte seule (Badge carré arrondi avec lettre C + 4 barres de croissance) -->
    <template v-if="variant === 'mark'">
      <svg
        class="brand-mark-svg"
        viewBox="0 0 44 44"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        aria-label="Catharsis Icon"
      >
        <!-- Fond doux du badge -->
        <rect
          x="1.5"
          y="1.5"
          width="41"
          height="41"
          rx="10"
          class="mark-bg"
        />

        <!-- Lettre C géométrique et moderne -->
        <path
          d="M 23 16 C 17.5 16 13 19.5 13 25 C 13 30.5 17.5 34 23 34 C 26.5 34 29 32.2 30 30.5"
          class="mark-letter-c"
          stroke-width="3"
          stroke-linecap="round"
        />

        <!-- Les 4 traits en histogramme de croissance ascendant (Piste 1) -->
        <g class="growth-bars">
          <!-- Barre 1 (niveau 1 - départ) -->
          <line
            x1="19"
            y1="19.5"
            x2="24"
            y2="14.5"
            class="growth-bar bar-1"
          />
          <!-- Barre 2 (niveau 2) -->
          <line
            x1="23.5"
            y1="19.5"
            x2="30.5"
            y2="12.5"
            class="growth-bar bar-2"
          />
          <!-- Barre 3 (niveau 3) -->
          <line
            x1="28"
            y1="19.5"
            x2="37"
            y2="10.5"
            class="growth-bar bar-3"
          />
          <!-- Barre 4 (sommet - croissance maximale) -->
          <line
            x1="32.5"
            y1="19.5"
            x2="43.5"
            y2="8.5"
            class="growth-bar bar-4"
          />
        </g>
      </svg>
    </template>

    <!-- Variante 2 : Logo officiel complet avec texte Catharsis et les 4 traits en histogramme ascendant -->
    <template v-else>
      <div class="brand-full-container">
        <svg
          class="brand-full-svg"
          viewBox="0 0 210 66"
          fill="none"
          xmlns="http://www.w3.org/2000/svg"
          aria-label="Catharsis - Business Analytics"
        >
          <!-- Les 4 traits de croissance ascendante (Piste 1 : Histogramme d'analytics) -->
          <g class="growth-bars">
            <!-- Barre 1 : niveau de départ (court) -->
            <line
              x1="18"
              y1="26"
              x2="28"
              y2="18.5"
              class="growth-bar bar-1"
            />
            <!-- Barre 2 : progression -->
            <line
              x1="26"
              y1="26"
              x2="39"
              y2="15"
              class="growth-bar bar-2"
            />
            <!-- Barre 3 : accélération -->
            <line
              x1="34"
              y1="26"
              x2="50"
              y2="11.5"
              class="growth-bar bar-3"
            />
            <!-- Barre 4 : sommet de croissance / conversion -->
            <line
              x1="42"
              y1="26"
              x2="61"
              y2="8"
              class="growth-bar bar-4"
            />
          </g>

          <!-- Titre principal Catharsis -->
          <text
            x="16"
            y="47"
            class="brand-title-text"
          >Catharsis</text>

          <!-- Sous-titre Business analytics -->
          <g v-if="showSubtitle" transform="translate(18, 61)">
            <text class="subtitle-business" x="0" y="0">Business</text>
            <text class="subtitle-analytics" x="56" y="0">analytics</text>
          </g>
        </svg>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: 'full' | 'mark'
    size?: 'sm' | 'md' | 'lg'
    showSubtitle?: boolean
  }>(),
  {
    variant: 'full',
    size: 'md',
    showSubtitle: true,
  }
)
</script>

<style scoped>
.catharsis-brand {
  --brand-navy: #0f172a;
  --brand-green: var(--green, #22941a);
  --brand-green-bright: var(--bright-fern, #38a700);
  --mark-bg-color: #f8fafc;
  --mark-border: #e2e8f0;
  display: inline-flex;
  align-items: center;
  user-select: none;
}

/* Tailles */
.size-sm .brand-full-svg {
  height: 38px;
  width: auto;
}
.size-sm .brand-mark-svg {
  width: 28px;
  height: 28px;
}

.size-md .brand-full-svg {
  height: 48px;
  width: auto;
}
.size-md .brand-mark-svg {
  width: 36px;
  height: 36px;
}

.size-lg .brand-full-svg {
  height: 60px;
  width: auto;
}
.size-lg .brand-mark-svg {
  width: 44px;
  height: 44px;
}

/* Badge icône */
.mark-bg {
  fill: var(--mark-bg-color);
  stroke: var(--mark-border);
  stroke-width: 1.2px;
  transition: all 0.2s ease;
}

.mark-letter-c {
  stroke: var(--brand-navy);
  fill: none;
}

/* Logo complet */
.brand-full-container {
  display: inline-flex;
  align-items: center;
}

.brand-full-svg {
  display: block;
}

.brand-title-text {
  font-family: 'Inter Tight', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 26.5px;
  font-weight: 800;
  fill: var(--brand-navy);
  letter-spacing: -0.04em;
}

.subtitle-business {
  font-family: 'Inter Tight', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 10.5px;
  font-weight: 800;
  fill: var(--brand-navy);
  letter-spacing: -0.01em;
}

.subtitle-analytics {
  font-family: 'Inter Tight', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 10.5px;
  font-weight: 700;
  fill: var(--brand-green-bright);
  letter-spacing: -0.01em;
}

/* Traits de l'histogramme de croissance (Piste 1) */
.growth-bar {
  stroke: var(--brand-green-bright);
  stroke-width: 2.6px;
  stroke-linecap: round;
  transition: transform 0.2s cubic-bezier(0.34, 1.56, 0.64, 1), stroke 0.2s ease, filter 0.2s ease;
  transform-origin: bottom center;
}

.bar-1 { opacity: 0.85; }
.bar-2 { opacity: 0.90; }
.bar-3 { opacity: 0.95; }
.bar-4 { opacity: 1.0; }

/* Micro-interaction dynamique au survol : légère impulsion de croissance */
.catharsis-brand:hover .growth-bar {
  filter: drop-shadow(0 0 2.5px rgba(56, 167, 0, 0.4));
}
.catharsis-brand:hover .bar-1 {
  transform: translateY(-0.5px) scaleY(1.04);
  transition-delay: 0.02s;
}
.catharsis-brand:hover .bar-2 {
  transform: translateY(-1px) scaleY(1.06);
  transition-delay: 0.05s;
}
.catharsis-brand:hover .bar-3 {
  transform: translateY(-1.5px) scaleY(1.08);
  transition-delay: 0.08s;
}
.catharsis-brand:hover .bar-4 {
  transform: translateY(-2px) scaleY(1.10);
  transition-delay: 0.11s;
}

/* Support thème sombre */
:global(.dark-theme) .catharsis-brand,
:global(.dark) .catharsis-brand {
  --brand-navy: #f8fafc;
  --mark-bg-color: #1e293b;
  --mark-border: #334155;
}
</style>

