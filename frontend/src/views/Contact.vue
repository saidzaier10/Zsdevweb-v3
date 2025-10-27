<template>
  <div class="min-h-screen bg-white">
    <!-- Header -->
    <section class="bg-black text-white py-16">
      <div class="container mx-auto px-4">
        <h1 class="text-5xl font-bold text-center">Contact</h1>
        <p class="text-xl text-gray-300 text-center mt-4">Discutons de votre projet</p>
      </div>
    </section>

    <section class="py-16">
      <div class="container mx-auto px-4 max-w-4xl">
        <div class="grid md:grid-cols-2 gap-12">
          <!-- Formulaire -->
          <div>
            <h2 class="text-3xl font-bold mb-6">Envoyez-moi un message</h2>
            <form @submit.prevent="submitForm" class="space-y-4">
              <div>
                <label class="block font-bold mb-2">Nom *</label>
                <input v-model="form.name" type="text" required class="w-full border-2 border-black p-3" placeholder="Votre nom">
              </div>
              <div>
                <label class="block font-bold mb-2">Email *</label>
                <input v-model="form.email" type="email" required class="w-full border-2 border-black p-3" placeholder="votre@email.com">
              </div>
              <div>
                <label class="block font-bold mb-2">Téléphone</label>
                <input v-model="form.phone" type="tel" class="w-full border-2 border-black p-3" placeholder="+33 X XX XX XX XX">
              </div>
              <div>
                <label class="block font-bold mb-2">Message *</label>
                <textarea v-model="form.message" required rows="5" class="w-full border-2 border-black p-3" placeholder="Décrivez votre projet..."></textarea>
              </div>
              <button type="submit" class="bg-black text-white px-8 py-3 font-bold hover:bg-gray-800 transition w-full">
                Envoyer le message
              </button>
            </form>
            <p v-if="submitted" class="mt-4 text-green-600 font-bold">Message envoyé avec succès !</p>
          </div>

          <!-- Informations -->
          <div>
            <h2 class="text-3xl font-bold mb-6">Informations</h2>
            <div class="space-y-6">
              <div class="border-2 border-black p-6">
                <h3 class="font-bold text-xl mb-2">Email</h3>
                <p class="text-gray-600">contact@zsdevweb.com</p>
              </div>
              <div class="border-2 border-black p-6">
                <h3 class="font-bold text-xl mb-2">Téléphone</h3>
                <p class="text-gray-600">+33 X XX XX XX XX</p>
              </div>
              <div class="border-2 border-black p-6">
                <h3 class="font-bold text-xl mb-2">Disponibilité</h3>
                <p class="text-gray-600">Lundi - Vendredi<br>9h00 - 18h00</p>
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

const form = ref({
  name: '',
  email: '',
  phone: '',
  message: ''
})

const submitted = ref(false)

const submitForm = () => {
  console.log('Formulaire soumis:', form.value)
  submitted.value = true
  // TODO: Intégrer avec l'API backend plus tard
  setTimeout(() => {
    submitted.value = false
    form.value = { name: '', email: '', phone: '', message: '' }
  }, 3000)
}
</script>