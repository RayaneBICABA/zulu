# Frontend -- Architecture et Structure

## Stack technique

| Outil | Role |
|---|---|
| React 19 | Bibliotheque UI |
| Vite 8 | Build tool et serveur de dev |
| React Router DOM 7 | Routage SPA |
| Tailwind CSS v4 | Styling utilitaire (plugin Vite, pas de fichier de config separe) |
| Framer Motion 12 | Animations |
| Lucide React | Icones |
| Capacitor 7 | Pont natif pour iOS et Android |
| ESLint 10 + react-hooks + react-refresh | Linting et conventions |

---

## Structure des dossiers

```
frontend/
├── public/                    Fichiers statiques servis tels quels
│   ├── favicon.svg
│   └── icons.svg              Sprite SVG (reseaux sociaux, etc.)
├── src/
│   ├── assets/                Images, polices importees dans le code
│   │   ├── fonts/             (reserve)
│   │   ├── icons/             (reserve)
│   │   ├── images/            (reserve)
│   │   └── hero.png
│   ├── components/
│   │   ├── ui/                Composants purs et reutilisables
│   │   └── layout/            Composants de structure de page
│   ├── constants/             Valeurs fixes : couleurs, routes, endpoints
│   ├── features/              Domaines metier (auth, etc.)
│   │   └── auth/              Systeme d'authentification
│   │       ├── context/       AuthProvider (etat utilisateur)
│   │       ├── hooks/         useAuth (consommateur du contexte)
│   │       ├── components/    ProtectedRoute, SocialLoginButton
│   │       └── pages/         Login, Register, ForgotPassword, ResetPassword, VerifyEmail
│   ├── hooks/                 Hooks React personnalises
│   ├── pages/                 Une page = une route
│   ├── services/              Appels API et logique d'acces aux donnees
│   ├── App.jsx                Definition des routes
│   ├── main.jsx               Point d'entree React
│   └── index.css              Import Tailwind, theme et styles globaux
├── android/                  Projet natif Android (generé par Capacitor)
├── capacitor.config.ts       Configuration Capacitor
├── index.html
├── vite.config.js
├── package.json
├── eslint.config.js
├── vercel.json
├── .env
└── .env.example
```

---

## Capacitor (application mobile)

Capacitor transforme l'application web en une application Android native. Le projet natif se trouve dans `android/`.

### Configuration

Le fichier `capacitor.config.ts` definit les parametres :

```typescript
import { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.zulustarter.app',    // Identifiant unique de l'application
  appName: 'Zulu Starter',          // Nom affiche sur l'appareil
  webDir: 'dist',                    // Dossier du build web (output de Vite)
  server: {
    androidScheme: 'https',          // Schema utilise pour les requetes reseau
  },
}

export default config
```

### Workflow de developpement mobile

1. **Developper le web** comme d'habitude (`npm run dev`)
2. **Builder le web** : `npm run build`
3. **Synchroniser** : `npm run cap:sync` (copie le build dans `android/`)
4. **Ouvrir Android Studio** : `npm run cap:open:android`
5. **Lancer l'application** depuis Android Studio sur un emulateur ou un appareil physique

Pour un cycle rapide : `npm run cap:build` combine les etapes 2 et 3.

### Live reload sur appareil

Pour voir les modifications en temps reel sur un appareil Android :

1. Lancer le serveur de dev : `npm run dev:network`
2. Modifier temporairement `capacitor.config.ts` :

```typescript
server: {
  url: 'http://192.168.1.42:5173',  // Adresse IP locale de votre machine
  cleartext: true,                    // Necessaire pour HTTP en dev
  androidScheme: 'http',
}
```

3. Synchroniser et lancer : `npm run cap:sync && npm run cap:open:android`

Ne pas committer la configuration `server.url` -- elle est propre au developpement local.

### Notes importantes

- Le dossier `android/` est versionne (commit). Il contient le projet Android generee une seule fois par `npx cap add android`
- Les fichiers generes dans `android/app/src/main/assets/` ne sont pas commit (ignores par le `.gitignore` d'Android)
- Le build de production passe par Vercel pour le web et par Android Studio pour le mobile
- Node.js >= 18 requis (>= 22 recommande pour Capacitor 8)

---

## Role de chaque couche

Le principe est la **separation par responsabilite**, pas simplement par type de fichier.

### components/ui/

Composants d'interface generiques, **sans logique metier, sans appel API, sans connaissance du routing**.

Un composant ui ne connait jamais l'existence d'un service ou d'une route. Il recoit des props et affiche quelque chose.

**Fichiers actuels :** Badge, Button, Card, Input, Spinner

**Regle :** si un composant a besoin de savoir ce qu'est un "utilisateur" ou une "connexion", il ne va pas dans ui/. Il va dans pages/ ou dans features/.

### components/layout/

Composants qui structurent une page entiere : barre de navigation, conteneur de page avec animation, menu lateral.

**Fichiers actuels :** Navbar, PageWrapper, Sidebar

**Sidebar** est un composant generique de navigation laterale pret pour tout ecran de type dashboard. Il prend une liste d'items `{ to, label, icon }` et gere l'etat actif via la route courante. Aucune logique metier.

### constants/

Toute valeur fixe utilisee a plusieurs endroits du code vit ici, jamais codee en dur dans un composant.

| Fichier | Contenu |
|---|---|
| `colors.js` | Palette complete : primary, secondary, success, warning, error, info + variantes light, gray |
| `api.js` | URL de base de l'API + tous les endpoints disponibles |
| `routes.js` | Chemins de toutes les routes de l'application |

**Regle :** toute couleur utilisee dans un composant doit exister dans `constants/colors.js` ou etre une classe Tailwind issue du `@theme` defini dans `index.css`. Aucun hex en dur.

### features/auth/

Contient toute la logique liee a l'authentification et au controle d'acces.

#### Context & Hook

**AuthProvider** (`context/AuthProvider.jsx`) : contexte React qui encapsule l'etat utilisateur et fournit les methodes suivantes :

| Methode | Description |
|---|---|
| `user` | Objet utilisateur connecte (null si non connecte) |
| `loading` | Boolen pendant le chargement du profil |
| `login(credentials)` | Authentification, stocke les tokens |
| `register(data)` | Inscription |
| `logout()` | Deconnexion, efface les tokens |
| `refreshUser()` | Recharger le profil depuis l'API |
| `hasRole(role)` | Verifier si l'utilisateur a un role |
| `hasPermission(perm)` | Verifier si l'utilisateur a une permission |
| `isAuthenticated` | Boolen indiquant si un utilisateur est connecte |

**useAuth** (`hooks/useAuth.js`) : hook React qui consomme le AuthContext. Doit etre utilise a l'interieur d'un AuthProvider.

```jsx
import useAuth from '../../features/auth/hooks/useAuth'

const { user, login, logout, hasRole, hasPermission } = useAuth()
```

#### Composants

**ProtectedRoute** (`components/ProtectedRoute.jsx`) : wrapper de route qui verifie l'authentification et optionnellement les roles/permissions.

```jsx
// Route protegee simple
<ProtectedRoute>
  <DashboardPage />
</ProtectedRoute>

// Route reservee aux admins
<ProtectedRoute role="admin">
  <AdminPage />
</ProtectedRoute>

// Route avec permission specifique
<ProtectedRoute permission="users:delete">
  <DeleteUserPage />
</ProtectedRoute>
```

**SocialLoginButton** (`components/SocialLoginButton.jsx`) : bouton d'authentification sociale (Google OAuth). Redirige vers le backend qui gere le flux OAuth.

#### Pages

| Page | Route | Description |
|---|---|---|
| `LoginPage` | `/login` | Formulaire de connexion email/mot de passe + Google OAuth |
| `RegisterPage` | `/register` | Formulaire d'inscription avec validation cote client |
| `ForgotPasswordPage` | `/mot-de-passe-oublie` | Saisie email pour recevoir un lien de reinitialisation |
| `ResetPasswordPage` | `/reinitialiser-mot-de-passe` | Saisie du nouveau mot de passe avec token dans l'URL |
| `VerifyEmailPage` | `/verifier-email` | Verification automatique de l'email via le token dans l'URL |

Chaque page suit le meme pattern : validation cote client avant appel API, gestion des etats loading/error/success, redirection apres action reussie.

#### Diagramme de flux

```
App (AuthProvider)
  |
  +-- useAuth (hook consommateur)
  |
  +-- ProtectedRoute (guard)
  |
  +-- pages auth (Login, Register, etc.)
  |     |-- validation locale
  |     +-- authService.login() / register() / etc.
  |           +-- apiClient.post()
  |                 +-- auto-refresh JWT
  |
  +-- apiClient
        |-- intercepte les 401
        |-- tente un refresh token
        +-- echec => event auth:logout => deconnexion forcee
```

### hooks/

Hooks React reutilisables encapsulant une logique commune.

| Hook | Role |
|---|---|
| `useApi` | Hook generique embarquant les etats loading/error/data autour de n'importe quel appel service |

### pages/

Une page correspond a une route declaree dans App.jsx. Une page assemble des composants ui/ et layout/, utilise les hooks et les services, et contient la logique propre a cet ecran.

**Fichiers actuels :** HomePage, NotFoundPage, DashboardPage

### services/

Toute communication avec le backend passe exclusivement par ce dossier. Aucun composant ne doit appeler `fetch` directement.

| Service | Role |
|---|---|
| `apiClient.js` | Client HTTP bas niveau (get, post, put, delete). Ajoute automatiquement le header Authorization si un token JWT existe en localStorage. Intercepte les 401 et tente un refresh automatique. En cas d'echec, emet un evenement `auth:logout` pour forcer la deconnexion. |
| `authService.js` | Fonctions liees a l'authentification (login, register, logout, me, refresh, verifyEmail, forgotPassword, resetPassword, resendVerification). Geres les tokens (access + refresh) en localStorage. |

### Diagramme de classes UML

Le backend expose un diagramme de classes UML automatique, genere par introspection SQLAlchemy et rendu avec Mermaid.js :

| Endpoint | Description |
|---|---|
| `GET /api/diagram` | Texte Mermaid brut |
| `GET /api/diagram/view` | Page HTML interactive avec rendu, téléchargement PNG et copie du code |

#### apiClient -- Auto-refresh JWT

Le apiClient implemente un mecanisme d'auto-refresh :

1. Chaque requete est intercepetee par `authFetch`
2. Si la reponse est 401, le client tente de refresher le token via `/auth/refresh`
3. Pendant le refresh, les requetes concurrentes sont mises en file d'attente
4. Si le refresh reussit, toutes les requetes en file sont retentees
5. Si le refresh echoue, les tokens sont effaces et un evenement `auth:logout` est emis

---

## Flux de donnees standard

```
Page (ex: LoginPage)
  -> useAuth().login(credentials)
    -> authService.login(credentials)
      -> apiClient.post(endpoint, body)
        -> fetch() + auto-refresh + gestion erreur
          -> Backend Flask
```

Une page n'appelle jamais fetch ou apiClient directement. Elle passe par le AuthContext ou un service, idealement via le hook `useApi` pour beneficier des etats loading/error.

---

## Conventions de code

| Element | Convention | Exemple |
|---|---|---|
| Fichiers composants | PascalCase | `Button.jsx`, `HomePage.jsx` |
| Fichiers utilitaires | camelCase | `apiClient.js`, `useApi.js` |
| Variables et fonctions | camelCase | `handleSubmit`, `isActive` |
| Constantes exportees | SCREAMING_SNAKE_CASE | `COLORS`, `ROUTES`, `ENDPOINTS` |
| Composant par fichier | Un seul, `export default` en bas | `export default Button` |
| Props par defaut | Dans la signature, jamais `defaultProps` | `const Button = ({ variant = 'primary' }) =>` |

**Regles strictes :**
- Couleurs : toujours via `constants/colors.js` ou classes Tailwind du theme. Jamais d'hexadecimal en dur.
- Pas de logique API dans `components/ui/` ou `components/layout/`
- Pas d'appel fetch direct dans les pages sans passer par `services/`
- Pas de duplication de composants : si Button ne couvre pas un cas, etendre ses props
- Routes : toujours referencer via `ROUTES.*`, jamais de chemin en dur

---

## Clean Architecture appliquee au frontend

| Couche | Responsabilite | Ne doit JAMAIS contenir |
|---|---|---|
| ui/ | Affichage pur | Logique metier, appels API, connaissance du routing |
| layout/ | Structure de page | Logique metier |
| pages/ | Composition et logique d'ecran | Appel fetch direct |
| features/ | Domaine metier specifique | Dependances transverses |
| hooks/ | Logique reutilisable transverse | JSX |
| services/ | Acces aux donnees distantes | JSX, etat React, hooks |
| constants/ | Valeurs fixes | Logique, fonctions complexes |

---

## Ajouter une nouvelle fonctionnalite

**Exemple : page de connexion**

1. Verifier que l'endpoint existe dans `constants/api.js` (deja present : `ENDPOINTS.auth.login`)
2. Verifier que le service existe (deja present : `authService.login`)
3. Creer la page `pages/LoginPage.jsx`
4. Utiliser `useApi(authService.login)` pour gerer l'appel
5. Utiliser les composants `Input` et `Button` pour le formulaire
6. Ajouter la route dans `constants/routes.js` si necessaire (deja presente : `ROUTES.login`)
7. Declarer la route dans `App.jsx`
8. Ajouter le lien dans `Navbar.jsx` si necessaire

---

## Etat actuel du projet

**Implemente :**
- Structure de base complete (ui, layout, pages, services, hooks, constants)
- Client API generique avec auto-refresh JWT et file d'attente
- Service d'authentification complet (login, register, logout, me, refresh, verifyEmail, forgotPassword, resetPassword)
- Hook useApi generique
- AuthContext et useAuth avec gestion de session, roles et permissions
- ProtectedRoute avec support role/permission optionnel
- Pages : Login, Register, ForgotPassword, ResetPassword, VerifyEmail, Dashboard
- SocialLoginButton (Google OAuth)
- Page d'accueil (HomePage), tableau de bord (DashboardPage), page 404
- Navbar responsive avec menu mobile
- Sidebar generique pour dashboard
- Capacitor 7 configure pour Android (projet natif dans `android/`)

**Documentation :**
- docs/AUTH.md -- guide complet du systeme d'authentification et RBAC

---

## Travailler en equipe

- Une branche par fonctionnalite, jamais directement sur main
- Avant de commencer une page qui depend de l'API, verifier que l'endpoint existe dans `constants/api.js`. Si non, l'ajouter en premier et le signaler a la personne qui travaille sur le backend
- Ne jamais dupliquer un composant ui/ existant
- Toute couleur utilisee doit exister dans `constants/colors.js` ou le `@theme` de `index.css`
- Avant de pousser : `npm run lint`
- Utiliser `npm run dev:network` pour tester depuis d'autres appareils sur le reseau local
