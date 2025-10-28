<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
    <!-- Header -->
    <section class="bg-gradient-to-r from-primary-600 to-secondary-600 text-white py-12">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <h1 class="text-4xl md:text-5xl font-display font-bold mb-4">
            Calculateur de Devis
          </h1>
          <p class="text-xl text-blue-100">
            Obtenez une estimation personnalisée en quelques minutes
          </p>
        </div>
      </div>
    </section>

    <!-- Progress Bar -->
    <div class="bg-white border-b border-gray-200 sticky top-16 z-40 shadow-sm">
      <div class="container mx-auto px-4 py-4">
        <div class="max-w-4xl mx-auto">
          <div class="flex items-center justify-between mb-2">
            <span class="text-sm font-semibold text-dark-700">Étape {{ currentStep }} sur 7</span>
            <span class="text-sm font-semibold text-primary-600">{{ Math.round((currentStep / 7) * 100) }}%</span>
          </div>
          <div class="w-full bg-gray-200 rounded-full h-2.5 overflow-hidden">
            <div 
              class="bg-gradient-to-r from-primary-600 to-secondary-500 h-2.5 rounded-full transition-all duration-500 ease-out"
              :style="{ width: `${(currentStep / 7) * 100}%` }"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      <div class="max-w-4xl mx-auto">
        <!-- Stepper Navigation -->
        <div class="mb-8 overflow-x-auto">
          <div class="flex items-center justify-between min-w-max">
            <div 
              v-for="step in steps" 
              :key="step.number"
              class="flex items-center"
            >
              <div class="flex flex-col items-center">
                <div 
                  :class="[
                    'w-12 h-12 rounded-full flex items-center justify-center font-bold text-lg transition-all duration-300',
                    currentStep > step.number ? 'bg-green-500 text-white' : 
                    currentStep === step.number ? 'bg-gradient-to-r from-primary-600 to-secondary-500 text-white shadow-lg scale-110' : 
                    'bg-gray-200 text-gray-500'
                  ]"
                >
                  <svg v-if="currentStep > step.number" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                  </svg>
                  <span v-else>{{ step.number }}</span>
                </div>
                <span 
                  :class="[
                    'mt-2 text-xs font-medium text-center whitespace-nowrap',
                    currentStep === step.number ? 'text-primary-600' : 'text-gray-500'
                  ]"
                >
                  {{ step.label }}
                </span>
              </div>
              <div 
                v-if="step.number < 7"
                :class="[
                  'w-16 md:w-24 h-1 mx-2 transition-colors duration-300',
                  currentStep > step.number ? 'bg-green-500' : 'bg-gray-200'
                ]"
              ></div>
            </div>
          </div>
        </div>

        <!-- Step Content Card -->
        <div class="card p-8 mb-6 shadow-xl">
          <!-- Étape 1 : Informations Client -->
          <div v-if="currentStep === 1" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 mb-2">Vos Informations</h2>
              <p class="text-dark-600">Commençons par faire connaissance</p>
            </div>

            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-dark-700 mb-2">
                  Nom complet <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="quote.client_name"
                  type="text"
                  required
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="Jean Dupont"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 mb-2">
                  Email <span class="text-red-500">*</span>
                </label>
                <input
                  v-model="quote.client_email"
                  type="email"
                  required
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="jean@exemple.com"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 mb-2">
                  Téléphone <span class="text-dark-400 text-xs">(optionnel)</span>
                </label>
                <input
                  v-model="quote.client_phone"
                  type="tel"
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="+33 1 23 45 67 89"
                />
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 mb-2">
                  Entreprise <span class="text-dark-400 text-xs">(optionnel)</span>
                </label>
                <input
                  v-model="quote.company_name"
                  type="text"
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                  placeholder="Mon Entreprise"
                />
              </div>
            </div>
          </div>

          <!-- Étape 2 : Type de Projet -->
          <div v-if="currentStep === 2" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 mb-2">Type de Projet</h2>
              <p class="text-dark-600">Quel type de site souhaitez-vous créer ?</p>
            </div>

            <div v-if="loadingOptions" class="text-center py-12">
              <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-4 border-b-4 border-primary-600"></div>
            </div>

            <div v-else class="grid md:grid-cols-3 gap-6">
              <div
                v-for="type in projectTypes"
                :key="type.id"
                @click="quote.project_type = type.id"
                :class="[
                  'cursor-pointer p-6 border-3 rounded-xl transition-all duration-300 group',
                  quote.project_type === type.id
                    ? 'border-primary-500 bg-primary-50 shadow-lg scale-105'
                    : 'border-gray-200 hover:border-primary-300 hover:shadow-md'
                ]"
              >
                <div class="text-center">
                  <div 
                    :class="[
                      'w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center transition-all',
                      quote.project_type === type.id ? 'bg-primary-600' : 'bg-gray-200 group-hover:bg-primary-100'
                    ]"
                  >
                    <span :class="quote.project_type === type.id ? 'text-white text-2xl' : 'text-gray-600 text-2xl'">
                      {{ type.name === 'Site vitrine' ? '🖥️' : type.name === 'E-commerce' ? '🛒' : '⚡' }}
                    </span>
                  </div>
                  <h3 class="text-xl font-bold text-dark-900 mb-2">{{ type.name }}</h3>
                  <p class="text-sm text-dark-600 mb-4">{{ type.description }}</p>
                  <div 
                    :class="[
                      'text-2xl font-bold',
                      quote.project_type === type.id ? 'text-primary-600' : 'text-dark-800'
                    ]"
                  >
                    {{ type.base_price }} €
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Étape 3 : Option de Design -->
          <div v-if="currentStep === 3" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-secondary-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-secondary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 mb-2">Style de Design</h2>
              <p class="text-dark-600">Choisissez le niveau de design souhaité</p>
            </div>

            <div class="grid md:grid-cols-3 gap-6">
              <div
                v-for="option in designOptions"
                :key="option.id"
                @click="quote.design_option = option.id"
                :class="[
                  'cursor-pointer p-6 border-3 rounded-xl transition-all duration-300 group',
                  quote.design_option === option.id
                    ? 'border-secondary-500 bg-secondary-50 shadow-lg scale-105'
                    : 'border-gray-200 hover:border-secondary-300 hover:shadow-md'
                ]"
              >
                <div class="text-center">
                  <div 
                    :class="[
                      'w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center transition-all',
                      quote.design_option === option.id ? 'bg-secondary-600' : 'bg-gray-200 group-hover:bg-secondary-100'
                    ]"
                  >
                    <span :class="quote.design_option === option.id ? 'text-white text-2xl' : 'text-gray-600 text-2xl'">
                      {{ option.name === 'Simple' ? '📄' : option.name === 'Moderne' ? '🎨' : '✨' }}
                    </span>
                  </div>
                  <h3 class="text-xl font-bold text-dark-900 mb-2">{{ option.name }}</h3>
                  <p class="text-sm text-dark-600 mb-4">{{ option.description }}</p>
                  <div 
                    :class="[
                      'text-xl font-bold',
                      quote.design_option === option.id ? 'text-secondary-600' : 'text-dark-800'
                    ]"
                  >
                    + {{ option.price_supplement }} €
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Étape 4 : Niveau de Complexité -->
          <div v-if="currentStep === 4" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-purple-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 mb-2">Complexité</h2>
              <p class="text-dark-600">Niveau de complexité technique du projet</p>
            </div>

            <div class="grid md:grid-cols-3 gap-6">
              <div
                v-for="level in complexityLevels"
                :key="level.id"
                @click="quote.complexity_level = level.id"
                :class="[
                  'cursor-pointer p-6 border-3 rounded-xl transition-all duration-300 group',
                  quote.complexity_level === level.id
                    ? 'border-purple-500 bg-purple-50 shadow-lg scale-105'
                    : 'border-gray-200 hover:border-purple-300 hover:shadow-md'
                ]"
              >
                <div class="text-center">
                  <div 
                    :class="[
                      'w-16 h-16 mx-auto mb-4 rounded-full flex items-center justify-center transition-all',
                      quote.complexity_level === level.id ? 'bg-purple-600' : 'bg-gray-200 group-hover:bg-purple-100'
                    ]"
                  >
                    <span :class="quote.complexity_level === level.id ? 'text-white text-2xl' : 'text-gray-600 text-2xl'">
                      {{ level.name === 'Basique' ? '1️⃣' : level.name === 'Intermédiaire' ? '2️⃣' : '3️⃣' }}
                    </span>
                  </div>
                  <h3 class="text-xl font-bold text-dark-900 mb-2">{{ level.name }}</h3>
                  <p class="text-sm text-dark-600 mb-4">{{ level.description }}</p>
                  <div 
                    :class="[
                      'text-xl font-bold',
                      quote.complexity_level === level.id ? 'text-purple-600' : 'text-dark-800'
                    ]"
                  >
                    × {{ level.price_multiplier }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Étape 5 : Options Supplémentaires -->
          <div v-if="currentStep === 5" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-green-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 mb-2">Options Supplémentaires</h2>
              <p class="text-dark-600">Sélectionnez les services additionnels (optionnel)</p>
            </div>

            <div class="grid md:grid-cols-2 gap-4">
              <div
                v-for="option in supplementaryOptions"
                :key="option.id"
                @click="toggleSupplementaryOption(option.id)"
                :class="[
                  'cursor-pointer p-4 border-2 rounded-lg transition-all duration-300 flex items-start space-x-4',
                  quote.supplementary_options.includes(option.id)
                    ? 'border-green-500 bg-green-50 shadow-md'
                    : 'border-gray-200 hover:border-green-300'
                ]"
              >
                <div class="flex-shrink-0 mt-1">
                  <div 
                    :class="[
                      'w-6 h-6 rounded border-2 flex items-center justify-center transition-colors',
                      quote.supplementary_options.includes(option.id)
                        ? 'bg-green-500 border-green-500'
                        : 'border-gray-300'
                    ]"
                  >
                    <svg v-if="quote.supplementary_options.includes(option.id)" class="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                      <path fill-rule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clip-rule="evenodd"></path>
                    </svg>
                  </div>
                </div>
                <div class="flex-1">
                  <h3 class="font-bold text-dark-900 mb-1">{{ option.name }}</h3>
                  <p class="text-sm text-dark-600 mb-2">{{ option.description }}</p>
                  <p class="text-lg font-bold text-green-600">+ {{ option.price }} €</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Étape 6 : Détails du Projet -->
          <div v-if="currentStep === 6" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-orange-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 mb-2">Détails du Projet</h2>
              <p class="text-dark-600">Parlez-nous de votre vision</p>
            </div>

            <div class="space-y-6">
              <div>
                <label class="block text-sm font-semibold text-dark-700 mb-2">
                  Description du projet <span class="text-red-500">*</span>
                </label>
                <textarea
                  v-model="quote.project_description"
                  rows="6"
                  required
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all resize-none"
                  placeholder="Décrivez votre projet, vos objectifs, votre audience cible, les fonctionnalités souhaitées..."
                ></textarea>
                <p class="mt-2 text-sm text-dark-500">Minimum 10 caractères</p>
              </div>

              <div>
                <label class="block text-sm font-semibold text-dark-700 mb-2">
                  Date limite souhaitée <span class="text-dark-400 text-xs">(optionnel)</span>
                </label>
                <input
                  v-model="quote.deadline"
                  type="date"
                  :min="new Date().toISOString().split('T')[0]"
                  class="w-full px-4 py-3 border-2 border-gray-200 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all"
                />
              </div>
            </div>
          </div>

          <!-- Étape 7 : Récapitulatif -->
          <div v-if="currentStep === 7" class="space-y-6 animate-fade-in">
            <div class="text-center mb-6">
              <div class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
                <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
                </svg>
              </div>
              <h2 class="text-3xl font-bold text-dark-900 mb-2">Récapitulatif</h2>
              <p class="text-dark-600">Vérifiez les informations avant de soumettre</p>
            </div>

            <!-- Summary Card -->
            <div class="bg-gradient-to-br from-primary-50 to-secondary-50 rounded-xl p-6 border-2 border-primary-200">
              <div class="space-y-4">
                <!-- Client Info -->
                <div class="pb-4 border-b border-primary-200">
                  <h3 class="font-bold text-dark-900 mb-3 flex items-center">
                    <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                    </svg>
                    Vos informations
                  </h3>
                  <div class="grid md:grid-cols-2 gap-2 text-sm">
                    <p><span class="font-semibold">Nom:</span> {{ quote.client_name }}</p>
                    <p><span class="font-semibold">Email:</span> {{ quote.client_email }}</p>
                    <p v-if="quote.client_phone"><span class="font-semibold">Téléphone:</span> {{ quote.client_phone }}</p>
                    <p v-if="quote.company_name"><span class="font-semibold">Entreprise:</span> {{ quote.company_name }}</p>
                  </div>
                </div>

                <!-- Project Config -->
                <div class="pb-4 border-b border-primary-200">
                  <h3 class="font-bold text-dark-900 mb-3 flex items-center">
                    <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                    </svg>
                    Configuration
                  </h3>
                  <div class="space-y-2 text-sm">
                    <p><span class="font-semibold">Type:</span> {{ getSelectedProjectType()?.name }}</p>
                    <p><span class="font-semibold">Design:</span> {{ getSelectedDesignOption()?.name }}</p>
                    <p><span class="font-semibold">Complexité:</span> {{ getSelectedComplexityLevel()?.name }}</p>
                    <p v-if="quote.supplementary_options.length > 0">
                      <span class="font-semibold">Options:</span> 
                      <span class="ml-2">{{ getSelectedSupplementaryOptions().map(o => o.name).join(', ') }}</span>
                    </p>
                  </div>
                </div>

                <!-- Price Breakdown -->
                <div>
                  <h3 class="font-bold text-dark-900 mb-3 flex items-center">
                    <svg class="w-5 h-5 mr-2 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z"></path>
                    </svg>
                    Détail du prix
                  </h3>
                  <div class="space-y-2 text-sm">
                    <div class="flex justify-between">
                      <span>Base ({{ getSelectedProjectType()?.name }})</span>
                      <span class="font-semibold">{{ getSelectedProjectType()?.base_price }} €</span>
                    </div>
                    <div class="flex justify-between">
                      <span>Design ({{ getSelectedDesignOption()?.name }})</span>
                      <span class="font-semibold">+ {{ getSelectedDesignOption()?.price_supplement }} €</span>
                    </div>
                    <div class="flex justify-between">
                      <span>Multiplicateur ({{ getSelectedComplexityLevel()?.name }})</span>
                      <span class="font-semibold">× {{ getSelectedComplexityLevel()?.price_multiplier }}</span>
                    </div>
                    <div v-if="getSelectedSupplementaryOptions().length > 0">
                      <div v-for="opt in getSelectedSupplementaryOptions()" :key="opt.id" class="flex justify-between">
                        <span>{{ opt.name }}</span>
                        <span class="font-semibold">+ {{ opt.price }} €</span>
                      </div>
                    </div>
                    <div class="pt-3 mt-3 border-t-2 border-primary-300 flex justify-between items-center">
                      <span class="text-xl font-bold text-dark-900">Total estimé</span>
                      <span class="text-3xl font-bold text-primary-600">{{ calculateTotal() }} €</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Success/Error Messages -->
            <div v-if="successMessage" class="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg">
              <div class="flex items-start">
                <svg class="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                </svg>
                <div>
                  <h4 class="font-bold text-green-800">Devis envoyé avec succès !</h4>
                  <p class="text-sm text-green-700">{{ successMessage }}</p>
                </div>
              </div>
            </div>

            <div v-if="errorMessage" class="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
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
          </div>
        </div>

        <!-- Navigation Buttons -->
        <div class="flex justify-between items-center mt-8">
          <button
            v-if="currentStep > 1"
            @click="prevStep"
            class="inline-flex items-center space-x-2 px-6 py-3 border-2 border-gray-300 text-dark-700 rounded-lg font-semibold hover:bg-gray-50 transition-all duration-300"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
            </svg>
            <span>Précédent</span>
          </button>
          <div v-else></div>

          <button
            v-if="currentStep < 7"
            @click="nextStep"
            :disabled="!canProceed"
            class="btn-primary px-8 py-3 inline-flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span>Suivant</span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
            </svg>
          </button>

          <button
            v-else
            @click="submitQuote"
            :disabled="submitting"
            class="btn-primary px-8 py-3 inline-flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <span v-if="!submitting">Envoyer le devis</span>
            <span v-else class="flex items-center">
              <svg class="animate-spin h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Envoi en cours...
            </span>
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
          </button>
        </div>

        <!-- Price Display (always visible) -->
        <div class="mt-8 bg-gradient-to-r from-primary-600 to-secondary-600 text-white rounded-xl p-6 text-center shadow-xl">
          <p class="text-sm font-medium mb-2 opacity-90">Estimation actuelle</p>
          <p class="text-4xl font-bold">{{ calculateTotal() }} €</p>
          <p class="text-sm mt-2 opacity-75">Prix indicatif • Devis final personnalisé</p>
        </div>
      </div>
    </div>
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

const steps = [
  { number: 1, label: 'Client' },
  { number: 2, label: 'Type' },
  { number: 3, label: 'Design' },
  { number: 4, label: 'Complexité' },
  { number: 5, label: 'Options' },
  { number: 6, label: 'Détails' },
  { number: 7, label: 'Résumé' }
]

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
  
  if (projectType) {
    total = Number(projectType.base_price) || 0
    console.log('Après base price:', total)
  }
  
  if (designOption) {
    total += Number(designOption.price_supplement) || 0
    console.log('Après design option:', total)
  }
  
  if (complexityLevel) {
    total *= Number(complexityLevel.price_multiplier) || 1
    console.log('Après multiplicateur:', total)
  }
  
  if (suppOptions.length > 0) {
    const optionsTotal = suppOptions.reduce((sum, opt) => sum + (Number(opt.price) || 0), 0)
    total += optionsTotal
    console.log('Après options supplémentaires:', total)
  }
  
  const finalTotal = Math.round(total)
  console.log('Total final:', finalTotal)
  
  return finalTotal
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
    
    successMessage.value = 'Votre demande de devis a été envoyée avec succès ! Nous vous contacterons très prochainement.'
    
    setTimeout(() => {
      router.push('/')
    }, 3000)
  } catch (error) {
    console.error('Erreur lors de l\'envoi du devis:', error)
    errorMessage.value = error.response?.data?.detail || 'Une erreur est survenue. Veuillez réessayer.'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  try {
    loadingOptions.value = true
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
    console.error('Erreur lors du chargement des options:', error)
    errorMessage.value = 'Impossible de charger les options. Veuillez rafraîchir la page.'
  } finally {
    loadingOptions.value = false
  }
})
</script>