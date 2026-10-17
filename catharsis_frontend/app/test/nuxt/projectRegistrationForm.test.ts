import { mount } from '@vue/test-utils'
import { describe, expect, it } from 'vitest'
import projectRegistrationForm from '../../components/forms/projectRegistrationForm.vue'

describe('projectRegistrationForm', () => {
  it('requires a project name before submitting', async () => {
    const wrapper = mount(projectRegistrationForm, {
      global: {
        stubs: {
          BaseInput: {
            props: ['modelValue', 'label', 'errorMessage'],
            emits: ['update:modelValue'],
            template: '<div><input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" /><p v-if="errorMessage" role="alert">{{ errorMessage }}</p></div>'
          },
          mainButton: {
            template: '<button type="submit">Enregistrer</button>'
          }
        }
      }
    })

    await wrapper.find('form').trigger('submit')

    expect(wrapper.find('[role="alert"]').text()).toContain('Veuillez saisir le nom')
    expect(wrapper.emitted('submit')).toBeUndefined()
  })

  it('submits the trimmed project name', async () => {
    const wrapper = mount(projectRegistrationForm, {
      global: {
        stubs: {
          BaseInput: {
            props: ['modelValue', 'label', 'errorMessage'],
            emits: ['update:modelValue'],
            template: '<div><input :value="modelValue" @input="$emit(\'update:modelValue\', $event.target.value)" /><p v-if="errorMessage" role="alert">{{ errorMessage }}</p></div>'
          },
          mainButton: {
            template: '<button type="submit">Enregistrer</button>'
          }
        }
      }
    })

    await wrapper.find('input').setValue('  Mon application  ')
    await wrapper.find('form').trigger('submit')

    expect(wrapper.emitted('submit')).toEqual([[{ name: 'Mon application' }]])
  })
})
