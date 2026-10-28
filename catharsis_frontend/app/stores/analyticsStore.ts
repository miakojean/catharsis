import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface KpiMetric {
  value: number
  formatted: string
  trend: number
  is_positive: boolean
  period: string
}

export interface KpiData {
  users: KpiMetric
  revenue: KpiMetric
  conversion_rate: KpiMetric
  sessions: KpiMetric
}

export interface HeatmapData {
  days: string[]
  hours: string[]
  matrix: number[][]
}

export interface ActiveUsersTimeline {
  period: 'day' | 'month' | 'year'
  peak_value: number
  peak_label: string
  labels: string[]
  data: number[]
}

export interface DeviceCategory {
  name: string
  percentage: number
  count: number
  color: string
}

export interface DevicesData {
  total_visitors: number
  formatted_total: string
  breakdown: DeviceCategory[]
}

export interface AnalyticsPayload {
  site_id?: string | null
  kpi: KpiData
  heatmap: HeatmapData
  active_users: ActiveUsersTimeline
  devices: DevicesData
}

export interface AudienceResult {
  label: string
  visitors: number
}

export interface AudienceReport {
  dimension: string
  available: boolean
  message: string
  total_visitors: number
  results: AudienceResult[]
}

export const useAnalyticsStore = defineStore('analytics', () => {
  const { $api } = useNuxtApp()

  const isLoading = ref<boolean>(false)
  const errorMessage = ref<string>('')
  const selectedPeriod = ref<'day' | 'month' | 'year'>('month')
  const selectedSiteId = ref<string>('')

  // Default initial dynamic state (zero when no activity or site recorded)
  const kpi = ref<KpiData>({
    users: { value: 0, formatted: '0', trend: 0, is_positive: true, period: 'aucune donnée' },
    revenue: { value: 0, formatted: '—', trend: 0, is_positive: true, period: 'Non suivi' },
    conversion_rate: { value: 0, formatted: '—', trend: 0, is_positive: true, period: 'Non suivi' },
    sessions: { value: 0, formatted: '0', trend: 0, is_positive: true, period: 'aucune donnée' }
  })

  const heatmap = ref<HeatmapData>({
    days: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    hours: ['12 am', '2 am', '4 am', '6 am', '8 am', '10 am', '12 am', '12 am', '2 pm', '4 pm', '6 pm'],
    matrix: [
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
  })

  const activeUsers = ref<ActiveUsersTimeline>({
    period: 'month',
    peak_value: 0,
    peak_label: 'Pas de données',
    labels: [],
    data: []
  })

  const devices = ref<DevicesData>({
    total_visitors: 0,
    formatted_total: '0',
    breakdown: [
      { name: 'Desktop', percentage: 0, count: 0, color: '#2563eb' },
      { name: 'Mobile', percentage: 0, count: 0, color: '#38bdf8' },
      { name: 'Tablet', percentage: 0, count: 0, color: '#94a3b8' }
    ]
  })


  async function fetchAnalytics(params?: { site_id?: string; period?: 'day' | 'month' | 'year' }) {
    isLoading.value = true
    errorMessage.value = ''

    if (params?.period) selectedPeriod.value = params.period
    if (params?.site_id !== undefined) selectedSiteId.value = params.site_id

    const queryParams = new URLSearchParams()
    if (selectedSiteId.value) queryParams.append('site_id', selectedSiteId.value)
    if (selectedPeriod.value) queryParams.append('period', selectedPeriod.value)

    const url = `/event/analytics/${queryParams.toString() ? `?${queryParams.toString()}` : ''}`

    try {
      const response: AnalyticsPayload = await $api(url, {
        method: 'GET'
      })

      if (response) {
        if (response.kpi) kpi.value = response.kpi
        if (response.heatmap) heatmap.value = response.heatmap
        if (response.active_users) activeUsers.value = response.active_users
        if (response.devices) devices.value = response.devices
      }
      return true
    } catch (err: any) {
      errorMessage.value = err?.data?.error || err?.message || 'Erreur lors de la récupération des données analytics.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function setPeriod(period: 'day' | 'month' | 'year') {
    selectedPeriod.value = period
    await fetchAnalytics({ period })
  }

  async function setSite(siteId: string) {
    selectedSiteId.value = siteId
    await fetchAnalytics({ site_id: siteId })
  }

  async function fetchAudienceReport(
    dimension: string,
    params: { site_id: string; start_date?: string; end_date?: string },
  ) {
    return await $api<AudienceReport>('/event/audience/', {
      query: { dimension, ...params },
    })
  }

  return {
    isLoading,
    errorMessage,
    selectedPeriod,
    selectedSiteId,
    kpi,
    heatmap,
    activeUsers,
    devices,
    fetchAnalytics,
    fetchAudienceReport,
    setPeriod,
    setSite
  }
})
