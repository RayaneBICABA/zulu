<p align="center">
  <img src="ZAWANI.png" alt="ZAWANI" width="180" style="margin-right: 60px;">
  <img src="ZULU.png" alt="ZULU" width="180">
</p>

<h1 align="center">ZAWANI</h1>

<p align="center">
  Application mobile d'annuaire intelligent pour commerces locaux.
  <br>
  Developpee par la team <strong>ZULU</strong>.
</p>

## A propos

ZAWANI est une application mobile de mise en relation entre clients et commerces de proximite. Elle permet la decouverte, la recherche geolocalisee et la gestion de commerces locaux avec des fonctionnalites de notation intelligente, de favoris et de partage.

L'application se distingue par son modele utilisateur unifie : tout utilisateur peut naviguer, commenter, favoriser et creer ses propres commerces sans distinction de role artificiel.

## Stack technique

### Backend

| Technologie | Role |
|---|---|
| Python 3.11 + Flask 3.1 | Framework web REST |
| SQLAlchemy | ORM |
| Flask-Migrate (Alembic) | Migrations de base de donnees |
| Flask-JWT-Extended | Authentification par tokens JWT |
| Flask-Cors | Gestion du CORS |
| Marshmallow | Validation et serialisation |
| PostgreSQL 15 | Base de donnees relationnelle |
| Flasgger (Swagger) | Documentation interactive des API |
| Google Generative AI | Analyse automatique des avis (fallback keyword) |

### Frontend

| Technologie | Role |
|---|---|
| React 19 | Bibliotheque UI |
| Vite 8 | Build tool et serveur de dev |
| React Router DOM 7 | Routage SPA |
| Tailwind CSS v4 | Styling utilitaire |
| Framer Motion 12 | Animations |
| Lucide React | Icones |
| Capacitor 7 | Pont natif pour Android (APK) |
| Firebase JS SDK | Authentification (Google, email) |

### Infrastructure

| Outil | Role |
|---|---|
| Docker + Docker Compose | Conteneurisation DB et backend |
| Vercel | Deploiement frontend (PWA) |
| Render | Deploiement backend |
| Firebase Auth | Fournisseur d'identite |

## Fonctionnalites

- Authentification Firebase (Google, email, anonyme)
- Geolocalisation des commerces avec tri par distance
- Recherche et filtre par categorie
- Fiche commerce detaillee avec photos, horaires, contact
- Notation automatique des commentaires par analyse semantique
- Favoris avec synchronisation compte
- Creation et gestion de commerces (brouillon / publication)
- Dashboard de statistiques (vues, favoris, avis, note)
- Partage localisation via WhatsApp
- Mode hors-ligne partiel grace au stockage local

## Structure du projet

```
zawani/
  +-- backend/              Application Flask (API REST)
  |   +-- app/
  |   |   +-- models/       Modeles SQLAlchemy
  |   |   +-- routes/       Points d'entree HTTP (blueprints)
  |   |   +-- schemas/      Validation Marshmallow
  |   |   +-- services/     Logique metier
  |   +-- tests/            Tests unitaires
  |   +-- requirements.txt
  +-- frontend/             Application React (SPA + Capacitor)
  |   +-- android/          Projet natif Android
  |   +-- src/
  |   |   +-- components/   Composants UI
  |   |   +-- constants/    Configuration
  |   |   +-- features/     Modules fonctionnels (auth)
  |   |   +-- hooks/        Hooks reutilisables
  |   |   +-- pages/        Ecrans de l'application
  |   |   +-- services/     Appels API
  |   +-- capacitor.config.ts
  |   +-- package.json
  +-- docs/                 Documentation
  +-- tools/                Outils autonomes
  +-- docker-compose.yml
```

## Demarrage rapide

### Prerequis

- Docker et Docker Compose
- Node.js >= 18
- Python 3.11+
- Android Studio (optionnel, pour build APK)

### Backend

```bash
git clone <url-du-depot>
cd zawani

# Lancer la base de donnees et le backend
docker compose up -d

# Le backend est accessible sur http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Le frontend est accessible sur `http://localhost:5173`.

### Application mobile (Android)

```bash
cd frontend
npm run build
npx cap sync android
cd android
./gradlew assembleDebug
adb install app/build/outputs/apk/debug/app-debug.apk
```

## Variables d'environnement

### Backend

Copier `backend/.env.example` vers `backend/.env`.

```
SECRET_KEY=
JWT_SECRET_KEY=
DATABASE_URL=postgresql://zulu_user:zulu_pass@localhost:5432/zulu_db
FLASK_APP=run.py
FLASK_ENV=development
GEMINI_API_KEY=              # Optionnel, pour analyse IA des avis
FIREBASE_PROJECT_ID=
FIREBASE_PRIVATE_KEY=
FIREBASE_CLIENT_EMAIL=
```

### Frontend

Copier `frontend/.env.example` vers `frontend/.env`.

```
VITE_API_URL=http://localhost:5000/api
VITE_FIREBASE_API_KEY=
VITE_FIREBASE_AUTH_DOMAIN=
VITE_FIREBASE_PROJECT_ID=
```

## Equipe et contributions

Projet realise par la team **ZULU**. ZAWANI est construit sur le template full-stack ZULU qui fournit l'architecture, les conventions et les outils de productivite.

- Une branche par fonctionnalite, jamais directement sur `main`
- Lancer `npm run lint` et les tests avant de pousser
- La documentation de reference se trouve dans `docs/`
