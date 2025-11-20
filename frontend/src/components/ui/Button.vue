<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
  >
    <!-- Loader -->
    <svg
      v-if="loading"
      class="animate-spin h-4 w-4"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
    </svg>

    <!-- Icône gauche -->
    <slot name="icon-left" />

    <!-- Texte -->
    <span v-if="!loading || loadingText">
      {{ loading && loadingText ? loadingText : label }}
    </span>
    <slot v-if="!label" />

    <!-- Icône droite -->
    <slot name="icon-right" />
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { BUTTON_CLASSES } from '@/utils/constants'

const props = defineProps({
  label: String,
  type: {
    type: String,
    default: 'button',
    validator: (value) => ['button', 'submit', 'reset'].includes(value)
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'success', 'danger', 'warning', 'info', 'outline'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  loadingText: String,
  block: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const buttonClasses = computed(() => {
  return [
    BUTTON_CLASSES.base,
    BUTTON_CLASSES.sizes[props.size],
    BUTTON_CLASSES.variants[props.variant],
    {
      'w-full': props.block,
      'opacity-50 cursor-not-allowed': props.disabled || props.loading
    }
  ]
})

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event)
  }
}
</script>
