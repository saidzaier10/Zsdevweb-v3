/**
 * Animation Composable
 * Provides reusable animation utilities with Intersection Observer for performance
 */

import { ref, onMounted, onUnmounted, watch } from 'vue'

/**
 * Observe element visibility and trigger animations
 * @param {Object} options - Intersection Observer options
 * @returns {Object} - Reactive refs and observer methods
 */
export function useIntersectionObserver(options = {}) {
    const isVisible = ref(false)
    const target = ref(null)
    let observer = null

    const defaultOptions = {
        threshold: 0.1,
        rootMargin: '0px',
        ...options
    }

    onMounted(() => {
        if (!target.value) return

        observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                isVisible.value = entry.isIntersecting
            })
        }, defaultOptions)

        observer.observe(target.value)
    })

    onUnmounted(() => {
        if (observer && target.value) {
            observer.unobserve(target.value)
        }
    })

    return {
        target,
        isVisible
    }
}

/**
 * Staggered animation for lists
 * @param {Number} itemCount - Number of items to animate
 * @param {Number} delay - Delay between each item (ms)
 * @returns {Function} - Get delay for specific index
 */
export function useStaggerAnimation(itemCount, delay = 100) {
    const getDelay = (index) => {
        return `${index * delay}ms`
    }

    const getStyle = (index) => {
        return {
            animationDelay: getDelay(index)
        }
    }

    return {
        getDelay,
        getStyle
    }
}

/**
 * Parallax scroll effect
 * @param {Number} speed - Parallax speed multiplier (0-1)
 * @returns {Object} - Transform style
 */
export function useParallax(speed = 0.5) {
    const transform = ref('translateY(0px)')

    const handleScroll = () => {
        const scrolled = window.scrollY
        transform.value = `translateY(${scrolled * speed}px)`
    }

    onMounted(() => {
        window.addEventListener('scroll', handleScroll, { passive: true })
    })

    onUnmounted(() => {
        window.removeEventListener('scroll', handleScroll)
    })

    return {
        transform
    }
}

/**
 * Mouse move effect (for interactive cards)
 * @returns {Object} - Mouse position and transform
 */
export function useMouseMove() {
    const mouseX = ref(0)
    const mouseY = ref(0)
    const transform = ref('')

    const handleMouseMove = (event) => {
        const rect = event.currentTarget.getBoundingClientRect()
        const x = event.clientX - rect.left
        const y = event.clientY - rect.top

        const centerX = rect.width / 2
        const centerY = rect.height / 2

        const rotateX = ((y - centerY) / centerY) * 10
        const rotateY = ((centerX - x) / centerX) * 10

        transform.value = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.05, 1.05, 1.05)`
    }

    const handleMouseLeave = () => {
        transform.value = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)'
    }

    return {
        mouseX,
        mouseY,
        transform,
        handleMouseMove,
        handleMouseLeave
    }
}

/**
 * Scroll-triggered counter animation
 * @param {Number} target - Target number
 * @param {Number} duration - Animation duration (ms)
 * @returns {Object} - Current count and start function
 */
export function useCountUp(targetSource, duration = 2000) {
    const count = ref(0)
    const { target: elementRef, isVisible } = useIntersectionObserver({ threshold: 0.5 })
    let hasAnimated = false

    // Helper to get value whether it's a ref or primitive
    const getTargetValue = () => {
        return typeof targetSource === 'object' && targetSource.value !== undefined
            ? targetSource.value
            : targetSource
    }

    const animate = () => {
        const target = getTargetValue()
        if (!target) return // Don't animate to 0 or null

        const startTime = Date.now()
        const startValue = count.value // Start from current value (useful if target updates)

        const updateCount = () => {
            const now = Date.now()
            const progress = Math.min((now - startTime) / duration, 1)

            // Easing function (ease-out)
            const easeOut = 1 - Math.pow(1 - progress, 3)
            count.value = Math.floor(startValue + (target - startValue) * easeOut)

            if (progress < 1) {
                requestAnimationFrame(updateCount)
            } else {
                count.value = target
                hasAnimated = true
            }
        }

        requestAnimationFrame(updateCount)
    }

    // Watch for visibility and target changes
    // If visible and target changes (e.g. API load), animate to new target
    watch([isVisible, () => getTargetValue()], ([visible, newTarget]) => {
        if (visible && newTarget > 0) {
            animate()
        }
    })

    return {
        count,
        elementRef
    }
}
