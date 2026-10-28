import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useAnalyticsStore } from '../../stores/analyticsStore'
import KpiMatrixCard from '../../components/dashboard/KpiMatrixCard.vue'
import SessionsDeviceCard from '../../components/dashboard/SessionsDeviceCard.vue'
import ActiveUsersChart from '../../components/dashboard/ActiveUsersChart.vue'

describe('Analytics Dashboard & Store', () => {
  it('initializes store with default dynamic metrics at zero when no data exists', () => {
    setActivePinia(createPinia())
    const store = useAnalyticsStore()

    expect(store.kpi.users.formatted).toBe('0')
    expect(store.kpi.revenue.formatted).toBe('—')
    expect(store.kpi.revenue.period).toBe('Non suivi')
    expect(store.kpi.conversion_rate.formatted).toBe('—')
    expect(store.kpi.conversion_rate.period).toBe('Non suivi')
    expect(store.kpi.sessions.formatted).toBe('0')

    expect(store.heatmap.days.length).toBe(7)
    expect(store.heatmap.matrix.length).toBe(7)
    expect(store.heatmap.matrix[0]![0]).toBe(0)

    expect(store.activeUsers.peak_value).toBe(0)
    expect(store.activeUsers.labels).toEqual([])
    expect(store.activeUsers.data).toEqual([])
    expect(store.devices.total_visitors).toBe(0)
    expect(store.devices.formatted_total).toBe('0')
    expect(store.devices.breakdown[0]!.percentage).toBe(0)
  })


  it('renders dynamic KPI metrics in KpiMatrixCard', () => {
    setActivePinia(createPinia())
    const store = useAnalyticsStore()
    store.kpi.users.formatted = '1 520'
    store.kpi.revenue.formatted = '$12 450.00'

    const wrapper = mount(KpiMatrixCard)
    expect(wrapper.text()).toContain('1 520')
    expect(wrapper.text()).toContain('$12 450.00')
    expect(wrapper.text()).toContain('Conv Rate')
    expect(wrapper.text()).toContain('Session')
  })

  it('renders dynamic total visitors and legend in SessionsDeviceCard', () => {
    setActivePinia(createPinia())
    const store = useAnalyticsStore()
    store.devices.formatted_total = '42.890'
    store.devices.breakdown[0]!.percentage = 82.4

    const wrapper = mount(SessionsDeviceCard)
    expect(wrapper.text()).toContain('42.890')
    expect(wrapper.text()).toContain('82.4%')
    expect(wrapper.text()).toContain('Desktop')
    expect(wrapper.text()).toContain('Mobile')
  })

  it('renders dynamic active users timeline and period buttons in ActiveUsersChart', () => {
    setActivePinia(createPinia())
    const store = useAnalyticsStore()
    store.activeUsers.peak_label = 'Test Peak Date'
    store.activeUsers.peak_value = 99999
    store.activeUsers.data = [99999]

    const wrapper = mount(ActiveUsersChart)
    expect(wrapper.text()).toContain('Test Peak Date')
    expect(wrapper.text()).toContain('99 999')
    expect(wrapper.findAll('.filter-opt').length).toBe(3)
  })
})
