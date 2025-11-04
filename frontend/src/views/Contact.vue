<template>
  <div class="min-h-screen bg-white dark:bg-dark-900 transition-colors duration-200">
    <!-- Header -->
    <section class="bg-gradient-to-br from-primary-600 to-secondary-600 dark:from-primary-900 dark:to-secondary-900 text-white py-20">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-5xl md:text-6xl font-bold mb-4">Contactez-nous</h1>
        <p class="text-xl text-primary-100 dark:text-primary-200 max-w-2xl mx-auto">
          Une question ? Un projet ? N'hésitez pas à nous contacter
        </p>
      </div>
    </section>

    <!-- Contact Section -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <div class="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          <!-- Contact Form -->
          <div class="bg-white dark:bg-dark-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-dark-700">
            <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-6">Envoyez-nous un message</h2>
            
            <form @submit.prevent="handleSubmit" class="space-y-5">
              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Nom complet <span class="text-red-500">*</span>
                </label>
                <input 
                  v-model="form.name" 
                  type="text" 
                  required 
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="Votre nom"
                >
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Email <span class="text-red-500">*</span>
                </label>
                <input 
                  v-model="form.email" 
                  type="email" 
                  required 
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="votre@email.com"
                >
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Téléphone
                </label>
                <input 
                  v-model="form.phone" 
                  type="tel" 
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="+33 X XX XX XX XX"
                >
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Sujet <span class="text-red-500">*</span>
                </label>
                <input 
                  v-model="form.subject" 
                  type="text" 
                  required 
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="Sujet de votre message"
                >
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Message <span class="text-red-500">*</span>
                </label>
                <textarea 
                  v-model="form.message" 
                  rows="5" 
                  required 
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                  placeholder="Décrivez votre projet ou posez votre question..."
                ></textarea>
              </div>

              <button 
                type="submit" 
                :disabled="submitting"
                class="w-full bg-gradient-to-r from-primary-600 to-secondary-500 text-white px-8 py-4 rounded-lg font-bold text-lg hover:from-primary-700 hover:to-secondary-600 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
              >
                {{ submitting ? 'Envoi...' : 'Envoyer le message' }}
              </button>
            </form>

            <p v-if="successMessage" class="mt-4 text-green-600 dark:text-green-400 font-semibold text-center bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
              {{ successMessage }}
            </p>
            <p v-if="errorMessage" class="mt-4 text-red-600 dark:text-red-400 font-semibold text-center bg-red-50 dark:bg-red-900/20 p-3 rounded-lg">
              {{ errorMessage }}
            </p>
          </div>

          <!-- Contact Info -->
          <div class="space-y-8">
            <!-- Info Cards -->
            <div class="bg-white dark:bg-dark-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-dark-700">
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-6">Informations de contact</h2>
              
              <div class="space-y-6">
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-dark-900 dark:text-white mb-1">Email</h3>
                    <a href="mailto:contact@zsdevweb.com" class="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                      contact@zsdevweb.com
                    </a>
                  </div>
                </div>

                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-dark-900 dark:text-white mb-1">Téléphone</h3>
                    <a href="tel:+33XXXXXXXXX" class="text-dark-600 dark:text-dark-300 hover:text-primary-600 dark:hover:text-primary-400 transition-colors">
                      +33 X XX XX XX XX
                    </a>
                  </div>
                </div>

                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-bold text-dark-900 dark:text-white mb-1">Horaires</h3>
                    <p class="text-dark-600 dark:text-dark-300">Lun - Ven: 9h00 - 18h00</p>
                    <p class="text-dark-600 dark:text-dark-300">Sam - Dim: Fermé</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- FAQ -->
            <div class="bg-white dark:bg-dark-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-dark-700">
              <h2 class="text-2xl font-bold text-dark-900 dark:text-white mb-6">Questions fréquentes</h2>
              
              <div class="space-y-4">
                <details class="group">
                  <summary class="font-semibold text-dark-900 dark:text-white cursor-pointer list-none flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-700 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-600 transition-colors">
                    <span>Quel est le délai moyen pour un projet ?</span>
                    <svg class="w-5 h-5 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                  </summary>
                  <p class="mt-3 text-dark-600 dark:text-dark-300 px-4">
                    Le délai varie selon la complexité du projet, généralement entre 2 et 8 semaines.
                  </p>
                </details>

                <details class="group">
                  <summary class="font-semibold text-dark-900 dark:text-white cursor-pointer list-none flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-700 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-600 transition-colors">
                    <span>Proposez-vous un support après livraison ?</span>
                    <svg class="w-5 h-5 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                  </summary>
                  <p class="mt-3 text-dark-600 dark:text-dark-300 px-4">
                    Oui, nous offrons un support et maintenance continue selon vos besoins.
                  </p>
                </details>

                <details class="group">
                  <summary class="font-semibold text-dark-900 dark:text-white cursor-pointer list-none flex items-center justify-between p-4 bg-gray-50 dark:bg-dark-700 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-600 transition-colors">
                    <span>Comment se déroule le processus de développement ?</span>
                    <svg class="w-5 h-5 transition-transform group-open:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                  </summary>
                  <p class="mt-3 text-dark-600 dark:text-dark-300 px-4">
                    Consultation → Devis → Design → Développement → Tests → Livraison → Support
                  </p>
                </details>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { sendContactMessage } from '../api/contact'

const form = ref({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const submitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const handleSubmit = async () => {
  submitting.value = true
  successMessage.value = ''
  errorMessage.value = ''

  try {
    const response = await sendContactMessage(form.value)

    // Afficher le message de succès du backend
    successMessage.value = response.data.message || 'Message envoyé avec succès ! Nous vous répondrons dans les plus brefs délais.'

    // Reset form
    form.value = {
      name: '',
      email: '',
      phone: '',
      subject: '',
      message: ''
    }
  } catch (error) {
    console.error('Erreur lors de l\'envoi du message:', error)

    // Gérer les erreurs de validation
    if (error.response?.data) {
      const errors = error.response.data
      if (typeof errors === 'object' && !errors.message) {
        // Afficher les erreurs de validation
        const errorMessages = Object.values(errors).flat().join(' ')
        errorMessage.value = errorMessages || "Erreur lors de l'envoi du message. Veuillez réessayer."
      } else {
        errorMessage.value = errors.message || errors.detail || "Erreur lors de l'envoi du message. Veuillez réessayer."
      }
    } else {
      errorMessage.value = "Erreur lors de l'envoi du message. Veuillez réessayer."
    }
  } finally {
    submitting.value = false
  }
}
</script>