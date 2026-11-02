import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface PeriodValue {
  key: string
  label: string
  start: string | null
  end: string | null
}

const STORAGE_KEY = 'catharsis-period-filter'

function isPeriodValue(value: unknown): value is PeriodValue {
  if (!value || typeof value !== 'object') return false

  const period = value as Record<string, unknown>
  return (
    typeof period.key === 'string' &&
    typeof period.label === 'string' &&
    (typeof period.start === 'string' || period.start === null) &&
    (typeof period.end === 'string' || period.end === null)
  )
}

export const usePeriodFilterStore = defineStore('periodFilter', () => {
  const selectedPeriod = ref<PeriodValue | null>(null)

  function setPeriod(period: PeriodValue) {
    selectedPeriod.value = period
    if (typeof window !== 'undefined') {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(period))
    }
  }

  function initializePeriod(defaultPeriod: PeriodValue, currentPeriod?: PeriodValue) {
    if (selectedPeriod.value) return selectedPeriod.value

    if (currentPeriod) {
      setPeriod(currentPeriod)
      return currentPeriod
    }

    if (typeof window !== 'undefined') {
      const cachedPeriod = window.localStorage.getItem(STORAGE_KEY)
      if (cachedPeriod) {
        try {
          const parsedPeriod: unknown = JSON.parse(cachedPeriod)
          if (isPeriodValue(parsedPeriod)) {
            setPeriod(parsedPeriod)
            return parsedPeriod
          }
          console.warn('La période enregistrée dans le cache est invalide.')
        } catch (error) {
          if (!(error instanceof SyntaxError)) throw error
          console.warn('La période enregistrée dans le cache est illisible.', error)
        }
      }
    }

    setPeriod(defaultPeriod)
    return defaultPeriod
  }

  return { selectedPeriod, setPeriod, initializePeriod }
})
