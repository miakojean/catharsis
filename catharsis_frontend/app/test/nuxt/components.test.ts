import { mount } from '@vue/test-utils'
import { describe, it, expect } from 'vitest'
import registrationForm from '../../components/forms/registrationForm.vue'

describe('registrationForm', () => {
  it('doit afficher correctement le titre et tous les champs requis', () => {
    const wrapper = mount(registrationForm, {
      global: {
        stubs: {
          BaseInput: {
            props: ['label'],
            template: '<div class="base-input-stub" :data-label="label" />'
          },
          mainButton: {
            template: '<button class="main-button-stub" type="button">Commencer</button>'
          }
        }
      }
    })

    expect(wrapper.find('h3').text()).toBe('Inscrivez-vous')

    const inputs = wrapper.findAll('.base-input-stub')
    expect(inputs.length).toBe(3)
    expect(inputs[0].attributes('data-label')).toBe('Email')
    expect(inputs[1].attributes('data-label')).toBe('Username')
    expect(inputs[2].attributes('data-label')).toBe('Mot de passe')

    expect(wrapper.find('.main-button-stub').exists()).toBe(true)
  })

  it('doit déclencher la fonction de soumission lors de la validation du formulaire', async () => {
    const wrapper = mount(registrationForm, {
      global: {
        stubs: {
          BaseInput: {
            props: ['label'],
            template: '<div class="base-input-stub" :data-label="label" />'
          },
          mainButton: {
            template: '<button class="main-button-stub" type="button">Commencer</button>'
          }
        }
      }
    })

    await wrapper.find('form').trigger('submit')

    expect(wrapper.emitted('submit')).toBeTruthy()
  })
})