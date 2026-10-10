<template>
  <button 
    :type="type" 
    class="main-pill-button" 
    :disabled="isLoading || disabled"
    :class="{ 'is-loading': isLoading, 'is-disabled': disabled }"
    @click="$emit('click', $event)"
  >
    <span v-if="!isLoading" class="btn-content">
      <slot>{{ label }}</slot>
    </span>
    <span v-else class="spinner-wrapper">
      <svg class="spinner" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle class="spinner-track" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3"></circle>
        <path class="spinner-head" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
    </span>
  </button>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    type?: 'button' | 'submit' | 'reset'
    label?: string
    isLoading?: boolean
    disabled?: boolean
  }>(),
  {
    type: 'submit',
    label: 'Sign in with email',
    isLoading: false,
    disabled: false
  }
)

defineEmits<{
  (e: 'click', event: MouseEvent): void
}>()
</script>

<style scoped>
.main-pill-button {
  width: 100%;
  height: 44px;
  padding: 0 1.5rem;
  background-color: #111111;
  color: #ffffff;
  border: 1px solid #111111;
  border-radius: 9999px;
  font-size: 0.875rem;
  font-weight: 500;
  letter-spacing: -0.01em;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.06);
}

.main-pill-button:hover:not(:disabled) {
  background-color: #242424;
  border-color: #242424;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.12), 0 2px 4px -1px rgba(0, 0, 0, 0.07);
}

.main-pill-button:active:not(:disabled) {
  background-color: #000000;
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.main-pill-button:disabled {
  opacity: 0.65;
  cursor: not-allowed;
  transform: none;
}

.spinner-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner {
  width: 20px;
  height: 20px;
  animation: spin 0.8s linear infinite;
}

.spinner-track {
  opacity: 0.25;
}

.spinner-head {
  opacity: 0.9;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
