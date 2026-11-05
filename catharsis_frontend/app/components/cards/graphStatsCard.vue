<template>
    <article class="stat-cards" :class="{ 'is-loading': isLoading }">

        <!-- En-tête : icône + titre à gauche, description à droite -->
        <header class="stat-cards-header">
            <div class="header-title">
                <span class="header-pin" aria-hidden="true">
                    <svg viewBox="0 0 24 24" width="20" height="20">
                        <defs>
                            <linearGradient :id="`${uid}-pin`" x1="0" y1="0" x2="1" y2="1">
                                <stop offset="0%" stop-color="#60a5fa" />
                                <stop offset="100%" stop-color="#2563eb" />
                            </linearGradient>
                        </defs>
                        <path
                            :fill="`url(#${uid}-pin)`"
                            d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7Z"
                        />
                        <circle cx="12" cy="9" r="2.6" fill="#ffffff" />
                    </svg>
                </span>
                <h3>{{ title }}</h3>
            </div>
            <p class="header-description">{{ description || 'Répartition des visiteurs' }}</p>
        </header>

        <!-- Anneau interactif -->
        <div class="chart-wrap">
            <svg class="donut" viewBox="0 0 300 300" role="img" :aria-label="`${title} : répartition`">
                <!-- Aucun segment : anneau neutre -->
                <circle
                    v-if="segments.length === 0"
                    :cx="C" :cy="C" :r="R"
                    fill="none" stroke="currentColor" class="donut-empty" :stroke-width="ARC_W"
                />

                <!-- Segments proportionnels -->
                <template v-else>
                    <g
                        v-for="seg in segments"
                        :key="seg.index"
                        class="seg"
                        :class="{ 'is-active': seg.index === activeIndex }"
                        tabindex="0"
                        role="button"
                        :aria-label="`${seg.label} : ${seg.visitors} visiteurs, ${formatPercent(seg.percent)} %`"
                        @mouseenter="hovered = seg.index"
                        @mouseleave="hovered = null"
                        @focus="hovered = seg.index"
                        @blur="hovered = null"
                    >
                        <!-- Bande pastel intérieure (visible sur TOUS les segments) -->
                        <path
                            v-if="seg.bandPath"
                            class="band"
                            :d="seg.bandPath"
                            :fill="pastelFor(seg.index)"
                            :stroke="pastelFor(seg.index)"
                            :stroke-width="BAND_STROKE"
                            stroke-linejoin="round"
                        />

                        <!-- Zone de survol élargie -->
                        <path
                            class="hit"
                            :d="seg.arcPath"
                            fill="none"
                            stroke="transparent"
                            :stroke-width="28"
                        />

                        <!-- Arc coloré extérieur -->
                        <path
                            class="arc"
                            :d="seg.arcPath"
                            fill="none"
                            :stroke="colorFor(seg.index)"
                            :stroke-width="ARC_W"
                            :stroke-linecap="segments.length > 1 ? 'round' : 'butt'"
                        />
                    </g>
                </template>
            </svg>

            <!-- Texte central (affiche par défaut le segment le plus grand) -->
            <div class="center-info">
                <template v-if="activeRow">
                    <span class="center-label" :title="activeRow.label">{{ activeRow.label }}</span>
                    <span class="center-value">
                        <i class="center-dot" :style="{ background: colorFor(activeIndex) }"></i>
                        {{ (activeRow.visitors || 0).toLocaleString('fr-FR') }}
                        <span class="center-percent">[{{ formatPercent(activeRow.percent) }}%]</span>
                    </span>
                </template>
                <span v-else class="center-label">Aucune donnée</span>
            </div>
        </div>

        <!-- Légende -->
        <ul v-if="rows && rows.length" class="legend-list">
            <li
                v-for="(row, index) in rows"
                :key="row.label"
                :title="row.label"
                :class="{ 'is-active': index === activeIndex }"
                @mouseenter="hovered = index"
                @mouseleave="hovered = null"
            >
                <span class="legend-color" :style="{ background: colorFor(index) }"></span>
                <span class="legend-label">{{ row.label }}</span>
            </li>
        </ul>

        <div class="stat-cards-footer">
            <p class="footer-total">
                Total visiteurs <strong>{{ formattedTotal }}</strong>
            </p>
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
import { computed, ref, useId } from 'vue'
import { useThemeStore } from '~/stores/themeStore'

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

defineEmits(['goTo'])

const uid = `gsc-${useId()}`
const themeStore = useThemeStore()

/* ---------- Géométrie ---------- */
const C = 150               // centre du viewBox
const R = 138               // rayon de l'arc fin extérieur
const ARC_W = 5.5           // épaisseur normale de l'arc
const ARC_GAP = 0.05        // espace fin entre deux arcs (rad)
const BAND_STROKE = 10      // contour de la bande : arrondit ses angles
const BAND_OUTER = R - 10   // bord externe de la bande
const BAND_INNER = R - 52   // bord interne de la bande (~42px d'épaisseur)

/* ---------- Palette de couleurs ---------- */
const colors = ['#3b82f6', '#8b5cf6', '#10b981', '#f59e0b', '#64748b', '#ec4899', '#06b6d4']

const lightPastels = ['#dbeafe', '#ede9fe', '#d1fae5', '#fef3c7', '#e2e8f0', '#fce7f3', '#cffafe']
const darkPastels = ['#1e3a5f', '#2e1065', '#064e3b', '#78350f', '#334155', '#831843', '#164e63']

const colorFor = (index: number) => colors[index % colors.length]
const pastelFor = (index: number) => {
    const list = themeStore.isDark ? darkPastels : lightPastels
    return list[index % list.length]
}

function polar(r: number, angle: number) {
    return { x: C + r * Math.sin(angle), y: C - r * Math.cos(angle) }
}

function arcPath(r: number, a0: number, a1: number) {
    const diff = a1 - a0
    if (diff >= Math.PI * 2 - 0.02) {
        // Cercle complet
        const mid = a0 + Math.PI
        const p0 = polar(r, a0)
        const pm = polar(r, mid)
        return `M ${p0.x} ${p0.y} A ${r} ${r} 0 1 1 ${pm.x} ${pm.y} A ${r} ${r} 0 1 1 ${p0.x} ${p0.y}`
    }
    const large = diff > Math.PI ? 1 : 0
    const p0 = polar(r, a0)
    const p1 = polar(r, a1)
    return `M ${p0.x} ${p0.y} A ${r} ${r} 0 ${large} 1 ${p1.x} ${p1.y}`
}

function sectorPath(r1: number, r2: number, a0: number, a1: number) {
    const diff = a1 - a0
    if (diff <= 0.02) return ''

    if (diff >= Math.PI * 2 - 0.04) {
        // Anneau complet
        const mid = a0 + Math.PI
        const o0 = polar(r2, a0)
        const om = polar(r2, mid)
        const i0 = polar(r1, a0)
        const im = polar(r1, mid)
        return [
            `M ${o0.x} ${o0.y}`,
            `A ${r2} ${r2} 0 1 1 ${om.x} ${om.y}`,
            `A ${r2} ${r2} 0 1 1 ${o0.x} ${o0.y}`,
            `M ${i0.x} ${i0.y}`,
            `A ${r1} ${r1} 0 1 0 ${im.x} ${im.y}`,
            `A ${r1} ${r1} 0 1 0 ${i0.x} ${i0.y}`,
            'Z'
        ].join(' ')
    }

    const large = diff > Math.PI ? 1 : 0
    const o0 = polar(r2, a0)
    const o1 = polar(r2, a1)
    const i1 = polar(r1, a1)
    const i0 = polar(r1, a0)
    return [
        `M ${o0.x} ${o0.y}`,
        `A ${r2} ${r2} 0 ${large} 1 ${o1.x} ${o1.y}`,
        `L ${i1.x} ${i1.y}`,
        `A ${r1} ${r1} 0 ${large} 0 ${i0.x} ${i0.y}`,
        'Z',
    ].join(' ')
}

/* ---------- Calcul des segments garantissant les vraies proportions ---------- */
const segments = computed(() => {
    const rawRows = props.rows ?? []
    if (rawRows.length === 0) return []

    // Conserver les lignes ayant une valeur positive
    const valid = rawRows
        .map((row, index) => ({ row, originalIndex: index }))
        .filter(({ row }) => (row.visitors > 0 || row.percent > 0))

    if (valid.length === 0) return []

    // Calcul de la base totale réelle affichée
    const sumVisitors = valid.reduce((acc, { row }) => acc + (row.visitors || 0), 0)
    const sumPercent = valid.reduce((acc, { row }) => acc + (row.percent || 0), 0)
    const baseTotal = sumVisitors > 0 ? sumVisitors : (sumPercent > 0 ? sumPercent : 100)

    const isSingle = valid.length === 1
    const inset = BAND_STROKE / 2

    let cursor = 0
    return valid.map(({ row, originalIndex }) => {
        const val = sumVisitors > 0 ? (row.visitors || 0) : (row.percent || 0)
        // Ratio exact sur le cercle complet (360°)
        const ratio = baseTotal > 0 ? val / baseTotal : (1 / valid.length)
        const span = ratio * Math.PI * 2
        const start = cursor
        const end = cursor + span
        cursor = end

        // Espace angulaire pour l'arc extérieur
        const g = isSingle ? 0 : Math.min(ARC_GAP / 2, span * 0.15)
        const arc = arcPath(R, start + g, end - g)

        // Espace angulaire adapté pour la bande pastel
        const bGap = isSingle ? 0 : Math.min(0.04, span * 0.08)
        const b0 = start + bGap
        const b1 = end - bGap
        const band = sectorPath(BAND_INNER + inset, BAND_OUTER - inset, b0, b1)

        // Pourcentage affiché : conserve row.percent si déjà renseigné, sinon proportion relative
        const displayPercent = row.percent > 0 ? row.percent : Math.round(ratio * 1000) / 10

        return {
            index: originalIndex,
            label: row.label,
            visitors: row.visitors ?? 0,
            percent: displayPercent,
            arcPath: arc,
            bandPath: band,
        }
    })
})

/* ---------- Interaction & sélection active ---------- */
const hovered = ref<number | null>(null)

// Détermine l'index du segment ayant la plus grande valeur
const defaultIndex = computed(() => {
    let best = -1
    let max = -1
    ;(props.rows ?? []).forEach((row, index) => {
        const val = (row.visitors ?? 0) > 0 ? row.visitors : (row.percent ?? 0)
        if (val > max) {
            max = val
            best = index
        }
    })
    return best >= 0 ? best : 0
})

const activeIndex = computed(() => hovered.value ?? defaultIndex.value)

// Récupère la ligne correspondante au segment actif avec son pourcentage calculé
const activeRow = computed(() => {
    const rows = props.rows ?? []
    const raw = rows[activeIndex.value]
    if (!raw) return null

    // Cherche le segment calculé correspondant pour avoir le pourcentage exact
    const matchedSeg = segments.value.find(s => s.index === activeIndex.value)
    return {
        ...raw,
        percent: matchedSeg ? matchedSeg.percent : (raw.percent || 0),
    }
})

function formatPercent(value: number) {
    const rounded = Math.round(value * 10) / 10
    return Number.isInteger(rounded) ? String(rounded) : rounded.toFixed(1).replace('.', ',')
}

const formattedTotal = computed(() => {
    if (props.total > 0) return props.total.toLocaleString('fr-FR')
    const sum = (props.rows ?? []).reduce((acc, r) => acc + (r.visitors || 0), 0)
    return sum.toLocaleString('fr-FR')
})
</script>

<style scoped>
.stat-cards {
    width: 100%;
    min-height: 320px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--card-bg, #ffffff);
    border-radius: 1.25rem;
    border: 1px solid var(--border-color, #eef0f4);
    box-shadow:
        0 1px 2px rgba(15, 23, 42, 0.04),
        0 18px 40px -18px rgba(15, 23, 42, 0.14);
    font-family: 'Inter Tight', 'Inter', sans-serif;
    color: var(--text-heading, #0f172a);
    transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease, opacity 0.2s ease;
}

.stat-cards.is-loading {
    opacity: 0.6;
}

/* ---------- En-tête ---------- */
.stat-cards-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.75rem;
}

.header-title {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    min-width: 0;
}

.header-pin {
    display: inline-flex;
    flex-shrink: 0;
}

.header-title h3 {
    margin: 0;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-heading, #0f172a);
    letter-spacing: -0.01em;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.header-description {
    margin: 0;
    flex-shrink: 0;
    font-size: 0.9rem;
    color: var(--text-muted, #8a90a2);
}

/* ---------- Anneau ---------- */
.chart-wrap {
    position: relative;
    width: 100%;
    max-width: 230px;
    aspect-ratio: 1 / 1;
    margin: 0.5rem auto;
}

.donut {
    width: 100%;
    height: 100%;
    overflow: visible;
}

.donut-empty {
    color: var(--border-color, #e2e8f0);
}

.seg {
    cursor: pointer;
    outline: none;
}

.arc {
    transition: stroke-width 0.2s ease, opacity 0.2s ease;
}

.seg.is-active .arc,
.seg:focus-visible .arc {
    stroke-width: 8.5;
}

/* Bande pastel : visible sur TOUS les segments, en surbrillance sur l'actif */
.band {
    opacity: 0.8;
    transition: opacity 0.2s ease;
}

.seg:hover .band,
.seg.is-active .band,
.seg:focus-visible .band {
    opacity: 1;
}

/* ---------- Texte central ---------- */
.center-info {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.25rem;
    padding: 0 18%;
    text-align: center;
    pointer-events: none;
}

.center-label {
    max-width: 100%;
    font-size: 0.8125rem;
    color: var(--text-muted, #6b7280);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.center-value {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 1.35rem;
    font-weight: 600;
    line-height: 1.1;
    color: var(--text-heading, #0f172a);
    letter-spacing: -0.02em;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
}

.center-percent {
    font-size: 1.15rem;
    color: var(--text-muted, #94a3b8);
}

.center-dot {
    flex-shrink: 0;
    width: 7px;
    height: 7px;
    border-radius: 50%;
}

/* ---------- Légende ---------- */
.legend-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.5rem 1rem;
}

.legend-list li {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    max-width: 100%;
    font-size: 0.85rem;
    color: var(--text-muted, #8a90a2);
    cursor: pointer;
    transition: color 0.15s ease;
}

.legend-list li.is-active,
.legend-list li:hover {
    color: var(--text-heading, #0f172a);
    font-weight: 500;
}

.legend-color {
    flex-shrink: 0;
    width: 9px;
    height: 9px;
    border-radius: 50%;
}

.legend-label {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    min-width: 0;
}

/* ---------- Pied de carte ---------- */
.stat-cards-footer {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.footer-total {
    margin: 0;
    font-size: 0.85rem;
    color: var(--text-muted, #8a90a2);
}

.footer-total strong {
    margin-left: 0.25rem;
    font-weight: 600;
    color: var(--text-heading, #0f172a);
}

button {
    color: var(--text-heading, #333);
    cursor: pointer;
}

.stat-cards-footer svg {
    color: var(--bright-fern);
}

.stat-cards-button {
    transition: ease-in 0.3s;
}

.stat-cards-button:hover {
    transform: translateY(-5px);
}

@media (prefers-reduced-motion: reduce) {
    .arc,
    .band {
        transition: none;
    }
}

@media (max-width: 520px) {
    .stat-cards-header {
        flex-direction: column;
        align-items: flex-start;
    }
}
</style>
