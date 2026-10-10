<template>
  <div class="input-group" :class="{ 'has-error': !!errorMessage, 'is-disabled': disabled }">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>

    <div class="input-wrapper">
      <span v-if="$slots.prepend" class="input-icon input-icon-left">
        <slot name="prepend"></slot>
      </span>

      <input
        :id="inputId"
        ref="inputRef"
        :type="computedType"
        class="form-input"
        :class="{
          'pl-icon': $slots.prepend,
          'pr-icon': $slots.append || showPasswordToggle || type === 'password'
        }"
        :value="modelValue"
        :disabled="disabled"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        :aria-invalid="!!errorMessage"
        :aria-describedby="errorMessage ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined"
        v-bind="$attrs"
        @input="handleInput"
        @blur="$emit('blur', $event)"
        @focus="$emit('focus', $event)"
      />

      <!-- Password visibility toggle button -->
      <button
        v-if="showPasswordToggle || type === 'password'"
        type="button"
        class="input-icon input-icon-right toggle-password-btn"
        @click="togglePasswordVisibility"
        :title="isPasswordVisible ? 'Hide password' : 'Show password'"
        tabindex="-1"
      >
        <!-- Eye open icon -->
        <svg v-if="isPasswordVisible" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.6" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
          <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
        </svg>
        <!-- Eye closed icon -->
        <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.6" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
        </svg>
      </button>

      <span v-else-if="$slots.append" class="input-icon input-icon-right">
        <slot name="append"></slot>
      </span>
    </div>

    <!-- Error message -->
    <p v-if="errorMessage" :id="`${inputId}-error`" class="input-feedback error-message">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="msg-icon">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      <span>{{ errorMessage }}</span>
    </p>

    <!-- Hint message -->
    <p v-else-if="hint" :id="`${inputId}-hint`" class="input-feedback hint-message">
      {{ hint }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, useId } from 'vue'

const props = withDefaults(
  defineProps<{
    modelValue?: string | number
    label?: string
    errorMessage?: string
    hint?: string
    id?: string
    type?: string
    disabled?: boolean
    required?: boolean
    placeholder?: string
    autocomplete?: string
    showPasswordToggle?: boolean
  }>(),
  {
    modelValue: '',
    label: '',
    errorMessage: '',
    hint: '',
    id: '',
    type: 'text',
    disabled: false,
    required: false,
    placeholder: '',
    autocomplete: 'off',
    showPasswordToggle: false
  }
)

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'blur', event: FocusEvent): void
  (e: 'focus', event: FocusEvent): void
}>()

const generatedId = useId()
const inputId = computed(() => props.id || `input-${generatedId}`)
const isPasswordVisible = ref(false)

const computedType = computed(() => {
  if (props.type === 'password' || props.showPasswordToggle) {
    return isPasswordVisible.value ? 'text' : 'password'
  }
  return props.type
})

const togglePasswordVisibility = () => {
  isPasswordVisible.value = !isPasswordVisible.value
}

const handleInput = (event: Event) => {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<style scoped>
.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  width: 100%;
}

.input-label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #374151;
  letter-spacing: -0.01em;
  margin-left: 0.25rem;
}

.required-mark {
  color: #ef4444;
  margin-left: 2px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  width: 100%;
}

.form-input {
  width: 100%;
  height: 44px;
  padding: 0 1.25rem;
  font-size: 0.875rem;
  line-height: 1.5;
  color: #171717;
  background-color: #ffffff;
  border: 1px solid #e5e5e5;
  border-radius: 9999px;
  outline: none;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.02);
}

.form-input::placeholder {
  color: #a3a3a3;
  font-weight: 400;
}

.form-input:hover:not(:disabled) {
  border-color: #d4d4d4;
}

.form-input:focus {
  border-color: #111111;
  box-shadow: 0 0 0 1px #111111;
}

.pl-icon {
  padding-left: 2.75rem;
}

.pr-icon {
  padding-right: 2.75rem;
}

.input-icon {
  position: absolute;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  color: #9ca3af;
  pointer-events: none;
}

.input-icon-left {
  left: 0.25rem;
}

.input-icon-right {
  right: 0.25rem;
}

.toggle-password-btn {
  background: none;
  border: none;
  cursor: pointer;
  pointer-events: auto;
  padding: 0;
  color: #9ca3af;
  transition: color 0.15s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toggle-password-btn:hover {
  color: #171717;
}

.toggle-password-btn svg {
  width: 18px;
  height: 18px;
}

/* Error state */
.has-error .form-input {
  border-color: #ef4444;
}

.has-error .form-input:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 1px #ef4444;
}

.input-feedback {
  font-size: 0.75rem;
  margin-top: 0.25rem;
  margin-left: 0.5rem;
  display: flex;
  align-items: center;
  gap: 4px;
}

.error-message {
  color: #ef4444;
}

.hint-message {
  color: #6b7280;
}

.msg-icon {
  width: 13px;
  height: 13px;
  flex-shrink: 0;
}

/* Disabled */
.is-disabled .form-input {
  background-color: #f5f5f5;
  color: #a3a3a3;
  cursor: not-allowed;
  border-color: #e5e5e5;
}
</style>
