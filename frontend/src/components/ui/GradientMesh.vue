<template>
  <div class="gradient-mesh-container" :class="{ 'animate': animated }">
    <div 
      v-for="(blob, index) in blobs" 
      :key="index"
      class="gradient-blob"
      :class="`blob-${index + 1}`"
      :style="getBlobStyle(blob, index)"
    ></div>
    
    <!-- Optional overlay for better text readability -->
    <div v-if="overlay" class="gradient-overlay" :style="overlayStyle"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

/**
 * GradientMesh Component
 * Animated gradient mesh background with customizable blobs
 * 
 * @prop {Array} colors - Array of gradient colors (default: primary/secondary)
 * @prop {Number} blobCount - Number of gradient blobs (2-5)
 * @prop {Boolean} animated - Enable blob animation
 * @prop {Number} speed - Animation speed multiplier (0.5-2)
 * @prop {Boolean} overlay - Add dark overlay for text readability
 * @prop {Number} overlayOpacity - Overlay opacity (0-1)
 */
const props = defineProps({
  colors: {
    type: Array,
    default: () => ['#3b82f6', '#14b8a6', '#8b5cf6']
  },
  blobCount: {
    type: Number,
    default: 3,
    validator: (value) => value >= 2 && value <= 5
  },
  animated: {
    type: Boolean,
    default: true
  },
  speed: {
    type: Number,
    default: 1,
    validator: (value) => value >= 0.5 && value <= 2
  },
  overlay: {
    type: Boolean,
    default: true
  },
  overlayOpacity: {
    type: Number,
    default: 0.4,
    validator: (value) => value >= 0 && value <= 1
  }
})

const blobs = computed(() => {
  const positions = [
    { top: '-10%', left: '-10%', size: '40%' },
    { top: '-20%', right: '-10%', size: '50%' },
    { bottom: '-15%', left: '10%', size: '45%' },
    { bottom: '-10%', right: '-5%', size: '35%' },
    { top: '30%', left: '40%', size: '30%' }
  ]
  
  return positions.slice(0, props.blobCount).map((pos, index) => ({
    ...pos,
    color: props.colors[index % props.colors.length]
  }))
})

const getBlobStyle = (blob, index) => {
  const baseDelay = index * 1.5
  const duration = 7 / props.speed
  
  return {
    top: blob.top,
    left: blob.left,
    right: blob.right,
    bottom: blob.bottom,
    width: blob.size,
    height: blob.size,
    background: `radial-gradient(circle, ${blob.color} 0%, transparent 70%)`,
    animationDuration: `${duration}s`,
    animationDelay: `${baseDelay}s`
  }
}

const overlayStyle = computed(() => ({
  background: `linear-gradient(135deg, 
    rgba(15, 23, 42, ${props.overlayOpacity}) 0%, 
    rgba(30, 41, 59, ${props.overlayOpacity * 0.8}) 100%
  )`
}))
</script>

<style scoped>
.gradient-mesh-container {
  position: absolute;
  inset: 0;
  overflow: hidden;
  z-index: 0;
}

.gradient-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  opacity: 0.6;
  mix-blend-mode: screen;
  will-change: transform;
}

.animate .gradient-blob {
  animation: blob infinite ease-in-out;
}

.blob-1 {
  animation-delay: 0s;
}

.blob-2 {
  animation-delay: 1.5s;
}

.blob-3 {
  animation-delay: 3s;
}

.blob-4 {
  animation-delay: 4.5s;
}

.blob-5 {
  animation-delay: 6s;
}

@keyframes blob {
  0%, 100% {
    transform: translate(0px, 0px) scale(1) rotate(0deg);
  }
  25% {
    transform: translate(30px, -50px) scale(1.1) rotate(90deg);
  }
  50% {
    transform: translate(-20px, 30px) scale(0.9) rotate(180deg);
  }
  75% {
    transform: translate(40px, 20px) scale(1.05) rotate(270deg);
  }
}

.gradient-overlay {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}

/* Dark mode adjustments */
.dark .gradient-blob {
  opacity: 0.4;
}

.dark .gradient-overlay {
  background: linear-gradient(135deg, 
    rgba(15, 23, 42, 0.6) 0%, 
    rgba(30, 41, 59, 0.5) 100%
  ) !important;
}

/* GPU Acceleration */
.gradient-blob {
  transform: translateZ(0);
  backface-visibility: hidden;
}
</style>
