<template>
  <div class="marquee-container" :style="containerStyle">
    <div 
      class="marquee-content"
      :class="{ 'paused': isPaused }"
      :style="marqueeStyle"
      @mouseenter="pauseOnHover && (isPaused = true)"
      @mouseleave="pauseOnHover && (isPaused = false)"
    >
      <!-- Original content -->
      <div class="marquee-items">
        <slot></slot>
      </div>
      
      <!-- Duplicated content for seamless loop -->
      <div class="marquee-items" aria-hidden="true">
        <slot></slot>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

/**
 * InfiniteMarquee Component
 * Infinite scrolling marquee with auto-duplication and pause on hover
 * 
 * @prop {Number} duration - Animation duration in seconds
 * @prop {Boolean} reverse - Reverse scroll direction
 * @prop {Boolean} pauseOnHover - Pause animation on hover
 * @prop {String} gap - Gap between items (Tailwind class or CSS value)
 */
const props = defineProps({
  duration: {
    type: Number,
    default: 30
  },
  reverse: {
    type: Boolean,
    default: false
  },
  pauseOnHover: {
    type: Boolean,
    default: true
  },
  gap: {
    type: String,
    default: '2rem'
  }
})

const isPaused = ref(false)

const containerStyle = computed(() => ({
  '--marquee-gap': props.gap
}))

const marqueeStyle = computed(() => ({
  animationDuration: `${props.duration}s`,
  animationDirection: props.reverse ? 'reverse' : 'normal'
}))
</script>

<style scoped>
.marquee-container {
  overflow: hidden;
  position: relative;
  width: 100%;
  mask-image: linear-gradient(
    to right,
    transparent 0%,
    black 10%,
    black 90%,
    transparent 100%
  );
  -webkit-mask-image: linear-gradient(
    to right,
    transparent 0%,
    black 10%,
    black 90%,
    transparent 100%
  );
}

.marquee-content {
  display: flex;
  animation: marquee linear infinite;
  will-change: transform;
}

.marquee-content.paused {
  animation-play-state: paused;
}

.marquee-items {
  display: flex;
  gap: var(--marquee-gap, 2rem);
  align-items: center;
  flex-shrink: 0;
  min-width: 100%;
  padding-right: var(--marquee-gap, 2rem);
}

@keyframes marquee {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

/* GPU Acceleration */
.marquee-content {
  transform: translateZ(0);
  backface-visibility: hidden;
  perspective: 1000px;
}
</style>
