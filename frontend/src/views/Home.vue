<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-black text-white py-32">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-5xl md:text-6xl font-bold mb-6">
          Développeur Web Full Stack
        </h1>
        <p class="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
          Je crée des sites web modernes, performants et sur mesure pour votre entreprise.
        </p>
        <div class="flex gap-4 justify-center">
          <router-link to="/portfolio" class="bg-white text-black px-8 py-3 rounded font-bold hover:bg-gray-200 transition">
            Voir mes projets
          </router-link>
          <router-link to="/devis" class="border-2 border-white px-8 py-3 rounded font-bold hover:bg-white hover:text-black transition">
            Demander un devis
          </router-link>
        </div>
      </div>
    </section>

    <!-- Services Section -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <h2 class="text-4xl font-bold text-center mb-12">Mes Services</h2>
        <div class="grid md:grid-cols-3 gap-8">
          <div class="border-2 border-black p-8 text-center hover:bg-black hover:text-white transition">
            <h3 class="text-2xl font-bold mb-4">Sites Vitrines</h3>
            <p class="text-gray-600">Sites de présentation élégants et professionnels pour votre activité.</p>
          </div>
          <div class="border-2 border-black p-8 text-center hover:bg-black hover:text-white transition">
            <h3 class="text-2xl font-bold mb-4">E-commerce</h3>
            <p class="text-gray-600">Boutiques en ligne complètes avec paiement sécurisé.</p>
          </div>
          <div class="border-2 border-black p-8 text-center hover:bg-black hover:text-white transition">
            <h3 class="text-2xl font-bold mb-4">Applications Web</h3>
            <p class="text-gray-600">Applications web sur mesure adaptées à vos besoins.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="bg-black text-white py-16">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-4xl font-bold mb-6">Prêt à démarrer votre projet ?</h2>
        <p class="text-xl text-gray-300 mb-8">Obtenez un devis gratuit en quelques minutes.</p>
        <router-link to="/devis" class="bg-white text-black px-8 py-3 rounded font-bold hover:bg-gray-200 transition inline-block">
          Obtenir un devis
        </router-link>
      </div>
    </section>
  </div>
</template>