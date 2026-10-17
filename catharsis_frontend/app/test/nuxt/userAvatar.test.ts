import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import UserAvatar from '../../components/user/UserAvatar.vue'
import { computeUserInitials } from '../../stores/authStore'

describe('computeUserInitials', () => {
  it('returns initials from dotted email', () => {
    expect(computeUserInitials({ email: 'jane.doe@example.com' })).toBe('JD')
  })

  it('returns initials from underscore email', () => {
    expect(computeUserInitials({ email: 'john_smith@example.com' })).toBe('JS')
  })

  it('returns initials from single word email', () => {
    expect(computeUserInitials({ email: 'alexandre@example.com' })).toBe('AL')
  })

  it('returns explicit initials if provided', () => {
    expect(computeUserInitials({ initials: 'mj', email: 'test@example.com' })).toBe('MJ')
  })

  it('returns initials from username with space', () => {
    expect(computeUserInitials({ username: 'Catharsis Studio' })).toBe('CS')
  })

  it('returns ?? for undefined user', () => {
    expect(computeUserInitials(null)).toBe('??')
  })
})

describe('UserAvatar', () => {
  it('displays explicitly passed initials', () => {
    const wrapper = mount(UserAvatar, {
      props: {
        initials: 'AB'
      }
    })
    expect(wrapper.find('.avatar-initials').text()).toBe('AB')
  })

  it('computes initials from email prop', () => {
    const wrapper = mount(UserAvatar, {
      props: {
        email: 'sophie.martin@domain.fr'
      }
    })
    expect(wrapper.find('.avatar-initials').text()).toBe('SM')
  })

  it('applies the selected size class', () => {
    const wrapper = mount(UserAvatar, {
      props: {
        size: 'lg'
      }
    })
    expect(wrapper.classes()).toContain('avatar-lg')
  })

  it('renders status dot when showStatus is true', () => {
    const wrapper = mount(UserAvatar, {
      props: {
        showStatus: true,
        status: 'online'
      }
    })
    expect(wrapper.find('.avatar-status-dot').exists()).toBe(true)
    expect(wrapper.find('.status-online').exists()).toBe(true)
  })
})
