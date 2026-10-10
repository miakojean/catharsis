<template>
  <div class="auth-page">
    <Head>
      <Title>Inscription — Catharsis</Title>
      <Meta name="description" content="Créez votre compte Catharsis." />
    </Head>

    <AuthLayout
      mode="registration"
      switch-route="/auth/login"
      @social="handleSocialAuth"
    >
      <template #default="{ lang }">
        <RegistrationForm :lang="lang" />
      </template>
    </AuthLayout>
  </div>
</template>

<script setup lang="ts">
import AuthLayout from '~/components/layout/AuthLayout.vue'
import RegistrationForm from '~/components/forms/registrationForm.vue'

const handleSocialAuth = (provider: 'google' | 'apple') => {
  console.log(`Initiating ${provider} authentication...`)
  // Social auth integration point
  alert(`Inscription avec ${provider.toUpperCase()} en cours de configuration.`)
}
</script>

<style scoped>
.auth-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f9f9f9;
}
</style>
