<template>
    <article class="stat-cards" :class="{ 'is-loading': isLoading }">
        
        <div class="stat-cards-header">
            <h3>{{ title }}</h3>
            <!-- Affiche un message personnalisé ou une description par défaut -->
            <p>{{ description || 'Répartition des visiteurs' }}</p>
        </div>

        <div class="stat-cards-body">
            <!-- Graphique à gauche -->
            <div class="left-side">
                <div class="chart-stage">
                    <div class="my-circle-chart" :style="{ background: dynamicGradient }">
                        <div class="inner">
                            <!-- Affichage du nombre total de la carte -->
                            <div id="number">{{ total }}</div>
                            <span class="sub-label">Visiteurs</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Légende générée depuis les données API à droite -->
            <div class="right-side w-full">
                <p v-if="!rows || rows.length === 0" class="empty-note">
                    Aucune donnée
                </p>
                <ul v-else class="legend-list w-full">
                    <li v-for="(row, index) in rows" :key="row.label" :title="row.label">
                        <span class="legend-color" :style="{ background: legendDot(index) }"></span>
                        <span class="legend-label">{{ row.label }}</span>
                        <span class="legend-value">({{ row.percent.toFixed(1) }}%)</span>
                    </li>
                </ul>
            </div>
        </div>

        <div class="stat-cards-footer">
            <button type="button" class="stat-cards-button flex gap-2" @click="$emit('goTo', to)">
                <span>Voir plus</span>
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="size-6">
                    <path fill-rule="evenodd" d="M12 2.25c-5.385 0-9.75 4.365-9.75 9.75s4.365 9.75 9.75 9.75 9.75-4.365 9.75-9.75S17.385 2.25 12 2.25Zm4.28 10.28a.75.75 0 0 0 0-1.06l-3-3a.75.75 0 1 0-1.06 1.06l1.72 1.72H8.25a.75.75 0 0 0 0 1.5h5.69l-1.72 1.72a.75.75 0 1 0 1.06 1.06l3-3Z" clip-rule="evenodd" />
                </svg>
            </button>
        </div>
    </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router';

interface RowData {
    label: string
    visitors: number
    percent: number
}

const props = withDefaults(defineProps<{
    title?: string
    description?: string
    total?: number
    rows?: RowData[]
    isLoading?: boolean
    to?: string | object
}>(), {
    title: 'Statistiques',
    description: '',
    total: 0,
    rows: () => [],
    isLoading: false,
    to: '/dashboard/myusers'
})

const emits = defineEmits(['goTo'])


// Palette plus saturée : chaque segment reste bien distinct (plus de bleus délavés)
const colors = ['#1d4ed8', '#06b6d4', '#8b5cf6', '#f59e0b', '#ec4899']

// Calcul dynamique du dégradé conique (graphique en anneau)
const dynamicGradient = computed(() => {
    if (!props.rows || props.rows.length === 0) {
        return 'conic-gradient(#e2e8f0 0% 100%)' // Gris par défaut si vide
    }

    let gradientStr: string[] = []
    let currentPercent = 0

    props.rows.forEach((row, index) => {
        const color = colors[index % colors.length]
        const nextPercent = currentPercent + row.percent
        gradientStr.push(`${color} ${currentPercent}% ${nextPercent}%`)
        currentPercent = nextPercent
    })

    // S'il reste un écart (ex: si on limite à 5 résultats et qu'il reste 15% pour "Autres")
    if (currentPercent < 100) {
        gradientStr.push(`#e2e8f0 ${currentPercent}% 100%`)
    }

    return `conic-gradient(${gradientStr.join(', ')})`
})

// Pastille de légende en "bille" : même effet de volume que le graphique
function legendDot(index: number) {
    const c = colors[index % colors.length]
    return `radial-gradient(circle at 30% 28%, color-mix(in srgb, ${c} 45%, white), ${c} 70%)`
}
</script>

<style scoped>
.stat-cards {
    /* Largeur ajustée pour s'adapter à la grille Tailwind/CSS de ta page */
    width: 100%;
    min-height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 1.5rem;
    background: #ffffff;
    border-radius: 1rem;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04), 0 8px 24px -12px rgba(15, 23, 42, 0.12);
    font-family: 'Inter', sans-serif;
    transition: opacity 0.2s;
}

.stat-cards.is-loading {
    opacity: 0.6;
}

.stat-cards-header h3 {
    font-size: 1.1rem;
    color: #0f172a;
    margin: 0 0 0.25rem 0;
}

.stat-cards-header p {
    font-size: 0.85rem;
    color: #64748b;
    margin: 0;
}

.stat-cards-body {
    display: flex;
    align-items: center;
    justify-content: space-around;
    gap: 1.5rem;
    flex: 1;
    margin-top: 1rem;
    margin-bottom: 1rem;
}

/* ---------- Graphique 3D léger ---------- */

.left-side {
    position: relative;
    flex-shrink: 0;
}

/* Perspective + ombre portée au sol */
.chart-stage {
    position: relative;
    perspective: 700px;
    padding-bottom: 14px;
}

.chart-stage::after {
    content: '';
    position: absolute;
    left: 50%;
    bottom: 0;
    width: 110px;
    height: 14px;
    transform: translateX(-50%);
    background: radial-gradient(ellipse at center, rgba(15, 23, 42, 0.28), transparent 70%);
    filter: blur(3px);
    transition: width 0.4s ease, opacity 0.4s ease;
}

.my-circle-chart {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 140px;
    width: 140px;
    border-radius: 50%;
    transform-style: preserve-3d;
    transform: rotateX(0deg) rotateY(0deg);
    transition: transform 0.5s cubic-bezier(0.2, 0.8, 0.2, 1), box-shadow 0.5s ease;
    box-shadow:
        0 14px 22px -8px rgba(29, 78, 216, 0.45),   /* lueur colorée dessous */
        0 4px 8px rgba(15, 23, 42, 0.18),            /* ombre de contact */
        inset 0 2px 3px rgba(255, 255, 255, 0.65),   /* arête éclairée en haut */
        inset 0 -5px 9px rgba(0, 0, 0, 0.28);        /* arête dans l'ombre en bas */
}

/* Reflet de lumière + assombrissement progressif : donne du volume à l'anneau */
.my-circle-chart::after {
    content: '';
    position: absolute;
    inset: 0;
    border-radius: 50%;
    pointer-events: none;
    background:
        radial-gradient(circle at 28% 20%, rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0) 42%),
        linear-gradient(160deg, rgba(255, 255, 255, 0) 45%, rgba(0, 0, 0, 0.22) 100%);
}

/* Le graphique s'incline légèrement au survol de la carte */
.stat-cards:hover .my-circle-chart {
    transform: rotateX(14deg) rotateY(-10deg);
    box-shadow:
        10px 18px 24px -8px rgba(29, 78, 216, 0.5),
        0 4px 8px rgba(15, 23, 42, 0.2),
        inset 0 2px 3px rgba(255, 255, 255, 0.65),
        inset 0 -5px 9px rgba(0, 0, 0, 0.28);
}

.stat-cards:hover .chart-stage::after {
    width: 90px;
    opacity: 0.8;
}

/* Centre en creux : le trou semble taillé dans l'anneau */
.inner {
    position: relative;
    z-index: 1;
    height: 105px;
    width: 105px;
    background: radial-gradient(circle at 50% 28%, #ffffff 0%, #f1f5f9 100%);
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    transform: translateZ(8px);
    box-shadow:
        inset 0 6px 10px -2px rgba(15, 23, 42, 0.22),
        inset 0 -2px 4px rgba(255, 255, 255, 0.9),
        0 1px 1px rgba(255, 255, 255, 0.7);
}

#number {
    font-weight: 700;
    font-size: 1.25rem;
    color: #0f172a;
    line-height: 1;
    text-shadow: 0 1px 0 #ffffff;
}

.sub-label {
    font-size: 0.7rem;
    color: #64748b;
    margin-top: 0.2rem;
}

/* ---------- Légende ---------- */

.right-side {
    flex: 1;
    min-width: 0; /* Évite les débordements */
}

.empty-note {
    color: #94a3b8;
    font-size: 0.875rem;
    text-align: center;
}

.legend-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.65rem;
}

.legend-list li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #475569;
}

.legend-color {
    flex-shrink: 0;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.35), inset 0 -1px 2px rgba(0, 0, 0, 0.2);
}

.legend-label {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    font-weight: 500;
    color: #1e293b;
    max-width: 120px;
}

.legend-value {
    color: #64748b;
    font-size: 0.75rem;
    margin-left: auto; /* Pousse la valeur à droite */
}

/* ---------- Pied de carte ---------- */

.stat-cards-footer{
    width: 100%;
    display: flex;
    justify-content: flex-end;
    
}

button{
    color: #333;
    cursor: pointer;
}

.stat-cards-footer svg{
    color: var(--bright-fern);
}

.stat-cards-button{
    transition: ease-in 0.3s;
}

.stat-cards-button:hover{
    transform: translateY(-5px);
}

/* Respect des préférences d'accessibilité : pas d'inclinaison animée */
@media (prefers-reduced-motion: reduce) {
    .my-circle-chart,
    .chart-stage::after {
        transition: none;
    }

    .stat-cards:hover .my-circle-chart {
        transform: none;
    }
}

@media(min-width:768px){
    
    .stat-cards-body {
        display: flex;
        align-items: center;
        justify-content: space-around;
        gap: 1.5rem;
        flex: 1;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
}

@media(min-width:1280px){
    
    .stat-cards-body {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: space-around;
        gap: 1.5rem;
        flex: 1;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
}
</style>