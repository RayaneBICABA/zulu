<p align="center">
  <img src="ZULU.png" alt="Zulu Starter" width="180">
</p>

<h1 align="center">Zulu Starter</h1>

<p align="center">
  Base solide pour hackathons et projets full-stack.
  <br>
  Flask 3.1 &middot; React 19 &middot; PostgreSQL 15 &middot; Docker
</p>

## A propos

Zulu Starter est un template de projet full-stack pret a l'emploi, concu pour demarrer un hackathon ou un projet sans perdre de temps sur la configuration initiale.

Le projet suit les principes de **Clean Architecture** avec une separation stricte des responsabilites, des conventions de code claires, et une documentation complete pour le travail en equipe.

## Stack technique

### Backend

| Technologie | Role |
|---|---|
| Python 3.11 + Flask 3.1 | Framework web |
| SQLAlchemy | ORM |
| Flask-Migrate (Alembic) | Migrations de base de donnees |
| Flask-JWT-Extended | Authentification par tokens JWT |
| Flask-Cors | Gestion du CORS |
| Marshmallow | Validation et serialisation des donnees |
| PostgreSQL 15 | Base de donnees relationnelle |
| Flasgger (Swagger) | Documentation interactive des API |
| Pytest | Tests unitaires et d'integration |

### Frontend

| Technologie | Role |
|---|---|
| React 19 | Bibliotheque UI |
| Vite 8 | Build tool et serveur de dev |
| React Router DOM 7 | Routage SPA |
| Tailwind CSS v4 | Styling utilitaire |
| Framer Motion 12 | Animations |
| Lucide React | Icones |
| ESLint 10 | Linting et conventions |

### Infrastructure

| Outil | Role |
|---|---|
| Docker + Docker Compose | Conteneurisation de la DB et du backend |
| Vercel | Deploiement frontend |
| Render | Deploiement backend |

## Structure du projet

```
zulu-starter/
├── backend/              Application Flask (API)
│   ├── app/
│   │   ├── models/       Modeles SQLAlchemy
│   │   ├── routes/       Points d'entree HTTP (blueprints)
│   │   ├── schemas/      Validation Marshmallow
│   │   └── services/     Logique metier
│   ├── tests/            Tests unitaires et d'integration
│   └── requirements.txt  Dependances Python
├── frontend/             Application React (SPA)
│   ├── src/
│   │   ├── components/   Composants UI et layout
│   │   ├── constants/    Configuration centralisee
│   │   ├── hooks/        Hooks reutilisables
│   │   ├── pages/        Ecrans de l'application
│   │   └── services/     Appels API
│   └── package.json
├── docs/                 Documentation
│   ├── BACKEND.md
│   ├── FRONTEND.md
│   ├── COMMANDS.md
│   └── FRONTEND_COMMANDS.md
├── docker-compose.yml    Services Docker (PostgreSQL + backend)
└── ZULU.png              Logo du projet
```

## Prerequisites

- Docker et Docker Compose installes (pour la base de donnees et le backend)
- Node.js >= 18 (pour le frontend)
- Python 3.11+ (pour le backend si lance sans Docker)

## Demarrage rapide

### 1. Cloner le depot

```bash
git clone <url-du-depot>
cd zulu-starter
```

### 2. Lancer la base de donnees et le backend avec Docker

```bash
docker compose up -d
```

Le backend est accessible sur `http://localhost:5000`.

### 3. Lancer le frontend

```bash
cd frontend
npm install
npm run dev
```

Le frontend est accessible sur `http://localhost:5173`.

### 4. Ouvrir l'application

Rendez-vous sur `http://localhost:5173` dans votre navigateur.

## Commandes principales

### Backend (avec Docker)

```bash
docker compose up -d        # Demarrer les services
docker compose down         # Arreter les services
docker compose logs -f      # Voir les logs
```

### Backend (sans Docker)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask run --host=0.0.0.0 --port=5000 --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev                 # Serveur local
npm run dev:network         # Serveur accessible sur le reseau
npm run build               # Build de production
npm run lint                # Verification du code
```

## Documentation

| Document | Contenu |
|---|---|
| `docs/BACKEND.md` | Architecture backend, conventions, guide d'ajout de ressources, tests |
| `docs/FRONTEND.md` | Architecture frontend, roles des couches, conventions, travail en equipe |
| `docs/COMMANDS.md` | Commandes Docker, Python, migrations, tests, Git workflow |
| `docs/FRONTEND_COMMANDS.md` | Commandes frontend (dev, build, lint, preview, deploiement) |

## Variables d'environnement

### Backend

Copier `backend/.env.example` vers `backend/.env` et renseigner :

```
SECRET_KEY=une-chaine-aleatoire-longue
JWT_SECRET_KEY=une-autre-chaine-aleatoire
DATABASE_URL=postgresql://zulu_user:zulu_pass@localhost:5432/zulu_db
DB_HOST=localhost
DB_PORT=5432
DB_NAME=zulu_db
DB_USER=zulu_user
DB_PASSWORD=zulu_pass
FLASK_APP=run.py
FLASK_ENV=development
```

### Frontend

Copier `frontend/.env.example` vers `frontend/.env` :

```env
VITE_API_URL=http://localhost:5000/api
```

## Equipe et contributions

- Une branche par fonctionnalite, jamais directement sur `main`
- Lancer `npm run lint` et `pytest` avant de pousser
- Consulter la documentation dans `docs/` pour les conventions de code
- Les couleurs du theme sont definies dans `frontend/src/constants/colors.js` et `frontend/src/index.css`
- Tout nouvel endpoint backend doit etre ajoute a `frontend/src/constants/api.js`
