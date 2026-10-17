export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const token = useCookie('token') // Ne fonctionnera que si le cookie n'est PAS HttpOnly

  const api = $fetch.create({
    baseURL: config.public.apiBase || 'http://localhost:8000',

    // ✅ INDISPENSABLE : Autorise l'échange de cookies (cart_session_id, tokens...)
    credentials: 'include',

    onRequest({ options }) {
      // ✅ Garde ceci uniquement si tes tokens ne sont pas en HttpOnly
      if (token.value) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token.value}`,
        }
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