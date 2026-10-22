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
                <div class="my-circle-chart" :style="{ background: dynamicGradient }">
                    <div class="inner">
                        <!-- Affichage du nombre total de la carte -->
                        <div id="number">{{ total }}</div>
                        <span class="sub-label">Visiteurs</span>
                    </div>
                </div>
            </div>
            
            <!-- Légende générée depuis les données API à droite -->
            <div class="right-side">
                <p v-if="!rows || rows.length === 0" class="empty-note">
                    Aucune donnée
                </p>
                <ul v-else class="legend-list">
                    <li v-for="(row, index) in rows" :key="row.label" :title="row.label">
                        <span class="legend-color" :style="{ backgroundColor: colors[index % colors.length] }"></span>
                        <span class="legend-label">{{ row.label }}</span>
                        <span class="legend-value">({{ row.percent.toFixed(1) }}%)</span>
                    </li>
                </ul>
            </div>
        </div>

        <div class="stat-cards-footer">
            <NuxtLink :to="to" class="footer-link" aria-label="En savoir plus">
                En savoir plus
                <span class="arrow">&rarr;</span>
            </NuxtLink>
        </div>
    </article>
</template>

<script setup lang="ts">
import { computed } from 'vue'

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
    to: '/dashboard/users'
})

// Palette de couleurs pour le graphique et la légende
const colors = ['#2563eb', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe']

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
        gradientStr.push(`#f1f5f9 ${currentPercent}% 100%`)
    }

    return `conic-gradient(${gradientStr.join(', ')})`
})
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

.my-circle-chart {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 140px;
    width: 140px;
    border-radius: 50%;
    /* L'ombre a été adoucie pour coller au design moderne */
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.inner {
    height: 105px;
    width: 105px;
    background-color: #ffffff;
    border-radius: 50%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    box-shadow: inset 0 2px 4px 0 rgba(0, 0, 0, 0.06);
}

#number {
    font-weight: 700;
    font-size: 1.25rem;
    color: #0f172a;
    line-height: 1;
}

.sub-label {
    font-size: 0.7rem;
    color: #64748b;
    margin-top: 0.2rem;
}

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
    width: 10px;
    height: 10px;
    border-radius: 50%;
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

.stat-cards-footer {
    display: flex;
    justify-content: flex-end;
}

.footer-link {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
    font-weight: 600;
    color: #2563eb;
    text-decoration: none;
    transition: color 0.2s;
}

.footer-link:hover {
    color: #1d4ed8;
}

.arrow {
    font-size: 1.1rem;
}
</style>