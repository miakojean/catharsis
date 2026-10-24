import { flushPromises, mount } from '@vue/test-utils'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import VisitorsSummary from '../../components/dashboard/VisitorsSummary.vue'

const { fetchAudienceReport } = vi.hoisted(() => ({
  fetchAudienceReport: vi.fn(),
}))

vi.mock('../../stores/analyticsStore', () => ({
  useAnalyticsStore: () => ({ fetchAudienceReport }),
}))

describe('VisitorsSummary period filtering', () => {
  beforeEach(() => {
    fetchAudienceReport.mockReset()
    fetchAudienceReport.mockResolvedValue({
      dimension: 'devices',
      available: true,
      message: '',
      total_visitors: 0,
      results: [],
    })
  })

  it('loads all audience charts with the selected period and reloads on period change', async () => {
    const wrapper = mount(VisitorsSummary, {
      props: { siteId: 'site-test' },
      global: {
        stubs: {
          'graph-stats-card': true,
        },
      },
    })
    await flushPromises()

    expect(fetchAudienceReport).toHaveBeenCalledTimes(6)
    const initialCalls = fetchAudienceReport.mock.calls
    expect(initialCalls.map(([dimension]) => dimension)).toEqual([
      'countries',
      'sources',
      'devices',
      'browsers',
      'operating-systems',
      'pages',
    ])
    for (const [, params] of initialCalls) {
      expect(params).toMatchObject({ site_id: 'site-test' })
      expect(params.start_date).toMatch(/^\d{4}-\d{2}-\d{2}$/)
      expect(params.end_date).toMatch(/^\d{4}-\d{2}-\d{2}$/)
    }

    await wrapper.find('.trigger').trigger('click')
    await wrapper.findAll('.presets li')[1].trigger('click')
    await flushPromises()

    expect(fetchAudienceReport).toHaveBeenCalledTimes(12)
    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    const yesterdayIso = [
      yesterday.getFullYear(),
      String(yesterday.getMonth() + 1).padStart(2, '0'),
      String(yesterday.getDate()).padStart(2, '0'),
    ].join('-')
    for (const [, params] of fetchAudienceReport.mock.calls.slice(6)) {
      expect(params).toMatchObject({
        site_id: 'site-test',
        start_date: yesterdayIso,
        end_date: yesterdayIso,
      })
    }
    wrapper.unmount()
  })
})
