# Commandes Frontend -- Zulu Starter

## Prerequisites

- Node.js >= 18 installe
- Les dependances installees : `npm install`
- Android Studio installe (pour compiler et lancer l'application mobile)
- Optionnel : un appareil Android ou un emulateur pour tester l'application mobile

---

## Demarrage

### Lancer le serveur de developpement local

```bash
cd frontend
npm run dev
```

Serveur accessible sur `http://localhost:5173` (port par defaut de Vite).

### Lancer le serveur accessible sur le reseau local

```bash
cd frontend
npm run dev:network
```

Cette commande expose le serveur sur l'ensemble du reseau local.
Utilisez l'adresse IP de votre machine (affichee dans le terminal au demarrage) pour y acceder depuis un autre appareil (mobile, tablette, autre PC).

Exemple de sortie :
```
> VITE v8.0.0  ready in 150ms
> Local:   http://localhost:5173/
> Network: http://192.168.1.42:5173/
```

---

## Construction et deploiement

### Compiler pour la production

```bash
cd frontend
npm run build
```

Genere le build de production dans le dossier `dist/`.

### Previsualiser le build de production

```bash
cd frontend
npm run preview
```

Sert le contenu du dossier `dist/` en local pour verifier le rendu final avant deploiement.

---

## Application mobile (Capacitor)

### Synchroniser le build web avec le projet Android

```bash
cd frontend
npm run cap:sync
```

Copie les fichiers du dossier `dist/` (build web) dans le projet Android (`android/app/src/main/assets/public`).

### Ouvrir le projet dans Android Studio

```bash
cd frontend
npm run cap:open:android
```

Lance Android Studio avec le projet Android pre-configure. A partir de la, vous pouvez compiler et lancer l'application sur un emulateur ou un appareil physique.

### Builder le web puis synchroniser

```bash
cd frontend
npm run cap:build
```

Raccourci qui execute `npm run build` puis `npm run cap:sync` en une seule commande.

### Ajouter un plugin Capacitor

```bash
cd frontend
npm install @capacitor/nom-du-plugin
npx cap sync
```

---

## Qualite du code

### Linter

```bash
cd frontend
npm run lint
```

Verifie l'ensemble du code avec ESLint. Corriger toute erreur avant de pousser.

---

## Variables d'environnement

Creer le fichier `.env` a partir du template :

```bash
cp .env.example .env
```

Contenu par defaut :

```env
VITE_API_URL=http://localhost:5000/api
```

| Variable | Description | Valeur par defaut |
|---|---|---|
| `VITE_API_URL` | URL de base de l'API backend | `http://localhost:5000/api` |

---

## Gestion des dependances

### Installer les dependances

```bash
cd frontend
npm install
```

### Ajouter une dependance

```bash
npm install <nom-du-package>
```

### Ajouter une dependance de developpement

```bash
npm install -D <nom-du-package>
```

---

## Deploiement

Le projet est configure pour un deploiement sur **Vercel** (fichier `vercel.json`).

Configuration actuelle :
- Framework : Vite
- Commande de build : `npm run build`
- Dossier de sortie : `dist`
- Rewrites : toutes les routes redirigent vers `index.html` (support SPA)

Pour deployer :

```bash
# Via l'interface Vercel
vercel --prod

# Ou via Git (si le projet est lie a Vercel)
git push
```
