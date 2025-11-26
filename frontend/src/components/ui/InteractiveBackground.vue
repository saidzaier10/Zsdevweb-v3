<template>
  <canvas ref="canvasRef" class="absolute inset-0 w-full h-full pointer-events-none"
    :style="{ opacity: opacity }"></canvas>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'
import { isLowEndDevice } from '../../utils/performance'
import { useThemeStore } from '../../stores/theme'

const themeStore = useThemeStore()

// Line color based on theme
const lineColor = computed(() => {
  return themeStore.isDark ? '255, 255, 255' : '30, 41, 59' // White in dark mode, Slate-800 in light mode
})

const props = defineProps({
  opacity: {
    type: Number,
    default: 0.6
  },
  particleCount: {
    type: Number,
    default: 100 // Increased for more density
  },
  connectionDistance: {
    type: Number,
    default: 150
  },
  mouseDistance: {
    type: Number,
    default: 200
  }
})

const canvasRef = ref(null)
let ctx = null
let animationFrameId = null
let particles = []
let mouse = { x: null, y: null }

// Performance optimization variables
let lastTime = 0
const fpsInterval = 1000 / 30 // Limit to 30 FPS
let isPageVisible = true

// Enhanced Color Palette (Reverted to original tech colors)
const colors = [
  '#3b82f6', // Blue
  '#14b8a6', // Teal
  '#8b5cf6'  // Violet
]

// Particle Class
class Particle {
  constructor(canvas) {
    this.canvas = canvas
    this.x = Math.random() * canvas.width
    this.y = Math.random() * canvas.height
    this.vx = (Math.random() - 0.5) * 0.5
    this.vy = (Math.random() - 0.5) * 0.5
    this.size = Math.random() * 3 + 2 // Increased size: 2-5px for better visibility
    this.color = colors[Math.floor(Math.random() * colors.length)]
  }

  update() {
    this.x += this.vx
    this.y += this.vy

    // Bounce off edges
    if (this.x < 0 || this.x > this.canvas.width) this.vx *= -1
    if (this.y < 0 || this.y > this.canvas.height) this.vy *= -1

    // Mouse interaction
    if (mouse.x != null) {
      const dx = mouse.x - this.x
      const dy = mouse.y - this.y
      const distance = Math.sqrt(dx * dx + dy * dy)

      if (distance < props.mouseDistance) {
        const forceDirectionX = dx / distance
        const forceDirectionY = dy / distance
        const force = (props.mouseDistance - distance) / props.mouseDistance

        // Repulsion effect
        const directionX = forceDirectionX * force * 2
        const directionY = forceDirectionY * force * 2

        this.vx -= directionX * 0.05
        this.vy -= directionY * 0.05
      }
    }
  }

  draw() {
    ctx.beginPath()
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
    ctx.fillStyle = this.color
    ctx.globalAlpha = 0.8 // Increased particle opacity
    ctx.fill()
    ctx.globalAlpha = 1.0 // Reset
  }
}

const init = () => {
  const canvas = canvasRef.value
  if (!canvas) return

  canvas.width = canvas.parentElement.clientWidth
  canvas.height = canvas.parentElement.clientHeight
  ctx = canvas.getContext('2d')

  particles = []

  // Adjust particle count based on screen size and device capabilities
  let count = props.particleCount
  if (window.innerWidth < 768) {
    count = Math.floor(count / 2) // Half particles on mobile
  }
  if (isLowEndDevice()) {
    count = Math.floor(count / 2) // Further reduce on low-end devices
  }

  for (let i = 0; i < count; i++) {
    particles.push(new Particle(canvas))
  }
}

const animate = (timestamp) => {
  if (!ctx || !canvasRef.value || !isPageVisible) return

  // FPS Limiting logic
  const elapsed = timestamp - lastTime
  if (elapsed > fpsInterval) {
    lastTime = timestamp - (elapsed % fpsInterval)

    ctx.clearRect(0, 0, canvasRef.value.width, canvasRef.value.height)

    for (let i = 0; i < particles.length; i++) {
      particles[i].update()
      particles[i].draw()

      // Draw connections
      for (let j = i; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x
        const dy = particles[i].y - particles[j].y
        const distance = Math.sqrt(dx * dx + dy * dy)

        if (distance < props.connectionDistance) {
          ctx.beginPath()
          // Increased opacity calculation for higher contrast
          ctx.strokeStyle = `rgba(${lineColor.value}, ${1.5 * (1 - distance / props.connectionDistance)})`
          ctx.lineWidth = 1.5 // Thicker lines (was 0.5)
          ctx.moveTo(particles[i].x, particles[i].y)
          ctx.lineTo(particles[j].x, particles[j].y)
          ctx.stroke()
        }
      }
    }
  }

  animationFrameId = requestAnimationFrame(animate)
}

const handleResize = () => {
  init()
}

const handleMouseMove = (e) => {
  mouse.x = e.clientX
  mouse.y = e.clientY
}

const handleMouseLeave = () => {
  mouse.x = null
  mouse.y = null
}

const handleTouchMove = (e) => {
  mouse.x = e.touches[0].clientX
  mouse.y = e.touches[0].clientY
}

const handleVisibilityChange = () => {
  isPageVisible = !document.hidden
  if (isPageVisible) {
    lastTime = performance.now()
    animate(lastTime)
  } else {
    cancelAnimationFrame(animationFrameId)
  }
}

onMounted(() => {
  init()
  lastTime = performance.now()
  animate(lastTime)

  window.addEventListener('resize', handleResize)
  document.addEventListener('visibilitychange', handleVisibilityChange)

  // Attach event listeners to window for global interaction
  window.addEventListener('mousemove', handleMouseMove)
  window.addEventListener('mouseout', handleMouseLeave)
  window.addEventListener('touchmove', handleTouchMove)
  window.addEventListener('touchend', handleMouseLeave)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('visibilitychange', handleVisibilityChange)

  window.removeEventListener('mousemove', handleMouseMove)
  window.removeEventListener('mouseout', handleMouseLeave)
  window.removeEventListener('touchmove', handleTouchMove)
  window.removeEventListener('touchend', handleMouseLeave)

  cancelAnimationFrame(animationFrameId)
})
</script>
