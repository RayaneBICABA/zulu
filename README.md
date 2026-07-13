<p align="center">
  <img src="ShootSplashScreen.png" alt="ZAWANI" width="250">
</p>

<h1 align="center">ZAWANI</h1>

<p align="center">
  <strong>Application mobile d'annuaire intelligent pour commerces locaux</strong>
  <br>
  Decouvrez, geolocalisez et interagissez avec les commerces de proximite.
</p>

<p align="center">
  <a href="#">
    <img src="https://img.shields.io/badge/Android-3DDC84?style=for-the-badge&logo=android&logoColor=white" alt="Android">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
  </a>
  <a href="#">
    <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  </a>
</p>

---

## Aperçu

<p align="center">
  <img src="docs/screenshots/01-accueil.png" width="200" alt="Accueil">
  <img src="docs/screenshots/02-commerce-detail.png" width="200" alt="Fiche commerce">
  <img src="docs/screenshots/06-commerce-avis.png" width="200" alt="Avis">
  <img src="docs/screenshots/03-favoris.png" width="200" alt="Favoris">
  <img src="docs/screenshots/04-profil.png" width="200" alt="Profil">
  <img src="docs/screenshots/05-commerce-dashboard.png" width="200" alt="Dashboard">
</p>

## Fonctionnalites

- **Authentification** Firebase (Google, email, anonyme)
- **Geolocalisation** des commerces avec tri par distance
- **Recherche et filtre** par categorie
- **Fiche commerce** detaillee avec photos, horaires, contact
- **Notation intelligente** des commentaires par analyse semantique
- **Favoris** avec synchronisation compte
- **Creation et gestion** de commerces (brouillon / publication)
- **Dashboard** de statistiques (vues, favoris, avis, note)
- **Partage** localisation via WhatsApp
- **Mode hors-ligne** partiel grace au stockage local

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
| Render | Deploiement backend |
| Firebase Auth | Fournisseur d'identite |

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

## Collaborateurs

| GitHub | Nom |
|---|---|
| @PANK4SS | Pankassi Jean-Louis Rayane BICABA |
| @AllcodIn | — |
| @brecheyn | NADINGA Yiénouyaba Pharès |
| @noagthiombiano257-gif | Jeannine257 |
| @Patisilga226 | SILGA Patricia |
