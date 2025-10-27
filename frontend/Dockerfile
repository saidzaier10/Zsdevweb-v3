FROM node:22-alpine

# Répertoire de travail
WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier tout le projet
COPY . .

# Exposer le port
EXPOSE 5173

# Commande pour démarrer le serveur de dev
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]