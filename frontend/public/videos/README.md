# 🎬 Vidéos de Fond

## Placement de la vidéo

Placez votre vidéo de fond d'accueil dans ce dossier avec le nom :
- `hero-background.mp4` (format principal)
- `hero-background.webm` (optionnel, pour meilleure compatibilité)

## 🔧 Activation de la vidéo

Une fois votre vidéo placée ici, vous devez activer son affichage en ajoutant du code JavaScript dans `Home.vue`.

**Ajoutez ce code dans la section `<script setup>` de Home.vue :**

```javascript
// Référence pour la vidéo
const heroVideo = ref(null)
const videoContainer = ref(null)

// Fonction pour créer et insérer la vidéo dynamiquement
const loadVideo = () => {
  const video = document.createElement('video')
  video.ref = 'heroVideo'
  video.autoplay = true
  video.muted = true
  video.loop = true
  video.playsInline = true
  video.className = 'absolute inset-0 w-full h-full object-cover scale-110'
  video.style.filter = 'blur(0px)'

  // Ajouter les sources
  const mp4Source = document.createElement('source')
  mp4Source.src = '/videos/hero-background.mp4'
  mp4Source.type = 'video/mp4'
  video.appendChild(mp4Source)

  // Source WebM optionnelle
  const webmSource = document.createElement('source')
  webmSource.src = '/videos/hero-background.webm'
  webmSource.type = 'video/webm'
  video.appendChild(webmSource)

  // Ralentir la vidéo pour un effet élégant
  video.playbackRate = 0.5 // ⭐ Ajustez cette valeur

  // Insérer la vidéo en premier dans le conteneur
  const container = document.querySelector('.hero-video-container')
  if (container) {
    container.insertBefore(video, container.firstChild)
  }

  heroVideo.value = video
}

// Dans onMounted, ajoutez :
onMounted(() => {
  loadStatistics()
  loadVideo() // ⭐ Charger la vidéo
})
```

**Et ajoutez une classe à votre conteneur de vidéo dans le template :**

```vue
<div class="absolute inset-0 w-full h-full overflow-hidden hero-video-container">
```

## ⚙️ Configuration de la Vitesse

Vitesses recommandées pour `playbackRate` :
- `0.25` = Ultra lent (très cinématique)
- `0.5` = Lent (élégant) ⭐ **Recommandé**
- `0.75` = Moyennement lent
- `1.0` = Vitesse normale

## Recommandations

### Format et Qualité
- **Format recommandé** : MP4 (H.264) pour compatibilité maximale
- **Résolution** : 1920x1080 (Full HD) ou 1280x720 (HD)
- **Durée** : 10-30 secondes en boucle
- **Poids** : < 5 Mo pour un chargement rapide
- **FPS** : 24-30 fps

### Contenu de la Vidéo
Pour une vidéo de fond professionnelle :
- ✅ Mouvements lents et fluides
- ✅ Pas de texte ou d'éléments distrayants
- ✅ Tonalités neutres ou en accord avec votre palette (bleu/teal)
- ✅ Bonne visibilité : éviter les zones trop sombres ou trop claires
- ❌ Éviter les mouvements brusques
- ❌ Éviter les couleurs trop saturées

### Exemples de vidéos adaptées
- Code qui s'écrit
- Particules animées
- Abstrait géométrique
- Cityscape time-lapse
- Workspace en action

## Sources de Vidéos Gratuites

### Sites recommandés :
1. **Pexels Videos** : https://www.pexels.com/videos/
2. **Pixabay** : https://pixabay.com/videos/
3. **Coverr** : https://coverr.co/
4. **Videvo** : https://www.videvo.net/

### Recherches suggérées :
- "coding abstract"
- "technology background"
- "digital particles"
- "blue abstract"
- "tech workspace"

## Optimisation de la Vidéo

Si votre vidéo est trop lourde, utilisez **FFmpeg** pour la compresser :

```bash
# Installer FFmpeg (macOS)
brew install ffmpeg

# Compresser une vidéo
ffmpeg -i input.mp4 -vcodec h264 -crf 28 -preset fast hero-background.mp4

# Convertir en WebM (optionnel)
ffmpeg -i hero-background.mp4 -c:v libvpx-vp9 -b:v 1M hero-background.webm
```

### Options de compression :
- `-crf 28` : Qualité (18-28, plus bas = meilleure qualité)
- `-preset fast` : Vitesse d'encodage
- `-b:v 1M` : Bitrate (ajuster selon besoin)

## Fallback

Si aucune vidéo n'est placée ici, l'accueil utilisera automatiquement :
- Un fond gradient animé (bleu → teal)
- Des blobs animés pour l'effet dynamique

## Test

Après avoir placé votre vidéo :
1. Rechargez la page d'accueil
2. Vérifiez que la vidéo se lit en boucle
3. Testez sur mobile (la vidéo doit s'adapter)
4. Vérifiez que le texte reste lisible

---

**Note** : La vidéo est automatiquement en mode `muted` (silencieux) et `autoplay` pour respecter les bonnes pratiques web.
