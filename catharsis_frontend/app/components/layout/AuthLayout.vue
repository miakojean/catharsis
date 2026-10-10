<template>
  <div class="auth-viewport">
    <!-- Ambient canvas framing container -->
    <main class="auth-card-container">
      <div class="auth-card">
        
        <!-- Left Side: Clean Form Panel -->
        <section class="auth-form-panel">
          
          <!-- Top Row: Minimalist Brand Logo & Language Switcher -->
          <div class="auth-top-bar">
            <NuxtLink to="/" class="logo-link" title="Catharsis Home">
              <AuthLogo />
            </NuxtLink>

            <!-- Discreet Language Switcher -->
            <button 
              type="button" 
              class="lang-toggle-btn"
              @click="toggleLang"
              :title="currentLang === 'en' ? 'Passer en Français' : 'Switch to English'"
            >
              <span :class="{ 'active-lang': currentLang === 'en' }">EN</span>
              <span class="lang-divider">/</span>
              <span :class="{ 'active-lang': currentLang === 'fr' }">FR</span>
            </button>
          </div>

          <!-- Centered Form Content Wrapper -->
          <div class="auth-content-box">
            
            <!-- Heading & Subtitle -->
            <header class="auth-header">
              <h1 class="auth-title">{{ displayTitle }}</h1>
              <p class="auth-subtitle">{{ displaySubtitle }}</p>
            </header>

            <!-- Social Auth Pill Buttons -->
            <div v-if="showSocial" class="social-wrapper">
              <SocialButtons
                :google-label="currentLang === 'en' ? 'Sign In with Google' : 'Continuer avec Google'"
                :apple-label="currentLang === 'en' ? 'Sign In with Apple' : 'Continuer avec Apple'"
                @google="handleSocial('google')"
                @apple="handleSocial('apple')"
              />

              <!-- Divider -->
              <div class="auth-divider">
                <span class="divider-line"></span>
                <span class="divider-text">{{ currentLang === 'en' ? 'Or' : 'ou' }}</span>
                <span class="divider-line"></span>
              </div>
            </div>

            <!-- Form Slot (Fields + Submit Button) -->
            <div class="form-slot-wrapper">
              <slot :lang="currentLang" />
            </div>

            <!-- Switch Auth Link (Login <-> Register) -->
            <footer class="auth-switch-section">
              <p class="switch-prompt">
                {{ displaySwitchText }}
                <NuxtLink :to="switchRoute" class="switch-link">
                  {{ displaySwitchActionText }}
                </NuxtLink>
              </p>
            </footer>
          </div>

          <!-- Bottom Footer Navigation Links -->
          <nav class="auth-bottom-nav" aria-label="Legal & Support">
            <a href="#" class="nav-link" @click.prevent>{{ currentLang === 'en' ? 'Help' : 'Aide' }}</a>
            <span class="nav-sep">·</span>
            <a href="#" class="nav-link" @click.prevent>{{ currentLang === 'en' ? 'Terms' : 'Conditions' }}</a>
            <span class="nav-sep">·</span>
            <a href="#" class="nav-link" @click.prevent>{{ currentLang === 'en' ? 'Privacy' : 'Confidentialité' }}</a>
          </nav>
        </section>

        <!-- Right Side: Business Analytics Graphics Panel -->
        <aside class="auth-art-panel" aria-label="Aperçu des indicateurs d'analyse">
          <AuthAnalyticsVisual :lang="currentLang" />
        </aside>

      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import AuthLogo from '../auth/AuthLogo.vue'
import SocialButtons from '../buttons/socialButtons.vue'
import AuthAnalyticsVisual from '../auth/AuthAnalyticsVisual.vue'

const props = withDefaults(
  defineProps<{
    mode: 'login' | 'registration'
    titleEn?: string
    titleFr?: string
    subtitleEn?: string
    subtitleFr?: string
    switchRoute?: string
    showSocial?: boolean
  }>(),
  {
    mode: 'login',
    titleEn: '',
    titleFr: '',
    subtitleEn: '',
    subtitleFr: '',
    switchRoute: '/auth/registration',
    showSocial: true
  }
)

const emit = defineEmits<{
  (e: 'social', provider: 'google' | 'apple'): void
}>()

// Default language state (persisted in session / local storage if available)
const currentLang = ref<'en' | 'fr'>('en')

const toggleLang = () => {
  currentLang.value = currentLang.value === 'en' ? 'fr' : 'en'
}

const displayTitle = computed(() => {
  if (props.mode === 'login') {
    return currentLang.value === 'en'
      ? (props.titleEn || 'Welcome back!')
      : (props.titleFr || 'Ravi de vous revoir !')
  } else {
    return currentLang.value === 'en'
      ? (props.titleEn || 'Create an account')
      : (props.titleFr || 'Inscrivez-vous')
  }
})

const displaySubtitle = computed(() => {
  if (props.mode === 'login') {
    return currentLang.value === 'en'
      ? (props.subtitleEn || 'Your work, your team, your flow — all in one place.')
      : (props.subtitleFr || 'Votre travail, votre équipe, votre flux — réunis en un seul endroit.')
  } else {
    return currentLang.value === 'en'
      ? (props.subtitleEn || 'Your work, your team, your flow — all in one place.')
      : (props.subtitleFr || 'Commencez avec Catharsis — tout au même endroit.')
  }
})

const displaySwitchText = computed(() => {
  if (props.mode === 'login') {
    return currentLang.value === 'en'
      ? "Don't have an account?"
      : "Vous n'avez pas de compte ?"
  } else {
    return currentLang.value === 'en'
      ? 'Already have an account?'
      : 'Vous avez déjà un compte ?'
  }
})

const displaySwitchActionText = computed(() => {
  if (props.mode === 'login') {
    return currentLang.value === 'en' ? 'Sign Up' : "S'inscrire"
  } else {
    return currentLang.value === 'en' ? 'Sign In' : 'Se connecter'
  }
})

const handleSocial = (provider: 'google' | 'apple') => {
  emit('social', provider)
}
</script>

<style scoped>
/* Full screen viewport */
.auth-viewport {
  min-height: 100vh;
  width: 100%;
  margin: 0;
  padding: 0;
  display: flex;
  overflow-x: hidden;
  background-color: #ffffff;
}

@media (min-width: 768px) {
  .auth-viewport {
    padding: 0;
  }
}

.auth-card-container {
  width: 100%;
  min-height: 100vh;
  display: flex;
  margin: 0;
  padding: 0;
}

/* Full-screen edge-to-edge 50/50 split layout */
.auth-card {
  width: 100%;
  min-height: 100vh;
  background-color: #ffffff;
  border-radius: 0;
  border: none;
  box-shadow: none;
  display: grid;
  grid-template-columns: 1fr;
}

@media (min-width: 900px) {
  .auth-card {
    grid-template-columns: 1fr 1fr;
    min-height: 100vh;
  }
}

/* Left Form Column */
.auth-form-panel {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 2.5rem 2rem 2rem;
  background-color: #ffffff;
  min-height: 100vh;
  box-sizing: border-box;
}

@media (min-width: 640px) {
  .auth-form-panel {
    padding: 3rem 3rem 2rem;
  }
}

@media (min-width: 1024px) {
  .auth-form-panel {
    padding: 3.5rem 4.5rem 2.5rem;
  }
}

@media (min-width: 1280px) {
  .auth-form-panel {
    padding: 4rem 5.5rem 3rem;
  }
}

.auth-top-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  margin-bottom: 1.25rem;
}

.logo-link {
  display: inline-flex;
  text-decoration: none;
}

.lang-toggle-btn {
  background: none;
  border: 1px solid #e5e5e5;
  border-radius: 9999px;
  padding: 0.2rem 0.55rem;
  font-size: 0.6875rem;
  font-weight: 500;
  color: #737373;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: all 0.15s ease;
}

.lang-toggle-btn:hover {
  border-color: #d4d4d4;
  color: #171717;
}

.lang-divider {
  color: #d4d4d4;
}

.active-lang {
  color: #111111;
  font-weight: 600;
}

/* Centered content box */
.auth-content-box {
  width: 100%;
  max-width: 360px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
}

.auth-header {
  text-align: center;
  margin-bottom: 1.5rem;
}

.auth-title {
  font-size: 1.875rem;
  font-weight: 600;
  letter-spacing: -0.03em;
  color: #111111;
  margin: 0 0 0.5rem 0;
  line-height: 1.2;
}

@media (min-width: 640px) {
  .auth-title {
    font-size: 2.125rem;
  }
}

.auth-subtitle {
  font-size: 0.8125rem;
  line-height: 1.45;
  color: #737373;
  margin: 0 auto;
  max-width: 290px;
  letter-spacing: -0.01em;
}

.social-wrapper {
  display: flex;
  flex-direction: column;
  margin-bottom: 0.5rem;
}

/* Or Divider */
.auth-divider {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 1.15rem 0;
  width: 100%;
}

.divider-line {
  flex: 1;
  height: 1px;
  background-color: #ebebeb;
}

.divider-text {
  padding: 0 0.75rem;
  font-size: 0.75rem;
  color: #a3a3a3;
  font-weight: 400;
}

.form-slot-wrapper {
  width: 100%;
}

/* Switch link section */
.auth-switch-section {
  text-align: center;
  margin-top: 1.25rem;
}

.switch-prompt {
  font-size: 0.8125rem;
  color: #737373;
  margin: 0;
}

.switch-link {
  color: #111111;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
  margin-left: 0.25rem;
  transition: color 0.15s ease;
}

.switch-link:hover {
  color: #000000;
  text-decoration-thickness: 2px;
}

/* Bottom Help Terms Privacy navigation */
.auth-bottom-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  margin-top: 2rem;
  padding-top: 0.5rem;
}

.nav-link {
  font-size: 0.75rem;
  color: #a3a3a3;
  text-decoration: none;
  transition: color 0.15s ease;
}

.nav-link:hover {
  color: #525252;
}

.nav-sep {
  font-size: 0.75rem;
  color: #d4d4d4;
}

/* Right Art Panel */
.auth-art-panel {
  display: none;
  position: relative;
  width: 100%;
  height: 100%;
  min-height: 100%;
  background-color: #0f0f11;
  overflow: hidden;
}

@media (min-width: 900px) {
  .auth-art-panel {
    display: flex;
    align-items: stretch;
  }
}
</style>
