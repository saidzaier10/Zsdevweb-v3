# Zsdevweb v3

Application web de portfolio et de gestion de devis pour freelance.

## Fonctionnalités

- **Portfolio** : Présentation des projets réalisés avec filtrage par technologies.
- **Calculateur de Devis** : Estimation de prix interactive et personnalisée pour les clients.
- **Gestion de Contact** : Formulaire de contact sécurisé.
- **Administration** : Interface complète pour gérer les projets, les devis et les messages.

## Technologies

### Frontend
- **Vue.js 3** (Composition API)
- **Vite** (Build tool)
- **Tailwind CSS** (Styling)

### Backend
- **Python** & **Django**
- **Django REST Framework** (API)
- **PostgreSQL** (Base de données)
- **Redis** (Cache)

## Installation

### Avec Docker (Recommandé)

1. Clonez le projet :
   ```bash
   git clone <votre-repo>
   cd Zsdevwebv3
   ```

2. Lancez les conteneurs :
   ```bash
   docker-compose up --build
   ```

3. Accédez à l'application :
   - **Frontend** : http://localhost:5173
   - **Backend API** : http://localhost:8000
   - **Admin** : http://localhost:8000/admin

### Développement Local

#### Backend

1. Naviguez dans le dossier backend :
   ```bash
   cd backend
   ```

2. Créez et activez un environnement virtuel :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Lancez le serveur :
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

#### Frontend

1. Naviguez dans le dossier frontend :
   ```bash
   cd frontend
   ```

2. Installez les dépendances :
   ```bash
   npm install
   ```

3. Lancez le serveur de développement :
   ```bash
   npm run dev
   ```