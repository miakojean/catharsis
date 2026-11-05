import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  const isDark = ref(false)

  function applyTheme() {
    if (typeof document === 'undefined') return
    if (isDark.value) {
      document.documentElement.classList.add('dark')
      document.documentElement.classList.add('dark-theme')
    } else {
      document.documentElement.classList.remove('dark')
      document.documentElement.classList.remove('dark-theme')
    }
  }

  function initTheme() {
    if (typeof window === 'undefined') return
    const saved = localStorage.getItem('catharsis_theme')
    if (saved !== null) {
      isDark.value = saved === 'dark'
    } else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      isDark.value = true
    }
    applyTheme()
  }

  function setTheme(dark: boolean) {
    isDark.value = dark
    if (typeof window !== 'undefined') {
      localStorage.setItem('catharsis_theme', dark ? 'dark' : 'light')
    }
    applyTheme()
  }

  function toggleTheme() {
    setTheme(!isDark.value)
  }

  return {
    isDark,
    initTheme,
    setTheme,
    toggleTheme,
    applyTheme,
  }
})

