<template>
  <div class="auth-page">
    <Head>
      <Title>Connexion — Catharsis</Title>
      <Meta name="description" content="Connectez-vous à votre compte Catharsis." />
    </Head>

    <AuthLayout
      mode="login"
      switch-route="/auth/registration"
      @social="handleSocialAuth"
    >
      <template #default="{ lang }">
        <LoginForm :lang="lang" />
      </template>
    </AuthLayout>
  </div>
</template>

<script setup lang="ts">
import AuthLayout from '~/components/layout/AuthLayout.vue'
import LoginForm from '~/components/forms/loginForm.vue'

const handleSocialAuth = (provider: 'google' | 'apple') => {
  console.log(`Initiating ${provider} authentication...`)
  // Social auth integration point
  alert(`Connexion avec ${provider.toUpperCase()} en cours de configuration.`)
}
</script>

<style scoped>
.auth-page {
  width: 100%;
  min-height: 100vh;
  background: #f9f9f9
}
</style>