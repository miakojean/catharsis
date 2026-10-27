<!-- components/PeriodFilter.vue -->
<template>
    <div class="period-filter" ref="rootRef">
        <button class="trigger" @click="toggle">
          <span class="label">{{ currentLabel }}</span>
          <svg class="chevron" :class="{ open }" width="12" height="12" viewBox="0 0 24 24">
            <path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" fill="none" />
          </svg>
        </button>

        <div v-if="open" class="dropdown">
            <!-- Presets -->
            <ul class="presets">
            <li
                v-for="p in presets"
                :key="p.key"
                :class="{ active: selectedKey === p.key }"
                @click="selectPreset(p)"
            >
                {{ p.label }}
            </li>
            </ul>

            <div class="divider" />

            <!-- Custom range -->
            <div class="custom">
            <span class="custom-title">Personnalisé</span>
            <div class="row">
                <label>
                Du
                <input type="date" v-model="customStart" :max="customEnd" />
                </label>
                <label>
                Au
                <input type="date" v-model="customEnd" :min="customStart" />
                </label>
            </div>
            <button
                class="apply"
                :disabled="!customStart || !customEnd"
                @click="applyCustom"
            >
                Appliquer
            </button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'

export interface PeriodValue {
  key: string
  label: string
  start: string | null // ISO date "YYYY-MM-DD"
  end: string | null
}

const props = defineProps<{
  modelValue?: PeriodValue
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: PeriodValue): void
  (e: 'change', value: PeriodValue): void
}>()

/* ---------- helpers ---------- */
const toISO = (d: Date) => {
  const year = d.getFullYear()
  const month = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}
const startOfDay = (d: Date) => new Date(d.getFullYear(), d.getMonth(), d.getDate())
const addDays = (d: Date, n: number) => {
  const r = new Date(d)
  r.setDate(r.getDate() + n)
  return r
}

const today = () => startOfDay(new Date())

/* ---------- presets ---------- */
interface Preset { key: string; label: string; range: () => [string, string] }

const presets: Preset[] = [
  {
    key: 'day', // Modifié (anciennement 'today')
    label: "Aujourd'hui",
    range: () => [toISO(today()), toISO(today())],
  },
  {
    key: 'yesterday',
    label: 'Hier',
    range: () => {
      const y = addDays(today(), -1)
      return [toISO(y), toISO(y)]
    },
  },
  {
    key: 'last7',
    label: '7 derniers jours',
    range: () => [toISO(addDays(today(), -6)), toISO(today())],
  },
  {
    key: 'last30',
    label: '30 derniers jours',
    range: () => [toISO(addDays(today(), -29)), toISO(today())],
  },
  {
    key: 'month', // Modifié (anciennement 'thisMonth')
    label: 'Ce mois-ci',
    range: () => {
      const d = today()
      const start = new Date(d.getFullYear(), d.getMonth(), 1)
      const end = new Date(d.getFullYear(), d.getMonth() + 1, 0)
      return [toISO(start), toISO(end)]
    },
  },
  {
    key: 'lastMonth',
    label: 'Mois dernier',
    range: () => {
      const d = today()
      const start = new Date(d.getFullYear(), d.getMonth() - 1, 1)
      const end = new Date(d.getFullYear(), d.getMonth(), 0)
      return [toISO(start), toISO(end)]
    },
  },
  {
    key: 'year', // Modifié (anciennement 'thisYear')
    label: 'Cette année',
    range: () => {
      const y = today().getFullYear()
      return [`${y}-01-01`, `${y}-12-31`]
    },
  },
]

/* ---------- state ---------- */
const open = ref(false)
const rootRef = ref<HTMLElement | null>(null)

const selectedKey = ref<string>(props.modelValue?.key ?? 'day')
const currentLabel = ref<string>(props.modelValue?.label ?? 'Aujourd\'hui')

const customStart = ref<string>(props.modelValue?.start ?? '')
const customEnd = ref<string>(props.modelValue?.end ?? '')

/* ---------- actions ---------- */
function emitPeriod(v: PeriodValue) {
  emit('update:modelValue', v)
  emit('change', v)
}

function selectPreset(p: Preset) {
  const [start, end] = p.range()
  selectedKey.value = p.key
  currentLabel.value = p.label
  customStart.value = start
  customEnd.value = end
  open.value = false
  emitPeriod({ key: p.key, label: p.label, start, end })
}

function applyCustom() {
  if (!customStart.value || !customEnd.value) return
  selectedKey.value = 'custom'
  currentLabel.value = `${formatFr(customStart.value)} → ${formatFr(customEnd.value)}`
  open.value = false
  emitPeriod({
    key: 'custom',
    label: currentLabel.value,
    start: customStart.value,
    end: customEnd.value,
  })
}

function formatFr(iso: string) {
  const [y, m, d] = iso.split('-')
  return `${d}/${m}/${y}`
}

function toggle() {
  open.value = !open.value
}

/* ---------- click outside ---------- */
function onClickOutside(e: MouseEvent) {
  if (rootRef.value && !rootRef.value.contains(e.target as Node)) {
    open.value = false
  }
}

onMounted(() => document.addEventListener('mousedown', onClickOutside))
onBeforeUnmount(() => document.removeEventListener('mousedown', onClickOutside))

/* ---------- sync external modelValue ---------- */
watch(
  () => props.modelValue,
  (v) => {
    if (!v) return
    selectedKey.value = v.key
    currentLabel.value = v.label
    if (v.start) customStart.value = v.start
    if (v.end) customEnd.value = v.end
  }
)

/* ---------- init : émet la valeur par défaut si rien fourni ---------- */
onMounted(() => {
  if (!props.modelValue) {
    const p = presets.find((x) => x.key === selectedKey.value) ?? presets[3]
    selectPreset(p)
  }
})
</script>

<style scoped>

.period-filter {
  position: relative;
  display: inline-block;
  font-family: system-ui, sans-serif;
  font-size: 14px;
}

.trigger {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #fff;
  cursor: pointer;
  transition: border-color 0.15s;
}

.trigger:hover {
  border-color: #9ca3af;
}

.chevron {
  transition: transform 0.15s;
}

.chevron.open {
  transform: rotate(180deg);
}

.dropdown {
  position: absolute;
  top: calc(100% + 6px);
  right: 0;
  z-index: 100;
  width: 280px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
  padding: 8px;
}

.presets {
  list-style: none;
  margin: 0;
  padding: 0;
}

.presets li {
  padding: 8px 10px;
  border-radius: 6px;
  cursor: pointer;
  color: #374151;
}

.presets li:hover {
  background: #f3f4f6;
}

.presets li.active {
  background: #eef2ff;
  color: #4338ca;
  font-weight: 500;
}

.divider {
  height: 1px;
  background: #e5e7eb;
  margin: 8px 0;
}

.custom {
  padding: 4px 6px 6px;
}

.custom-title {
  font-size: 12px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.row {
  display: flex;
  gap: 8px;
  margin: 8px 0;
}

.row label {
  display: flex;
  flex-direction: column;
  font-size: 12px;
  color: #4b5563;
  gap: 4px;
  flex: 1;
}

.row input {
  padding: 6px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 13px;
}

.apply {
  width: 100%;
  padding: 8px;
  border: none;
  border-radius: 6px;
  background: #4f46e5;
  color: white;
  font-weight: 500;
  cursor: pointer;
}

.apply:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.apply:not(:disabled):hover {
  background: #4338ca;
}
</style>