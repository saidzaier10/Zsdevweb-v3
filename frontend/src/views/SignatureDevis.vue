<template>
  <div class="min-h-screen bg-gray-50 dark:bg-dark-900 py-12">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
      <!-- Loading -->
      <div v-if="loading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>

      <!-- Devis expiré -->
      <div v-else-if="quote && quote.is_expired" class="bg-white dark:bg-dark-800 rounded-lg shadow-lg p-8 text-center">
        <div class="text-orange-500 mb-4">
          <svg class="mx-auto h-24 w-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Ce devis a expiré
        </h2>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          La date de validité de ce devis est dépassée. Veuillez contacter ZsDevWeb pour obtenir un nouveau devis.
        </p>
        <a
          href="mailto:said.zaier@gmail.com"
          class="inline-block px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
        >
          Contacter ZsDevWeb
        </a>
      </div>

      <!-- Devis déjà signé -->
      <div v-else-if="quote && quote.signed_at" class="bg-white dark:bg-dark-800 rounded-lg shadow-lg p-8 text-center">
        <div class="text-green-500 mb-4">
          <svg class="mx-auto h-24 w-24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
          Devis déjà signé
        </h2>
        <p class="text-gray-600 dark:text-gray-400 mb-2">
          Ce devis a été signé le {{ formatDate(quote.signed_at) }}
        </p>
        <p class="text-gray-600 dark:text-gray-400 mb-6">
          par <strong>{{ quote.signer_name }}</strong>
        </p>
        <img
          v-if="quote.signature_image"
          :src="quote.signature_image"
          alt="Signature"
          class="mx-auto border border-gray-300 dark:border-gray-600 rounded p-2 bg-white max-w-xs"
        />
      </div>

      <!-- Formulaire de signature -->
      <div v-else-if="quote" class="bg-white dark:bg-dark-800 rounded-lg shadow-lg overflow-hidden">
        <!-- Header -->
        <div class="bg-gradient-to-r from-indigo-600 to-indigo-700 px-8 py-6">
          <h1 class="text-3xl font-bold text-white">Signature électronique</h1>
          <p class="text-indigo-100 mt-1">{{ quote.quote_number }}</p>
        </div>

        <!-- Résumé du devis -->
        <div class="px-8 py-6 bg-gray-50 dark:bg-dark-700 border-b border-gray-200 dark:border-gray-600">
          <h2 class="text-xl font-bold text-gray-900 dark:text-white mb-4">Résumé du devis</h2>
          <div class="grid md:grid-cols-2 gap-4">
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Projet</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ quote.project_type_detail?.name }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Montant total</p>
              <p class="text-2xl font-bold text-indigo-600 dark:text-indigo-400">{{ quote.total_ttc }} € TTC</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Valide jusqu'au</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ formatDate(quote.expires_at) }}</p>
            </div>
            <div>
              <p class="text-sm text-gray-500 dark:text-gray-400">Durée estimée</p>
              <p class="font-medium text-gray-900 dark:text-white">{{ quote.estimated_duration_days }} jours</p>
            </div>
          </div>
        </div>

        <!-- Formulaire -->
        <div class="px-8 py-6">
          <form @submit.prevent="submitSignature">
            <!-- Nom du signataire -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nom complet *
              </label>
              <input
                v-model="signerName"
                type="text"
                required
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 dark:bg-dark-700 dark:text-white"
                placeholder="Votre nom complet"
              />
            </div>

            <!-- Canvas de signature -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Signature *
              </label>
              <div class="border-2 border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden bg-white">
                <canvas
                  ref="signatureCanvas"
                  @mousedown="startDrawing"
                  @mousemove="draw"
                  @mouseup="stopDrawing"
                  @mouseleave="stopDrawing"
                  @touchstart="startDrawing"
                  @touchmove="draw"
                  @touchend="stopDrawing"
                  class="w-full cursor-crosshair"
                  width="800"
                  height="200"
                ></canvas>
              </div>
              <button
                type="button"
                @click="clearSignature"
                class="mt-2 text-sm text-indigo-600 hover:text-indigo-700"
              >
                Effacer la signature
              </button>
            </div>

            <!-- Conditions -->
            <div class="mb-6">
              <label class="flex items-start">
                <input
                  v-model="termsAccepted"
                  type="checkbox"
                  required
                  class="mt-1 mr-3 h-5 w-5 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <span class="text-sm text-gray-700 dark:text-gray-300">
                  J'accepte les conditions générales de vente et confirme que les informations de ce devis sont exactes. 
                  Cette signature électronique a la même valeur juridique qu'une signature manuscrite. *
                </span>
              </label>
            </div>

            <!-- Actions -->
            <div class="flex gap-4">
              <button
                type="submit"
                :disabled="submitting || !termsAccepted || !signerName"
                class="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors font-medium disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {{ submitting ? 'Signature en cours...' : 'Signer et accepter le devis' }}
              </button>
              <button
                type="button"
                @click="$router.push('/')"
                class="px-6 py-3 bg-gray-200 dark:bg-dark-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-300 dark:hover:bg-dark-600 transition-colors font-medium"
              >
                Annuler
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPublicQuote, signQuote } from '../api/quotes'
import { useToastStore } from '../stores/toast'

const route = useRoute()
const router = useRouter()
const toastStore = useToastStore()

const quote = ref(null)
const loading = ref(false)
const submitting = ref(false)

const signatureCanvas = ref(null)
const signerName = ref('')
const termsAccepted = ref(false)

let ctx = null
let isDrawing = false

const fetchQuote = async () => {
  loading.value = true
  try {
    const response = await getPublicQuote(route.params.token)
    quote.value = response.data
    
    // Initialiser le canvas après le chargement
    await new Promise(resolve => setTimeout(resolve, 100))
    initCanvas()
  } catch (error) {
    console.error('Erreur chargement devis:', error)
    toastStore.addToast('Devis introuvable ou token invalide', 'error')
    router.push('/')
  } finally {
    loading.value = false
  }
}

const initCanvas = () => {
  if (signatureCanvas.value) {
    ctx = signatureCanvas.value.getContext('2d')
    ctx.strokeStyle = '#000000'
    ctx.lineWidth = 2
    ctx.lineCap = 'round'
    ctx.lineJoin = 'round'
  }
}

const getMousePos = (e) => {
  const rect = signatureCanvas.value.getBoundingClientRect()
  const scaleX = signatureCanvas.value.width / rect.width
  const scaleY = signatureCanvas.value.height / rect.height
  
  if (e.touches && e.touches[0]) {
    return {
      x: (e.touches[0].clientX - rect.left) * scaleX,
      y: (e.touches[0].clientY - rect.top) * scaleY
    }
  }
  
  return {
    x: (e.clientX - rect.left) * scaleX,
    y: (e.clientY - rect.top) * scaleY
  }
}

const startDrawing = (e) => {
  e.preventDefault()
  isDrawing = true
  const pos = getMousePos(e)
  ctx.beginPath()
  ctx.moveTo(pos.x, pos.y)
}

const draw = (e) => {
  if (!isDrawing) return
  e.preventDefault()
  
  const pos = getMousePos(e)
  ctx.lineTo(pos.x, pos.y)
  ctx.stroke()
}

const stopDrawing = () => {
  isDrawing = false
}

const clearSignature = () => {
  ctx.clearRect(0, 0, signatureCanvas.value.width, signatureCanvas.value.height)
}

const submitSignature = async () => {
  if (!signerName.value || !termsAccepted.value) {
    toastStore.addToast('Veuillez remplir tous les champs obligatoires', 'error')
    return
  }

  // Vérifier que la signature n'est pas vide
  const imageData = ctx.getImageData(0, 0, signatureCanvas.value.width, signatureCanvas.value.height)
  const isEmpty = !imageData.data.some(channel => channel !== 0)
  
  if (isEmpty) {
    toastStore.addToast('Veuillez signer dans le cadre prévu', 'error')
    return
  }

  submitting.value = true
  try {
    const signatureData = signatureCanvas.value.toDataURL('image/png')
    
    await signQuote(route.params.token, {
      signature: signatureData,
      signer_name: signerName.value,
      terms_accepted: termsAccepted.value
    })
    
    toastStore.addToast('Devis signé avec succès !', 'success')
    
    // Rediriger après 2 secondes
    setTimeout(() => {
      router.push('/')
    }, 2000)
  } catch (error) {
    console.error('Erreur signature:', error)
    toastStore.addToast(
      error.response?.data?.error || 'Erreur lors de la signature',
      'error'
    )
  } finally {
    submitting.value = false
  }
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('fr-FR', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric'
  })
}

onMounted(() => {
  fetchQuote()
})
</script>