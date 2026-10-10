<template>
  <div class="social-auth-grid">
    <!-- Google Button -->
    <button
      type="button"
      class="social-pill-btn"
      @click="$emit('google')"
      :aria-label="googleLabel"
    >
      <svg class="social-icon" width="18" height="18" viewBox="0 0 24 24">
        <path
          fill="#4285F4"
          d="M23.745 12.27c0-.7-.06-1.4-.19-2.07H12v4.51h6.6c-.29 1.52-1.14 2.82-2.4 3.68v3.05h3.88c2.27-2.09 3.665-5.17 3.665-9.17z"
        />
        <path
          fill="#34A853"
          d="M12 24c3.24 0 5.95-1.08 7.93-2.91l-3.88-3.05c-1.08.72-2.45 1.16-4.05 1.16-3.12 0-5.77-2.1-6.72-4.93H1.25v3.15C3.26 21.36 7.33 24 12 24z"
        />
        <path
          fill="#FBBC05"
          d="M5.28 14.27c-.25-.72-.38-1.49-.38-2.27s.13-1.55.38-2.27V6.58H1.25C.45 8.18 0 9.98 0 12s.45 3.82 1.25 5.42l4.03-3.15z"
        />
        <path
          fill="#EA4335"
          d="M12 4.75c1.77 0 3.35.61 4.6 1.8l3.42-3.42C17.95 1.19 15.24 0 12 0 7.33 0 3.26 2.64 1.25 6.58l4.03 3.15c.95-2.83 3.6-4.98 6.72-4.98z"
        />
      </svg>
      <span class="btn-text">{{ googleLabel }}</span>
    </button>

    <!-- Apple Button -->
    <button
      type="button"
      class="social-pill-btn"
      @click="$emit('apple')"
      :aria-label="appleLabel"
    >
      <svg class="social-icon" width="17" height="17" viewBox="0 0 24 24" fill="currentColor">
        <path
          d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M15.97 6.37c.62-.75 1.04-1.8 0.92-2.85-.9.04-2 .6-2.65 1.35-.58.66-1.09 1.73-.95 2.76 1.01.08 2.06-.51 2.68-1.26z"
        />
      </svg>
      <span class="btn-text">{{ appleLabel }}</span>
    </button>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    googleLabel?: string
    appleLabel?: string
  }>(),
  {
    googleLabel: 'Sign In with Google',
    appleLabel: 'Sign In with Apple'
  }
)

defineEmits<{
  (e: 'google'): void
  (e: 'apple'): void
}>()
</script>

<style scoped>
.social-auth-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;
  width: 100%;
}

.social-pill-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  height: 42px;
  padding: 0 0.75rem;
  background-color: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 9999px;
  color: #171717;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
  white-space: nowrap;
}

.social-pill-btn:hover {
  background-color: #fafafa;
  border-color: #d4d4d4;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

.social-pill-btn:active {
  transform: translateY(0);
  background-color: #f5f5f5;
}

.social-icon {
  flex-shrink: 0;
}

.btn-text {
  overflow: hidden;
  text-overflow: ellipsis;
  letter-spacing: -0.01em;
}

@media (max-width: 420px) {
  .social-auth-grid {
    grid-template-columns: 1fr;
  }
}
</style>
