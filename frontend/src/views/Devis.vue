<template>
  <div class="min-h-screen bg-white dark:bg-dark-900 transition-colors duration-200">
    <!-- Header -->
    <section class="bg-gradient-to-br from-primary-600 to-secondary-600 dark:from-primary-900 dark:to-secondary-900 text-white py-16">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-5xl md:text-6xl font-bold mb-4">Calculateur de Devis</h1>
        <p class="text-xl text-primary-100 dark:text-primary-200 max-w-2xl mx-auto">
          Obtenez une estimation instantanée pour votre projet en quelques clics
        </p>
      </div>
    </section>

    <!-- Progress Bar -->
    <section class="bg-gray-50 dark:bg-dark-800 py-6 sticky top-16 z-40 border-b border-gray-200 dark:border-dark-700">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-semibold text-dark-700 dark:text-dark-200">Étape {{ currentStep }} sur 7</span>
            <span class="text-sm font-semibold text-primary-600 dark:text-primary-400">{{ Math.round((currentStep / 7) * 100) }}%</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-dark-700 rounded-full h-3 overflow-hidden">
            <div 
              class="bg-gradient-to-r from-primary-600 to-secondary-500 h-full rounded-full transition-all duration-500 ease-out"
              :style="{ width: `${(currentStep / 7) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Form Content -->
    <section class="py-16">
      <div class="container mx-auto px-4 max-w-4xl">
        <div v-if="loadingOptions" class="text-center py-16">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p class="mt-4 text-dark-600 dark:text-dark-300">Chargement...</p>
        </div>

        <div v-else class="bg-white dark:bg-dark-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-dark-700">
          <!-- Étape 1 : Informations client -->
          <div v-if="currentStep === 1" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <svg class="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Vos informations</h2>
              <p class="text-dark-600 dark:text-dark-300">Commençons par faire connaissance</p>
            </div>
            
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Nom complet <span class="text-red-500">*</span>
                </label>
                <input 
                  v-model="quote.client_name" 
                  type="text" 
                  required 
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="Votre nom complet"
                >
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Email <span class="text-red-500">*</span>
                </label>
                <input 
                  v-model="quote.client_email" 
                  type="email" 
                  required 
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="votre@email.com"
                >
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Téléphone <span class="text-dark-400 dark:text-dark-500 text-xs">(optionnel)</span>
                </label>
                <input 
                  v-model="quote.client_phone" 
                  type="tel" 
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="+33 X XX XX XX XX"
                >
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Entreprise <span class="text-dark-400 dark:text-dark-500 text-xs">(optionnel)</span>
                </label>
                <input 
                  v-model="quote.company_name" 
                  type="text" 
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="Nom de votre entreprise"
                >
              </div>
            </div>
          </div>

          <!-- Étape 2 : Type de projet -->
          <div v-if="currentStep === 2" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <svg class="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Type de projet</h2>
              <p class="text-dark-600 dark:text-dark-300">Quel type de site souhaitez-vous ?</p>
            </div>
            
            <div class="grid md:grid-cols-3 gap-4">
              <div 
                v-for="type in projectTypes" 
                :key="type.id"
                @click="quote.project_type = type.id"
                :class="[
                  'border-2 p-6 rounded-xl cursor-pointer transition-all duration-200',
                  quote.project_type === type.id 
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-lg' 
                    : 'border-gray-200 dark:border-dark-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white dark:bg-dark-700'
                ]"
              >
                <h3 class="text-xl font-bold mb-2" :class="quote.project_type === type.id ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'">
                  {{ type.name }}
                </h3>
                <p class="text-sm mb-4" :class="quote.project_type === type.id ? 'text-dark-700 dark:text-dark-300' : 'text-dark-600 dark:text-dark-400'">
                  {{ type.description }}
                </p>
                <p class="text-2xl font-bold" :class="quote.project_type === type.id ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'">
                  {{ type.base_price }}€
                </p>
              </div>
            </div>
          </div>

          <!-- Étape 3 : Option de design -->
          <div v-if="currentStep === 3" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <svg class="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Option de design</h2>
              <p class="text-dark-600 dark:text-dark-300">Choisissez le niveau de personnalisation</p>
            </div>
            
            <div class="grid md:grid-cols-3 gap-4">
              <div 
                v-for="option in designOptions" 
                :key="option.id"
                @click="quote.design_option = option.id"
                :class="[
                  'border-2 p-6 rounded-xl cursor-pointer transition-all duration-200',
                  quote.design_option === option.id 
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-lg' 
                    : 'border-gray-200 dark:border-dark-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white dark:bg-dark-700'
                ]"
              >
                <h3 class="text-xl font-bold mb-2" :class="quote.design_option === option.id ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'">
                  {{ option.name }}
                </h3>
                <p class="text-sm mb-4" :class="quote.design_option === option.id ? 'text-dark-700 dark:text-dark-300' : 'text-dark-600 dark:text-dark-400'">
                  {{ option.description }}
                </p>
                <p class="text-2xl font-bold" :class="quote.design_option === option.id ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'">
                  +{{ option.price_supplement }}€
                </p>
              </div>
            </div>
          </div>

          <!-- Étape 4 : Niveau de complexité -->
          <div v-if="currentStep === 4" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <svg class="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Niveau de complexité</h2>
              <p class="text-dark-600 dark:text-dark-300">Définissez les fonctionnalités nécessaires</p>
            </div>
            
            <div class="grid md:grid-cols-3 gap-4">
              <div 
                v-for="level in complexityLevels" 
                :key="level.id"
                @click="quote.complexity_level = level.id"
                :class="[
                  'border-2 p-6 rounded-xl cursor-pointer transition-all duration-200',
                  quote.complexity_level === level.id 
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-lg' 
                    : 'border-gray-200 dark:border-dark-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white dark:bg-dark-700'
                ]"
              >
                <h3 class="text-xl font-bold mb-2" :class="quote.complexity_level === level.id ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'">
                  {{ level.name }}
                </h3>
                <p class="text-sm mb-4" :class="quote.complexity_level === level.id ? 'text-dark-700 dark:text-dark-300' : 'text-dark-600 dark:text-dark-400'">
                  {{ level.description }}
                </p>
                <p class="text-2xl font-bold" :class="quote.complexity_level === level.id ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'">
                  ×{{ level.price_multiplier }}
                </p>
              </div>
            </div>
          </div>

          <!-- Étape 5 : Options supplémentaires -->
          <div v-if="currentStep === 5" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <svg class="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Options supplémentaires</h2>
              <p class="text-dark-600 dark:text-dark-300">Ajoutez des services complémentaires</p>
            </div>
            
            <div class="space-y-4">
              <div 
                v-for="option in supplementaryOptions" 
                :key="option.id"
                @click="toggleSupplementaryOption(option.id)"
                :class="[
                  'border-2 p-6 rounded-xl cursor-pointer transition-all duration-200 flex justify-between items-center',
                  quote.supplementary_options.includes(option.id) 
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 shadow-lg' 
                    : 'border-gray-200 dark:border-dark-600 hover:border-primary-300 dark:hover:border-primary-700 bg-white dark:bg-dark-700'
                ]"
              >
                <div>
                  <h3 class="text-xl font-bold mb-1" :class="quote.supplementary_options.includes(option.id) ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'">
                    {{ option.name }}
                  </h3>
                  <p class="text-sm" :class="quote.supplementary_options.includes(option.id) ? 'text-dark-700 dark:text-dark-300' : 'text-dark-600 dark:text-dark-400'">
                    {{ option.description }}
                  </p>
                </div>
                <div class="flex items-center space-x-3">
                  <p class="text-2xl font-bold" :class="quote.supplementary_options.includes(option.id) ? 'text-primary-600 dark:text-primary-400' : 'text-dark-900 dark:text-white'">
                    +{{ option.price }}€
                  </p>
                  <div 
                    :class="[
                      'w-6 h-6 rounded-full border-2 flex items-center justify-center',
                      quote.supplementary_options.includes(option.id) 
                        ? 'border-primary-500 bg-primary-500' 
                        : 'border-gray-300 dark:border-dark-500'
                    ]"
                  >
                    <svg v-if="quote.supplementary_options.includes(option.id)" class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Étape 6 : Description et deadline -->
          <div v-if="currentStep === 6" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <svg class="w-8 h-8 text-primary-600 dark:text-primary-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Détails du Projet</h2>
              <p class="text-dark-600 dark:text-dark-300">Parlez-nous de votre vision</p>
            </div>

            <div class="space-y-6">
              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Description du projet <span class="text-red-500">*</span>
                </label>
                <textarea
                  v-model="quote.project_description"
                  rows="6"
                  required
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                  placeholder="Décrivez votre projet, vos objectifs, votre audience cible, les fonctionnalités souhaitées..."
                ></textarea>
                <p class="mt-2 text-sm text-dark-500 dark:text-dark-400">Minimum 10 caractères</p>
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 dark:text-dark-200 mb-2">
                  Date limite souhaitée <span class="text-dark-400 dark:text-dark-500 text-xs">(optionnel)</span>
                </label>
                <input
                  v-model="quote.deadline"
                  type="date"
                  :min="new Date().toISOString().split('T')[0]"
                  class="w-full px-4 py-3 border-2 border-gray-200 dark:border-dark-600 dark:bg-dark-700 dark:text-white rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                />
              </div>
            </div>
          </div>

          <!-- Étape 7 : Récapitulatif -->
          <div v-if="currentStep === 7" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full mb-4">
                <svg class="w-8 h-8 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Récapitulatif</h2>
              <p class="text-dark-600 dark:text-dark-300">Vérifiez les informations avant l'envoi</p>
            </div>
            
            <div class="space-y-6">
              <!-- Summary Card -->
              <div class="bg-gray-50 dark:bg-dark-700 rounded-xl p-6 border border-gray-200 dark:border-dark-600">
                <h3 class="text-xl font-bold text-dark-900 dark:text-white mb-4">Informations du projet</h3>
                <div class="space-y-3 text-dark-700 dark:text-dark-300">
                  <div class="flex justify-between">
                    <span class="font-semibold">Client :</span>
                    <span>{{ quote.client_name }}</span>
                  </div>
                  <div class="flex justify-between">
                    <span class="font-semibold">Email :</span>
                    <span>{{ quote.client_email }}</span>
                  </div>
                  <div v-if="quote.client_phone" class="flex justify-between">
                    <span class="font-semibold">Téléphone :</span>
                    <span>{{ quote.client_phone }}</span>
                  </div>
                  <div v-if="quote.company_name" class="flex justify-between">
                    <span class="font-semibold">Entreprise :</span>
                    <span>{{ quote.company_name }}</span>
                  </div>
                </div>
              </div>

              <!-- Price Breakdown -->
              <div class="bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 rounded-xl p-6 border-2 border-primary-200 dark:border-primary-800">
                <h3 class="text-xl font-bold text-dark-900 dark:text-white mb-4">Détail du devis</h3>
                <div class="space-y-3">
                  <div class="flex justify-between text-dark-700 dark:text-dark-300">
                    <span>Base ({{ getSelectedProjectType()?.name }})</span>
                    <span class="font-semibold">{{ getSelectedProjectType()?.base_price }} €</span>
                  </div>
                  <div class="flex justify-between text-dark-700 dark:text-dark-300">
                    <span>Design ({{ getSelectedDesignOption()?.name }})</span>
                    <span class="font-semibold">+ {{ getSelectedDesignOption()?.price_supplement }} €</span>
                  </div>
                  <div class="flex justify-between text-dark-700 dark:text-dark-300">
                    <span>Multiplicateur ({{ getSelectedComplexityLevel()?.name }})</span>
                    <span class="font-semibold">× {{ getSelectedComplexityLevel()?.price_multiplier }}</span>
                  </div>
                  <div v-if="getSelectedSupplementaryOptions().length > 0">
                    <div v-for="opt in getSelectedSupplementaryOptions()" :key="opt.id" class="flex justify-between text-dark-700 dark:text-dark-300">
                      <span>{{ opt.name }}</span>
                      <span class="font-semibold">+ {{ opt.price }} €</span>
                    </div>
                  </div>
                  <div class="pt-3 mt-3 border-t-2 border-primary-300 dark:border-primary-700 flex justify-between items-center">
                    <span class="text-xl font-bold text-dark-900 dark:text-white">Total estimé</span>
                    <span class="text-3xl font-bold text-primary-600 dark:text-primary-400">{{ calculateTotal() }} €</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Success/Error Messages -->
            <div v-if="successMessage" class="bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500 p-4 rounded-lg">
              <div class="flex items-start">
                <svg class="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <div>
                  <h4 class="font-bold text-green-800 dark:text-green-300">Devis envoyé avec succès !</h4>
                  <p class="text-sm text-green-700 dark:text-green-400">{{ successMessage }}</p>
                </div>
              </div>
            </div>

            <div v-if="errorMessage" class="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-500 p-4 rounded-lg">
              <div class="flex items-start">
                <svg class="h-6 w-6 text-red-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                </svg>
                <div>
                  <h4 class="font-bold text-red-800 dark:text-red-300">Erreur</h4>
                  <p class="text-sm text-red-700 dark:text-red-400">{{ errorMessage }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Navigation Buttons -->
          <div class="flex gap-4 mt-8 pt-6 border-t border-gray-200 dark:border-dark-600">
            <button
              v-if="currentStep > 1"
              @click="prevStep"
              class="flex-1 px-6 py-3 border-2 border-gray-300 dark:border-dark-600 text-dark-700 dark:text-dark-200 rounded-lg font-semibold hover:bg-gray-50 dark:hover:bg-dark-700 transition-all"
            >
              ← Précédent
            </button>
            
            <button
              v-if="currentStep < 7"
              @click="nextStep"
              :disabled="!canProceed"
              class="flex-1 bg-gradient-to-r from-primary-600 to-secondary-500 text-white px-6 py-3 rounded-lg font-semibold hover:from-primary-700 hover:to-secondary-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
            >
              Suivant →
            </button>

            <button
              v-if="currentStep === 7"
              @click="submitQuote"
              :disabled="submitting"
              class="flex-1 bg-gradient-to-r from-green-600 to-green-500 text-white px-6 py-3 rounded-lg font-semibold hover:from-green-700 hover:to-green-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg"
            >
              {{ submitting ? 'Envoi...' : 'Envoyer le devis' }}
            </button>
          </div>
        </div>

        <!-- Floating Price Display (visible on steps 2-6) -->
        <div v-if="currentStep >= 2 && currentStep <= 6" class="mt-8 bg-gradient-to-r from-primary-600 to-secondary-600 dark:from-primary-900 dark:to-secondary-900 text-white rounded-xl p-6 text-center shadow-xl">
          <p class="text-sm font-medium mb-2 opacity-90">Estimation actuelle</p>
          <p class="text-4xl font-bold">{{ calculateTotal() }} €</p>
          <p class="text-sm mt-2 opacity-75">Prix indicatif • Devis final personnalisé</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  getProjectTypes, 
  getDesignOptions, 
  getComplexityLevels, 
  getSupplementaryOptions,
  createQuote 
} from '../api/quotes'

const router = useRouter()

const currentStep = ref(1)
const loadingOptions = ref(true)
const submitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const quote = ref({
  client_name: '',
  client_email: '',
  client_phone: '',
  company_name: '',
  project_type: null,
  design_option: null,
  complexity_level: null,
  supplementary_options: [],
  project_description: '',
  deadline: ''
})

const projectTypes = ref([])
const designOptions = ref([])
const complexityLevels = ref([])
const supplementaryOptions = ref([])

onMounted(async () => {
  try {
    const [types, designs, levels, options] = await Promise.all([
      getProjectTypes(),
      getDesignOptions(),
      getComplexityLevels(),
      getSupplementaryOptions()
    ])
    
    projectTypes.value = types.data.results || types.data
    designOptions.value = designs.data.results || designs.data
    complexityLevels.value = levels.data.results || levels.data
    supplementaryOptions.value = options.data.results || options.data
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
    errorMessage.value = 'Erreur lors du chargement des options'
  } finally {
    loadingOptions.value = false
  }
})

const canProceed = computed(() => {
  switch (currentStep.value) {
    case 1:
      return quote.value.client_name && quote.value.client_email
    case 2:
      return quote.value.project_type !== null
    case 3:
      return quote.value.design_option !== null
    case 4:
      return quote.value.complexity_level !== null
    case 5:
      return true // Options supplémentaires optionnelles
    case 6:
      return quote.value.project_description && quote.value.project_description.length >= 10
    default:
      return true
  }
})

const toggleSupplementaryOption = (id) => {
  const index = quote.value.supplementary_options.indexOf(id)
  if (index > -1) {
    quote.value.supplementary_options.splice(index, 1)
  } else {
    quote.value.supplementary_options.push(id)
  }
}

const getSelectedProjectType = () => {
  return projectTypes.value.find(t => t.id === quote.value.project_type)
}

const getSelectedDesignOption = () => {
  return designOptions.value.find(o => o.id === quote.value.design_option)
}

const getSelectedComplexityLevel = () => {
  return complexityLevels.value.find(l => l.id === quote.value.complexity_level)
}

const getSelectedSupplementaryOptions = () => {
  return supplementaryOptions.value.filter(o => quote.value.supplementary_options.includes(o.id))
}

const calculateTotal = () => {
  let total = 0
  
  const projectType = getSelectedProjectType()
  const designOption = getSelectedDesignOption()
  const complexityLevel = getSelectedComplexityLevel()
  const suppOptions = getSelectedSupplementaryOptions()
  
  console.log('=== Calcul du total ===')
  console.log('projectType:', projectType)
  console.log('designOption:', designOption)
  console.log('complexityLevel:', complexityLevel)
  console.log('suppOptions:', suppOptions)
  
  if (!projectType || !designOption || !complexityLevel) {
    console.log('Données manquantes pour le calcul')
    return 0
  }
  
  // Convertir en nombres avec Number() qui est plus fiable que parseFloat
  total = Number(projectType.base_price) + Number(designOption.price_supplement)
  total = total * Number(complexityLevel.price_multiplier)
  
  console.log('Total avant options supplémentaires:', total)
  
  // Ajouter les options supplémentaires
  suppOptions.forEach(option => {
    console.log('Ajout option:', option.name, option.price)
    total += Number(option.price)
  })
  
  console.log('Total final:', total)
  
  return Math.round(total)
}

const nextStep = () => {
  if (canProceed.value && currentStep.value < 7) {
    currentStep.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const prevStep = () => {
  if (currentStep.value > 1) {
    currentStep.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const submitQuote = async () => {
  try {
    submitting.value = true
    errorMessage.value = ''
    successMessage.value = ''
    
    await createQuote(quote.value)
    
    successMessage.value = 'Votre demande de devis a été envoyée avec succès ! Nous vous contacterons dans les plus brefs délais.'
    
    setTimeout(() => {
      router.push('/')
    }, 3000)
  } catch (error) {
    errorMessage.value = "Erreur lors de l'envoi du devis. Veuillez réessayer."
    console.error('Erreur:', error)
  } finally {
    submitting.value = false
  }
}
</script>