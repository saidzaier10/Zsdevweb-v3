<template>
  <div class="min-h-screen bg-white">
    <!-- Header -->
    <section class="bg-black text-white py-16">
      <div class="container mx-auto px-4">
        <h1 class="text-5xl font-bold text-center">Calculateur de Devis</h1>
        <p class="text-xl text-gray-300 text-center mt-4">Obtenez une estimation instantanée pour votre projet</p>
      </div>
    </section>

    <!-- Formulaire -->
    <section class="py-16">
      <div class="container mx-auto px-4 max-w-4xl">
        <div v-if="loading" class="text-center py-16">
          <p class="text-xl">Chargement...</p>
        </div>

        <div v-else class="border-2 border-black p-8">
          <!-- Étape 1 : Informations client -->
          <div v-if="step === 1" class="space-y-6">
            <h2 class="text-3xl font-bold mb-6">1. Vos informations</h2>
            
            <div>
              <label class="block font-bold mb-2">Nom *</label>
              <input v-model="form.client_name" type="text" required class="w-full border-2 border-black p-3" placeholder="Votre nom">
            </div>

            <div>
              <label class="block font-bold mb-2">Email *</label>
              <input v-model="form.client_email" type="email" required class="w-full border-2 border-black p-3" placeholder="votre@email.com">
            </div>

            <div>
              <label class="block font-bold mb-2">Téléphone</label>
              <input v-model="form.client_phone" type="tel" class="w-full border-2 border-black p-3" placeholder="+33 X XX XX XX XX">
            </div>

            <div>
              <label class="block font-bold mb-2">Entreprise</label>
              <input v-model="form.company_name" type="text" class="w-full border-2 border-black p-3" placeholder="Nom de votre entreprise">
            </div>

            <button @click="nextStep" class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition w-full">
              Suivant
            </button>
          </div>

          <!-- Étape 2 : Type de projet -->
          <div v-if="step === 2" class="space-y-6">
            <h2 class="text-3xl font-bold mb-6">2. Type de projet</h2>
            
            <div class="grid md:grid-cols-3 gap-4">
              <div 
                v-for="type in projectTypes" 
                :key="type.id"
                @click="selectProjectType(type)"
                :class="[
                  'border-2 p-6 cursor-pointer transition',
                  form.project_type === type.id ? 'bg-black text-white border-black' : 'border-black hover:bg-gray-100'
                ]"
              >
                <h3 class="text-xl font-bold mb-2">{{ type.name }}</h3>
                <p class="mb-4 text-sm" :class="form.project_type === type.id ? 'text-gray-300' : 'text-gray-600'">
                  {{ type.description }}
                </p>
                <p class="text-2xl font-bold">{{ type.base_price }}€</p>
              </div>
            </div>

            <div class="flex gap-4">
              <button @click="prevStep" class="border-2 border-black px-8 py-3 font-bold hover:bg-gray-100 transition flex-1">
                Précédent
              </button>
              <button @click="nextStep" :disabled="!form.project_type" class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition flex-1 disabled:bg-gray-400">
                Suivant
              </button>
            </div>
          </div>

          <!-- Étape 3 : Option de design -->
          <div v-if="step === 3" class="space-y-6">
            <h2 class="text-3xl font-bold mb-6">3. Option de design</h2>
            
            <div class="grid md:grid-cols-3 gap-4">
              <div 
                v-for="option in designOptions" 
                :key="option.id"
                @click="selectDesignOption(option)"
                :class="[
                  'border-2 p-6 cursor-pointer transition',
                  form.design_option === option.id ? 'bg-black text-white border-black' : 'border-black hover:bg-gray-100'
                ]"
              >
                <h3 class="text-xl font-bold mb-2">{{ option.name }}</h3>
                <p class="mb-4 text-sm" :class="form.design_option === option.id ? 'text-gray-300' : 'text-gray-600'">
                  {{ option.description }}
                </p>
                <p class="text-2xl font-bold">+{{ option.price_supplement }}€</p>
              </div>
            </div>

            <div class="flex gap-4">
              <button @click="prevStep" class="border-2 border-black px-8 py-3 font-bold hover:bg-gray-100 transition flex-1">
                Précédent
              </button>
              <button @click="nextStep" :disabled="!form.design_option" class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition flex-1 disabled:bg-gray-400">
                Suivant
              </button>
            </div>
          </div>

          <!-- Étape 4 : Niveau de complexité -->
          <div v-if="step === 4" class="space-y-6">
            <h2 class="text-3xl font-bold mb-6">4. Niveau de complexité</h2>
            
            <div class="grid md:grid-cols-3 gap-4">
              <div 
                v-for="level in complexityLevels" 
                :key="level.id"
                @click="selectComplexityLevel(level)"
                :class="[
                  'border-2 p-6 cursor-pointer transition',
                  form.complexity_level === level.id ? 'bg-black text-white border-black' : 'border-black hover:bg-gray-100'
                ]"
              >
                <h3 class="text-xl font-bold mb-2">{{ level.name }}</h3>
                <p class="mb-4 text-sm" :class="form.complexity_level === level.id ? 'text-gray-300' : 'text-gray-600'">
                  {{ level.description }}
                </p>
                <p class="text-2xl font-bold">x{{ level.price_multiplier }}</p>
              </div>
            </div>

            <div class="flex gap-4">
              <button @click="prevStep" class="border-2 border-black px-8 py-3 font-bold hover:bg-gray-100 transition flex-1">
                Précédent
              </button>
              <button @click="nextStep" :disabled="!form.complexity_level" class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition flex-1 disabled:bg-gray-400">
                Suivant
              </button>
            </div>
          </div>

          <!-- Étape 5 : Options supplémentaires -->
          <div v-if="step === 5" class="space-y-6">
            <h2 class="text-3xl font-bold mb-6">5. Options supplémentaires</h2>
            
            <div class="space-y-4">
              <div 
                v-for="option in supplementaryOptions" 
                :key="option.id"
                @click="toggleSupplementaryOption(option.id)"
                :class="[
                  'border-2 p-6 cursor-pointer transition flex justify-between items-center',
                  form.supplementary_options.includes(option.id) ? 'bg-black text-white border-black' : 'border-black hover:bg-gray-100'
                ]"
              >
                <div>
                  <h3 class="text-xl font-bold mb-1">{{ option.name }}</h3>
                  <p class="text-sm" :class="form.supplementary_options.includes(option.id) ? 'text-gray-300' : 'text-gray-600'">
                    {{ option.description }}
                  </p>
                </div>
                <p class="text-2xl font-bold">+{{ option.price }}€</p>
              </div>
            </div>

            <div class="flex gap-4">
              <button @click="prevStep" class="border-2 border-black px-8 py-3 font-bold hover:bg-gray-100 transition flex-1">
                Précédent
              </button>
              <button @click="nextStep" class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition flex-1">
                Suivant
              </button>
            </div>
          </div>

          <!-- Étape 6 : Description et deadline -->
          <div v-if="step === 6" class="space-y-6">
            <h2 class="text-3xl font-bold mb-6">6. Détails du projet</h2>
            
            <div>
              <label class="block font-bold mb-2">Description du projet *</label>
              <textarea v-model="form.project_description" required rows="5" class="w-full border-2 border-black p-3" placeholder="Décrivez votre projet en détail..."></textarea>
            </div>

            <div>
              <label class="block font-bold mb-2">Date limite souhaitée</label>
              <input v-model="form.deadline" type="date" class="w-full border-2 border-black p-3">
            </div>

            <div class="flex gap-4">
              <button @click="prevStep" class="border-2 border-black px-8 py-3 font-bold hover:bg-gray-100 transition flex-1">
                Précédent
              </button>
              <button @click="nextStep" class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition flex-1">
                Voir le récapitulatif
              </button>
            </div>
          </div>

          <!-- Étape 7 : Récapitulatif et soumission -->
          <div v-if="step === 7" class="space-y-6">
            <h2 class="text-3xl font-bold mb-6">7. Récapitulatif</h2>
            
            <div class="bg-gray-100 p-6 space-y-4">
              <div class="flex justify-between">
                <span class="font-bold">Type de projet :</span>
                <span>{{ getProjectTypeName() }}</span>
              </div>
              <div class="flex justify-between">
                <span class="font-bold">Option de design :</span>
                <span>{{ getDesignOptionName() }}</span>
              </div>
              <div class="flex justify-between">
                <span class="font-bold">Niveau de complexité :</span>
                <span>{{ getComplexityLevelName() }}</span>
              </div>
              <div v-if="form.supplementary_options.length > 0" class="border-t pt-4">
                <p class="font-bold mb-2">Options supplémentaires :</p>
                <ul class="list-disc list-inside">
                  <li v-for="optionId in form.supplementary_options" :key="optionId">
                    {{ getSupplementaryOptionName(optionId) }}
                  </li>
                </ul>
              </div>
              <div class="border-t pt-4">
                <div class="flex justify-between text-3xl font-bold">
                  <span>Prix total estimé :</span>
                  <span>{{ calculateTotal() }}€</span>
                </div>
              </div>
            </div>

            <p v-if="submitError" class="text-red-600 font-bold">{{ submitError }}</p>
            <p v-if="submitSuccess" class="text-green-600 font-bold">✓ Devis envoyé avec succès !</p>

            <div class="flex gap-4">
              <button @click="prevStep" class="border-2 border-black px-8 py-3 font-bold hover:bg-gray-100 transition flex-1">
                Précédent
              </button>
              <button @click="submitQuote" :disabled="submitting" class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition flex-1 disabled:bg-gray-400">
                {{ submitting ? 'Envoi...' : 'Envoyer le devis' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import quotesAPI from '../api/quotes'

const router = useRouter()

const step = ref(1)
const loading = ref(true)
const submitting = ref(false)
const submitError = ref('')
const submitSuccess = ref(false)

const projectTypes = ref([])
const designOptions = ref([])
const complexityLevels = ref([])
const supplementaryOptions = ref([])

const form = ref({
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

onMounted(async () => {
  try {
    const [types, designs, levels, options] = await Promise.all([
      quotesAPI.getProjectTypes(),
      quotesAPI.getDesignOptions(),
      quotesAPI.getComplexityLevels(),
      quotesAPI.getSupplementaryOptions()
    ])
    
    projectTypes.value = types.data.results || types.data
    designOptions.value = designs.data.results || designs.data
    complexityLevels.value = levels.data.results || levels.data
    supplementaryOptions.value = options.data.results || options.data
  } catch (error) {
    console.error('Erreur lors du chargement:', error)
  } finally {
    loading.value = false
  }
})

const nextStep = () => {
  if (step.value < 7) step.value++
}

const prevStep = () => {
  if (step.value > 1) step.value--
}

const selectProjectType = (type) => {
  form.value.project_type = type.id
}

const selectDesignOption = (option) => {
  form.value.design_option = option.id
}

const selectComplexityLevel = (level) => {
  form.value.complexity_level = level.id
}

const toggleSupplementaryOption = (optionId) => {
  const index = form.value.supplementary_options.indexOf(optionId)
  if (index > -1) {
    form.value.supplementary_options.splice(index, 1)
  } else {
    form.value.supplementary_options.push(optionId)
  }
}

const getProjectTypeName = () => {
  const type = projectTypes.value.find(t => t.id === form.value.project_type)
  return type ? `${type.name} (${type.base_price}€)` : ''
}

const getDesignOptionName = () => {
  const option = designOptions.value.find(o => o.id === form.value.design_option)
  return option ? `${option.name} (+${option.price_supplement}€)` : ''
}

const getComplexityLevelName = () => {
  const level = complexityLevels.value.find(l => l.id === form.value.complexity_level)
  return level ? `${level.name} (x${level.price_multiplier})` : ''
}

const getSupplementaryOptionName = (optionId) => {
  const option = supplementaryOptions.value.find(o => o.id === optionId)
  return option ? `${option.name} (+${option.price}€)` : ''
}

const calculateTotal = () => {
  const projectType = projectTypes.value.find(t => t.id === form.value.project_type)
  const designOption = designOptions.value.find(o => o.id === form.value.design_option)
  const complexityLevel = complexityLevels.value.find(l => l.id === form.value.complexity_level)
  
  if (!projectType || !designOption || !complexityLevel) return 0
  
  // Convertir en nombres avec parseFloat
  let total = parseFloat(projectType.base_price) + parseFloat(designOption.price_supplement)
  total = total * parseFloat(complexityLevel.price_multiplier)
  
  form.value.supplementary_options.forEach(optionId => {
    const option = supplementaryOptions.value.find(o => o.id === optionId)
    if (option) total += parseFloat(option.price)
  })
  
  return Math.round(total)
}

const submitQuote = async () => {
  submitting.value = true
  submitError.value = ''
  submitSuccess.value = false
  
  try {
    await quotesAPI.createQuote(form.value)
    submitSuccess.value = true
    
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (error) {
    submitError.value = 'Erreur lors de l\'envoi du devis. Veuillez réessayer.'
    console.error('Erreur:', error)
  } finally {
    submitting.value = false
  }
}
</script>