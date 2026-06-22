# Commandes Frontend -- Zulu Starter

## Prerequisites

- Node.js >= 18 installe
- Les dependances installees : `npm install`

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
