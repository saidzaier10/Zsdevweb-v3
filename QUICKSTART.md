# 🚀 Démarrage Rapide (Quickstart)

Voici les commandes essentielles pour lancer le projet **Zsdevweb v3** sur **macOS**.

## ⚙️ Configuration Initiale (Important)

Avant de lancer quoi que ce soit, vous devez configurer les variables d'environnement.

1. Copiez le fichier d'exemple :
   ```bash
   cp .env.example .env
   ```
2. Modifiez le fichier `.env` avec vos propres valeurs (si nécessaire).

---

## 🐳 Option 1 : Docker (Recommandé)

C'est la méthode la plus simple, tout est configuré automatiquement.

```bash
# Lancer l'application
docker-compose up --build
```

Une fois lancé :
- **Frontend** : http://localhost:5173
- **Backend API** : http://localhost:8000
- **Admin** : http://localhost:8000/admin

> **Note** : Pour arrêter, faites `Ctrl+C` puis `docker-compose down` pour nettoyer.

---

## 💻 Option 2 : Développement Local

### Pré-requis
- Python 3.x (`brew install python`)
- Node.js & npm (`brew install node`)
- PostgreSQL (`brew install postgresql`)
- Redis (`brew install redis`)

### 1. Backend (Django)

```bash
cd backend

# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Lancer le serveur
python manage.py runserver
```

### 2. Frontend (Vue.js)

Ouvrez un **nouveau terminal** :

```bash
cd frontend

# Installer les dépendances
npm install

# Lancer le serveur de dev
npm run dev
```

---

## 🛠 Commandes Utiles

### Créer un superutilisateur (Admin)
```bash
# Avec Docker
docker-compose exec backend python manage.py createsuperuser

# En local
python manage.py createsuperuser
```

### Accéder au shell de la base de données
```bash
# Avec Docker
docker-compose exec db psql -U zs -d zsdevweb
```

### Voir les logs
```bash
docker-compose logs -f
```
