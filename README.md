# Zsdevweb v3 - Système de Gestion de Devis et Portfolio

## 📋 Description

**Zsdevweb v3** est une application web complète permettant la gestion de devis clients et l'affichage d'un portfolio professionnel. Ce projet a été conçu dans le cadre de mon cursus scolaire pour démontrer mes compétences en développement Fullstack.

L'application permet aux utilisateurs de :
- Consulter un portfolio de projets et de compétences.
- Demander des devis personnalisés via un formulaire interactif.
- Signer électroniquement les devis.
- Gérer leur profil client.

Pour les administrateurs, elle offre :
- Une gestion complète des devis (création, modification, validation).
- Un tableau de bord des statistiques.
- La gestion du contenu du portfolio (projets, témoignages).

## 🛠 Technologies Utilisées

Ce projet repose sur une architecture moderne et robuste :

### Backend
- **Framework** : Django 5 (Python)
- **API** : Django REST Framework (DRF)
- **Base de données** : PostgreSQL
- **Cache & Files d'attente** : Redis
- **Sécurité** : JWT (JSON Web Tokens), WAF personnalisé

### Frontend
- **Framework** : Vue.js 3
- **Build Tool** : Vite
- **Styling** : Tailwind CSS
- **State Management** : Pinia

### DevOps
- **Conteneurisation** : Docker & Docker Compose
- **Serveur Web** : Nginx (Reverse Proxy)

## 🚀 Installation et Démarrage

### Pré-requis
- Docker et Docker Compose installés sur votre machine.

### Configuration

1. **Cloner le dépôt** (si ce n'est pas déjà fait).

2. **Configurer les variables d'environnement** :
   Copiez le fichier d'exemple `.env.example` vers `.env` :
   ```bash
   cp .env.example .env
   ```
   *Note : Le fichier `.env.example` contient des valeurs par défaut fonctionnelles pour le développement.*

### Lancement avec Docker (Recommandé)

La méthode la plus simple pour lancer le projet est d'utiliser Docker Compose.

1. **Construire et lancer les conteneurs** :
   ```bash
   docker-compose up --build
   ```

2. **Accéder à l'application** :
   - **Frontend (Site Web)** : [http://localhost:5173](http://localhost:5173)
   - **Backend (API)** : [http://localhost:8000/api](http://localhost:8000/api)
   - **Interface d'Administration** : [http://localhost:8000/admin](http://localhost:8000/admin)

3. **Arrêter l'application** :
   ```bash
   docker-compose down
   ```

## 💻 Développement Local (Sans Docker)

Si vous préférez installer les dépendances manuellement :

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Tests

Le projet inclut une suite de tests unitaires complète pour le backend.

Pour lancer les tests via Docker :
```bash
docker-compose run --rm backend python manage.py test
```

## 👤 Auteur

**Said Zaier**
*Étudiant à Holberton School*

---
*Projet réalisé dans le cadre académique - 2025*