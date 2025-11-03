<template>
  <button
    ref="buttonRef"
    :class="[
      'relative overflow-hidden',
      buttonClasses,
      disabled && 'opacity-50 cursor-not-allowed'
    ]"
    :disabled="disabled || loading"
    @click="handleClick"
  >
    <!-- Ripple effect container -->
    <span
      v-for="(ripple, index) in ripples"
      :key="index"
      class="absolute rounded-full bg-white/30 pointer-events-none animate-ripple"
      :style="{
        left: `${ripple.x}px`,
        top: `${ripple.y}px`,
        width: `${ripple.size}px`,
        height: `${ripple.size}px`,
      }"
    ></span>

    <!-- Loading spinner -->
    <span
      v-if="loading"
      class="inline-flex items-center"
    >
      <svg class="animate-spin -ml-1 mr-3 h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      {{ loadingText }}
    </span>

    <!-- Slot content (normal state) -->
    <span v-else class="relative z-10 inline-flex items-center gap-2">
      <slot></slot>
    </span>
  </button>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'outline', 'ghost'].includes(value)
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
  loadingText: {
    type: String,
    default: 'Chargement...'
  },
  fullWidth: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const buttonRef = ref(null)
const ripples = ref([])

const buttonClasses = computed(() => {
  const classes = []

  // Variant classes
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    outline: 'btn-outline',
    ghost: 'bg-transparent hover:bg-dark-100 dark:hover:bg-dark-800 text-dark-700 dark:text-dark-200 transition-all duration-300'
  }
  classes.push(variants[props.variant])

  // Size classes
  const sizes = {
    sm: 'px-4 py-2 text-sm',
    md: 'px-6 py-3',
    lg: 'px-8 py-4 text-lg'
  }
  if (props.size !== 'md') { // md déjà inclus dans btn-primary/secondary
    classes.push(sizes[props.size])
  }

  // Full width
  if (props.fullWidth) {
    classes.push('w-full')
  }

  return classes.join(' ')
})

const handleClick = (event) => {
  if (props.disabled || props.loading) return

  // Créer un effet ripple
  const button = buttonRef.value
  const rect = button.getBoundingClientRect()
  const size = Math.max(rect.width, rect.height)
  const x = event.clientX - rect.left - size / 2
  const y = event.clientY - rect.top - size / 2

  const ripple = { x, y, size }
  ripples.value.push(ripple)

  // Retirer le ripple après l'animation
  setTimeout(() => {
    ripples.value.shift()
  }, 600)

  emit('click', event)
}
</script>

<style scoped>
@keyframes ripple {
  0% {
    transform: scale(0);
    opacity: 1;
  }
  100% {
    transform: scale(4);
    opacity: 0;
  }
}

.animate-ripple {
  animation: ripple 600ms linear;
}
</style>
