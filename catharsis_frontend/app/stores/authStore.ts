import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useProjectSiteStore } from "~/stores/projectSiteStore";

export interface User {
  id?: string;
  username?: string;
  email: string;
  password?: string;
  initials?: string;
  phone_number?: string;
}

export function computeUserInitials(user?: Partial<User> | null): string {
  if (!user) return '??';
  if (user.initials && user.initials.trim()) {
    return user.initials.trim().toUpperCase();
  }
  if (user.username && user.username.trim()) {
    const parts = user.username.trim().split(/\s+/);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    return user.username.trim().slice(0, 2).toUpperCase();
  }
  if (user.email && user.email.trim()) {
    const namePart = user.email.split('@')[0];
    const parts = namePart.split(/[._\-+]+/).filter(Boolean);
    if (parts.length >= 2) {
      return (parts[0][0] + parts[1][0]).toUpperCase();
    }
    if (namePart.length >= 2) {
      return namePart.slice(0, 2).toUpperCase();
    }
    if (namePart.length === 1) {
      return namePart.toUpperCase();
    }
  }
  return '??';
}

export const useAuthStore = defineStore('auth', () => {
  const { $api } = useNuxtApp();

  // ui-ux
  const isLoading = ref<boolean>(false);
  const message = ref({
    successMessage: '',
    errorMessage: ''
  });

  // state
  const userCookie = useCookie<User | null>('user');
  const user = ref<User>(userCookie.value || {
    id: '',
    username: '',
    email: '',
    password: '',
    initials: ''
  });

  const initials = computed(() => computeUserInitials(user.value));


  // actions
  async function registration(payload: User) {
    isLoading.value = true;
    message.value.errorMessage = '';
    message.value.successMessage = '';

    try {
      const response = await $api('/account/customer/', {
        method: 'POST',
        body: payload
      });

      if (response) {
        message.value.successMessage = "Votre compte a été créé avec succès !";
        return true;
      } else {
        message.value.errorMessage = "Un problème est survenu lors de la création de votre compte";
        return false;
      }
    } catch (err: any) {
      message.value.errorMessage = err?.data?.error || err?.message || "Un problème est survenu, veuillez réessayer plus tard";
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  async function login(payload: { email: string; password?: string }) {
    isLoading.value = true;
    message.value.errorMessage = '';
    message.value.successMessage = '';

    try {
      const response: any = await $api('/account/login/', {
        method: 'POST',
        body: payload
      });

      if (response && response.access_token) {
        const tokenCookie = useCookie('token');
        tokenCookie.value = response.access_token;
        const refreshTokenCookie = useCookie<string | null>('refresh_token');
        refreshTokenCookie.value = response.refresh_token || null;
        
        if (response.user) {
          user.value = response.user;
          userCookie.value = response.user;
        } else {
          user.value.email = payload.email;
          userCookie.value = { email: payload.email };
        }

        message.value.successMessage = "Connexion réussie !";
        return true;
      } else {
        message.value.successMessage = "Connexion réussie !";
        return true;
      }
    } catch (err: any) {
      message.value.errorMessage = err?.data?.error || "Identifiants invalides ou erreur de connexion";
      return false;
    } finally {
      isLoading.value = false;
    }
  }

  async function logout() {
    isLoading.value = true;
    message.value.errorMessage = '';
    message.value.successMessage = '';

    const tokenCookie = useCookie<string | null>('token');
    const refreshTokenCookie = useCookie<string | null>('refresh_token');

    try {
      if (refreshTokenCookie.value) {
        await $api('/account/logout/', {
          method: 'POST',
          body: { refresh: refreshTokenCookie.value }
        });
      }

      message.value.successMessage = 'Vous êtes déconnecté.';
      return true;
    } catch (err: any) {
      message.value.errorMessage =
        err?.data?.detail ||
        err?.data?.error ||
        err?.message ||
        'La session locale a été fermée, mais le jeton n’a pas pu être révoqué côté serveur.';
      return false;
    } finally {
      tokenCookie.value = null;
      refreshTokenCookie.value = null;
      userCookie.value = null;
      user.value = {
        id: '',
        username: '',
        email: ''
      };
      useProjectSiteStore().projects = [];
      isLoading.value = false;
    }
  }

  async function fetchCurrentUser() {
    const tokenCookie = useCookie<string | null>('token');
    if (!tokenCookie.value) return null;

    try {
      const response: any = await $api('/account/me/', {
        method: 'GET'
      });
      if (response) {
        user.value = {
          ...user.value,
          ...response
        };
        userCookie.value = user.value;
        return user.value;
      }
    } catch {
      // Fallback silently if session cannot be refreshed
    }
    return null;
  }

  function clearMessages() {
    message.value.errorMessage = '';
    message.value.successMessage = '';
  }

  return {
    isLoading,
    message,
    user,
    initials,
    registration,
    login,
    logout,
    fetchCurrentUser,
    clearMessages
  };
});