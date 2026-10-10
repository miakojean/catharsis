import { defineStore } from "pinia";
import { ref } from "vue";

export interface User {
  id?: string;
  username?: string;
  email: string;
  password?: string;
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
    password: ''
  });

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

  function clearMessages() {
    message.value.errorMessage = '';
    message.value.successMessage = '';
  }

  return {
    isLoading,
    message,
    user,
    registration,
    login,
    clearMessages
  };
});