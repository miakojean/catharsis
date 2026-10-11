import { defineStore } from "pinia";
import { ref } from "vue";
import type { User } from "#imports";

export interface Project {
    id: string
    customer: User
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

            if (response && response.results) {
                projects.value = response.results
            }
            console.log(projects.value)
            return true
        } catch (err: any) {
            message.value.errorMessage = err?.data?.error || "Un problème est survenu, veuillez réessayer plus tard"
            return false
        } finally {
            isLoading.value = false
        }
    }

    function clearMessages() {
        message.value.errorMessage = ''
        message.value.successMessage = ''
    }

    return {
        projects,
        isLoading,
        message,
        getProjects,
        clearMessages
    }
})