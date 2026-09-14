export default defineNuxtPlugin(async () => {
  
  const config = useRuntimeConfig()
  
  // 🛠️ CORRECTION 1 : Récupérer le token depuis les cookies Nuxt
  const token = useCookie('token') 

    const api = $fetch.create({
        baseURL: config.public.apiBase || 'http://localhost:8000',
        credentials: 'include', // ✅ Laisse ça, c'est très bien pour le CSRF et les sessions

        onRequest({ options }) {
        // 🛠️ CORRECTION 2 : Réinjecter le token JWT pour authentifier l'utilisateur
        if (token.value) {
            options.headers = {
            ...options.headers,
            Authorization: `Bearer ${token.value}`
            }
        }

        const method = options.method?.toUpperCase() || 'GET'
        if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
            const csrfFromBrowser = useCookie('csrftoken').value;
            if (csrfFromBrowser) {
            options.headers = {
                ...options.headers,
                'X-CSRFToken': csrfFromBrowser
            }
            } else {
            console.warn("🚨 Aucun cookie CSRF trouvé dans le navigateur !")
            }
        }
    },

    onResponseError({ response }) {
      if (response.status === 403) throw new Error('Erreur serveur')
      if (response.status === 500) throw new Error('Erreur serveur')
    },
  })

  // Initialiser le token CSRF au chargement de l'app
  /* try {
    await api('/account/csrf/')
    console.log('✅ Token CSRF initialisé')
  } catch (err) {
    console.warn('⚠️ Erreur lors de l\'initialisation du token CSRF:', err)
  }*/

  return { provide: { api } }
})