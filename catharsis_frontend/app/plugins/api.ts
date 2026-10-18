export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const csrfCookie = useCookie<string | null>('csrftoken')
  let csrfHeaderToken = csrfCookie.value

  const api = $fetch.create({
    baseURL: config.public.apiBase || 'http://localhost:8000',
    credentials: 'include',

    onRequest({ options }) {
      const csrfToken = csrfHeaderToken || csrfCookie.value
      if (csrfToken) {
        options.headers = {
          ...options.headers,
          'X-CSRFToken': csrfToken,
        }
      }
    },

    onResponse({ response }) {
      if (response.url.includes('/account/csrf/')) {
        const data = response._data as { csrfToken?: string } | undefined
        csrfHeaderToken = data?.csrfToken || csrfHeaderToken
      }
    },

    onResponseError({ response }) {
      if (response.status === 401) navigateTo('/auth/login')
      if (response.status === 500) throw new Error('Erreur serveur')
    },
  })

  return {
    provide: { api }
  }
})
