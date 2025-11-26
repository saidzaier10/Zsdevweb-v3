<template>
  <button
    ref="btnRef"
    :class="[
      'modern-button',
      variantClass,
      sizeClass,
      { 'w-full': fullWidth, 'is-loading': loading, 'is-disabled': disabled }
    ]"
    :disabled="disabled || loading"
    @mousemove="handleMouseMove"
    @mouseleave="handleMouseLeave"
    @click="handleClick"
  >
    <!-- Glow Effect Background -->
    <div 
      v-if="glow" 
      class="glow-effect"
      :style="glowStyle"
    ></div>

    <!-- Content -->
    <span class="relative z-10 flex items-center justify-center gap-2">
      <svg v-if="loading" class="animate-spin h-5 w-5" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <slot v-else></slot>
    </span>
  </button>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (val) => ['primary', 'secondary', 'outline', 'ghost', 'glass'].includes(val)
  },
  size: {
    type: String,
    default: 'md',
    validator: (val) => ['sm', 'md', 'lg'].includes(val)
  },
  glow: {
    type: Boolean,
    default: true
  },
  fullWidth: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['click'])

const btnRef = ref(null)
const mouseX = ref(0)
const mouseY = ref(0)

const variantClass = computed(() => {
  const variants = {
    primary: 'btn-primary',
    secondary: 'btn-secondary',
    outline: 'btn-outline',
    ghost: 'btn-ghost',
    glass: 'btn-glass'
  }
  return variants[props.variant]
})

const sizeClass = computed(() => {
  const sizes = {
    sm: 'text-sm px-4 py-2',
    md: 'text-base px-6 py-3',
    lg: 'text-lg px-8 py-4'
  }
  return sizes[props.size]
})

const glowStyle = computed(() => ({
  background: `radial-gradient(circle at ${mouseX.value}px ${mouseY.value}px, rgba(255,255,255,0.2) 0%, transparent 50%)`
}))

const handleMouseMove = (e) => {
  if (!btnRef.value || props.disabled) return
  const rect = btnRef.value.getBoundingClientRect()
  mouseX.value = e.clientX - rect.left
  mouseY.value = e.clientY - rect.top
}

const handleMouseLeave = () => {
  mouseX.value = -100
  mouseY.value = -100
}

const handleClick = (e) => {
  if (!props.disabled && !props.loading) {
    emit('click', e)
  }
}
</script>

<style scoped>
.modern-button {
  position: relative;
  overflow: hidden;
  border-radius: 0.75rem;
  font-weight: 600;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  transform: translateZ(0); /* GPU accel */
}

.modern-button:active {
  transform: scale(0.98);
}

.glow-effect {
  position: absolute;
  inset: 0;
  pointer-events: none;
  transition: opacity 0.3s;
}

/* Variants */
.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-primary:hover {
  box-shadow: 0 8px 20px rgba(37, 99, 235, 0.4);
  transform: translateY(-1px);
}

.btn-secondary {
  background: white;
  color: #3b82f6;
  border: 2px solid #3b82f6;
}

.dark .btn-secondary {
  background: #1e293b;
  border-color: #3b82f6;
  color: #60a5fa;
}

.btn-outline {
  background: transparent;
  border: 2px solid #e2e8f0;
  color: #64748b;
}

.dark .btn-outline {
  border-color: #334155;
  color: #94a3b8;
}

.btn-outline:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.btn-ghost {
  background: transparent;
  color: #64748b;
}

.btn-ghost:hover {
  background: rgba(0,0,0,0.05);
  color: #3b82f6;
}

.dark .btn-ghost:hover {
  background: rgba(255,255,255,0.05);
}

.btn-glass {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
}

.btn-glass:hover {
  background: rgba(255, 255, 255, 0.2);
}

.is-disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none !important;
}
</style>
