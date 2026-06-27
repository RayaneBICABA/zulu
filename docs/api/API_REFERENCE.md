# Zulu API Reference

> **Base URL :** `http://localhost:5000/api`
> **Authentification :** Bearer Token (JWT) dans le header `Authorization`

---

## Table des matieres

1. [Authentification](#authentification)
2. [OAuth (Google)](#oauth-google)
3. [Administration](#administration)
4. [Commerce (Stepper)](#commerce-stepper)
5. [Categories](#categories)
6. [Artisan Dashboard](#artisan-dashboard)
7. [Vues (Profile)](#vues-profile)
8. [Favoris](#favoris)
9. [Images de Produits](#images-de-produits)
10. [Geolocalisation](#geolocalisation)
11. [Health](#health)

---

## Authentification

### POST `/api/auth/register`

Inscription d'un nouvel utilisateur.

**Body :**
```json
{
  "email": "user@example.com",
  "password": "motdepasse123",
  "first_name": "John",
  "last_name": "Doe"
}
```

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| email | string | Oui | Email unique |
| password | string | Oui | Min 8 caracteres |
| first_name | string | Non | Prenom |
| last_name | string | Non | Nom |

**Reponse 201 :**
```json
{
  "message": "Inscription reussie.",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_verified": false,
    "is_active": true,
    "roles": ["client"],
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  }
}
```

> Le role `client` est attribue automatiquement a l'inscription.

**Erreurs :**
- `400` — Champs manquants ou invalides
- `409` — Email deja utilise

---

### POST `/api/auth/login`

Connexion d'un utilisateur.

**Body :**
```json
{
  "email": "user@example.com",
  "password": "motdepasse123"
}
```

**Reponse 200 :**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "is_verified": false,
    "is_active": true,
    "roles": ["client"],
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  }
}
```

**Erreurs :**
- `400` — Champs manquants
- `401` — Identifiants incorrects ou compte desactive

---

### POST `/api/auth/refresh`

Rafraichir le token d'acces. Necessite le `refresh_token` dans le header.

**Header :**
```
Authorization: Bearer <refresh_token>
```

**Reponse 200 :**
```json
{
  "access_token": "eyJ..."
}
```

---

### GET `/api/auth/me`

Recuperer les informations de l'utilisateur connecte.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "is_verified": false,
  "is_active": true,
  "roles": ["client"],
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Erreurs :**
- `401` — Token manquant ou invalide
- `404` — Utilisateur introuvable

---

### POST `/api/auth/verify-email`

Confirmer l'adresse email via un token.

**Body :**
```json
{
  "token": "token-de-verification"
}
```

**Reponse 200 :**
```json
{
  "message": "Email verifie avec succes.",
  "user": { ... }
}
```

**Erreurs :**
- `400` — Token invalide ou expire

---

### POST `/api/auth/forgot-password`

Envoyer un email de reinitialisation de mot de passe.

**Body :**
```json
{
  "email": "user@example.com"
}
```

**Reponse 200 :**
```json
{
  "message": "Si un compte existe avec cet email, un lien de reinitialisation a ete envoye."
}
```

---

### POST `/api/auth/reset-password`

Reinitialiser le mot de passe avec un token.

**Body :**
```json
{
  "token": "token-de-reinitialisation",
  "password": "nouveau-mot-de-passe"
}
```

**Reponse 200 :**
```json
{
  "message": "Mot de passe reinitialise avec succes."
}
```

**Erreurs :**
- `400` — Token invalide ou mot de passe < 8 caracteres

---

### POST `/api/auth/resend-verification`

Renvoyer l'email de verification.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "message": "Email de verification renvoye."
}
```

**Erreurs :**
- `400` — Email deja verifie
- `401` — Token manquant ou invalide
- `404` — Utilisateur introuvable

---

### POST `/api/auth/logout`

Deconnexion — le front supprime le token du storage. JWT stateless, pas de blacklist.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "message": "Deconnexion reussie."
}
```

**Notes :**
- Le token expire naturellement (15min access / 7j refresh)
- Le front doit supprimer le token du storage (localStorage/cookies)
- Pas de blacklist côté serveur

**Erreurs :**
- `401` — Token manquant ou invalide

---

## OAuth (Google)

### GET `/api/auth/google/login`

Rediriger vers Google pour l'authentification.

**Reponse :** Redirection 302 vers Google

---

### GET `/api/auth/google/callback`

Callback apres authentification Google.

**Reponse 200 :**
```json
{
  "access_token": "eyJ...",
  "refresh_token": "eyJ...",
  "user": { ... }
}
```

**Erreurs :**
- `401` — Authentification Google echouee
- `501` — Google OAuth non configure

---

## Administration

> Routes admin necessitant le role `admin` sauf `GET /api/admin/roles`.

### GET `/api/admin/roles`

Lister tous les roles. **Pas d'authentification requise.**

**Reponse 200 :**
```json
[
  {
    "id": 1,
    "name": "client",
    "description": "Client — cherche des services",
    "permissions": []
  },
  {
    "id": 2,
    "name": "artisan",
    "description": "Artisan — prestataire de service",
    "permissions": []
  },
  {
    "id": 3,
    "name": "admin",
    "description": "Administrateur du systeme",
    "permissions": []
  }
]
```

**Roles par defaut :**
- `client` — attribue automatiquement a l'inscription
- `artisan` — prestataire de service
- `admin` — gestion du systeme

---

### POST `/api/admin/roles`

Creer un nouveau role.

**Body :**
```json
{
  "name": "moderator",
  "description": "Moderateur du site"
}
```

**Reponse 201 :**
```json
{
  "id": 2,
  "name": "moderator",
  "description": "Moderateur du site",
  "permissions": []
}
```

**Erreurs :**
- `400` — Champs manquants
- `401` — Token manquant ou invalide
- `403` — Role admin requis
- `409` — Le role existe deja

---

### GET `/api/admin/permissions`

Lister toutes les permissions.

**Reponse 200 :**
```json
[
  {
    "id": 1,
    "codename": "users:read",
    "name": "Lire les utilisateurs"
  }
]
```

---

### POST `/api/admin/permissions`

Creer une nouvelle permission.

**Body :**
```json
{
  "codename": "posts:delete",
  "name": "Supprimer les articles",
  "description": "Permission de supprimer des articles"
}
```

**Reponse 201 :**
```json
{
  "id": 2,
  "codename": "posts:delete",
  "name": "Supprimer les articles"
}
```

**Erreurs :**
- `400` — Champs manquants
- `409` — La permission existe deja

---

### POST `/api/admin/users/<user_id>/roles`

Assigner un role a un utilisateur.

**Body :**
```json
{
  "role_name": "admin"
}
```

**Reponse 200 :**
```json
{
  "message": "Role assigne.",
  "user": { ... }
}
```

**Erreurs :**
- `400` — Utilisateur ou role introuvable

---

### DELETE `/api/admin/users/<user_id>/roles`

Retirer un role a un utilisateur.

**Body :**
```json
{
  "role_name": "admin"
}
```

**Reponse 200 :**
```json
{
  "message": "Role retire.",
  "user": { ... }
}
```

**Erreurs :**
- `400` — L'utilisateur ne possede pas ce role

---

### GET `/api/admin/users/<user_id>/roles`

Voir les roles d'un utilisateur.

**Reponse 200 :**
```json
[
  {
    "id": 1,
    "name": "admin",
    "description": "Administrator",
    "permissions": []
  }
]
```

**Erreurs :**
- `404` — Utilisateur introuvable

---

### POST `/api/admin/roles/<role_name>/permissions`

Assigner une permission a un role.

**Body :**
```json
{
  "permission_codename": "users:delete"
}
```

**Reponse 200 :**
```json
{
  "message": "Permission assignee au role.",
  "role": { ... }
}
```

**Erreurs :**
- `400` — Role ou permission introuvable

---

## Commerce (Stepper)

> Workflow de creation d'un commerce en 3 etapes.
> Toutes les routes necessitent un `access_token` sauf `GET /api/categories`.

### POST `/api/commerces` — Step 1

Creer un commerce (draft). Le commerce est cree avec `is_active: false`.

**Header :**
```
Authorization: Bearer <access_token>
```

**Body :**
```json
{
  "nom_commercial": "Boulangerie du Coin",
  "whatsapp_numero": "+22507070707",
  "contact_telephonique": "+22501010101",
  "categorie_id": 1,
  "description": "Meilleur pain de la ville"
}
```

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| nom_commercial | string | Oui | Nom du commerce (max 200) |
| whatsapp_numero | string | Non | Numero WhatsApp |
| contact_telephonique | string | Non | Numero de telephone |
| categorie_id | integer | Oui | ID de la categorie |
| description | string | Non | Description de l'activite (max 2000) |

**Reponse 201 :**
```json
{
  "id": 1,
  "user_id": 1,
  "nom_commercial": "Boulangerie du Coin",
  "whatsapp_numero": "+22507070707",
  "contact_telephonique": "+22501010101",
  "categorie_id": 1,
  "description": "Meilleur pain de la ville",
  "latitude": null,
  "longitude": null,
  "adresse_complete": null,
  "is_verified": false,
  "is_active": false,
  "step": 1,
  "photos": [],
  "horaires": [],
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Erreurs :**
- `400` — Champs manquants ou categorie inconnue/inactive
- `401` — Token manquant ou invalide

---

### PUT `/api/commerces/<commerce_id>/localisation` — Step 2

Ajouter la localisation et les horaires d'ouverture.

**Header :**
```
Authorization: Bearer <access_token>
```

**Body :**
```json
{
  "latitude": 12.37143,
  "longitude": -1.51966,
  "adresse_complete": "123 Avenue de l'Innovation, Secteur 5, Ouagadougou, Burkina Faso",
  "horaires": [
    {"jour": "lundi", "heure_ouverture": "08:00", "heure_fermeture": "18:00", "est_ferme": false, "est_24h": false},
    {"jour": "mardi", "heure_ouverture": "08:00", "heure_fermeture": "18:00", "est_ferme": false, "est_24h": false},
    {"jour": "mercredi", "heure_ouverture": "08:00", "heure_fermeture": "18:00", "est_ferme": false, "est_24h": false},
    {"jour": "jeudi", "heure_ouverture": "08:00", "heure_fermeture": "18:00", "est_ferme": false, "est_24h": false},
    {"jour": "vendredi", "heure_ouverture": "08:00", "heure_fermeture": "18:00", "est_ferme": false, "est_24h": false},
    {"jour": "samedi", "heure_ouverture": "08:00", "heure_fermeture": "12:00", "est_ferme": false, "est_24h": false},
    {"jour": "dimanche", "heure_ouverture": null, "heure_fermeture": null, "est_ferme": true, "est_24h": false}
  ]
}
```

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| latitude | float | Oui | Latitude GPS |
| longitude | float | Oui | Longitude GPS |
| adresse_complete | string | Oui | Adresse textuelle (max 500) |
| horaires | array | Oui | **Exactement 7 objets** (un par jour, lundi a dimanche) |

**Objet horaire :**

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| jour | string | Oui | `lundi`, `mardi`, `mercredi`, `jeudi`, `vendredi`, `samedi`, `dimanche` (minuscules) |
| heure_ouverture | string | Null OK | Format `HH:MM` (ex: `08:00`). `null` si `est_ferme: true` |
| heure_fermeture | string | Null OK | Format `HH:MM` (ex: `18:00`). `null` si `est_ferme: true` |
| est_ferme | boolean | Non | `true` si ferme ce jour (defaut: `false`) |
| est_24h | boolean | Non | `true` si ouvert 24h (defaut: `false`) |

**Notes :**
- Les jours doivent etre en **minuscules** (`lundi`, pas `Lundi`)
- Si `est_ferme: true`, envoyer `null` pour `heure_ouverture` et `heure_fermeture`
- Les 7 jours sont obligatoires, meme pour les jours fermes

**Reponse 200 :**
```json
{
  "id": 1,
  "user_id": 1,
  "nom_commercial": "BICABA SHOP",
  "whatsapp_numero": "07 92 60 54",
  "contact_telephonique": "07 92 60 54",
  "categorie_id": 1,
  "description": "Pro en confection de table",
  "latitude": 12.37143,
  "longitude": -1.51966,
  "adresse_complete": "123 Avenue de l'Innovation, Secteur 5, Ouagadougou",
  "is_verified": false,
  "is_active": false,
  "step": 2,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Erreurs :**
- `400` — Champs manquants, 7 horaires requis, jour invalide (minuscules), heure au format `HH:MM`
- `401` — Token manquant ou invalide
- `403` — Pas le proprietaire du commerce

---

### POST `/api/commerces/<commerce_id>/photos` — Step 3

Uploader des photos (1 a 3 images).

**Header :**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Body (FormData) :**

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| photos | file[] | Oui | 1 a 3 images (JPG, PNG, WebP, max 5MB chacune) |

**Exemple JavaScript :**
```javascript
const formData = new FormData();
files.forEach(file => formData.append('photos', file));

const response = await fetch('/api/commerces/1/photos', {
  method: 'POST',
  headers: { 'Authorization': `Bearer ${token}` },
  body: formData,
});
```

**Reponse 201 :**
```json
[
  {
    "id": 1,
    "commerce_id": 1,
    "url": "https://res.cloudinary.com/.../image.jpg",
    "alt_text": "Photo 1",
    "ordre": 1,
    "is_principale": true
  }
]
```

**Erreurs :**
- `400` — Aucune photo, type non autorise, fichier trop volumineux, max 3 photos
- `401` — Token manquant ou invalide
- `403` — Pas le proprietaire du commerce

---

### DELETE `/api/commerces/<commerce_id>/photos/<photo_id>`

Supprimer une photo.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "message": "Photo supprimee."
}
```

**Erreurs :**
- `400` — Photo introuvable ou pas le proprietaire

---

### PATCH `/api/commerces/<commerce_id>/publish`

Publier le commerce (passe `is_active` a `true`). Verifie que toutes les etapes sont completes.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "id": 1,
  "user_id": 1,
  "nom_commercial": "Boulangerie du Coin",
  "is_active": true,
  ...
}
```

**Erreurs :**
- `400` — Etape 2 non terminee (localisation manquante) ou Etape 3 non terminee (aucune photo)
- `401` — Token manquant ou invalide
- `403` — Pas le proprietaire du commerce

---

### GET `/api/commerces/<commerce_id>`

Recuperer les details d'un commerce.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "id": 1,
  "user_id": 1,
  "nom_commercial": "Boulangerie du Coin",
  "whatsapp_numero": "+22507070707",
  "contact_telephonique": "+22501010101",
  "categorie_id": 1,
  "description": "Meilleur pain de la ville",
  "latitude": 5.36,
  "longitude": -4.0083,
  "adresse_complete": "Abidjan, Cocody",
  "is_verified": false,
  "is_active": true,
  "step": 3,
  "photos": [
    {
      "id": 1,
      "url": "https://res.cloudinary.com/.../image.jpg",
      "alt_text": "Photo 1",
      "ordre": 1,
      "is_principale": true
    }
  ],
  "horaires": [
    {
      "id": 1,
      "jour": "lundi",
      "heure_ouverture": "08:00",
      "heure_fermeture": "18:00",
      "est_ferme": false,
      "est_24h": false
    }
  ],
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Erreurs :**
- `400` — Pas le proprietaire du commerce
- `401` — Token manquant ou invalide

---

## Categories

### GET `/api/categories`

Lister les categories actives. **Pas d'authentification requise.**

**Reponse 200 :**
```json
[
  {
    "id": 1,
    "nom": "Boulangerie",
    "is_active": true,
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  },
  {
    "id": 2,
    "nom": "Restaurant",
    "is_active": true,
    "created_at": "2025-01-01T00:00:00",
    "updated_at": "2025-01-01T00:00:00"
  }
]
```

---

### POST `/api/categories`

Creer une nouvelle categorie.

**Header :**
```
Authorization: Bearer <access_token>
```

**Body :**
```json
{
  "nom": "Coiffure"
}
```

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| nom | string | Oui | Nom unique (max 150) |

**Reponse 201 :**
```json
{
  "id": 3,
  "nom": "Coiffure",
  "is_active": true,
  "created_at": "2025-01-01T00:00:00",
  "updated_at": "2025-01-01T00:00:00"
}
```

**Erreurs :**
- `400` — Champs manquants ou invalides
- `401` — Token manquant ou invalide
- `409` — La categorie existe deja

---

## Artisan Dashboard

### GET `/api/artisan/home`

Dashboard de l'artisan — "Bienvenue, Prenom" + stats + commerce complet.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "message": "Bienvenue, Admin",
  "commerce": {
    "id": 1,
    "user_id": 1,
    "nom_commercial": "BICABA SHOP",
    "description": "Pro en confection de table",
    "categorie": {"id": 1, "nom": "Menusier", "is_active": true},
    "is_vendeur_produits": false,
    "is_active": true,
    "stats": {
      "nb_vues_profile": 142,
      "nb_favoris": 23,
      "last_vue_at": "2026-06-27T10:30:00"
    },
    "photos": [...],
    "horaires": [...],
    "produit_images": [...]
  },
  "geolocalisation_url": "https://wa.me/?text=..."
}
```

**Erreurs :**
- `401` — Token manquant ou invalide
- `404` — Aucun commerce trouve pour cet artisan

---

### GET `/api/artisan/profile`

Profil complet de l'artisan connecte — infos utilisateur + tous ses commerces.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "user": {
    "id": 4,
    "email": "artisan_pro@zulu.com",
    "first_name": "Kofi",
    "last_name": "Artisan",
    "is_verified": true
  },
  "commerces": [
    {
      "id": 2,
      "nom_commercial": "Atelier Kofi",
      "contact_telephonique": null,
      "whatsapp_numero": null,
      "is_active": false
    }
  ],
  "nb_commerces_actifs": 1
}
```

**Notes :**
- Concu pour le multi-commerce futur (retourne un tableau `commerces[]`)
- `nb_commerces_actifs` : nombre de commerces actifs uniquement (`is_active: true`)
- `is_verified` : email verifie ou non
- `is_active` : commerce active (publie) ou en draft

**Erreurs :**
- `401` — Token manquant ou invalide
- `404` — Utilisateur introuvable

---

## Vues (Profile)

### POST `/api/commerces/<commerce_id>/vues`

Enregistrer une vue sur le profile d'un commerce. **Pas d'auth requise.**
Anti-spam : une meme IP ne comptabilise qu'une vue toutes les 24h.

**Body :** (vide ou JSON)

**Reponse 201 :**
```json
{
  "message": "Vue enregistree.",
  "counted": true
}
```

Si doublon dans les 24h :
```json
{
  "message": "Vue deja enregistree.",
  "counted": false
}
```

---

## Favoris

### POST `/api/commerces/<commerce_id>/favoris`

Ajouter un commerce aux favoris.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 201 :**
```json
{
  "message": "Ajoute aux favoris.",
  "favori": {"id": 1, "user_id": 1, "commerce_id": 1}
}
```

**Erreurs :**
- `400` — Deja en favori
- `401` — Token manquant ou invalide

---

### DELETE `/api/commerces/<commerce_id>/favoris`

Retirer un commerce des favoris.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "message": "Retire des favoris."
}
```

**Erreurs :**
- `400` — Favori introuvable
- `401` — Token manquant ou invalide

---

### GET `/api/favoris`

Lister les favoris de l'utilisateur connecte.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "commerce_id": 1,
    "commerce": { ... }
  }
]
```

---

## Images de Produits

### POST `/api/commerces/<commerce_id>/produit-images`

Uploader une image de produit (max 5, uniquement si `is_vendeur_produits: true`).

**Header :**
```
Authorization: Bearer <access_token>
Content-Type: multipart/form-data
```

**Body (FormData) :**

| Champ | Type | Requis | Description |
|-------|------|--------|-------------|
| image | file | Oui | Image JPG, PNG ou WebP (max 5MB) |

**Reponse 201 :**
```json
{
  "id": 1,
  "commerce_id": 1,
  "url": "https://res.cloudinary.com/.../image.jpg",
  "ordre": 1
}
```

**Erreurs :**
- `400` — Max 5 images, type non autorise, fichier trop volumineux
- `403` — Ce commerce ne vend pas de produits

---

### DELETE `/api/commerces/<commerce_id>/produit-images/<image_id>`

Supprimer une image de produit.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "message": "Image produit supprimee."
}
```

**Erreurs :**
- `400` — Image introuvable
- `403` — Acces refuse

---

## Geolocalisation

### GET `/api/commerces/<commerce_id>/geolocalisation`

Generer un lien WhatsApp pour partager la localisation du commerce.

**Header :**
```
Authorization: Bearer <access_token>
```

**Reponse 200 :**
```json
{
  "geolocalisation_url": "https://wa.me/?text=Voici+la+localisation+de+BICABA+SHOP+sur+Google+Maps:+https://maps.google.com/?q=12.37,-1.51"
}
```

**Notes :**
- Le lien ouvre WhatsApp avec le message pre-rempli
- L'utilisateur choisit ensuite les contacts a qui envoyer

---

## Health

### GET `/api/health`

Verifier que l'API est operationnelle. **Pas d'authentification requise.**

**Reponse 200 :**
```json
{
  "status": "ok",
  "message": "Zulu Starter API is running"
}
```

---

## Flow du Stepper (Recapitulatif)

```
1. POST /api/auth/register          → Inscription (role "client" auto-assigne)
2. POST /api/auth/login             → Recuperer les tokens
3. GET  /api/categories             → Lister les categories
4. POST /api/commerces              → Step 1: Infos de base
5. PUT  /api/commerces/{id}/localisation → Step 2: Geo + 7 Horaires
6. POST /api/commerces/{id}/photos  → Step 3: Photos (1 a 3, Cloudinary)
7. PATCH /api/commerces/{id}/publish → Finaliser (is_active = true)
```

**Notes :**
- Le commerce est cree en draft (`is_active: false`)
- L'artisan peut naviguer entre les etapes (avant/arriere)
- Chaque step doit etre rempli avant de passer au suivant
- `publish` verifie que toutes les etapes sont completes
- Les 7 horaires sont obligatoires (jours en minuscules)
- Si un jour est ferme, envoyer `null` pour les heures

---

## Headers communs

| Header | Valeur | Quand |
|--------|--------|-------|
| Authorization | `Bearer <access_token>` | Toutes les routes authentifiees |
| Content-Type | `application/json` | Routes avec body JSON |
| Content-Type | `multipart/form-data` | Upload de photos |

---

## Codes d'erreur

| Code | Signification |
|------|---------------|
| 400 | Requete invalide (champs manquants, validation echouee) |
| 401 | Non authentifie (token manquant, invalide ou expire) |
| 403 | Non autorise (role ou permissions insuffisants) |
| 404 | Ressource introuvable |
| 409 | Conflit (email ou role deja existant) |
| 429 | Trop de requetes (rate limiting) |
| 500 | Erreur serveur interne |
