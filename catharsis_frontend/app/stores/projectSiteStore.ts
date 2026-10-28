import { defineStore } from "pinia";
import { ref, computed } from "vue";

export interface Project {
    id: string
    site_id: string
    name: string
    created_at: string
    updated_at: string
}

export const useProjectSiteStore = defineStore('projectSite', () => {
    const { $api } = useNuxtApp();

    const projects = ref<Project[]>([])
    const isLoading = ref<boolean>(false)
    const message = ref({
        successMessage: '',
        errorMessage: ''
    })

    async function getProjects() {
        isLoading.value = true
        message.value.errorMessage = ''
        message.value.successMessage = ''

        try {
            const response: any = await $api('/event/', {
                method: 'GET'
            })

            projects.value = Array.isArray(response) ? response : response?.results ?? []
            return true
        } catch (err: any) {
            message.value.errorMessage = err?.data?.error || "Un problème est survenu, veuillez réessayer plus tard"
            return false
        } finally {
            isLoading.value = false
        }
    }

    async function createProject(payload: { name: string }): Promise<Project | null> {
        isLoading.value = true
        message.value.errorMessage = ''
        message.value.successMessage = ''

        try {
            const project: Project = await $api('/event/', {
                method: 'POST',
                body: payload
            })

            projects.value = [project, ...projects.value]
            message.value.successMessage = 'Votre site a été enregistré avec succès.'
            return project
        } catch (err: any) {
            message.value.errorMessage =
                err?.data?.name?.[0] ||
                err?.data?.detail ||
                err?.data?.error ||
                err?.message ||
                'Un problème est survenu lors de l’enregistrement du site.'
            return null
        } finally {
            isLoading.value = false
        }
    }

    const config = useRuntimeConfig()
    const trackerUrl = computed(() => (config.public?.trackerScriptUrl as string) || 'http://localhost:8000/static/tracker.js')

    function getScriptSnippet(siteId: string): string {
        return `<script\n  defer\n  src="${trackerUrl.value}"\n  data-site-id="${siteId}">\n</script>`
    }

    function getFrameworkSnippet(siteId: string): string {
        return `<!-- Nuxt (nuxt.config.ts) / Vue (index.html) -->
useHead({
  script: [
    {
      src: '${trackerUrl.value}',
      defer: true,
      'data-site-id': '${siteId}',
    }
  ]
})`
    }

    function getManualEventSnippet(eventName = 'inscription_terminee', properties = '{ plan: "pro" }'): string {
        return `// Déclencher un événement personnalisé
window.Catharsis?.trackEvent('${eventName}', ${properties})`
    }

    function clearMessages() {
        message.value.errorMessage = ''
        message.value.successMessage = ''
    }

    return {
        projects,
        isLoading,
        message,
        trackerUrl,
        getProjects,
        createProject,
        getScriptSnippet,
        getFrameworkSnippet,
        getManualEventSnippet,
        clearMessages
    }
})