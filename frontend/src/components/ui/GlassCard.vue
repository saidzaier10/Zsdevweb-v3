<template>
  <div 
    :class="[
      'glass-card-component',
      variantClass,
      { 'glass-hover': hover, 'cursor-pointer': clickable }
    ]"
    :style="customStyle"
    @click="handleClick"
  >
    <slot></slot>
  </div>
</template>

<script setup>
import { computed } from 'vue'

/**
 * GlassCard Component
 * Modern glassmorphism card with customizable variants
 * 
 * @prop {String} variant - Card variant: 'light', 'strong', 'primary', 'secondary'
 * @prop {Boolean} hover - Enable hover effect
 * @prop {Boolean} clickable - Show pointer cursor
 * @prop {String} borderRadius - Custom border radius (e.g., 'lg', 'xl', '2xl')
 * @prop {Number} blur - Custom blur amount (px)
 */
const props = defineProps({
  variant: {
    type: String,
    default: 'light',
    validator: (value) => ['light', 'strong', 'primary', 'secondary'].includes(value)
  },
  hover: {
    type: Boolean,
    default: true
  },
  clickable: {
    type: Boolean,
    default: false
  },
  borderRadius: {
    type: String,
    default: 'xl'
  },
  blur: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['click'])

const variantClass = computed(() => {
  const variants = {
    light: 'glass',
    strong: 'glass-strong',
    primary: 'glass-primary',
    secondary: 'glass-secondary'
  }
  return variants[props.variant] || variants.light
})

const customStyle = computed(() => {
  const styles = {}
  
  if (props.borderRadius) {
    const radiusMap = {
      'sm': '0.375rem',
      'md': '0.5rem',
      'lg': '0.75rem',
      'xl': '1rem',
      '2xl': '1.5rem',
      'full': '9999px'
    }
    styles.borderRadius = radiusMap[props.borderRadius] || props.borderRadius
  }
  
  if (props.blur) {
    styles.backdropFilter = `blur(${props.blur}px)`
    styles.webkitBackdropFilter = `blur(${props.blur}px)`
  }
  
  return styles
})

const handleClick = (event) => {
  if (props.clickable) {
    emit('click', event)
  }
}
</script>

<style scoped>
.glass-card-component {
  position: relative;
  padding: 1.5rem;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.glass-primary {
  background: rgba(37, 99, 235, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(37, 99, 235, 0.2);
  box-shadow: 0 8px 32px 0 rgba(37, 99, 235, 0.15);
}

.glass-secondary {
  background: rgba(20, 184, 166, 0.1);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(20, 184, 166, 0.2);
  box-shadow: 0 8px 32px 0 rgba(20, 184, 166, 0.15);
}

.dark .glass-primary {
  background: rgba(37, 99, 235, 0.15);
  border-color: rgba(37, 99, 235, 0.3);
}

.dark .glass-secondary {
  background: rgba(20, 184, 166, 0.15);
  border-color: rgba(20, 184, 166, 0.3);
}

/* GPU Acceleration */
.glass-card-component {
  transform: translateZ(0);
  will-change: transform;
}
</style>
