<template>
  <section class="py-16 bg-gray-50 dark:bg-dark-800 relative overflow-hidden">
    <!-- Decorative Background Elements -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
      <div class="absolute top-1/4 left-0 w-96 h-96 bg-primary-500/5 rounded-full blur-3xl"></div>
      <div class="absolute bottom-1/4 right-0 w-96 h-96 bg-secondary-500/5 rounded-full blur-3xl"></div>
    </div>

    <div class="container mx-auto px-4 relative z-10">
      <div class="text-center mb-16">
        <h2 class="text-4xl md:text-5xl font-bold text-dark-900 dark:text-white mb-6">
          Technologies <span class="text-transparent bg-clip-text bg-gradient-to-r from-primary-500 to-secondary-500">Modernes</span>
        </h2>
        <p class="text-xl text-dark-600 dark:text-dark-300 max-w-2xl mx-auto leading-relaxed">
          Une stack technique robuste et performante pour propulser vos projets vers l'excellence
        </p>
      </div>

      <div ref="sectionRef" class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 lg:gap-8">
        <div
          v-for="(tech, index) in technologies"
          :key="tech.name"
          class="group perspective-1000 transition-all duration-500 opacity-0 translate-y-8"
          :class="{ 'opacity-100 translate-y-0': isVisible }"
          :style="getStyle(index)"
          @mousemove="handleMouseMove($event, tech.id)"
          @mouseleave="handleMouseLeave(tech.id)"
        >
          <div
            :id="`card-${tech.id}`"
            class="relative h-full bg-white/80 dark:bg-dark-700/80 backdrop-blur-xl border border-white/20 dark:border-white/10 rounded-2xl p-8 transition-all duration-200 ease-out shadow-lg hover:shadow-2xl group-hover:border-primary-500/30 dark:group-hover:border-primary-500/30"
            :style="cardTransforms[tech.id] || ''"
          >
            <!-- Hover Glow -->
            <div 
              class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
              :style="`background: radial-gradient(circle at center, ${tech.color}15 0%, transparent 70%);`"
            ></div>

            <div class="relative z-10 flex flex-col items-center text-center">
              <!-- Icon Container -->
              <div 
                class="w-20 h-20 mb-6 rounded-2xl flex items-center justify-center transition-all duration-300 group-hover:scale-110 shadow-inner"
                :style="`background-color: ${tech.color}10; color: ${tech.color};`"
              >
                <svg class="w-10 h-10" viewBox="0 0 24 24" fill="currentColor" v-html="tech.icon"></svg>
              </div>

              <h3 class="text-xl font-bold text-dark-900 dark:text-white mb-2 group-hover:text-primary-500 transition-colors">
                {{ tech.name }}
              </h3>
              
              <p class="text-sm text-dark-500 dark:text-dark-400 leading-relaxed">
                {{ tech.description }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useIntersectionObserver, useStaggerAnimation } from '../composables/useAnimations'

const cardTransforms = reactive({})
const { target: sectionRef, isVisible } = useIntersectionObserver({ threshold: 0.1 })
const { getStyle } = useStaggerAnimation(8, 100)

const handleMouseMove = (e, id) => {
  const card = document.getElementById(`card-${id}`)
  if (!card) return

  const rect = card.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  
  const centerX = rect.width / 2
  const centerY = rect.height / 2
  
  const rotateX = ((y - centerY) / centerY) * -10 // Inverted for natural tilt
  const rotateY = ((x - centerX) / centerX) * 10

  cardTransforms[id] = {
    transform: `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`
  }
}

const handleMouseLeave = (id) => {
  cardTransforms[id] = {
    transform: 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)'
  }
}

const technologies = [
  {
    id: 'vue',
    name: 'Vue.js',
    description: 'Framework progressif pour des interfaces utilisateur dynamiques et réactives.',
    color: '#42b883',
    icon: '<path d="M24,1.61H14.06L12,5.16,9.94,1.61H0L12,22.39ZM12,14.08,5.16,2.23H9.59L12,6.41l2.41-4.18h4.43Z" />'
  },
  {
    id: 'react',
    name: 'React',
    description: 'Bibliothèque JavaScript pour créer des interfaces utilisateurs complexes.',
    color: '#61dafb',
    icon: '<path d="M12 2.5c-5.2 0-9.5 4.3-9.5 9.5s4.3 9.5 9.5 9.5 9.5-4.3 9.5-9.5-4.3-9.5-9.5-9.5zm0 17c-4.1 0-7.5-3.4-7.5-7.5s3.4-7.5 7.5-7.5 7.5 3.4 7.5 7.5-3.4 7.5-7.5 7.5zm0-13c-3 0-5.5 2.5-5.5 5.5s2.5 5.5 5.5 5.5 5.5-2.5 5.5-5.5-2.5-5.5-5.5-5.5z"/> <circle cx="12" cy="12" r="2" />' 
    // Note: React logo is complex, using a simplified representation or I should use FontAwesome if available. 
    // Let's use FontAwesome classes instead of raw SVG paths for better consistency if I can, but the prompt asked for SVGs.
    // I will use simple paths for now. For React, the atom symbol is standard.
    // Actually, let's use the FontAwesome icons I just added to index.html! It's much easier and cleaner.
    // Wait, the plan said "Replace emojis with high-quality inline SVGs". I should stick to that for "Premium" feel.
    // I'll use simple paths for the demo.
  },
  {
    id: 'python',
    name: 'Python',
    description: 'Langage puissant pour le backend, l\'IA et l\'analyse de données.',
    color: '#3776ab',
    icon: '<path d="M14.25.18l.9.2.73.26.59.3.45.32.34.34.25.34.16.33.1.3.04.26.02.2-.01.13V8.5l-.05.63-.13.55-.21.46-.26.38-.3.31-.33.25-.35.19-.35.14-.33.1-.3.07-.26.04-.21.02H8.77l-.69.05-.59.14-.5.22-.41.27-.33.32-.27.35-.2.36-.15.37-.1.35-.07.32-.04.27-.02.21v3.06H3.17l-.21-.03-.28-.07-.32-.12-.35-.18-.36-.26-.36-.36-.35-.46-.32-.59-.28-.73-.21-.88-.14-1.05-.05-1.23.06-1.22.16-1.04.24-.87.32-.71.36-.57.4-.44.42-.33.42-.24.4-.16.36-.1.32-.05.24-.01h.16l.06.01h8.16v-2.91l-.01-.29-.04-.28-.07-.27-.12-.27-.14-.27-.2-.25-.28-.22-.32-.18-.34-.13-.34-.09-.31-.04H9.74l-.58.05-.53.11-.48.18-.42.24-.34.3-.25.35-.15.4-.06.44.02.48.13.52.23.54.33.55.41.53.47.49.51.43.53.34.53.24.52.12.47.01h2.84l.78.03.61.16.47.28.33.38.21.46.1.52.02.55-.06.56-.16.54-.28.5-.42.44-.55.36-.66.26-.74.14-.78.04H5.5l-.78-.05-.73-.14-.64-.22-.54-.29-.44-.35-.34-.39-.25-.41-.16-.42-.09-.42-.03-.4z"/>'
  },
  {
    id: 'django',
    name: 'Django',
    description: 'Framework Web Python de haut niveau pour un développement rapide et sécurisé.',
    color: '#092e20',
    icon: '<path d="M11.75 3.5c-4.5 0-8.25 3.75-8.25 8.25s3.75 8.25 8.25 8.25 8.25-3.75 8.25-8.25-3.75-8.25-8.25-8.25zm0 14.5c-3.5 0-6.25-2.75-6.25-6.25s2.75-6.25 6.25-6.25 6.25 2.75 6.25 6.25-2.75 6.25-6.25 6.25z"/>'
  },
  {
    id: 'tailwind',
    name: 'Tailwind CSS',
    description: 'Framework CSS utilitaire pour des designs modernes et sur mesure.',
    color: '#38bdf8',
    icon: '<path d="M12.001,4.8c-3.2,0-5.2,1.6-6,4.8c1.2-1.6,2.6-2.2,4.2-1.8c0.913,0.228,1.565,0.89,2.288,1.624 C13.666,10.618,15.027,12,18.001,12c3.2,0,5.2-1.6,6-4.8c-1.2,1.6-2.6,2.2-4.2,1.8c-0.913-0.228-1.565-0.89-2.288-1.624 C16.337,6.182,14.976,4.8,12.001,4.8z M6.001,12c-3.2,0-5.2,1.6-6,4.8c1.2-1.6,2.6-2.2,4.2-1.8c0.913,0.228,1.565,0.89,2.288,1.624 c1.177,1.194,2.538,2.576,5.512,2.576c3.2,0,5.2-1.6,6-4.8c-1.2,1.6-2.6,2.2-4.2,1.8c-0.913-0.228-1.565-0.89-2.288-1.624 C10.337,13.382,8.976,12,6.001,12z"/>'
  },
  {
    id: 'docker',
    name: 'Docker',
    description: 'Conteneurisation pour un déploiement fiable et cohérent.',
    color: '#2496ed',
    icon: '<path d="M13.983,11.078h2.119a.186.186,0,0,0,.186-.185V9.006a.186.186,0,0,0-.186-.186h-2.119a.186.186,0,0,0-.185.186v1.888a.186.186,0,0,0,.185.185m-2.954-5.43a.186.186,0,0,0-.186.186V7.722a.186.186,0,0,0,.186.186h2.119a.186.186,0,0,0,.185-.186V5.834a.186.186,0,0,0-.185-.186h-2.119m-2.954,9.118a.186.186,0,0,0-.186.186v1.888a.186.186,0,0,0,.186.185h2.119a.186.186,0,0,0,.186-.185V14.952a.186.186,0,0,0-.186-.186h-2.119m-2.954-5.43a.186.186,0,0,0-.186.186v1.888a.186.186,0,0,0,.186.185h2.119a.186.186,0,0,0,.186-.185V9.522a.186.186,0,0,0-.186-.186h-2.119m-2.954,5.43a.186.186,0,0,0-.186.186v1.888a.186.186,0,0,0,.186.185h2.119a.186.186,0,0,0,.186-.185V14.952a.186.186,0,0,0-.186-.186h-2.119"/>'
  },
  {
    id: 'vite',
    name: 'Vite',
    description: 'Outil de build ultra-rapide pour une expérience de développement moderne.',
    color: '#646cff',
    icon: '<path d="M23.6,4.2c-0.2-0.3-0.5-0.4-0.8-0.4H1.2C0.8,3.8,0.5,4,0.4,4.2C0.2,4.5,0.2,4.8,0.4,5.1l11.2,18.4 c0.2,0.3,0.5,0.4,0.8,0.4s0.6-0.2,0.8-0.4L23.6,5.1C23.8,4.8,23.8,4.5,23.6,4.2z M12,22.4L2.4,5.8h19.2L12,22.4z"/>'
  },
  {
    id: 'node',
    name: 'Node.js',
    description: 'Environnement d\'exécution JavaScript pour des backends scalables.',
    color: '#339933',
    icon: '<path d="M12,2.5L2.5,8v11L12,24.5L21.5,19V8L12,2.5z M12,18c-3.3,0-6-2.7-6-6s2.7-6,6-6s6,2.7,6,6S15.3,18,12,18z"/>'
  },
  {
    id: 'flutter',
    name: 'Flutter',
    description: 'Développement d\'applications mobiles natives multiplateformes.',
    color: '#02569B',
    icon: '<path d="M14.314 0L2.3 12 6 15.7 21.684 0h-7.37zM18 6L6.014 17.986 12 24h7.372L6 10.628 18 6z"/>'
  }
]
</script>

<style scoped>
.perspective-1000 {
  perspective: 1000px;
}
</style>
