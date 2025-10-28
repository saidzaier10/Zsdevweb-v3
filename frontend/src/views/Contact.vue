<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
    <!-- Header -->
    <section class="bg-gradient-to-r from-primary-600 to-secondary-600 text-white py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-3xl mx-auto text-center">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-white/10 backdrop-blur-md rounded-full mb-6">
            <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
            </svg>
          </div>
          <h1 class="text-5xl md:text-6xl font-display font-bold mb-4 animate-fade-in">
            Contactez-moi
          </h1>
          <p class="text-xl md:text-2xl text-blue-100 animate-slide-up">
            Une question ? Un projet ? Discutons-en ensemble !
          </p>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-6xl mx-auto">
          <div class="grid lg:grid-cols-5 gap-8">
            <!-- Contact Form - Left Side (3 columns) -->
            <div class="lg:col-span-3">
              <div class="card p-8 shadow-xl">
                <div class="mb-6">
                  <h2 class="text-3xl font-bold text-dark-900 mb-2">Envoyez-moi un message</h2>
                  <p class="text-dark-600">Je vous répondrai dans les plus brefs délais</p>
                </div>

                <form @submit.prevent="handleSubmit" class="space-y-6">
                  <!-- Name -->
                  <div>
                    <label for="name" class="block text-sm font-semibold text-dark-700 mb-2">
                      Nom complet <span class="text-red-500">*</span>
                    </label>
                    <div class="relative">
                      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                        </svg>
                      </div>
                      <input
                        id="name"
                        v-model="form.name"
                        type="text"
                        required
                        class="block w-full pl-10 pr-3 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                        placeholder="Jean Dupont"
                      />
                    </div>
                  </div>

                  <!-- Email -->
                  <div>
                    <label for="email" class="block text-sm font-semibold text-dark-700 mb-2">
                      Email <span class="text-red-500">*</span>
                    </label>
                    <div class="relative">
                      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                        </svg>
                      </div>
                      <input
                        id="email"
                        v-model="form.email"
                        type="email"
                        required
                        class="block w-full pl-10 pr-3 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                        placeholder="jean@exemple.com"
                      />
                    </div>
                  </div>

                  <!-- Phone -->
                  <div>
                    <label for="phone" class="block text-sm font-semibold text-dark-700 mb-2">
                      Téléphone <span class="text-dark-400 text-xs">(optionnel)</span>
                    </label>
                    <div class="relative">
                      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                        </svg>
                      </div>
                      <input
                        id="phone"
                        v-model="form.phone"
                        type="tel"
                        class="block w-full pl-10 pr-3 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                        placeholder="+33 1 23 45 67 89"
                      />
                    </div>
                  </div>

                  <!-- Subject -->
                  <div>
                    <label for="subject" class="block text-sm font-semibold text-dark-700 mb-2">
                      Sujet <span class="text-red-500">*</span>
                    </label>
                    <div class="relative">
                      <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                        </svg>
                      </div>
                      <select
                        id="subject"
                        v-model="form.subject"
                        required
                        class="block w-full pl-10 pr-3 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all appearance-none cursor-pointer"
                      >
                        <option value="">Sélectionnez un sujet</option>
                        <option value="devis">Demande de devis</option>
                        <option value="question">Question générale</option>
                        <option value="collaboration">Proposition de collaboration</option>
                        <option value="autre">Autre</option>
                      </select>
                      <div class="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                        <svg class="h-5 w-5 text-dark-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                        </svg>
                      </div>
                    </div>
                  </div>

                  <!-- Message -->
                  <div>
                    <label for="message" class="block text-sm font-semibold text-dark-700 mb-2">
                      Message <span class="text-red-500">*</span>
                    </label>
                    <textarea
                      id="message"
                      v-model="form.message"
                      rows="6"
                      required
                      class="block w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                      placeholder="Parlez-moi de votre projet ou de votre demande..."
                    ></textarea>
                    <p class="mt-2 text-sm text-dark-500">Minimum 10 caractères</p>
                  </div>

                  <!-- Success Message -->
                  <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg animate-fade-in">
                    <div class="flex items-start">
                      <svg class="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                      </svg>
                      <div>
                        <h4 class="font-bold text-green-800">Message envoyé avec succès !</h4>
                        <p class="text-sm text-green-700">{{ successMessage }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Error Message -->
                  <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg animate-fade-in">
                    <div class="flex items-start">
                      <svg class="h-6 w-6 text-red-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                      </svg>
                      <div>
                        <h4 class="font-bold text-red-800">Erreur</h4>
                        <p class="text-sm text-red-700">{{ errorMessage }}</p>
                      </div>
                    </div>
                  </div>

                  <!-- Submit Button -->
                  <button
                    type="submit"
                    :disabled="loading"
                    class="w-full btn-primary py-3.5 text-lg font-semibold disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <span v-if="!loading" class="flex items-center justify-center">
                      <span>Envoyer le message</span>
                      <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
                      </svg>
                    </span>
                    <span v-else class="flex items-center justify-center">
                      <svg class="animate-spin h-5 w-5 mr-3" fill="none" viewBox="0 0 24 24">
                        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Envoi en cours...
                    </span>
                  </button>
                </form>
              </div>
            </div>

            <!-- Contact Info - Right Side (2 columns) -->
            <div class="lg:col-span-2 space-y-6">
              <!-- Contact Details Card -->
              <div class="card p-6 shadow-xl">
                <h3 class="text-xl font-bold text-dark-900 mb-6 flex items-center">
                  <svg class="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Informations de contact
                </h3>

                <div class="space-y-4">
                  <!-- Email -->
                  <div class="flex items-start space-x-4 p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition-colors">
                    <div class="flex-shrink-0">
                      <div class="w-12 h-12 bg-primary-600 rounded-lg flex items-center justify-center">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                        </svg>
                      </div>
                    </div>
                    <div>
                      <h4 class="font-semibold text-dark-900 mb-1">Email</h4>
                      <a href="mailto:contact@zsdevweb.com" class="text-primary-600 hover:text-primary-700 transition-colors">
                        contact@zsdevweb.com
                      </a>
                    </div>
                  </div>

                  <!-- Phone -->
                  <div class="flex items-start space-x-4 p-4 bg-secondary-50 rounded-lg hover:bg-secondary-100 transition-colors">
                    <div class="flex-shrink-0">
                      <div class="w-12 h-12 bg-secondary-600 rounded-lg flex items-center justify-center">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                        </svg>
                      </div>
                    </div>
                    <div>
                      <h4 class="font-semibold text-dark-900 mb-1">Téléphone</h4>
                      <a href="tel:+33123456789" class="text-secondary-600 hover:text-secondary-700 transition-colors">
                        +33 1 23 45 67 89
                      </a>
                    </div>
                  </div>

                  <!-- Location -->
                  <div class="flex items-start space-x-4 p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors">
                    <div class="flex-shrink-0">
                      <div class="w-12 h-12 bg-purple-600 rounded-lg flex items-center justify-center">
                        <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        </svg>
                      </div>
                    </div>
                    <div>
                      <h4 class="font-semibold text-dark-900 mb-1">Localisation</h4>
                      <p class="text-purple-600">Paris, France</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Business Hours Card -->
              <div class="card p-6 shadow-xl bg-gradient-to-br from-primary-50 to-secondary-50">
                <h3 class="text-xl font-bold text-dark-900 mb-4 flex items-center">
                  <svg class="w-6 h-6 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Horaires de disponibilité
                </h3>
                <div class="space-y-3 text-sm">
                  <div class="flex justify-between py-2 border-b border-primary-200">
                    <span class="font-medium text-dark-700">Lundi - Vendredi</span>
                    <span class="text-dark-600">9h00 - 18h00</span>
                  </div>
                  <div class="flex justify-between py-2 border-b border-primary-200">
                    <span class="font-medium text-dark-700">Samedi</span>
                    <span class="text-dark-600">10h00 - 16h00</span>
                  </div>
                  <div class="flex justify-between py-2">
                    <span class="font-medium text-dark-700">Dimanche</span>
                    <span class="text-red-600 font-semibold">Fermé</span>
                  </div>
                </div>
                <div class="mt-4 pt-4 border-t border-primary-200">
                  <p class="text-xs text-dark-600 italic">
                    💡 Réponse garantie sous 24h les jours ouvrables
                  </p>
                </div>
              </div>

              <!-- Social Links Card -->
              <div class="card p-6 shadow-xl">
                <h3 class="text-xl font-bold text-dark-900 mb-4">Suivez-moi</h3>
                <div class="flex space-x-3">
                  <a href="https://github.com" target="_blank" class="w-12 h-12 bg-dark-800 hover:bg-primary-600 rounded-lg flex items-center justify-center transition-colors group">
                    <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
                    </svg>
                  </a>
                  <a href="https://linkedin.com" target="_blank" class="w-12 h-12 bg-[#0077B5] hover:bg-primary-600 rounded-lg flex items-center justify-center transition-colors">
                    <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
                    </svg>
                  </a>
                  <a href="https://twitter.com" target="_blank" class="w-12 h-12 bg-[#1DA1F2] hover:bg-primary-600 rounded-lg flex items-center justify-center transition-colors">
                    <svg class="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M23 3a10.9 10.9 0 01-3.14 1.53 4.48 4.48 0 00-7.86 3v1A10.66 10.66 0 013 4s-4 9 5 13a11.64 11.64 0 01-7 2c9 5 20 0 20-11.5a4.5 4.5 0 00-.08-.83A7.72 7.72 0 0023 3z"></path>
                    </svg>
                  </a>
                </div>
              </div>

              <!-- Quick Action Card -->
              <div class="card p-6 shadow-xl bg-gradient-to-r from-primary-600 to-secondary-600 text-white">
                <h3 class="text-xl font-bold mb-2">Besoin d'un devis rapide ?</h3>
                <p class="text-blue-100 mb-4 text-sm">
                  Utilisez notre calculateur de devis pour obtenir une estimation en quelques clics
                </p>
                <router-link 
                  to="/devis" 
                  class="inline-flex items-center space-x-2 bg-white text-primary-700 px-4 py-2.5 rounded-lg font-semibold hover:bg-blue-50 transition-colors text-sm"
                >
                  <span>Calculer un devis</span>
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                  </svg>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <div class="text-center mb-12">
            <h2 class="section-title">Questions Fréquentes</h2>
            <p class="text-xl text-dark-600">Vous avez des questions ? Voici quelques réponses</p>
          </div>

          <div class="space-y-4">
            <details class="card p-6 cursor-pointer group">
              <summary class="font-semibold text-dark-900 flex items-center justify-between">
                <span>Quel est votre délai de réponse ?</span>
                <svg class="w-5 h-5 text-primary-600 transform group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </summary>
              <p class="mt-4 text-dark-600 leading-relaxed">
                Je m'engage à répondre à tous les messages sous 24h les jours ouvrables. Pour les demandes urgentes, n'hésitez pas à me contacter directement par téléphone.
              </p>
            </details>

            <details class="card p-6 cursor-pointer group">
              <summary class="font-semibold text-dark-900 flex items-center justify-between">
                <span>Proposez-vous des consultations gratuites ?</span>
                <svg class="w-5 h-5 text-primary-600 transform group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </summary>
              <p class="mt-4 text-dark-600 leading-relaxed">
                Oui ! La première consultation de 30 minutes est gratuite et sans engagement. C'est l'occasion de discuter de votre projet et de voir comment je peux vous aider.
              </p>
            </details>

            <details class="card p-6 cursor-pointer group">
              <summary class="font-semibold text-dark-900 flex items-center justify-between">
                <span>Travaillez-vous avec des clients à l'international ?</span>
                <svg class="w-5 h-5 text-primary-600 transform group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </summary>
              <p class="mt-4 text-dark-600 leading-relaxed">
                Absolument ! Je travaille avec des clients dans toute la France et à l'international. La plupart de mes échanges se font en ligne (visioconférence, email, etc.).
              </p>
            </details>

            <details class="card p-6 cursor-pointer group">
              <summary class="font-semibold text-dark-900 flex items-center justify-between">
                <span>Quels sont vos tarifs ?</span>
                <svg class="w-5 h-5 text-primary-600 transform group-open:rotate-180 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
              </summary>
              <p class="mt-4 text-dark-600 leading-relaxed">
                Mes tarifs varient selon la complexité et les besoins de chaque projet. Utilisez mon calculateur de devis pour obtenir une estimation, ou contactez-moi directement pour un devis personnalisé.
              </p>
            </details>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const form = ref({
  name: '',
  email: '',
  phone: '',
  subject: '',
  message: ''
})

const loading = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const handleSubmit = async () => {
  try {
    loading.value = true
    errorMessage.value = ''
    successMessage.value = ''

    // Validation basique
    if (form.value.message.length < 10) {
      errorMessage.value = 'Le message doit contenir au moins 10 caractères.'
      return
    }

    // TODO: Implémenter l'envoi réel vers le backend
    // Pour l'instant, simulation
    await new Promise(resolve => setTimeout(resolve, 1500))
    
    console.log('Formulaire soumis:', form.value)
    
    successMessage.value = 'Votre message a été envoyé avec succès ! Je vous répondrai dans les plus brefs délais.'
    
    // Reset form
    form.value = {
      name: '',
      email: '',
      phone: '',
      subject: '',
      message: ''
    }
  } catch (error) {
    console.error('Erreur lors de l\'envoi:', error)
    errorMessage.value = 'Une erreur est survenue. Veuillez réessayer ou me contacter directement par email.'
  } finally {
    loading.value = false
  }
}
</script>