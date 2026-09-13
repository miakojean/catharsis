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
            'pr-icon': $slots.append || showPasswordToggle
            }"
            :value="modelValue"
            :disabled="disabled"
            :aria-invalid="!!errorMessage"
            :aria-describedby="errorMessage ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined"
            v-bind="$attrs"
            @input="handleInput"
            @blur="$emit('blur', $event)"
            :placeholder="placeholder"
        />

        <!-- Bouton d'affichage du mot de passe -->
        <button
            v-if="showPasswordToggle"
            type="button"
            class="input-icon input-icon-right toggle-password-btn"
            @click="togglePasswordVisibility"
            title="Afficher/Masquer le mot de passe"
        >
            <svg v-if="isPasswordVisible" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 0 0 1.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.451 10.451 0 0 1 12 4.5c4.756 0 8.773 3.162 10.065 7.498a10.522 10.522 0 0 1-4.293 5.774M6.228 6.228 3 3m3.228 3.228 3.65 3.65m7.894 7.894L21 21m-3.228-3.228-3.65-3.65m0 0a3 3 0 1 0-4.243-4.243m4.242 4.242L9.88 9.88" />
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 0 1 0-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178Z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
            </svg>
        </button>

        <span v-else-if="$slots.append" class="input-icon input-icon-right">
            <slot name="append"></slot>
        </span>
    </div>

    <p v-if="errorMessage" :id="`${inputId}-error`" class="message error-message">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="msg-icon">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      {{ errorMessage }}
    </p>

    <p v-else-if="hint" :id="`${inputId}-hint`" class="message hint-message">
      {{ hint }}
    </p>
  </div>
</template>

<script>
import { useId, computed, ref } from 'vue'

export default {
  name: 'BaseInput',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    errorMessage: {
      type: String,
      default: ''
    },
    hint: {
      type: String,
      default: ''
    },
    id: {
      type: String,
      default: null
    },
    type: {
      type: String,
      default: 'text'
    },
    disabled: {
      type: Boolean,
      default: false
    },
    required: {
      type: Boolean,
      default: false
    },
    placeholder: {
      type: String,
      default: "Entrer votre nom"
    },
    showPasswordToggle: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'blur'],
  setup(props, { emit }) {
    const generatedId = useId();
    const inputId = computed(() => props.id || `input-${generatedId}`);

    const isPasswordVisible = ref(false);

    // Calcule le type d'input dynamiquement
    const computedType = computed(() => {
      if (props.showPasswordToggle) {
        return isPasswordVisible.value ? 'text' : 'password';
      }
      return props.type;
    });

    const togglePasswordVisibility = () => {
      isPasswordVisible.value = !isPasswordVisible.value;
    };

    const handleInput = (event) => {
      emit('update:modelValue', event.target.value);
    };

    return {
      inputId,
      handleInput,
      isPasswordVisible,
      computedType,
      togglePasswordVisibility
    };
  }
};
</script>

<style scoped>
/* Variables CSS pour faciliter la personnalisation */
.input-group {
  --error-color: #ef4444;
  --text-color: #1f2937;
  --label-color: #374151;
  --border-color: #ebebeb;
  --focus-ring: rgba(59, 130, 246, 0.25);
  --bg-disabled: #f3f4f6;

  display: flex;
  flex-direction: column;
  gap: 1rem;
  font-family: sans-serif;
  width: 100%;
  max-width: 400px;

}

.input-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--label-color);
  display: block;
}

.required-mark {
  color: var(--error-color);
  margin-left: 2px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--text-color);
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid var(--border-color);
  outline: none;
  border-radius: 1.5rem;
  transition: border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
}

/* Gestion du focus */
.form-input:focus {
  outline: none;
  /*border-color: var(--primary-color);*/
  box-shadow: 0 0 0 3px var(--focus-ring);
}

input::placeholder {
    color: #C7C5C5;
}

/* Gestion des icônes */
.input-icon {
  position: absolute;
  top: 0;
  bottom: 0;
  margin-right: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  color: #9ca3af;
  pointer-events: none; /* L'icône ne bloque pas le clic */
}

.input-icon-left { left: 0; }
.input-icon-right { right: 0; }

.pl-icon {
  padding-left: 3rem; /* au lieu de 2.5rem */
}
.pr-icon {
  padding-right: 3rem;
}

/* Styles spécifiques pour le bouton de mot de passe */
.toggle-password-btn {
  background: none;
  border: none;
  cursor: pointer;
  pointer-events: auto; /* Remplace le pointer-events: none de .input-icon */
  padding: 0;
  transition: color 0.2s ease;
}

.toggle-password-btn:hover {
  color: var(--primary-color, #156ca9);
}

.toggle-password-btn svg {
  width: 20px;
  height: 20px;
}

/* État d'erreur */
.has-error .form-input {
  border-color: var(--error-color);
}

.has-error .form-input:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.25);
}

.has-error .input-label {
  color: var(--error-color);
}

.has-error .input-icon {
  color: var(--error-color);
}

/* Messages (Erreur et Hint) */
.message {
  font-size: 0.8rem;
  margin-top: 0.375rem;
  display: flex;
  align-items: center;
  gap: 4px;
}

.error-message {
  color: var(--error-color);
}

.hint-message {
  color: #6b7280;
}

.msg-icon {
  width: 14px;
  height: 14px;
}

/* État désactivé */
.is-disabled .form-input {
  background-color: var(--bg-disabled);
  cursor: not-allowed;
  opacity: 1;
}
</style>
