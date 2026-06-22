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
| Marshmallow | Validation et sérialisation des données |
| PostgreSQL 15 | Base de données relationnelle |
| Docker + Docker Compose | Conteneurisation |
| Swagger / Flasgger | Documentation interactive des API |
| Pytest | Tests unitaires et d'intégration |

---

## Structure des dossiers

```
backend/
├── app/
│   ├── __init__.py          # Factory create_app — initialise l'app et enregistre les blueprints
│   ├── config.py            # Configuration par environnement (dev, prod)
│   ├── extensions.py        # Instanciation des extensions Flask (db, jwt, migrate, cors)
│   ├── models/              # Modèles SQLAlchemy — représentent les tables de la base
│   │   ├── __init__.py      # Exports centralisés des modèles
│   │   └── base.py          # Modèle abstrait dont héritent tous les modèles
│   ├── routes/              # Blueprints Flask — définissent les endpoints HTTP
│   │   ├── __init__.py      # Enregistrement centralisé de tous les blueprints
│   │   └── health.py        # Endpoint GET /api/health
│   ├── schemas/             # Schémas Marshmallow — validation entrée et sérialisation sortie
│   └── services/            # Logique métier pure — sans dépendance à Flask ou HTTP
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures Pytest (app de test, client HTTP, DB en mémoire)
│   ├── unit/                # Tests unitaires — testent les services isolément
│   │   └── __init__.py
│   └── integration/         # Tests d'intégration — testent les routes HTTP complètes
│       └── __init__.py
├── migrations/              # Fichiers de migration générés automatiquement par Alembic
├── Dockerfile               # Image Docker du backend
├── requirements.txt         # Dépendances Python de production
├── requirements-dev.txt     # Dépendances Python de développement (pytest, etc.)
├── run.py                   # Point d'entrée de l'application
└── .env.example             # Template des variables d'environnement
```

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

### schemas/
Un schéma par ressource.
Utiliser load() pour valider et désérialiser les données entrantes.
Utiliser dump() pour sérialiser les données sortantes.

### config.py
Trois classes : Config (base), DevelopmentConfig, ProductionConfig.
Toutes les valeurs sensibles viennent du fichier .env via python-dotenv.
Jamais de valeur sensible en dur dans le code.

### extensions.py
Instancie les extensions sans les lier à une application concrète.
Le lien se fait dans create_app() via la méthode init_app() de chaque extension.
Ce pattern (Application Factory) évite les imports circulaires et facilite les tests.

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

### Installer Flasgger

Ajouter dans requirements.txt :

```
flasgger==0.9.7.1
```

Initialiser dans extensions.py :

```python
from flasgger import Swagger
swagger = Swagger()
```

Lier dans create_app() :

```python
swagger.init_app(app)
```

---

## Tests — Pytest

### Structure des tests

```
tests/
├── conftest.py        # Fixtures partagées entre tous les tests
├── unit/              # Tests des services (logique métier isolée)
└── integration/       # Tests des routes HTTP complètes
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
    yield
    with app.app_context():
        for table in reversed(_db.metadata.sorted_tables):
            _db.session.execute(table.delete())
        _db.session.commit()
```

### Exemple de test unitaire (service)

```python
# tests/unit/test_product_service.py
def test_create_product(app):
    with app.app_context():
        product = product_service.create({"name": "Mil", "price": 500})
        assert product.id is not None
        assert product.name == "Mil"
```

### Exemple de test d'intégration (route)

```python
# tests/integration/test_product_routes.py
def test_get_products_returns_200(client):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
```

### Lancer les tests

```bash
# Tous les tests
docker compose exec backend pytest

# Avec détail
docker compose exec backend pytest -v

# Un seul fichier
docker compose exec backend pytest tests/unit/test_product_service.py

# Avec couverture de code
docker compose exec backend pytest --cov=app
```

---

## Ajouter une nouvelle ressource

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
| FLASK_ENV | Environnement actif | development |
| SECRET_KEY | Clé secrète Flask | une-chaine-aleatoire-longue |
| JWT_SECRET_KEY | Clé de signature JWT | une-autre-chaine-aleatoire |
| DATABASE_URL | URL complète PostgreSQL | postgresql://user:pass@localhost:5432/db |
| DB_HOST | Hôte de la base | localhost |
| DB_PORT | Port PostgreSQL | 5432 |
| DB_NAME | Nom de la base | zulu_db |
| DB_USER | Utilisateur PostgreSQL | zulu_user |
| DB_PASSWORD | Mot de passe PostgreSQL | zulu_pass |

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