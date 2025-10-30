<template>
  <div class="signature-container">
    <div class="container mx-auto px-4 py-8">
      <!-- Loader -->
      <div v-if="loading" class="flex justify-center items-center min-h-screen">
        <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-indigo-600"></div>
      </div>

      <!-- Erreur -->
      <div v-else-if="error" class="max-w-2xl mx-auto">
        <div class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 text-center">
          <svg class="mx-auto h-12 w-12 text-red-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <h3 class="text-lg font-medium text-red-800 dark:text-red-200 mb-2">Erreur</h3>
          <p class="text-red-600 dark:text-red-300">{{ error }}</p>
        </div>
      </div>

      <!-- Devis déjà signé -->
      <div v-else-if="quote && quote.status === 'accepted'" class="max-w-2xl mx-auto">
        <div class="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6 text-center">
          <svg class="mx-auto h-12 w-12 text-green-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="text-lg font-medium text-green-800 dark:text-green-200 mb-2">Devis déjà signé</h3>
          <p class="text-green-600 dark:text-green-300">Ce devis a déjà été signé le {{ formatDate(quote.signed_at) }}</p>
        </div>
      </div>

      <!-- Devis expiré -->
      <div v-else-if="quote && isExpired" class="max-w-2xl mx-auto">
        <div class="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800 rounded-lg p-6 text-center">
          <svg class="mx-auto h-12 w-12 text-orange-500 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="text-lg font-medium text-orange-800 dark:text-orange-200 mb-2">Devis expiré</h3>
          <p class="text-orange-600 dark:text-orange-300">Ce devis a expiré le {{ formatDate(quote.valid_until) }}</p>
          <p class="text-sm text-orange-500 dark:text-orange-400 mt-2">Veuillez contacter ZsDevWeb pour obtenir un nouveau devis.</p>
        </div>
      </div>

      <!-- Formulaire de signature -->
      <div v-else-if="quote" class="max-w-4xl mx-auto">
        <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">Signature du devis</h1>
          <p class="text-gray-600 dark:text-gray-400 mb-8">{{ quote.quote_number }}</p>

          <!-- Récapitulatif du devis -->
          <div class="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 mb-8">
            <h2 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Récapitulatif</h2>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-700 dark:text-gray-300">Client</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ quote.client_name }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700 dark:text-gray-300">Montant total TTC</span>
                <span class="font-bold text-2xl text-indigo-600 dark:text-indigo-400">{{ formatPrice(quote.total_ttc) }} €</span>
              </div>
              <div v-if="quote.monthly_subscription_total > 0" class="flex justify-between">
                <span class="text-gray-700 dark:text-gray-300">Abonnement mensuel</span>
                <span class="font-semibold text-indigo-600 dark:text-indigo-400">{{ formatPrice(quote.monthly_subscription_total) }} €/mois</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700 dark:text-gray-300">Valide jusqu'au</span>
                <span class="font-medium text-gray-900 dark:text-white">{{ formatDate(quote.valid_until) }}</span>
              </div>
            </div>
          </div>

          <!-- Formulaire -->
          <form @submit.prevent="submitSignature" class="space-y-6">
            <!-- Nom complet -->
            <div>
              <label for="fullName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Nom complet <span class="text-red-500">*</span>
              </label>
              <input
                id="fullName"
                v-model="form.fullName"
                type="text"
                required
                placeholder="Votre nom complet"
                class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
              />
            </div>

            <!-- Canvas de signature -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Signature <span class="text-red-500">*</span>
              </label>
              <div class="border-2 border-gray-300 dark:border-gray-600 rounded-lg overflow-hidden bg-white">
                <canvas
                  ref="signatureCanvas"
                  @mousedown="startDrawing"
                  @mousemove="draw"
                  @mouseup="stopDrawing"
                  @mouseleave="stopDrawing"
                  @touchstart.prevent="startDrawing"
                  @touchmove.prevent="draw"
                  @touchend.prevent="stopDrawing"
                  class="w-full cursor-crosshair"
                  :width="canvasWidth"
                  :height="canvasHeight"
                ></canvas>
              </div>
              <div class="flex justify-end mt-2">
                <button
                  type="button"
                  @click="clearSignature"
                  class="text-sm text-indigo-600 dark:text-indigo-400 hover:underline"
                >
                  Effacer la signature
                </button>
              </div>
              <p v-if="signatureError" class="text-red-500 text-sm mt-1">{{ signatureError }}</p>
            </div>

            <!-- Acceptation des conditions -->
            <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
              <div class="flex items-start">
                <input
                  id="acceptTerms"
                  v-model="form.acceptTerms"
                  type="checkbox"
                  required
                  class="mt-1 h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded"
                />
                <label for="acceptTerms" class="ml-3 text-sm text-gray-700 dark:text-gray-300">
                  J'accepte les termes et conditions de ce devis. En signant, je reconnais avoir pris connaissance de l'ensemble des éléments du devis et je m'engage à respecter les conditions de paiement et de réalisation du projet. <span class="text-red-500">*</span>
                </label>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex gap-4">
              <button
                type="submit"
                :disabled="submitting || !form.acceptTerms"
                class="flex-1 px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors font-medium"
              >
                {{ submitting ? 'Signature en cours...' : 'Accepter et signer le devis' }}
              </button>
              <button
                type="button"
                @click="rejectQuote"
                :disabled="submitting"
                class="px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                Refuser
              </button>
            </div>
          </form>
        </div>

        <!-- Informations de contact -->
        <div class="mt-6 text-center text-sm text-gray-600 dark:text-gray-400">
          <p>Des questions ? Contactez-nous à <a href="mailto:contact@zsdevweb.com" class="text-indigo-600 dark:text-indigo-400 hover:underline">contact@zsdevweb.com</a></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { getPublicQuote, signQuote } from '@/api/quotes'
import { useToastStore } from '@/stores/toast'

const route = useRoute()
const router = useRouter()
const toast = useToastStore()

const quote = ref(null)
const loading = ref(true)
const error = ref(null)
const submitting = ref(false)

const form = ref({
  fullName: '',
  acceptTerms: false
})

// Canvas
const signatureCanvas = ref(null)
const canvasWidth = 800
const canvasHeight = 200
const isDrawing = ref(false)
const hasSignature = ref(false)
const signatureError = ref(null)
let ctx = null

// Computed
const isExpired = computed(() => {
  if (!quote.value) return false
  return new Date(quote.value.valid_until) < new Date()
})

// Methods
const fetchQuote = async () => {
  try {
    loading.value = true
    error.value = null
    const response = await getPublicQuote(route.params.token)
    quote.value = response.data
    
    // Pré-remplir le nom si disponible
    if (quote.value.client_name) {
      form.value.fullName = quote.value.client_name
    }
  } catch (err) {
    console.error('Erreur lors de la récupération du devis:', err)
    error.value = err.response?.data?.detail || 'Devis introuvable ou lien invalide'
  } finally {
    loading.value = false
  }
}

const initCanvas = () => {
  if (!signatureCanvas.value) return
  
  ctx = signatureCanvas.value.getContext('2d')
  ctx.strokeStyle = '#000000'
  ctx.lineWidth = 2
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
}

const getMousePos = (e) => {
  const rect = signatureCanvas.value.getBoundingClientRect()
  const scaleX = canvasWidth / rect.width
  const scaleY = canvasHeight / rect.height
  
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
  isDrawing.value = true
  hasSignature.value = true
  signatureError.value = null
  
  const pos = getMousePos(e)
  ctx.beginPath()
  ctx.moveTo(pos.x, pos.y)
}

const draw = (e) => {
  if (!isDrawing.value) return
  
  const pos = getMousePos(e)
  ctx.lineTo(pos.x, pos.y)
  ctx.stroke()
}

const stopDrawing = () => {
  if (!isDrawing.value) return
  isDrawing.value = false
  ctx.closePath()
}

const clearSignature = () => {
  ctx.clearRect(0, 0, canvasWidth, canvasHeight)
  hasSignature.value = false
  signatureError.value = null
}

const validateSignature = () => {
  if (!hasSignature.value) {
    signatureError.value = 'Veuillez signer avant de continuer'
    return false
  }
  
  // Vérifier que le canvas n'est pas vide
  const imageData = ctx.getImageData(0, 0, canvasWidth, canvasHeight)
  const pixels = imageData.data
  let hasContent = false
  
  for (let i = 0; i < pixels.length; i += 4) {
    if (pixels[i + 3] > 0) {
      hasContent = true
      break
    }
  }
  
  if (!hasContent) {
    signatureError.value = 'La signature ne peut pas être vide'
    return false
  }
  
  return true
}

const submitSignature = async () => {
  if (!validateSignature()) {
    return
  }
  
  try {
    submitting.value = true
    
    // Convertir la signature en base64
    const signatureDataUrl = signatureCanvas.value.toDataURL('image/png')
    
    const signatureData = {
      signature_name: form.value.fullName,
      signature_image: signatureDataUrl,
      ip_address: '' // Sera rempli par le backend
    }
    
    await signQuote(route.params.token, signatureData)
    
    toast.success('Devis signé', 'Merci ! Vous allez recevoir une confirmation par email.')
    
    // Rediriger vers une page de confirmation ou afficher un message
    setTimeout(() => {
      // Redirection vers page de succès ou home
      router.push('/')
    }, 2000)
    
  } catch (err) {
    console.error('Erreur lors de la signature:', err)
    toast.error('Erreur', err.response?.data?.detail || 'Impossible de signer le devis')
  } finally {
    submitting.value = false
  }
}

const rejectQuote = async () => {
  if (!confirm('Êtes-vous sûr de vouloir refuser ce devis ?')) {
    return
  }
  
  try {
    submitting.value = true
    
    // Appeler l'endpoint de rejet (à implémenter dans l'API)
    await signQuote(route.params.token, { status: 'rejected' })
    
    toast.success('Devis refusé', 'Merci de nous avoir informés.')
    
    setTimeout(() => {
      router.push('/')
    }, 2000)
    
  } catch (err) {
    console.error('Erreur lors du refus:', err)
    toast.error('Erreur', 'Impossible de refuser le devis')
  } finally {
    submitting.value = false
  }
}

const formatDate = (dateString) => {
  if (!dateString) return '-'
  const date = new Date(dateString)
  return new Intl.DateTimeFormat('fr-FR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date)
}

const formatPrice = (price) => {
  if (!price) return '0.00'
  return parseFloat(price).toFixed(2)
}

onMounted(() => {
  fetchQuote()
  initCanvas()
})

onBeforeUnmount(() => {
  // Cleanup
  if (isDrawing.value) {
    stopDrawing()
  }
})
</script>

<style scoped>
.signature-container {
  min-height: calc(100vh - 64px);
  background-color: #f9fafb;
}

.dark .signature-container {
  background-color: #111827;
}

canvas {
  touch-action: none;
}
</style>