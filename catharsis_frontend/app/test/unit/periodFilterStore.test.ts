import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { usePeriodFilterStore, type PeriodValue } from '../../stores/periodFilterStore'

const storage = new Map<string, string>()

const defaultPeriod: PeriodValue = {
  key: 'day',
  label: "Aujourd'hui",
  start: '2026-11-02',
  end: '2026-11-02',
}

beforeEach(() => {
  storage.clear()
  vi.stubGlobal('window', {
    localStorage: {
      getItem: (key: string) => storage.get(key) ?? null,
      setItem: (key: string, value: string) => storage.set(key, value),
    },
  })
  setActivePinia(createPinia())
})

afterEach(() => {
  vi.unstubAllGlobals()
})

describe('period filter store', () => {
  it('keeps the active period when initialized again', () => {
    const store = usePeriodFilterStore()
    store.initializePeriod(defaultPeriod)

    const selectedPeriod: PeriodValue = {
      key: 'last7',
      label: '7 derniers jours',
      start: '2026-10-27',
      end: '2026-11-02',
    }
    store.setPeriod(selectedPeriod)

    expect(store.initializePeriod(defaultPeriod)).toEqual(selectedPeriod)
    expect(store.selectedPeriod).toEqual(selectedPeriod)
  })

  it('restores a cached period after creating a new store instance', () => {
    const selectedPeriod: PeriodValue = {
      key: 'custom',
      label: '01/10/2026 → 15/10/2026',
      start: '2026-10-01',
      end: '2026-10-15',
    }
    usePeriodFilterStore().setPeriod(selectedPeriod)

    setActivePinia(createPinia())
    const restoredStore = usePeriodFilterStore()

    expect(restoredStore.initializePeriod(defaultPeriod)).toEqual(selectedPeriod)
    expect(restoredStore.selectedPeriod).toEqual(selectedPeriod)
  })
})
