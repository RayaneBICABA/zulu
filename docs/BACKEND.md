# Backend — Architecture & Structure

## Stack technique

| Outil | Role |
|---|---|
| Python 3.11 | Runtime |
| Flask 3.1 | Framework web |
| SQLAlchemy | ORM |
| Flask-Migrate | Migrations de base de données (Alembic) |
| Flask-JWT-Extended | Authentification par tokens JWT |
| Flask-Cors | Gestion du CORS |
| Flask-Limiter | Rate limiting |
| Marshmallow | Validation et sérialisation des données |
| PostgreSQL 15 | Base de données relationnelle |
| Docker + Docker Compose | Conteneurisation |
| Swagger / Flasgger | Documentation interactive des API |
| Redis 7 | Stockage du rate limiting (flask-limiter) |
| smtplib | Envoi d'emails SMTP (Gmail, Brevo, etc.) |
| Pytest | Tests unitaires et d'intégration |

---

## Structure des dossiers

```
backend/
├── app/
│   ├── __init__.py          # Factory create_app — initialise l'app et enregistre les blueprints
│   ├── config.py            # Configuration par environnement (dev, prod, test)
│   ├── extensions.py        # Instanciation des extensions Flask (db, jwt, migrate, cors, swagger, limiter)
│   ├── models/              # Modèles SQLAlchemy — représentent les tables de la base
│   │   ├── __init__.py      # Exports centralisés des modèles
│   │   ├── base.py          # Modèle abstrait dont héritent tous les modèles
│   │   ├── user.py          # User (email, password_hash, first_name, last_name, is_verified, is_active, roles M2M)
│   │   └── role.py          # Role (name, description, permissions M2M) + Permission (codename, name, description)
│   ├── routes/              # Blueprints Flask — définissent les endpoints HTTP
│   │   ├── __init__.py      # Enregistrement centralisé de tous les blueprints
│   │   ├── health.py        # Endpoint GET /api/health
│   │   ├── auth.py          # Blueprint /api/auth/* (register, login, refresh, me, verify-email, forgot-password, reset-password)
│   │   ├── oauth.py         # Blueprint /api/auth/google/* (login, callback)
│   │   ├── admin.py         # Blueprint /api/admin/* (roles, permissions, assignation)
│   │   └── diagram.py       # Blueprint /api/diagram/* (génération automatique de diagramme de classes UML)
│   ├── schemas/             # Schémas Marshmallow — validation entrée et sérialisation sortie
│   │   ├── __init__.py
│   │   └── auth_schema.py   # RegisterSchema, LoginSchema, UserSchema
│   └── services/            # Logique métier pure — sans dépendance à Flask ou HTTP
│       ├── __init__.py      # Instances des services (auth_service, role_service)
│       ├── auth_service.py  # AuthService : register, login, refresh, me, verify_email, forgot_password, reset_password
│       ├── role_service.py  # RoleService : CRUD roles/permissions, assignation + décorateurs @role_required, @permission_required
│       ├── email_service.py # Génération/confirmation de tokens (itsdangerous), envoi SMTP (smtplib)
│       ├── oauth_service.py # Authlib OAuth, init OAuth providers, google_login
│       └── diagram_service.py # Génération de diagramme de classes UML (Mermaid.js) par introspection SQLAlchemy
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures Pytest (app de test, client HTTP, DB en mémoire)
│   ├── unit/                # Tests unitaires — testent les services isolément
│   │   ├── __init__.py
│   │   ├── test_auth_service.py
│   │   └── test_role_service.py
│   └── integration/         # Tests d'intégration — testent les routes HTTP complètes
│       ├── __init__.py
│       ├── test_health.py
│       ├── test_auth.py
│       └── test_admin.py
├── migrations/              # Fichiers de migration générés automatiquement par Alembic
├── Dockerfile               # Image Docker du backend
├── requirements.txt         # Dépendances Python de production
├── run.py                   # Point d'entrée de l'application
├── pytest.ini               # Configuration Pytest
└── .env.example             # Template des variables d'environnement
```

---

## Authentification

Voir `docs/AUTH.md` pour la documentation complète du système d'authentification et RBAC.

### Architecture

```
Client
  POST /api/auth/login
    -> auth_bp.login()
      -> LoginSchema.load()      # Validation Marshmallow
      -> auth_service.login()    # Logique métier
        -> User.check_password() # Vérification bcrypt
        -> create_access_token() # JWT 15min
        -> create_refresh_token() # JWT 7 jours
      -> jsonify(result), 200
```

### Routes disponibles

#### Authentification publique

| Méthode | Endpoint | Rate limit | Description |
|---|---|---|---|
| POST | /api/auth/register | 3/min | Inscription |
| POST | /api/auth/login | 5/min | Connexion |
| POST | /api/auth/refresh | -- | Rafraîchir le token (Bearer refresh_token) |
| POST | /api/auth/verify-email | -- | Confirmer l'email |
| POST | /api/auth/forgot-password | 3/min | Demander un reset |
| POST | /api/auth/reset-password | 3/min | Réinitialiser le mot de passe |
| GET | /api/auth/google/login | -- | Redirection Google OAuth |
| GET | /api/auth/google/callback | 5/min | Callback Google |

#### Authentification requise (Bearer token)

| Méthode | Endpoint | Description |
|---|---|---|
| GET | /api/auth/me | Profil utilisateur |
| POST | /api/auth/resend-verification | Renvoyer l'email de confirmation |

#### Administration (Bearer token + admin role)

| Méthode | Endpoint | Description |
|---|---|---|
| GET | /api/admin/roles | Lister les rôles |
| POST | /api/admin/roles | Créer un rôle |
| GET | /api/admin/permissions | Lister les permissions |
| POST | /api/admin/permissions | Créer une permission |
| POST | /api/admin/users/<id>/roles | Assigner un rôle |
| DELETE | /api/admin/users/<id>/roles | Retirer un rôle |
| GET | /api/admin/users/<id>/roles | Voir les rôles d'un utilisateur |
| POST | /api/admin/roles/<name>/permissions | Assigner une permission à un rôle |

---

## Rôle de chaque couche

### models/
Contient uniquement les classes SQLAlchemy représentant les tables.
Aucune logique métier ici.
Tout modèle hérite de BaseModel qui fournit automatiquement :
- id (clé primaire auto-incrémentée)
- created_at (date de création)
- updated_at (date de dernière modification)
- save() — persiste l'objet en base
- delete() — supprime l'objet de la base
- to_dict() — sérialise l'objet en dictionnaire

### schemas/
Contient les schémas Marshmallow.
Deux usages : valider les données entrantes (body de requête) et sérialiser les données sortantes (réponse JSON).
Chaque schéma correspond à un modèle.
Les schémas sont le seul endroit où les règles de format et d'obligation des champs sont définies.

### services/
Contient la logique métier pure.
Un service reçoit des données déjà validées, applique les règles métier, interagit avec les modèles.
Un service ne connaît pas Flask. Pas de request, pas de jsonify, pas de code HTTP ici.
Ce découplage permet de tester la logique métier sans démarrer un serveur HTTP.

### routes/
Contient les blueprints Flask.
Le rôle d'une route est strictement limité à :
1. Recevoir la requête HTTP
2. Valider les données via le schéma correspondant
3. Appeler le service approprié
4. Retourner la réponse JSON avec le bon code HTTP

Une route ne contient pas de logique métier.
Une route ne fait pas de requête directe à la base de données.

### config.py
Trois classes : Config (base), DevelopmentConfig, ProductionConfig, TestingConfig.
Toutes les valeurs sensibles viennent du fichier .env via python-dotenv.
Jamais de valeur sensible en dur dans le code.

### extensions.py
Instancie les extensions sans les lier à une application concrète :
- db (SQLAlchemy)
- migrate (Flask-Migrate)
- jwt (Flask-JWT-Extended)
- cors (Flask-Cors)
- swagger (Flasgger)
- limiter (Flask-Limiter avec support Redis via LIMITER_STORAGE_URL)

### Decorators RBAC

```python
from app.services.role_service import role_required, permission_required

@role_required("admin")
def admin_only_route():
    pass

@permission_required("users:delete")
def delete_user():
    pass
```

---

## Documentation interactive des API — Flasgger (Swagger)

Flasgger génère automatiquement une interface Swagger accessible dans le navigateur.
Une fois le serveur lancé, la documentation est disponible à l'adresse :

```
http://localhost:5000/apidocs
```

### Ajouter la documentation à une route

Documenter chaque endpoint avec un docstring YAML dans la fonction de route :

```python
@product_bp.route("/products", methods=["GET"])
def get_products():
    """
    Liste tous les produits.
    ---
    tags:
      - Produits
    responses:
      200:
        description: Liste des produits retournée avec succès
      500:
        description: Erreur serveur
    """
    products = product_service.get_all()
    return jsonify([p.to_dict() for p in products]), 200
```

### Sécurité JWT dans Swagger

Pour documenter qu'une route nécessite un token JWT, ajouter la section security :

```python
responses:
  401:
    description: Token manquant ou invalide
security:
  - Bearer: []
```

**Toutes les routes admin et les routes protégées sont documentées avec Swagger.**

---

## Tests — Pytest

### Lancer les tests

```bash
cd backend
python -m pytest -v
```

### Structure des tests

```
tests/
├── conftest.py        # Fixtures partagées entre tous les tests
├── unit/              # Tests des services (logique métier isolée)
│   ├── test_auth_service.py
│   └── test_role_service.py
└── integration/       # Tests des routes HTTP complètes
    ├── test_health.py
    ├── test_auth.py
    └── test_admin.py
```

### conftest.py — Fixtures de base

```python
import pytest
from app import create_app
from app.extensions import db as _db

@pytest.fixture(scope="session")
def app():
    app = create_app("testing")
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def clean_db(app):
    """
    Nettoie toutes les tables après chaque test.
    Garantit l'isolation entre les tests.
    """
    yield
    with app.app_context():
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
```

### Couverture des tests (66 tests)

| Fichier | Tests | Ce qui est testé |
|---|---|---|
| `unit/test_auth_service.py` | 12 | register (validation, doublon), login (succès, mauvais password, email inconnu, inactif), verify_email (succès, token invalide), forgot/reset (envoi silencieux, changement, token invalide), me (succès, introuvable), refresh (succès, inactif) |
| `unit/test_role_service.py` | 10 | create_role (succès, doublon), list_roles, get_user_roles (introuvable), create_permission (succès, doublon), list_permissions, assign_role (succès, introuvable, doublon), remove_role, assign_permission (succès, role introuvable), has_permission |
| `integration/test_health.py` | 2 | Status 200, body correct |
| `integration/test_auth.py` | 15 | Register (201, 400, 409), Login (200, 401, 400), Me (200, 401), Refresh (200, 401), VerifyEmail (200, 400 x2), ForgotPassword (200 x2, 400), ResetPassword (200, 400 x2) |
| `integration/test_admin.py` | 15 | Roles (list admin/403/401, create 201/400/409), Permissions (list, create 201/409), Assign/remove role (200), Get user roles (200/404), Assign permission (200/400) |

---

## Sécurité

### Rate limiting (Redis)
- Login : 5 tentatives par minute
- Register : 3 tentatives par minute
- Forgot/reset password : 3 tentatives par minute
- Google callback : 5 tentatives par minute
- Réponse 429 avec message explicatif
- Désactivé en mode test (RATELIMIT_ENABLED = False)
- Stockage : Redis via `LIMITER_STORAGE_URL`. Si vide, utilise la mémoire (warning).

### Mots de passe
- Hashés avec `werkzeug.security.generate_password_hash` (pbkdf2:sha256)
- bcrypt installé en dépendance, utilisé si disponible
- Validation longueur minimale : 8 caractères

### Tokens JWT
- Access token : 15 minutes
- Refresh token : 7 jours
- Claims inclus : email, is_verified
- Gestion des erreurs : expired, invalid, missing

### Tokens de vérification
- Email verification : itsdangerous URLSafeTimedSerializer, expire 24h
- Password reset : itsdangerous URLSafeTimedSerializer, expire 1h
- Stockés dans l'URL, envoyés par email

### Emails (SMTP)
- Utilise `smtplib` avec TLS sur le port 587
- `MAIL_PASSWORD` obligatoire (pas de fallback) — lève une erreur si absent
- Pour Gmail : créer un [App Password](https://support.google.com/accounts/answer/185833) (pas le mot de passe du compte)
- Compatible avec tout fournisseur SMTP (Brevo 300/jour gratuit, SendGrid, Mailgun, etc.)

### Protection anti-énumération
- Forgot password retourne le même message que l'email existe ou non

---

## Diagramme de classes UML

Le module `diagram_service.py` inspecte tous les modèles SQLAlchemy enregistrés dans `app.extensions.db` et génère un diagramme de classes au format [Mermaid.js](https://mermaid.js.org/).

### Fonctionnement

1. Parcourt tous les modèles héritant de `BaseModel`
2. Extrait pour chaque modèle : les colonnes (nom, type, PK, FK, nullable, défaut), les relations (type de lien, multiplicité), l'héritage
3. Génère le texte Mermaid avec la syntaxe `classDiagram`
4. Retourne soit le texte brut, soit une page HTML interactive

### Endpoints

| Méthode | Endpoint | Description |
|---|---|---|
| GET | /api/diagram | Texte brut Mermaid (Content-Type: text/plain) |
| GET | /api/diagram/view | Page HTML avec rendu visuel du diagramme |

### Page HTML interactive (`/api/diagram/view`)

- Diagramme rendu avec Mermaid.js (CDN v11)
- Bouton **Telecharger PNG** : exporte le diagramme en PNG 2x via canvas + base64 data URI
- Bouton **Code source** : affiche le texte Mermaid brut
- Bouton **Copier le code** : copie le texte Mermaid dans le presse-papier
- Couleurs : rose `#c61458` et bleu foncé `#08275d`

### Architecture du code

```
app/services/diagram_service.py   — Logique pure (introspection, génération Mermaid, HTML)
app/routes/diagram.py            — Endpoints HTTP
```

Le service est découplé de Flask : `generate_mermaid()` retourne du texte, `get_html_diagram()` retourne du HTML. Les routes ne font que déléguer.

### Ajouter un modèle au diagramme

Le diagramme est généré dynamiquement. Il suffit de créer un modèle héritant de `BaseModel` et de l'exporter dans `app/models/__init__.py`. Le diagramme l'inclura automatiquement au prochain appel.

---

Exemple complet : ajouter la ressource "Produit"

1. Créer app/models/product.py — définir la classe Product qui hérite de BaseModel
2. Exporter dans app/models/__init__.py — ajouter from .product import Product
3. Créer app/schemas/product_schema.py — définir ProductSchema avec Marshmallow
4. Créer app/services/product_service.py — implémenter create, get_all, get_by_id, update, delete
5. Créer app/routes/product.py — créer le blueprint product_bp avec les endpoints
6. Enregistrer dans app/routes/__init__.py — ajouter app.register_blueprint(product_bp, url_prefix="/api")
7. Générer la migration — flask db migrate -m "add product table"
8. Appliquer la migration — flask db upgrade
9. Écrire les tests dans tests/unit/ et tests/integration/

---

## Variables d'environnement

Copier .env.example en .env et renseigner toutes les valeurs avant de démarrer.

| Variable | Description | Exemple |
|---|---|---|
| FLASK_APP | Point d'entrée Flask | run.py |
| FLASK_ENV | Environnement actif | production |
| SECRET_KEY | Clé secrète Flask / itsdangerous | une-chaine-aleatoire-longue |
| JWT_SECRET_KEY | Clé de signature JWT (>= 32 bytes) | une-autre-chaine-longue |
| DATABASE_URL | URL complète PostgreSQL | postgresql://user:pass@localhost:5432/db |
| DB_HOST | Hôte de la base | localhost |
| DB_PORT | Port PostgreSQL | 5432 |
| DB_NAME | Nom de la base | zulu_db |
| DB_USER | Utilisateur PostgreSQL | zulu_user |
| DB_PASSWORD | Mot de passe PostgreSQL | zulu_pass |
| FRONTEND_URL | URL du frontend (liens email) | http://localhost:5173 |
| LIMITER_STORAGE_URL | Redis URI pour le rate limiting (vide = mémoire) | redis://localhost:6379/0 |
| MAIL_SERVER | Serveur SMTP | smtp.gmail.com |
| MAIL_PORT | Port SMTP | 587 |
| MAIL_USERNAME | Utilisateur SMTP | rayanebicaba.dev@gmail.com |
| MAIL_PASSWORD | Mot de passe ou App Password SMTP | (obligatoire en prod) |
| MAIL_DEFAULT_SENDER | Adresse d'envoi par défaut | rayanebicaba.dev@gmail.com |
| MAIL_USE_TLS | TLS actif ou non | true |
| GOOGLE_CLIENT_ID | ID client Google OAuth (obligatoire pour Google login) | (optionnel) |
| GOOGLE_CLIENT_SECRET | Secret client Google OAuth (obligatoire pour Google login) | (optionnel) |

---

## Conventions obligatoires

- Nommage des fichiers et variables : snake_case
- Nommage des classes : PascalCase
- Un blueprint par ressource
- Un service par ressource
- Un schéma par ressource
- Aucune logique métier dans les routes
- Aucun accès direct à la base de données dans les routes
- Toujours valider les données entrantes via un schéma avant de les passer au service
- Toujours documenter les endpoints avec un docstring Swagger
- Tout nouveau modèle hérite de BaseModel
- Toute nouvelle fonctionnalité est accompagnée de ses tests
