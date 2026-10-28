import { mount } from '@vue/test-utils'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import IntegrationSnippet from '../../components/dashboard/IntegrationSnippet.vue'

describe('IntegrationSnippet', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('affiche le script HTML par défaut avec le siteId fourni', () => {
    const wrapper = mount(IntegrationSnippet, {
      props: {
        siteId: 'test_site_123',
        siteName: 'Mon Super Site'
      }
    })

    expect(wrapper.text()).toContain('Site ID:')
    expect(wrapper.text()).toContain('test_site_123')

    const code = wrapper.find('.code-content').text()
    expect(code).toContain('<script')
    expect(code).toContain('data-site-id="test_site_123"')
  })

  it('permet de basculer vers le format SPA / Nuxt et Événement Custom', async () => {
    const wrapper = mount(IntegrationSnippet, {
      props: {
        siteId: 'abc456',
        siteName: 'Mon Blog'
      }
    })

    const tabs = wrapper.findAll('.tab-btn')
    expect(tabs.length).toBe(3)

    // Clic sur l'onglet SPA
    await tabs[1]!.trigger('click')
    expect(wrapper.find('.code-content').text()).toContain('useHead')
    expect(wrapper.find('.code-content').text()).toContain('abc456')

    // Clic sur l'onglet Custom
    await tabs[2]!.trigger('click')
    expect(wrapper.find('.code-content').text()).toContain('window.Catharsis?.trackEvent')
  })

  it('copie le code dans le presse-papier lors du clic', async () => {
    const writeTextMock = vi.fn().mockResolvedValue(undefined)
    Object.defineProperty(navigator, 'clipboard', {
      value: {
        writeText: writeTextMock
      },
      configurable: true,
      writable: true
    })

    const wrapper = mount(IntegrationSnippet, {
      props: {
        siteId: 'copy_site_789'
      }
    })

    const copyBtn = wrapper.find('.copy-code-btn')
    await copyBtn.trigger('click')

    expect(writeTextMock).toHaveBeenCalledTimes(1)
    expect(writeTextMock).toHaveBeenCalledWith(expect.stringContaining('copy_site_789'))
  })
})
