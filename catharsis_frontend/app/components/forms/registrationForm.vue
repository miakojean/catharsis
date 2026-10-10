<template>
  <form class="auth-inner-form" @submit.prevent="handleSubmit" novalidate>
    
    <!-- Success Banner -->
    <div v-if="authStore.message.successMessage" class="feedback-alert success-alert" role="alert">
      <svg class="alert-icon" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
      </svg>
      <span>{{ authStore.message.successMessage }}</span>
    </div>

    <!-- Error Banner -->
    <div v-if="authStore.message.errorMessage" class="feedback-alert error-alert" role="alert">
      <svg class="alert-icon" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
      </svg>
      <span>{{ authStore.message.errorMessage }}</span>
    </div>

    <!-- Username Field -->
    <div class="field-item">
      <BaseInput
        v-model="form.username"
        type="text"
        :placeholder="lang === 'en' ? 'Choose a username' : 'Nom d\'utilisateur ou entreprise'"
        :error-message="errorMessage.username"
        autocomplete="username"
        required
      />
    </div>

    <!-- Email Field -->
    <div class="field-item">
      <BaseInput
        v-model="form.email"
        type="email"
        :placeholder="lang === 'en' ? 'Enter your email' : 'Entrez votre email'"
        :error-message="errorMessage.email"
        autocomplete="email"
        required
      />
    </div>

    <!-- Password Field -->
    <div class="field-item">
      <BaseInput
        v-model="form.password"
        type="password"
        :placeholder="lang === 'en' ? 'Create a password' : 'Créez un mot de passe'"
        :error-message="errorMessage.password"
        autocomplete="new-password"
        :show-password-toggle="true"
        required
      />
    </div>

    <!-- Terms hint -->
    <p class="terms-hint">
      {{ lang === 'en' 
        ? 'By signing up, you agree to our Terms and Privacy Policy.' 
        : 'En vous inscrivant, vous acceptez nos Conditions et notre Politique de confidentialité.' 
      }}
    </p>

    <!-- Submit Button (Black Pill matching screenshot) -->
    <div class="action-item">
      <MainButton
        type="submit"
        :is-loading="authStore.isLoading"
        :label="lang === 'en' ? 'Sign up with email' : 'Créer un compte'"
      />
    </div>

  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '~/stores/authStore'
import BaseInput from '../BaseInput/BaseInput.vue'
import MainButton from '../buttons/mainButton.vue'

withDefaults(
  defineProps<{
    lang?: 'en' | 'fr'
  }>(),
  {
    lang: 'en'
  }
)

const authStore = useAuthStore()
const router = useRouter()

const form = ref({
  username: '',
  email: '',
  password: ''
})

const errorMessage = ref({
  username: '',
  email: '',
  password: ''
})

const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/

function validateForm() {
  let isValid = true
  errorMessage.value = { username: '', email: '', password: '' }

  if (!form.value.username.trim()) {
    errorMessage.value.username = "Entrez un nom d'utilisateur"
    isValid = false
  }

  if (!form.value.email.trim()) {
    errorMessage.value.email = 'Entrez votre adresse email'
    isValid = false
  } else if (!emailRegex.test(form.value.email.trim())) {
    errorMessage.value.email = 'Veuillez fournir un email valide'
    isValid = false
  }

  if (!form.value.password) {
    errorMessage.value.password = 'Renseignez un mot de passe'
    isValid = false
  } else if (form.value.password.length < 6) {
    errorMessage.value.password = 'Le mot de passe doit contenir au moins 6 caractères'
    isValid = false
  }

  return isValid
}

async function handleSubmit() {
  if (!validateForm()) return

  const success = await authStore.registration({
    username: form.value.username.trim(),
    email: form.value.email.trim(),
    password: form.value.password
  })

  if (success) {
    setTimeout(() => {
      router.push('/auth/login')
    }, 1500)
  }
}
</script>

<style scoped>
.auth-inner-form {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  width: 100%;
  max-width: 100%;
  padding: 0;
  align-items: stretch;
}

.field-item {
  width: 100%;
}

.terms-hint {
  font-size: 0.6875rem;
  color: #8c8c8c;
  line-height: 1.4;
  margin: -0.15rem 0 0.15rem 0.25rem;
}

.action-item {
  width: 100%;
  margin-top: 0.25rem;
}

.feedback-alert {
  padding: 0.65rem 0.85rem;
  border-radius: 0.75rem;
  font-size: 0.8125rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}

.success-alert {
  background-color: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
}

.error-alert {
  background-color: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
}

.alert-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}
</style>