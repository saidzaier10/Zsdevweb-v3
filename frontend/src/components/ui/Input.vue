<template>
  <div class="w-full">
    <!-- Label -->
    <label v-if="label" :for="inputId" :class="labelClasses">
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>

    <!-- Input Container -->
    <div class="relative" :class="{ 'mt-2': label }">
      <!-- Icône gauche -->
      <div v-if="$slots['icon-left']" class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <slot name="icon-left" />
      </div>

      <!-- Input -->
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :min="min"
        :max="max"
        :step="step"
        :class="inputClasses"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
      />

      <!-- Icône droite -->
      <div v-if="$slots['icon-right']" class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
        <slot name="icon-right" />
      </div>
    </div>

    <!-- Message d'aide ou d'erreur -->
    <p v-if="error" class="mt-1 text-sm text-red-600 dark:text-red-400">
      {{ error }}
    </p>
    <p v-else-if="hint" class="mt-1 text-sm text-dark-500 dark:text-dark-400">
      {{ hint }}
    </p>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { INPUT_CLASSES } from '@/utils/constants'

const props = defineProps({
  modelValue: [String, Number],
  type: {
    type: String,
    default: 'text'
  },
  label: String,
  placeholder: String,
  error: String,
  hint: String,
  disabled: Boolean,
  readonly: Boolean,
  required: Boolean,
  min: [String, Number],
  max: [String, Number],
  step: [String, Number]
})

const emit = defineEmits(['update:modelValue', 'blur', 'focus'])

const inputId = ref(`input-${Math.random().toString(36).substr(2, 9)}`)
const isFocused = ref(false)

const labelClasses = computed(() => {
  return 'block text-sm font-medium text-dark-700 dark:text-dark-300'
})

const inputClasses = computed(() => {
  const baseClasses = INPUT_CLASSES.base
  let stateClasses = INPUT_CLASSES.states.default

  if (props.error) {
    stateClasses = INPUT_CLASSES.states.error
  } else if (props.disabled) {
    stateClasses = INPUT_CLASSES.states.disabled
  }

  const paddingClasses = []
  if (props.$slots['icon-left']) paddingClasses.push('pl-10')
  if (props.$slots['icon-right']) paddingClasses.push('pr-10')

  return [baseClasses, stateClasses, ...paddingClasses]
})

const handleInput = (event) => {
  emit('update:modelValue', event.target.value)
}

const handleBlur = (event) => {
  isFocused.value = false
  emit('blur', event)
}

const handleFocus = (event) => {
  isFocused.value = true
  emit('focus', event)
}
</script>
