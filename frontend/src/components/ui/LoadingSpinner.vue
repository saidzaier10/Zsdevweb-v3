<template>
  <div :class="containerClasses">
    <div :class="spinnerClasses"></div>
    <p v-if="message" :class="messageClasses">{{ message }}</p>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['xs', 'sm', 'md', 'lg', 'xl'].includes(value)
  },
  message: String,
  centered: {
    type: Boolean,
    default: true
  },
  fullScreen: {
    type: Boolean,
    default: false
  },
  color: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'white', 'dark'].includes(value)
  }
})

const containerClasses = computed(() => {
  return [
    props.centered && !props.fullScreen ? 'text-center py-12' : '',
    props.fullScreen ? 'fixed inset-0 flex items-center justify-center bg-white/80 dark:bg-dark-900/80 z-50' : ''
  ]
})

const spinnerClasses = computed(() => {
  const sizes = {
    xs: 'h-4 w-4',
    sm: 'h-8 w-8',
    md: 'h-12 w-12',
    lg: 'h-16 w-16',
    xl: 'h-24 w-24'
  }

  const colors = {
    primary: 'border-primary-600',
    white: 'border-white',
    dark: 'border-dark-800'
  }

  return [
    'inline-block animate-spin rounded-full border-b-2',
    sizes[props.size],
    colors[props.color]
  ]
})

const messageClasses = computed(() => {
  return 'mt-4 text-dark-600 dark:text-dark-300 font-medium'
})
</script>
