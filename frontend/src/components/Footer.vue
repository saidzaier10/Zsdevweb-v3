<template>
  <footer class="bg-black text-white py-8 mt-16">
    <div class="container mx-auto px-4">
      <div class="grid md:grid-cols-3 gap-8">
        <!-- Colonne 1 -->
        <div>
          <h3 class="text-xl font-bold mb-4">Zsdevweb</h3>
          <p class="text-gray-400">Développement web professionnel et sur mesure.</p>
        </div>
        
        <!-- Colonne 2 -->
        <div>
          <h3 class="text-xl font-bold mb-4">Liens rapides</h3>
          <ul class="space-y-2">
            <li><router-link to="/" class="text-gray-400 hover:text-white transition">Accueil</router-link></li>
            <li><router-link to="/portfolio" class="text-gray-400 hover:text-white transition">Portfolio</router-link></li>
            <li><router-link to="/devis" class="text-gray-400 hover:text-white transition">Devis</router-link></li>
            <li><router-link to="/contact" class="text-gray-400 hover:text-white transition">Contact</router-link></li>
          </ul>
        </div>
        
        <!-- Colonne 3 -->
        <div>
          <h3 class="text-xl font-bold mb-4">Contact</h3>
          <ul class="space-y-2 text-gray-400">
            <li>Email: contact@zsdevweb.com</li>
            <li>Tél: +33 X XX XX XX XX</li>
          </ul>
        </div>
      </div>
      
      <div class="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
        <p>&copy; {{ new Date().getFullYear() }} Zsdevweb. Tous droits réservés.</p>
      </div>
    </div>
  </footer>
</template>