import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export type ConversionGoalType = 'custom_event' | 'pageview_url'

export interface ConversionGoalItem {
  id: string
  site_id: string
  name: string
  goal_type: ConversionGoalType
  target_value: string
  conversions_count: number
  converted_sessions: number
  conversion_rate: number
  created_at: string
}

export interface ConversionsReport {
  site_id: string | null
  total_sessions: number
  total_conversions: number
  converted_sessions: number
  conversion_rate: number
  goals: ConversionGoalItem[]
}

export interface CreateConversionGoalPayload {
  site_id?: string
  name: string
  goal_type: ConversionGoalType
  target_value: string
}

export const useConversionStore = defineStore('conversion', () => {
  const { $api } = useNuxtApp()

  // Ux-ui
  const isLoading = ref<boolean>(false)
  const isSubmitting = ref<boolean>(false)
  const isCreateModalOpen = ref<boolean>(false)
  const message = ref({
    successMessage: '',
    errorMessage: '',
  })

  // states
  const selectedSiteId = ref<string>('')
  const totalSessions = ref<number>(0)
  const totalConversions = ref<number>(0)
  const convertedSessions = ref<number>(0)
  const globalConversionRate = ref<number>(0)
  const goals = ref<ConversionGoalItem[]>([])

  // Getters
  const hasGoals = computed(() => goals.value.length > 0)
  const customEventGoalsCount = computed(
    () => goals.value.filter((g) => g.goal_type === 'custom_event').length
  )
  const pageviewGoalsCount = computed(
    () => goals.value.filter((g) => g.goal_type === 'pageview_url').length
  )
  const topPerformingGoal = computed<ConversionGoalItem | null>(() => {
    if (goals.value.length === 0) return null
    return [...goals.value].sort((a, b) => b.conversion_rate - a.conversion_rate)[0] || null
  })

  // Actions
  function clearMessages() {
    message.value.successMessage = ''
    message.value.errorMessage = ''
  }

  function openCreateModal() {
    clearMessages()
    isCreateModalOpen.value = true
  }

  function closeCreateModal() {
    clearMessages()
    isCreateModalOpen.value = false
  }

  async function fetchConversions(params?: {
    site_id?: string
    start_date?: string | null
    end_date?: string | null
  }): Promise<ConversionsReport | null> {
    isLoading.value = true
    message.value.errorMessage = ''

    if (params?.site_id !== undefined) {
      selectedSiteId.value = params.site_id
    }

    try {
      const query: Record<string, string> = {}
      if (selectedSiteId.value) {
        query.site_id = selectedSiteId.value
      }
      if (params?.start_date && params?.end_date) {
        query.start_date = params.start_date
        query.end_date = params.end_date
      }

      const response = await $api<ConversionsReport>('/event/conversions/', {
        method: 'GET',
        query,
      })

      totalSessions.value = response.total_sessions ?? 0
      totalConversions.value = response.total_conversions ?? 0
      convertedSessions.value = response.converted_sessions ?? 0
      globalConversionRate.value = response.conversion_rate ?? 0
      goals.value = response.goals ?? []

      if (response.site_id && !selectedSiteId.value) {
        selectedSiteId.value = response.site_id
      }

      return response
    } catch (err: any) {
      message.value.errorMessage =
        err?.data?.detail ||
        err?.data?.date_range ||
        err?.message ||
        'Impossible de charger les objectifs de conversion.'
      return null
    } finally {
      isLoading.value = false
    }
  }

  async function createGoal(
    payload: CreateConversionGoalPayload,
    dateRange?: { start_date?: string | null; end_date?: string | null }
  ): Promise<boolean> {
    isSubmitting.value = true
    clearMessages()

    try {
      const bodyPayload: CreateConversionGoalPayload = {
        ...payload,
        site_id: payload.site_id || selectedSiteId.value,
      }

      await $api('/event/conversions/', {
        method: 'POST',
        body: bodyPayload,
      })

      message.value.successMessage = 'Objectif de conversion créé avec succès.'
      await fetchConversions({
        site_id: bodyPayload.site_id,
        start_date: dateRange?.start_date,
        end_date: dateRange?.end_date,
      })
      return true
    } catch (err: any) {
      message.value.errorMessage =
        err?.data?.target_value?.[0] ||
        err?.data?.name?.[0] ||
        err?.data?.site_id?.[0] ||
        err?.data?.detail ||
        err?.message ||
        'Une erreur est survenue lors de la création de l’objectif.'
      return false
    } finally {
      isSubmitting.value = false
    }
  }

  async function deleteGoal(
    goalId: string,
    dateRange?: { start_date?: string | null; end_date?: string | null }
  ): Promise<boolean> {
    isSubmitting.value = true
    clearMessages()

    try {
      await $api(`/event/conversions/${goalId}/`, {
        method: 'DELETE',
      })

      goals.value = goals.value.filter((g) => g.id !== goalId)
      message.value.successMessage = 'Objectif de conversion supprimé.'
      await fetchConversions({
        site_id: selectedSiteId.value,
        start_date: dateRange?.start_date,
        end_date: dateRange?.end_date,
      })
      return true
    } catch (err: any) {
      message.value.errorMessage =
        err?.data?.detail ||
        err?.message ||
        'Impossible de supprimer cet objectif de conversion.'
      return false
    } finally {
      isSubmitting.value = false
    }
  }

  return {
    // Ux-ui
    isLoading,
    isSubmitting,
    isCreateModalOpen,
    message,

    // states
    selectedSiteId,
    totalSessions,
    totalConversions,
    convertedSessions,
    globalConversionRate,
    goals,

    // Getters
    hasGoals,
    customEventGoalsCount,
    pageviewGoalsCount,
    topPerformingGoal,

    // Actions
    clearMessages,
    openCreateModal,
    closeCreateModal,
    fetchConversions,
    createGoal,
    deleteGoal,
  }
})

