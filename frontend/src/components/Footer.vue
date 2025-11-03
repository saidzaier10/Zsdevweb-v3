<template>
  <footer class="bg-dark-900 dark:bg-dark-950 text-white py-12 border-t border-dark-800 dark:border-dark-900">
    <div class="container mx-auto px-4">
      <div class="grid md:grid-cols-4 gap-8">
        <!-- À propos -->
        <div>
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-10 h-10 bg-gradient-to-br from-primary-600 to-secondary-500 rounded-lg flex items-center justify-center">
              <span class="text-white font-bold text-xl">Z</span>
            </div>
            <span class="text-xl font-display font-bold">Zsdevweb</span>
          </div>
          <p class="text-dark-300 dark:text-dark-400 text-sm leading-relaxed">
            Solutions web innovantes et sur mesure pour donner vie à vos projets digitaux.
          </p>
        </div>

        <!-- Navigation -->
        <div>
          <h3 class="font-bold text-lg mb-4">Navigation</h3>
          <ul class="space-y-2">
            <li>
              <router-link to="/" class="text-dark-300 dark:text-dark-400 hover:text-primary-400 transition-colors">
                Accueil
              </router-link>
            </li>
            <li>
              <router-link to="/portfolio" class="text-dark-300 dark:text-dark-400 hover:text-primary-400 transition-colors">
                Portfolio
              </router-link>
            </li>
            <li>
              <router-link to="/devis" class="text-dark-300 dark:text-dark-400 hover:text-primary-400 transition-colors">
                Devis
              </router-link>
            </li>
            <li>
              <router-link to="/contact" class="text-dark-300 dark:text-dark-400 hover:text-primary-400 transition-colors">
                Contact
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Services -->
        <div>
          <h3 class="font-bold text-lg mb-4">Services</h3>
          <ul class="space-y-2 text-dark-300 dark:text-dark-400 text-sm">
            <li>Développement Web</li>
            <li>Design UI/UX</li>
            <li>E-commerce</li>
            <li>SEO & Marketing</li>
          </ul>
        </div>

        <!-- Contact -->
        <div>
          <h3 class="font-bold text-lg mb-4">Contact</h3>
          <ul class="space-y-2 text-dark-300 dark:text-dark-400 text-sm">
            <li class="flex items-center space-x-2">
              <svg class="w-5 h-5 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
              </svg>
              <span>Zsdevweb team inscrivez-vous pour nous contacter</span>
            </li>
        
          </ul>
        </div>
      </div>

      <!-- Copyright -->
      <div class="border-t border-dark-800 dark:border-dark-900 mt-8 pt-8 text-center">
        <p class="text-dark-400 dark:text-dark-500 text-sm">
          © {{ new Date().getFullYear() }} Zsdevweb. Tous droits réservés.
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>