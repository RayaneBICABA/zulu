# API Convention Designer

## Objectif

Permettre aux developpeurs frontend et backend de s'accorder sur le contrat d'interface avant de commencer le developpement d'une fonctionnalite.

Ce fichier sert de **template vivant** : pour chaque nouvelle fonctionnalite, dupliquer le template endpoint, le remplir, et le partager en equipe.

---

## Conventions generales

### URLs

```
/api/{ressource}
/api/{ressource}/{id}
/api/{ressource}/{id}/{sous-ressource}
```

Toujours au pluriel, toujours en anglais, en kebab-case.

### Methodes HTTP

| Methode | Action | Code succes |
|---------|--------|-------------|
| GET | Lister une collection | 200 |
| GET | Obtenir un element | 200 |
| POST | Creer une ressource | 201 |
| PUT | Remplacer une ressource | 200 |
| PATCH | Modifier partiellement | 200 |
| DELETE | Supprimer une ressource | 204 |

### Corps de reponse

```json
{
  "data": { ... },
  "meta": { "page": 1, "per_page": 20, "total": 42 },
  "error": null
}
```

### Corps d'erreur

```json
{
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Description lisible du probleme",
    "details": [
      { "field": "email", "message": "Email deja utilise" }
    ]
  }
}
```

### Authentification

- Token JWT dans le header `Authorization: Bearer {access_token}`
- Refresh token dans le header `Authorization: Bearer {refresh_token}`
- Les endpoints proteges retournent 401 si token manquant ou expire

### Pagination

Parametres query : `?page=1&per_page=20`

Reponse :
```json
{
  "data": [ ... ],
  "meta": {
    "page": 1,
    "per_page": 20,
    "total": 42,
    "pages": 3
  }
}
```

### Formats standard

| Champ | Format |
|-------|--------|
| id | Integer auto-increment |
| created_at | ISO 8601 (`2026-06-23T12:00:00Z`) |
| updated_at | ISO 8601 |
| dates | ISO 8601 |
| emails | RFC 5321 |
| mots de passe | Min 8 caracteres, hache en base |
| boolean | `true` / `false` |

---

## Template endpoint

Pour chaque endpoint, remplir le tableau suivant :

```markdown
### `{METHODE} /api/{ressource}/{action}`

| Champ | Valeur |
|-------|--------|
| Description | ... |
| Auth requis | Oui / Non |
| Role requis | ... (optionnel) |
| Rate limit | ... |

**Parametres query** (si GET) :

| Nom | Type | Requis | Description |
|-----|------|--------|-------------|

**Body requete** (si POST/PUT/PATCH) :

```json
{
  "field": "type (requis/optionnel) — description"
}
```

**Reponse 200/201** :

```json
{
  "data": { ... },
  "meta": { ... },
  "error": null
}
```

**Erreurs possibles** :

| Code | Status | Condition |
|------|--------|-----------|
| VALIDATION_ERROR | 400 | Donnees invalides |
| NOT_FOUND | 404 | Ressource introuvable |
| UNAUTHORIZED | 401 | Token manquant ou invalide |
| FORBIDDEN | 403 | Permissions insuffisantes |
| CONFLICT | 409 | Conflit (doublon, etc.) |
| RATE_LIMITED | 429 | Trop de requetes |
```

---

## Exemple concret

### `POST /api/auth/register`

| Champ | Valeur |
|-------|--------|
| Description | Inscription d'un nouvel utilisateur |
| Auth requis | Non |
| Rate limit | 3/min |

**Body requete :**
```json
{
  "email": "string (requis) — email valide",
  "password": "string (requis) — min 8 caracteres",
  "first_name": "string (requis) — prenom",
  "last_name": "string (requis) — nom"
}
```

**Reponse 201 :**
```json
{
  "data": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "Jean",
    "last_name": "Dupont",
    "is_verified": false,
    "is_active": true
  },
  "error": null
}
```

**Erreurs :**
| Code | Status | Condition |
|------|--------|-----------|
| VALIDATION_ERROR | 400 | Champs manquants, email invalide, password trop court |
| CONFLICT | 409 | Email deja utilise |
| RATE_LIMITED | 429 | Trop de tentatives |

---

## Workflow

1. **Planification** : l'equipe identifie les endpoints necessaires pour une feature
2. **Redaction** : le backend cree le template endpoint dans une PR ou un ticket
3. **Validation** : le frontend valide que le contrat repond a ses besoins
4. **Implementation** : backend et frontend developpent en parallele sur le contrat valide
5. **Verification** : les tests d'integration backend valident le contrat ; le frontend consomme l'API reelle

---

## Ressources

- Backend en ligne : `http://localhost:5000`
- Swagger UI : `http://localhost:5000/apidocs`
- Frontend en ligne : `http://localhost:5173`
