# Commandes de référence — Zulu Starter

## Prérequis

- Docker et Docker Compose installés
- Python 3.11+
- pip

---

## Docker

### Démarrer tous les services (DB + Backend)

```bash
docker compose up
```

### Démarrer en arrière-plan

```bash
docker compose up -d
```

### Démarrer avec rebuild de l'image

```bash
docker compose up --build
```

### Arrêter tous les services

```bash
docker compose down
```

### Arrêter et supprimer les volumes (reset complet de la DB)

```bash
docker compose down -v
```

### Voir les logs en temps réel

```bash
docker compose logs -f
```

### Voir les logs d'un seul service

```bash
docker compose logs -f backend
docker compose logs -f db
```

### Entrer dans le container backend

```bash
docker compose exec backend bash
```

### Entrer dans le container PostgreSQL

```bash
docker compose exec db psql -U zulu_user -d zulu_db
```

### Statut des containers

```bash
docker compose ps
```

---

## Python / Flask (sans Docker — développement local)

### Créer un environnement virtuel

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

### Copier les variables d'environnement

```bash
cp .env.example .env
```

### Lancer le serveur Flask

```bash
flask run --host=0.0.0.0 --port=5000 --reload
```

### Lancer avec run.py

```bash
python run.py
```

---

## Migrations (Flask-Migrate / Alembic)

### Initialiser les migrations (une seule fois)

```bash
docker compose exec backend flask db init
```

### Générer une migration après modification d'un modèle

```bash
docker compose exec backend flask db migrate -m "description de la migration"
```

### Appliquer les migrations

```bash
docker compose exec backend flask db upgrade
```

### Revenir à la migration précédente

```bash
docker compose exec backend flask db downgrade
```

### Voir l'historique des migrations

```bash
docker compose exec backend flask db history
```

---

## Tests API (curl)

### Health check

```bash
curl http://localhost:5000/api/health
```

### Requête POST avec JSON

```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@test.com", "password": "secret123"}'
```

### Requête avec token JWT

```bash
curl http://localhost:5000/api/protected \
  -H "Authorization: Bearer VOTRE_TOKEN_ICI"
```

---

## Git — Workflow des branches

### Créer une branche feature

```bash
git checkout -b feature/nom-de-la-feature
```

### Pousser une branche

```bash
git push origin feature/nom-de-la-feature
```

### Branches principales du starter

| Branche | Contenu |
|---|---|
| main | Base propre sans auth |
| feature/auth | Système login / register avec JWT |
| feature/auth-roles | Auth + système de rôles (admin, user) |
