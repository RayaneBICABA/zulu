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
│   ├── features/              Domaines metier specifiques (vide, voir ci-dessous)
│   ├── hooks/                 Hooks React personnalises
│   ├── pages/                 Une page = une route
│   ├── services/              Appels API et logique d'acces aux donnees
│   ├── App.jsx                Definition des routes
│   ├── main.jsx               Point d'entree React
│   └── index.css              Import Tailwind, theme et styles globaux
├── index.html
├── vite.config.js
├── package.json
├── eslint.config.js
├── vercel.json
├── .env
└── .env.example
```

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

### features/

Dossier reserve pour les domaines metier specifiques au sujet du hackathon. Encore vide puisque le sujet n'est pas connu.

**Convention :** le jour du hackathon, chaque domaine metier recoit son propre sous-dossier ici, avec sa structure components/hooks/services interne si necessaire. Le dossier ui/ et layout/ restent strictement transverses.

### hooks/

Hooks React reutilisables encapsulant une logique commune.

| Hook | Role |
|---|---|
| `useApi` | Hook generique embarquant les etats loading/error/data autour de n'importe quel appel service |

### pages/

Une page correspond a une route declaree dans App.jsx. Une page assemble des composants ui/ et layout/, utilise les hooks et les services, et contient la logique propre a cet ecran.

**Fichiers actuels :** HomePage, NotFoundPage

### services/

Toute communication avec le backend passe exclusivement par ce dossier. Aucun composant ne doit appeler `fetch` directement.

| Service | Role |
|---|---|
| `apiClient.js` | Client HTTP bas niveau (get, post, put, delete). Ajoute automatiquement le header Authorization si un token JWT existe en localStorage. Lance une erreur lisible si la reponse n'est pas ok. |
| `authService.js` | Fonctions liees a l'authentification (login, register, logout, me, gestion du token). S'appuie sur apiClient et sur les endpoints definis dans constants/api.js. |

---

## Flux de donnees standard

```
Page (ex: LoginPage)
  -> hook useApi(authService.login)
    -> service authService.login()
      -> apiClient.post(endpoint, body)
        -> fetch() + gestion erreur
          -> Backend Flask
```

Une page n'appelle jamais fetch ou apiClient directement. Elle passe par un service, idealement via le hook `useApi` pour beneficier des etats loading/error.

**Exemple :**

```jsx
import useApi from '../hooks/useApi'
import authService from '../services/authService'

const LoginPage = () => {
  const { execute, loading, error } = useApi(authService.login)

  const handleSubmit = async (credentials) => {
    const result = await execute(credentials)
    authService.saveToken(result.token)
  }

  return (
    // ...
  )
}
```

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
- Client API generique avec gestion du token JWT
- Service d'authentification (login, register, logout, me)
- Hook useApi generique
- Page d'accueil (HomePage) et page 404
- Navbar responsive avec menu mobile
- Sidebar generique pour dashboard
- Dossier features/ cree, vide en attendant le sujet

**A implementer :**
- Pages Login et Register (le service existe, les pages non)
- Gestion des roles (RBAC) liee a la branche backend feature/auth-roles
- Tout domaine metier specifique dans features/

---

## Travailler en equipe

- Une branche par fonctionnalite, jamais directement sur main
- Avant de commencer une page qui depend de l'API, verifier que l'endpoint existe dans `constants/api.js`. Si non, l'ajouter en premier et le signaler a la personne qui travaille sur le backend
- Ne jamais dupliquer un composant ui/ existant
- Toute couleur utilisee doit exister dans `constants/colors.js` ou le `@theme` de `index.css`
- Avant de pousser : `npm run lint`
- Utiliser `npm run dev:network` pour tester depuis d'autres appareils sur le reseau local
