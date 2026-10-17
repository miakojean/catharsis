<template>
  <form class="auth-inner-form" @submit.prevent="handleSubmit" novalidate>
    
    <!-- Success Banner 
    <div v-if="authStore.message.successMessage" class="feedback-alert success-alert" role="alert">
      <svg class="alert-icon" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
      </svg>
      <span>{{ authStore.message.successMessage }}</span>
    </div> -->

    <!-- Error Banner -->
    <div v-if="authStore.message.errorMessage" class="feedback-alert error-alert" role="alert">
      <svg class="alert-icon" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
      </svg>
      <span>{{ authStore.message.errorMessage }}</span>
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
        :placeholder="lang === 'en' ? 'Enter your password' : 'Entrez votre mot de passe'"
        :error-message="errorMessage.password"
        autocomplete="current-password"
        :show-password-toggle="true"
        required
      />
    </div>

    <!-- Forgot Password Link -->
    <div class="row-meta">
      <a href="#" class="forgot-link" @click.prevent="handleForgotPassword">
        {{ lang === 'en' ? 'Forgot password?' : 'Mot de passe oublié ?' }}
      </a>
    </div>

    <!-- Submit Button (Black Pill matching screenshot) -->
    <div class="action-item">
      <MainButton
        type="submit"
        :is-loading="authStore.isLoading"
        :label="lang === 'en' ? 'Sign in with email' : 'Se connecter avec l\'email'"
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
  email: '',
  password: ''
})

const errorMessage = ref({
  email: '',
  password: ''
})

const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/

function validateForm() {
  let isValid = true
  errorMessage.value = { email: '', password: '' }

  if (!form.value.email.trim()) {
    errorMessage.value.email = 'Veuillez renseigner votre email'
    isValid = false
  } else if (!emailRegex.test(form.value.email.trim())) {
    errorMessage.value.email = 'Adresse email invalide'
    isValid = false
  }

  if (!form.value.password) {
    errorMessage.value.password = 'Veuillez saisir votre mot de passe'
    isValid = false
  }

  return isValid
}

async function handleSubmit() {
  if (!validateForm()) return

  const success = await authStore.login({
    email: form.value.email.trim(),
    password: form.value.password
  })

  if (success) {
    setTimeout(() => {
      router.push('/dashboard')
    }, 1000)
  }
}

function handleForgotPassword() {
  alert(langText('Un lien de réinitialisation vous sera envoyé.', 'A reset link will be sent to your email.'))
}

function langText(fr: string, en: string) {
  return fr
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

.row-meta {
  display: flex;
  justify-content: flex-end;
  padding: 0 0.5rem;
  margin-top: -0.25rem;
}

.forgot-link {
  font-size: 0.75rem;
  color: #737373;
  text-decoration: none;
  transition: color 0.15s ease;
}

.forgot-link:hover {
  color: #171717;
  text-decoration: underline;
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
