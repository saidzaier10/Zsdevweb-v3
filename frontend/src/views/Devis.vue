<template>
  <div class="min-h-screen bg-white dark:bg-dark-900 transition-colors duration-200">
    <!-- Header -->
    <section
      class="bg-gradient-to-br from-primary-600 to-secondary-600 dark:from-primary-900 dark:to-secondary-900 text-white py-16">
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
            <span class="text-sm font-semibold text-dark-700 dark:text-dark-200">Étape {{ currentStep }} sur 8</span>
            <span class="text-sm font-semibold text-primary-600 dark:text-primary-400">{{ Math.round((currentStep / 8) *
              100) }}%</span>
          </div>
          <div class="w-full bg-gray-200 dark:bg-dark-700 rounded-full h-3 overflow-hidden">
            <div
              class="bg-gradient-to-r from-primary-600 to-secondary-500 h-full rounded-full transition-all duration-500 ease-out"
              :style="{ width: `${(currentStep / 8) * 100}%` }"></div>
          </div>
        </div>
      </div>
    </section>

    <!-- Form Content -->
    <section class="py-16">
      <div class="container mx-auto px-4 max-w-4xl">
        <LoadingSpinner v-if="loadingOptions" message="Chargement..." class="py-16" />

        <GlassCard v-else class="p-8" variant="default" :hover-effect="false">
          <!-- Étape 1 : Sélection de la catégorie -->
          <div v-if="currentStep === 1" class="animate-fade-in-auto">
            <CategorySelector @category-selected="onCategorySelected" />
          </div>

          <!-- Étape 2 : Informations client -->
          <div v-if="currentStep === 2" class="space-y-6 animate-fade-in-auto">
            <div class="text-center mb-6">
              <div
                class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <IconUser />
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Vos informations</h2>
              <p class="text-dark-600 dark:text-dark-300">Commençons par faire connaissance</p>
            </div>

            <div class="space-y-4">
              <ModernInput id="client_name" v-model="quote.client_name" label="Nom complet" required />

              <ModernInput id="client_email" v-model="quote.client_email" type="email" label="Email" required />

              <ModernInput id="client_phone" v-model="quote.client_phone" type="tel" label="Téléphone (optionnel)" />

              <ModernInput id="company_name" v-model="quote.company_name" label="Entreprise (optionnel)" />
            </div>
          </div>

          <!-- Étape 3 : Type de projet -->
          <div v-if="currentStep === 3" class="space-y-6 animate-fade-in-auto">
            <div class="text-center mb-6">
              <div
                class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <IconProject />
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Type de projet</h2>
              <p class="text-dark-600 dark:text-dark-300">Quel type de site souhaitez-vous ?</p>
            </div>

            <div class="grid md:grid-cols-3 gap-4">
              <SelectionCard v-for="type in projectTypes" :key="type.id" :title="type.name"
                :description="type.description" :price-display="type.base_price + '€'"
                :selected="quote.project_type === type.id" @select="quote.project_type = type.id" />
            </div>
          </div>

          <!-- Étape 4 : Option de design -->
          <div v-if="currentStep === 4" class="space-y-6 animate-fade-in-auto">
            <div class="text-center mb-6">
              <div
                class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <IconDesign />
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Option de design</h2>
              <p class="text-dark-600 dark:text-dark-300">Choisissez le niveau de personnalisation</p>
            </div>

            <div class="grid md:grid-cols-3 gap-4">
              <SelectionCard v-for="option in designOptions" :key="option.id" :title="option.name"
                :description="option.description" :price-display="'+' + option.price_supplement + '€'"
                :selected="quote.design_option === option.id" @select="quote.design_option = option.id" />
            </div>
          </div>

          <!-- Étape 5 : Niveau de complexité -->
          <div v-if="currentStep === 5" class="space-y-6 animate-fade-in-auto">
            <div class="text-center mb-6">
              <div
                class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <IconComplexity />
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Niveau de complexité</h2>
              <p class="text-dark-600 dark:text-dark-300">Définissez les fonctionnalités nécessaires</p>
            </div>

            <div class="grid md:grid-cols-3 gap-4">
              <SelectionCard v-for="level in complexityLevels" :key="level.id" :title="level.name"
                :description="level.description" :price-display="'×' + level.price_multiplier"
                :selected="quote.complexity_level === level.id" @select="quote.complexity_level = level.id" />
            </div>
          </div>

          <!-- Étape 6 : Options supplémentaires -->
          <div v-if="currentStep === 6" class="space-y-6 animate-fade-in-auto">
            <div class="text-center mb-6">
              <div
                class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <IconOptions />
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Options supplémentaires</h2>
              <p class="text-dark-600 dark:text-dark-300">Ajoutez des services complémentaires</p>
            </div>

            <div class="space-y-4">
              <SelectionCard v-for="option in supplementaryOptions" :key="option.id" :title="option.name"
                :description="option.description" :price-display="'+' + option.price + '€'"
                :selected="quote.supplementary_options.includes(option.id)"
                @select="toggleSupplementaryOption(option.id)" class="flex items-center justify-between" />
            </div>
          </div>

          <!-- Étape 7 : Description et deadline -->
          <div v-if="currentStep === 7" class="space-y-6 animate-fade-in-auto">
            <div class="text-center mb-6">
              <div
                class="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4">
                <IconDetails />
              </div>
              <h2 class="text-3xl font-bold text-dark-900 dark:text-white mb-2">Détails du Projet</h2>
              <p class="text-dark-600 dark:text-dark-300">Parlez-nous de votre vision</p>
            </div>

            <div class="space-y-6">
              <ModernInput id="project_description" v-model="quote.project_description" type="textarea"
                label="Description du projet" required rows="6" />
              <p class="mt-2 text-sm text-dark-500 dark:text-dark-400 pl-1">Minimum 10 caractères</p>

              <ModernInput id="deadline" v-model="quote.deadline" type="date" label="Date limite souhaitée (optionnel)"
                :min="new Date().toISOString().split('T')[0]" />
            </div>
          </div>

          <!-- Étape 8 : Récapitulatif -->
          <div v-if="currentStep === 8" class="space-y-6 animate-fade-in-auto">
            <div class="text-center mb-6">
              <div
                class="inline-flex items-center justify-center w-16 h-16 bg-green-100 dark:bg-green-900/30 rounded-full mb-4">
                <IconSummary />
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
              <div
                class="bg-gradient-to-br from-primary-50 to-secondary-50 dark:from-primary-900/20 dark:to-secondary-900/20 rounded-xl p-6 border-2 border-primary-200 dark:border-primary-800">
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
                    <div v-for="opt in getSelectedSupplementaryOptions()" :key="opt.id"
                      class="flex justify-between text-dark-700 dark:text-dark-300">
                      <span>{{ opt.name }}</span>
                      <span class="font-semibold">+ {{ opt.price }} €</span>
                    </div>
                  </div>
                  <div
                    class="pt-3 mt-3 border-t-2 border-primary-300 dark:border-primary-700 flex justify-between items-center">
                    <span class="text-xl font-bold text-dark-900 dark:text-white">Total estimé</span>
                    <span class="text-3xl font-bold text-primary-600 dark:text-primary-400">{{ total }} €</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Success/Error Messages -->
            <div v-if="successMessage"
              class="bg-green-50 dark:bg-green-900/20 border-l-4 border-green-500 p-4 rounded-lg">
              <div class="flex items-start">
                <svg class="h-6 w-6 text-green-500 mr-3 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clip-rule="evenodd"></path>
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
                  <path fill-rule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clip-rule="evenodd"></path>
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
            <ModernButton v-if="currentStep > 1" @click="prevStep" variant="outline" class="flex-1">
              ← Précédent
            </ModernButton>

            <ModernButton v-if="currentStep < 8" @click="nextStep" :disabled="!canProceed" variant="primary"
              class="flex-1">
              Suivant →
            </ModernButton>

            <ModernButton v-if="currentStep === 8" @click="submitQuote" :loading="submitting" loading-text="Envoi..."
              variant="primary"
              class="flex-1 bg-gradient-to-r from-green-600 to-green-500 hover:from-green-700 hover:to-green-600 border-none">
              Envoyer le devis
            </ModernButton>
          </div>
        </GlassCard>

        <!-- Floating Price Display (visible on steps 3-7) -->
        <div v-if="currentStep >= 3 && currentStep <= 7"
          class="mt-8 bg-gradient-to-r from-primary-600 to-secondary-600 dark:from-primary-900 dark:to-secondary-900 text-white rounded-xl p-6 text-center shadow-xl">
          <p class="text-sm font-medium mb-2 opacity-90">Estimation actuelle</p>
          <p class="text-4xl font-bold">{{ total }} €</p>
          <p class="text-sm mt-2 opacity-75">Prix indicatif • Devis final personnalisé</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  getProjectTypes,
  getDesignOptions,
  getComplexityLevels,
  getSupplementaryOptions,
  createQuote
} from '../api/quotes'
import { LoadingSpinner } from '@/components/ui'
import { useApi } from '@/composables/useApi'
import CategorySelector from '../components/CategorySelector.vue'
import GlassCard from '../components/ui/GlassCard.vue'
import ModernInput from '../components/ui/ModernInput.vue'
import ModernButton from '../components/ui/ModernButton.vue'
import SelectionCard from '../components/ui/SelectionCard.vue'

// Icons
import IconUser from '../components/icons/IconUser.vue'
import IconProject from '../components/icons/IconProject.vue'
import IconDesign from '../components/icons/IconDesign.vue'
import IconComplexity from '../components/icons/IconComplexity.vue'
import IconOptions from '../components/icons/IconOptions.vue'
import IconDetails from '../components/icons/IconDetails.vue'
import IconSummary from '../components/icons/IconSummary.vue'

// Composables
import { useQuoteCalculator } from '@/composables/useQuoteCalculator'

const router = useRouter()
const { callApi } = useApi() || {}

const currentStep = ref(1)
const loadingOptions = ref(false)
const submitting = ref(false)
const successMessage = ref('')
const errorMessage = ref('')

const selectedCategory = ref(null)

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

// Initialize calculator composable
const {
  getSelectedProjectType,
  getSelectedDesignOption,
  getSelectedComplexityLevel,
  getSelectedSupplementaryOptions,
  total
} = useQuoteCalculator(quote, {
  projectTypes,
  designOptions,
  complexityLevels,
  supplementaryOptions
})

// Handler for category selection
const onCategorySelected = async (category) => {
  selectedCategory.value = category
  await loadCategoryOptions(category.slug)
  currentStep.value = 2 // Move to next step
}

// Load options filtered by category
const loadCategoryOptions = async (categorySlug) => {
  loadingOptions.value = true

  const response = await callApi(
    () => Promise.all([
      getProjectTypes(categorySlug),
      getDesignOptions(),
      getComplexityLevels(),
      getSupplementaryOptions(categorySlug)
    ]),
    {
      errorMessage: 'Erreur lors du chargement des options'
    }
  )

  if (response) {
    const [types, designs, levels, options] = response
    projectTypes.value = types.data.results || types.data
    designOptions.value = designs.data.results || designs.data
    complexityLevels.value = levels.data.results || levels.data
    supplementaryOptions.value = options.data.results || options.data
  }

  loadingOptions.value = false
}

const canProceed = computed(() => {
  switch (currentStep.value) {
    case 1:
      return selectedCategory.value !== null
    case 2:
      return quote.value.client_name && quote.value.client_email
    case 3:
      return quote.value.project_type !== null
    case 4:
      return quote.value.design_option !== null
    case 5:
      return quote.value.complexity_level !== null
    case 6:
      return true // Options supplémentaires optionnelles
    case 7:
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

// calculateTotal removed (moved to composable)

const nextStep = () => {
  if (canProceed.value && currentStep.value < 8) {
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
  submitting.value = true
  errorMessage.value = ''
  successMessage.value = ''

  const response = await callApi(
    () => createQuote(quote.value),
    {
      successMessage: 'Devis créé et envoyé par email avec succès !',
      errorMessage: "Erreur lors de l'envoi du devis. Veuillez réessayer."
    }
  )

  submitting.value = false

  if (response) {
    successMessage.value = `Votre devis ${response.data.quote_number} a été créé avec succès ! Un email de confirmation a été envoyé à ${quote.value.client_email}.`

    // Rediriger vers la page de mes devis après 2 secondes
    setTimeout(() => {
      router.push('/mes-devis')
    }, 2000)
  } else {
    errorMessage.value = "Erreur lors de l'envoi du devis. Veuillez réessayer."
  }
}
</script>
