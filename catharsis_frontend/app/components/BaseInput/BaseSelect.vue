<template>
  <div class="input__family">
    <label :for="label">{{ label }}</label>
    <select 
      :id="label"
      :value="modelValue"
      @change="onChange"
      :class="{ 'error': error }"
    >
      <option value="" disabled>-- Sélectionner --</option>
      <option 
        v-for="(item, index) in options" 
        :key="index" 
        :value="item.value"
      >
        {{ item.label }}
      </option>
    </select>
    <span v-if="error" class="error-message">{{ error }}</span>
  </div>
</template>

<script>
import { watch } from 'vue';

export default {
  name:'selectfamily',
  props: {
    label: {
      type: String,
      default: "Selectionner date"
    },
    options: {
      type: Array,
      default: () => []
    },
    modelValue: {
      type: String,
      default: ''
    },
    error: {
      type: String,
      default: ''
    }
  },
  emits: ['update:modelValue'],
  setup(props, { emit }) {
    const onChange = (event) => {
      const value = event.target.value;
      emit('update:modelValue', value);
    };

    // Optionnel: sync depuis le parent
    watch(() => props.modelValue, (newVal) => {
      // La valeur est déjà gérée par :value
    });

    return {
      onChange
    };
  }
}
</script>
    
  <style scoped>
  .input__family {
    display: flex;
    flex-direction: column;
    justify-content: start;
    gap: 0.5rem; 
    width: 100%;
    max-width: 600px;
  }

  label {
    font-size: 0.9rem;
    font-weight: 500;
    color: #535353;
  }

  select {
    padding: 0.9rem;
    border: 1px solid #ccc;
    border-radius: 0.6rem;
    font-size: 0.9rem;
    width: 100%;
    box-sizing: border-box;
    transition: ease-in-out 0.3s;
    outline: none;
  }

  select:focus {
    border-color: #2563eb;
  }

  select.error {
    border-color: #dc2626;
    background-color: #fef2f2;
  }

  option {
    font-size: 0.9rem;
  }

  .error-message {
    color: #dc2626;
    font-size: 0.8rem;
    font-weight: 500;
    margin-top: 0.25rem;
  }
</style>