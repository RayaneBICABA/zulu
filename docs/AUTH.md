# Systeme d'authentification et RBAC

## Vue d'ensemble

Le systeme d'authentification couvre l'inscription, la connexion, la verification email, la recuperation de mot de passe, l'authentification via Google OAuth, et le controle d'acces par roles et permissions (RBAC).

---

## Backend

### Architecture des fichiers

```
backend/app/
  models/
    user.py           User (email, password_hash, first_name, last_name, is_verified, is_active, roles M2M)
    role.py           Role (name, description, permissions M2M) + Permission (codename, name, description)
  schemas/
    auth_schema.py    RegisterSchema, LoginSchema, UserSchema (validation Marshmallow)
  services/
    auth_service.py   register, login, refresh, me, verify_email, forgot_password, reset_password
    oauth_service.py  google_login (auto-register ou connexion)
    role_service.py   create_role, assign_role, create_permission, assign_permission
    email_service.py  Generation/confirmation de tokens (itsdangerous), envoi SMTP (smtplib)
  routes/
    auth.py           Blueprint /api/auth/* (register, login, refresh, me, verify-email, forgot-password, reset-password)
    oauth.py          Blueprint /api/auth/google/* (login, callback)
    admin.py          Blueprint /api/admin/* (roles CRUD, permissions, assignation)
```

### Endpoints disponibles

#### Authentification

| Methode | Endpoint | Description | Rate limit | Auth |
|---|---|---|---|---|
| POST | /api/auth/register | Inscription | 3/min | Non |
| POST | /api/auth/login | Connexion | 5/min | Non |
| POST | /api/auth/refresh | Rafraichir le token | -- | Refresh token |
| GET | /api/auth/me | Profil utilisateur | -- | Access token |
| POST | /api/auth/verify-email | Confirmer l'email | -- | Non |
| POST | /api/auth/resend-verification | Renvoyer l'email de confirmation | -- | Access token |
| POST | /api/auth/forgot-password | Demande de reinitialisation | 3/min | Non |
| POST | /api/auth/reset-password | Reinitialiser le mot de passe | 3/min | Non |
| GET | /api/auth/google/login | Rediriger vers Google OAuth | -- | Non |
| GET | /api/auth/google/callback | Callback Google OAuth | 5/min | Non |

#### Administration RBAC

| Methode | Endpoint | Description | Auth |
|---|---|---|---|
| GET | /api/admin/roles | Lister les roles | admin |
| POST | /api/admin/roles | Creer un role | admin |
| GET | /api/admin/permissions | Lister les permissions | admin |
| POST | /api/admin/permissions | Creer une permission | admin |
| POST | /api/admin/users/<id>/roles | Assigner un role a un utilisateur | admin |
| DELETE | /api/admin/users/<id>/roles | Retirer un role a un utilisateur | admin |
| GET | /api/admin/users/<id>/roles | Voir les roles d'un utilisateur | admin |
| POST | /api/admin/roles/<name>/permissions | Assigner une permission a un role | admin |

### Securite

**Mots de passe :** haches avec `werkzeug.security.generate_password_hash` qui utilise bcrypt (car `bcrypt` est installe).

**Tokens JWT :**
- Access token : 15 minutes, stocke en memoire ou localStorage
- Refresh token : 7 jours, utilise pour obtenir un nouvel access token
- Claims inclus : `email`, `is_verified`

**Rate limiting :**
- Login : 5 tentatives par minute par IP
- Register : 3 tentatives par minute par IP
- Forgot/reset password : 3 tentatives par minute par IP
- Google callback : 5 tentatives par minute par IP
- Reponse 429 avec message explicatif

**Tokens de verification :**
- Email verification : `itsdangerous.URLSafeTimedSerializer`, expire apres 24h
- Password reset : `itsdangerous.URLSafeTimedSerializer`, expire apres 1h
- Stockes dans l'URL, envoyes par email

**Google OAuth :**
- Desactive si `GOOGLE_CLIENT_ID` et `GOOGLE_CLIENT_SECRET` ne sont pas configures
- Retourne 501 si non configure
- L'utilisateur est automatiquement cree si inexistant, avec `is_verified=True`

### RBAC

**Modeles de donnees :**

```
User --M2M--> Role --M2M--> Permission
```

**Decorateurs disponibles :**

```python
from app.services.role_service import role_required, permission_required

# Proteger une route par role
@role_required("admin")
def admin_route():
    pass

# Proteger par permission granulaire
@permission_required("users:delete")
def delete_user():
    pass
```

**Methode sur User :**

```python
user.has_role("admin")         # True/False
user.has_permission("users:read")  # True/False
```

**Extensibilite :** Le modele User est concu pour etre etendu via un profil One-to-One. Creez un modele `Profile` lie a `User` pour ajouter des champs specifiques a votre projet sans modifier le modele auth.

### Configuration

Variables d'environnement dans `backend/.env` :

```env
SECRET_KEY=une-chaine-longue-et-aleatoire
JWT_SECRET_KEY=une-autre-chaine-longue
FRONTEND_URL=http://localhost:5173
GOOGLE_CLIENT_ID=votre-google-client-id
GOOGLE_CLIENT_SECRET=votre-google-client-secret
```

### Exemples d'utilisation

```python
from app.services import auth_service, role_service

# Inscription
user = auth_service.register(email="test@test.com", password="secret123", first_name="John")

# Connexion
result = auth_service.login(email="test@test.com", password="secret123")
# result = { "access_token": "...", "refresh_token": "...", "user": {...} }

# RBAC
role_service.create_role("admin")
role_service.create_permission("posts:delete")
role_service.assign_permission("admin", "posts:delete")
role_service.assign_role(user.id, "admin")

# Verifications
user.has_role("admin")             # True
user.has_permission("posts:delete")  # True
```

---

## Frontend

A implementer dans `features/auth/`. Voir `docs/FRONTEND.md` pour l'architecture generale.

### Structure prevue

```
frontend/src/features/auth/
  components/
    LoginForm.jsx           Formulaire de connexion (props : onSubmit, loading, error)
    RegisterForm.jsx        Formulaire d'inscription (props : onSubmit, loading, error)
    SocialLoginButton.jsx   Bouton Google OAuth
    ProtectedRoute.jsx      Wrapper pour routes protegees (props : role, permission)
  pages/
    LoginPage.jsx
    RegisterPage.jsx
    ForgotPasswordPage.jsx
    ResetPasswordPage.jsx
    VerifyEmailPage.jsx
  hooks/
    useAuth.js              Contexte auth : user, login, logout, hasRole, hasPermission
```

### Hook useAuth

```jsx
import { useAuth } from '../../features/auth/hooks/useAuth'

const { user, login, logout, loading, hasRole, hasPermission } = useAuth()

hasRole('admin')              // True/False
hasPermission('users:delete') // True/False
```

### ProtectedRoute

```jsx
<ProtectedRoute role="admin">
  <DashboardPage />
</ProtectedRoute>

<ProtectedRoute permission="posts:edit">
  <EditPostPage />
</ProtectedRoute>
```

---

## Flux utilisateur types

### Inscription
1. POST /api/auth/register -> email de verification envoye
2. L'utilisateur clique sur le lien dans l'email
3. POST /api/auth/verify-email -> email confirme
4. POST /api/auth/login -> tokens JWT recus

### Connexion
1. POST /api/auth/login -> access_token + refresh_token
2. Access token utilise pour les requetes API (Authorization: Bearer)
3. POST /api/auth/refresh quand le token expire

### Mot de passe oublie
1. POST /api/auth/forgot-password -> email envoye
2. L'utilisateur clique sur le lien
3. POST /api/auth/reset-password -> nouveau mot de passe enregistre

### Google OAuth
1. Redirection vers GET /api/auth/google/login
2. L'utilisateur autorise sur Google
3. Callback recu, tokens JWT retournes
