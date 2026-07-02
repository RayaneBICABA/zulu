# ZAWANI — Architecture Technique & Documentation

> Annuaire Intelligent pour Commerces Locaux
> Concu et developpe par la team ZULU

---

## Table des matieres

1.  [Vue d'ensemble](#1-vue-densemble)
2.  [Stack technologique](#2-stack-technologique)
3.  [Architecture du systeme d'authentification](#3-architecture-du-systeme-dauthentification)
    - 3.1 [Authentification manuelle (email/mot de passe)](#31-authentification-manuelle-emailmot-de-passe)
    - 3.2 [Authentification Google via Firebase](#32-authentification-google-via-firebase)
    - 3.3 [Schema de flux JWT](#33-schema-de-flux-jwt)
    - 3.4 [Rate limiting et securite](#34-rate-limiting-et-securite)
4.  [Geolocalisation et tri par distance](#4-geolocalisation-et-tri-par-distance)
    - 4.1 [Acquisition automatique de la position](#41-acquisition-automatique-de-la-position)
    - 4.2 [Algorithme de distance — Haversine](#42-algorithme-de-distance--haversine)
5.  [Systeme de notation intelligent (IA)](#5-systeme-de-notation-intelligent-ia)
    - 5.1 [Pipeline d'analyse de sentiment](#51-pipeline-danalyse-de-sentiment)
    - 5.2 [Fallback par keywords](#52-fallback-par-keywords)
    - 5.3 [Mise a l'echelle et tolerance de panne](#53-mise-a-lechelle-et-tolerance-de-panne)
6.  [Orchestration telephonique et partage](#6-orchestration-telephonique-et-partage)
    - 6.1 [Appel telephonique direct (TEL)](#61-appel-telephonique-direct-tel)
    - 6.2 [Redirection WhatsApp](#62-redirection-whatsapp)
    - 6.3 [Partage de geolocalisation WhatsApp vers Google Maps](#63-partage-de-geolocalisation-whatsapp-vers-google-maps)
7.  [Architecture du projet](#7-architecture-du-projet)
    - 7.1 [Backend — Flask (Clean Architecture)](#71-backend--flask-clean-architecture)
    - 7.2 [Frontend — React + Capacitor](#72-frontend--react--capacitor)
8.  [Capacitor et le deploiement mobile](#8-capacitor-et-le-deploiement-mobile)
    - 8.1 [Role de Capacitor](#81-role-de-capacitor)
    - 8.2 [Android vs iOS](#82-android-vs-ios)
9.  [Glossaire technique](#9-glossaire-technique)

---

## 1. Vue d'ensemble

ZAWANI est une application mobile cross-platform native (React + Capacitor) de mise en relation entre clients et commerces de proximite. Elle repose sur une architecture full-stack avec un backend REST en Flask (Python) et un frontend en React 19, empaquete pour Android via Capacitor.

Points clefs de l'architecture :

- Modele utilisateur unifie : tout utilisateur peut consulter, commenter, favoriser et creer des commerces sans distinction de role
- Authentification decentralisee via Firebase Auth avec double pont JWT
- Geolocalisation avec tri spatial base sur la formule de Haversine
- Analyse semantique automatique des commentaires via Google Gemini AI avec fallback lexical
- Infrastructure conteneurisee (Docker) deployee sur Render et Vercel

---

## 2. Stack technologique

### Backend (API REST)

| Technologie | Version | Role |
|---|---|---|
| Python | 3.11 | Langage d'implementation |
| Flask | 3.1 | Framework HTTP REST |
| SQLAlchemy | 2.0 | ORM relationnel |
| Flask-Migrate / Alembic | — | Gestion des schemas de base de donnees |
| PostgreSQL | 15 | Base de donnees relationnelle |
| Flask-JWT-Extended | — | Emission et validation de tokens JWT |
| Marshmallow | 3.x | Serialisation et validation de donnees |
| Flasgger | — | Documentation interactive via Swagger UI |
| Google Generative AI | — | Analyse semantique des avis |
| Gunicorn | — | Serveur WSGI de production |

### Frontend (SPA)

| Technologie | Version | Role |
|---|---|---|
| React | 19 | Bibliotheque de construction d'interfaces |
| Vite | 8 | Bundler et serveur de developpement |
| React Router DOM | 7 | Routage cote client (SPA) |
| Tailwind CSS | 4 | Framework CSS utilitaire |
| Framer Motion | 12 | Moteur d'animations declaratives |
| Lucide React | — | Bibliotheque d'icones vectorielles |
| Firebase JS SDK | — | Authentification (Google, email) |
| Capacitor | 7 | Pont natif vers Android |

### Infrastructure

| Outil | Role |
|---|---|
| Docker + Docker Compose | Conteneurisation backend et base de donnees |
| Render | Hebergement backend (auto-deploiement depuis GitHub) |
| Vercel | Hebergement frontend (Web) |
| Firebase Auth | Fournisseur d'identite OAuth 2.0 + email/mot de passe |

---

## 3. Architecture du systeme d'authentification

### 3.1 Authentification manuelle (email/mot de passe)

L'utilisateur cree un compte via Firebase Auth avec email et mot de passe. Le flux est le suivant :

1.  L'utilisateur soumet email + mot de passe depuis l'interface React
2.  Firebase Auth cree l'utilisateur et retourne un `idToken` (JWT court terme, 1 heure)
3.  Le frontend transmet ce `idToken` au backend via `POST /auth/firebase-login`
4.  Le backend :
    - Verifie le token aupres de Firebase Admin SDK
    - Cree ou met a jour l'utilisateur dans PostgreSQL (upsert)
    - Emet un `access_token` JWT Flask (duree configurable, 15-30 minutes)
    - Emet un `refresh_token` JWT Flask (duree longue, 7 jours)
5.  Le frontend stocke les deux tokens dans `localStorage`
6.  Chaque requete API inclut le `access_token` dans l'en-tete `Authorization: Bearer <token>`
7.  En cas de `401 Unauthorized`, le `apiClient` declenche automatiquement un rafraichissement via `POST /auth/refresh` avec le `refresh_token`

### 3.2 Authentification Google via Firebase

1.  L'utilisateur clique sur "Continuer avec Google"
2.  Firebase Auth lance le flux OAuth 2.0 natif :
    - Sur mobile : Google Smart Lock / Chrome Custom Tab
    - Sur Web : Popup ou redirection
3.  Firebase retourne un `idToken` Google signe
4.  Le meme pipeline que l'auth manuelle est emprunte : `POST /auth/firebase-login`
5.  Le backend ne fait pas de distinction entre les modes d'auth — seul le `firebase_uid` compte

### 3.3 Schema de flux JWT

```
 FRONTEND (React)                     BACKEND (Flask)                 FIREBASE
       |                                    |                          |
       |-- 1. Email/Password ou Google -->  |                          |
       |                                    |-- 2. Verify idToken ---> |
       |                                    |<-- 3. User data -------- |
       |                                    |                          |
       |                                    |-- 4. Upsert PostgreSQL   |
       |                                    |-- 5. Generate JWT pair   |
       |<-- 6. access_token + refresh_token |                          |
       |                                    |                          |
       |-- 7. API call (Bearer token) ----> |                          |
       |                                    |-- 8. Validate JWT        |
       |<-- 9. Response ------------------- |                          |
       |                                    |                          |
       |-- 10. 401 Expired token ---------> |                          |
       |-- 11. POST /auth/refresh --------->|                          |
       |<-- 12. New access_token ---------- |                          |
```

### 3.4 Rate limiting et securite

Le rate limiting est implemente au niveau middleware Flask :

- **Tentatives de connexion** : 5 requetes par minute par adresse IP sur `/auth/firebase-login`
- **Inscription** : 3 requetes par minute par adresse IP
- **API general** : 60 requetes par minute par utilisateur authentifie

Les mesures de securite supplementaires incluent :

- Validation systematique des tokens Firebase via `firebase_admin.auth.verify_id_token`
- Rotation des refresh tokens : chaque utilisation d'un refresh token invalide le precedent
- Blacklist cote backend des refresh tokens revoques (stockee en memoire, extensible vers Redis)
- Protection CORS avec liste blanche d'origines autorisees
- Headers de securite HTTP (Content-Security-Policy, X-Frame-Options, Strict-Transport-Security)

---

## 4. Geolocalisation et tri par distance

### 4.1 Acquisition automatique de la position

Le systeme de geolocalisation repose sur le hook React `useUserLocation`, implemente sans plugin natif externe :

1.  **Detection de la position** : appel a l'API W3C `navigator.geolocation.getCurrentPosition()` avec les options suivantes :
    - `enableHighAccuracy: true` — active le GPS materiel si disponible
    - `timeout: 10000` — abandon apres 10 secondes
    - Cache de 30 secondes maximum (valeur implicite du navigateur)
2.  **Reverse geocoding** : les coordonnees sont envoyees a l'API Nominatim (OpenStreetMap) pour obtenir :
    - La ville (`city`, `town` ou `village`)
    - Le quartier (`suburb` ou `neighbourhood`)
    - L'adresse complete formatee
3.  **Mise en cache** : la position est persistee dans `localStorage` sous la cle `zawani_location` pour :
    - Eviter de solliciter le GPS a chaque ouverture de l'application
    - Fournir une position instantanee pendant le chargement (< 200ms vs 1-8s pour le GPS)
    - Permettre un affichage immediat de la ville dans l'en-tete

La position est mise a jour dans les cas suivants :
- Premiere ouverture de l'application apres installation
- L'utilisateur rafraichit la page
- La donnee en cache a expire (> 24 heures, non stocke actuellement)

Format du cache `localStorage` :

```json
{
  "latitude": 48.8566,
  "longitude": 2.3522,
  "adresse": "Paris, Ile-de-France, France",
  "ville": "Paris",
  "quartier": "Saint-Germain-des-Pres"
}
```

### 4.2 Algorithme de distance — Haversine

Le tri des commerces par distance est implemente cote backend dans `CommerceService.list_public_commerces()`.

#### Principe mathematique

La formule de Haversine calcule la distance orthodromique (grand cercle) entre deux points sur une sphere :

```
a = sin(Delta_lat / 2)^2
    + cos(lat1) * cos(lat2) * sin(Delta_lon / 2)^2

c = 2 * atan2(sqrt(a), sqrt(1 - a))

distance = R * c

ou R = 6371 km (rayon terrestre moyen)
```

#### Implementation

```python
import math

dlat = math.radians(float(c.latitude) - lat)
dlon = math.radians(float(c.longitude) - lng)
a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat)) * \
    math.cos(math.radians(float(c.latitude))) * math.sin(dlon / 2) ** 2
distance = 6371 * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
```

#### Pipeline de tri

1.  Le frontend envoie `lat` et `lng` en parametres de requete a `GET /api/commerces`
2.  Le backend filtre les commerces actifs (`is_active = True`)
3.  Pour chaque commerce possedant des coordonnees, la distance est calculee via Haversine
4.  Les commerces sont tries par distance croissante (les plus proches en premier)
5.  Les commerces sans coordonnees sont rejetes en fin de liste (distance = `inf`)
6.  La pagination est appliquee apres le tri (contrairement a une approche SQL LIMIT/OFFSET classique)
7.  Chaque commerce retourne un champ `distance_km` arrondi a 2 decimales

#### Performance et limites

- Complexite : O(n) en calcul, O(n log n) en tri — lineaire par rapport au nombre de commerces
- Le calcul est effectue en memoire (Python) et non dans la base de donnees, ce qui limite le passage a l'echelle au-dela de ~10 000 commerces
- Alternative pour montee en charge : extension PostGIS avec index spatial GiST et requete `<->` (distance operator)

---

## 5. Systeme de notation intelligent (IA)

### 5.1 Pipeline d'analyse de sentiment

Le systeme analyse automatiquement le contenu textuel des commentaires pour attribuer une note de 1 a 5 etoiles a chaque commerce.

#### Flux de traitement

1.  **Declencheur** : a chaque creation ou suppression d'un commentaire (`Commentaire`), la fonction `analyze_and_update_rating(commerce_id)` est appelee
2.  **Collecte** : tous les commentaires visibles du commerce sont aggregates
3.  **Analyse primaire (Gemini AI)** : les commentaires sont envoyes a Google Gemini (`generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash`) avec un prompt structure
4.  **Analyse secondaire (fallback)** : si l'API Gemini est indisponible (pas de cle, quota epuise, timeout), le systeme bascule sur une analyse lexicale locale
5.  **Mise a jour** : les champs `average_rating` et `rating_count` de la table `CommerceStats` sont mis a jour
6.  **Cache** : la fonction est egalement declenchee lors de la lecture (`GET /rating`) si le compteur cache ne correspond pas au nombre reel de commentaires

### 5.2 Fallback par keywords

L'analyse lexicale locale utilise deux listes de mots ponderes en francais :

#### Mots positifs (poids +1)

agreable, aimable, bien, bon, bravo, competant, cool, efficace, excellent, exceptionnel, extra, fidele, formidable, genial, honnete, incroyable, magnifique, merit, parfait, professionnel, propre, rapide, recommande, remarquable, serieux, service, super, top, tres bien, incroyable

#### Mots negatifs (poids -1)

abime, arnaque, cher, degueulasse, deçu, deception, dommage, eviter, horrible, impoli, incompetant, insatisfait, lent, long, mauvaise, moche, nul, pire, pourri, problème, retard, sale, terrible, trompe

#### Algorithme de scoring

```
score = (sum(poids_mots_positifs) + sum(poids_mots_negatifs)) / len(commentaires)
note  = abs(int(round(score))) si score > 0, sinon 1
note  = max(1, min(5, note))
```

Chaque commentaire est converti en minuscules, les mots sont extraits et compares aux listes. Le score final est une moyenne sur l'ensemble des commentaires, arrondie et bornee entre 1 et 5.

### 5.3 Mise a l'echelle et tolerance de panne

- L'analyse Gemini est optionnelle : l'application fonctionne integralement sans cle API configuree
- En cas d'echec de l'appel Gemini (timeout, quota, erreur reseau), l'exception est capturee, loggee en `warning`, et le fallback lexical prend le relais
- Si les deux methodes echouent, la note precedente est conservee (aucune remise a zero intempestive)
- La fonction est importee de maniere differee (`lazy import`) dans le service pour eviter les dependances circulaires

---

## 6. Orchestration telephonique et partage

### 6.1 Appel telephonique direct (TEL)

Le bouton d'appel utilise le protocole `tel:` standard :

```javascript
window.open(`tel:${phone}`, '_blank')
```

- Le navigateur mobile intercepte le protocole `tel:` et lance l'application telephone native
- Le numero affiche est celui du champ `whatsapp_numero` ou `contact_telephonique` du commerce
- Aucune permission speciale n'est requise au-dela de l'autorisation de telephone

### 6.2 Redirection WhatsApp

Le partage WhatsApp s'effectue via le protocole `https://wa.me/` :

```javascript
const numero = commerce.whatsapp_numero.replace(/[^0-9]/g, '')
window.open(`https://wa.me/${numero}`, '_blank')
```

- Le numero est nettoye de tout caractere non numerique avant d'etre insere dans l'URL
- Le protocole `wa.me` est reconnu nativement par WhatsApp sur Android et iOS
- Aucune API native ou plugin Capacitor n'est requis pour cette fonctionnalite

### 6.3 Partage de geolocalisation WhatsApp vers Google Maps

Le partage de localisation construit une URL Google Maps et la transmet via WhatsApp :

1.  Le backend genere une URL de geolocalisation : `https://www.google.com/maps?q=<lat>,<lng>`
2.  Le frontend ouvre cette URL via `window.open` avec le numero WhatsApp pre-rempli
3.  L'utilisateur peut envoyer le message contenant le lien Google Maps a son contact
4.  Le destinataire clique sur le lien et Google Maps s'ouvre avec l'itineraire vers le commerce

**Construction de l'URL de localisation** :

```
Input  : commerce.latitude = 48.8566, commerce.longitude = 2.3522
Output : https://www.google.com/maps?q=48.8566,2.3522
```

Cette approche ne necessite pas d'API Google Maps Payante — le lien `maps.google.com?q=` est universellement accessible.

---

## 7. Architecture du projet

### 7.1 Backend — Flask (Clean Architecture)

```
backend/
  +-- app/
  |   +-- models/          Couche de donnees (SQLAlchemy)
  |   |   +-- base.py      Classe de base avec timestamps
  |   |   +-- commerce.py  Modele Commerce + CommerceStats
  |   |   +-- commentaire.py
  |   |   +-- categorie.py
  |   |   +-- favori.py
  |   |   +-- photo.py
  |   |   +-- user.py
  |   +-- routes/          Couche de presentation (blueprints Flask)
  |   |   +-- auth.py      Endpoints d'authentification
  |   |   +-- commerce.py  CRUD commerces, favoris, commentaires
  |   |   +-- categories.py
  |   +-- schemas/         Couche de validation (Marshmallow)
  |   +-- services/        Couche metier (logique applicative)
  |   |   +-- auth_service.py
  |   |   +-- commerce_service.py
  |   |   +-- ai_service.py     (analyse de sentiment)
  |   +-- extensions.py    Initialisation des extensions Flask
  |   +-- config.py        Configuration centralisee
```

L'architecture suit les principes de **Clean Architecture** avec separation stricte des couches :

- **Models** : ne contiennent que la definition des donnees et leurs relations ORM
- **Services** : contiennent la logique metier, manipulent les models
- **Routes** : ne contiennent que la gestion des requetes HTTP (validation des entrees, appels aux services, formatage des reponses)
- **Schemas** : validation des entrees/sorties, decouplage entre la couche API et les models internes

### 7.2 Frontend — React + Capacitor

```
frontend/
  +-- src/
  |   +-- components/      Composants UI reutilisables
  |   |   +-- layout/      PageWrapper, BottomNav, Loader
  |   |   +-- ui/          CommerceCard, CommentSection, StarRating
  |   +-- constants/       Configuration (routes API, couleurs)
  |   +-- features/        Modules fonctionnels
  |   |   +-- auth/        Contexte, hooks, pages d'authentification
  |   +-- hooks/           Hooks reutilisables (useUserLocation)
  |   +-- pages/           Ecrans de l'application
  |   +-- services/        Appels API (couche de transport)
  |   +-- firebase.js      Configuration Firebase SDK
  +-- capacitor.config.ts  Configuration Capacitor
```

Structuration par fonctionnalite (`features/`) et par role technique (`components/`, `hooks/`, `services/`).

---

## 8. Capacitor et le deploiement mobile

ZAWANI suit un pipeline de livraison en trois couches distinctes :

```
Code source (React + Vite)
    |
    v
Application web (SPA) -- accessible via navigateur sur Vercel
    |
    v
Progressive Web App (PWA) -- artefact intermediaire avec manifest.json + service worker
    |
    v  Capacitor (bridge)
Application mobile cross-platform native (APK) -- empaquete, signe, distribuable
```

Le livrable final est un **APK Android natif** (cross-platform native app), et non une simple PWA. La PWA n'est qu'un artefact de build intermediaire dans le pipeline.

### 8.1 Role de Capacitor

Capacitor est le pont natif (native bridge) qui transforme le build web de production en une application mobile native. Contrairement a une PWA installee via le navigateur, l'APK produite par Capacitor possede :

- Un cycle de vie Android independant (processus, notifications, gestion memoire)
- Des permissions systemes declarees dans `AndroidManifest.xml`
- Une signature cryptographique pour la distribution sur Google Play
- Un acces aux API systemes via les plugins Capacitor (geolocalisation, stockage, deep links)
- Une integration native avec les services Google (Firebase Auth via Smart Lock / Custom Tabs)

Son role precis :

1.  **WebView native** : il encapsule le build de production (`dist/`) dans une WebView Android, offrant un rendu identique a celui du navigateur
2.  **Plugins natifs** : il fournit des API JavaScript pour acceder aux fonctionnalites du telephone (stockage local, camera, geolocalisation) sans ecrire de code Android natif
3.  **Cycle de vie** : il gere les evenements de cycle de vie de l'application Android (pause, reprise, arret)
4.  **Deep links** : il intercepte les URLs personnalisees (ex: `zawani://auth/callback`) pour la gestion des redirections OAuth
5.  **Configuration** : le fichier `capacitor.config.ts` centralise la configuration du projet (appId, nom, serveur, plugins)

### 8.2 Android vs iOS

| Aspect | Android | iOS |
|---|---|---|
| **Statut** | Entierement fonctionnel | Non deploye |
| **Build** | `./gradlew assembleDebug` | Necessite Xcode + Mac |
| **Distribution** | APK ou Google Play Store | Apple App Store |
| **Geolocalisation** | GPS + WiFi + reseau mobile | Meme stack (navigator.geolocation) |
| **Firebase Auth (Google)** | Smart Lock / Custom Tabs | ASWebAuthenticationSession |
| **Push notifications** | A implementer via Firebase Cloud Messaging | A implementer via APNs |
| **Cout de deploiement** | Compte Google Play unique (25$) | Compte Developpeur Apple (99$/an) |

**Pour deployer sur iOS**, les etapes supplementaires seraient :

1.  `npx cap add ios` pour generer le projet Xcode
2.  Configuration du certificat de signature et du provisioning profile
3.  Compilation via Xcode ou `xcodebuild`
4.  Soumission a l'App Store Connect pour revue

---

## 9. Glossaire technique

| Terme | Definition |
|---|---|
| **JWT (JSON Web Token)** | Token d'authentification auto-contenu compose d'un header, d'un payload et d'une signature. Utilise pour les access et refresh tokens. |
| **Access Token** | JWT de courte duree (15-30 min) transmis dans chaque requete API pour identifier l'utilisateur. |
| **Refresh Token** | JWT de longue duree (7 jours) utilise uniquement pour obtenir un nouvel access token sans reconnexion. |
| **Firebase idToken** | JWT emis par Firebase Auth apres une connexion reussie, contenant l'identite de l'utilisateur. |
| **OAuth 2.0** | Protocole standard d'autorisation deleguee. Utilise par Google pour permettre la connexion sans partage de mot de passe. |
| **Upsert** | Operation de base de donnees qui insere un enregistrement s'il n'existe pas, ou le met a jour s'il existe deja. |
| **Reverse Geocoding** | Conversion de coordonnees geographiques (latitude, longitude) en une adresse textuelle lisible. |
| **Formule de Haversine** | Formule trigonometrique calculant la distance orthodromique entre deux points sur une sphere (Terre). |
| **Orthodromie** | Plus court chemin entre deux points a la surface d'une sphere. |
| **PWA (Progressive Web App)** | Artefact de build intermediaire : application web avec manifest.json et service worker, installable sur ecran d'accueil. Dans le pipeline ZAWANI, la PWA est une etape avant l'empaquetage natif final via Capacitor. |
| **Cross-Platform Native App** | Application mobile compilee pour une plateforme native (Android, iOS) a partir d'une base de code unique (React). Le rendu UI s'effectue dans une WebView mais l'application possede toutes les caracteristiques d'une app native (cycle de vie, permissions, signature, distribution store). |
| **Capacitor Bridge** | Couche de communication entre le code JavaScript et les API natives Android/iOS. Permet d'invoquer la geolocalisation, le stockage, les deep links et autres fonctionnalites systeme depuis React, sans ecrire de code natif. |
| **WebView** | Composant natif permettant d'afficher du contenu web (HTML/CSS/JS) dans une application mobile. |
| **WSGI (Web Server Gateway Interface)** | Protocole standard de communication entre un serveur HTTP (Gunicorn) et une application Python (Flask). |
| **SPA (Single Page Application)** | Application web qui se charge une seule fois et met a jour dynamiquement le contenu sans rechargement de page. |
| **Gemini API** | API de Google permettant d'envoyer des prompts a un modele de langage large (LLM) pour generer des reponses textuelles. |
| **Analyse de sentiment** | Technique de traitement du langage naturel (NLP) visant a determiner la polarite emotionnelle d'un texte (positif, negatif, neutre). |
| **Fallback** | Mecanisme de repli active lorsque le systeme principal echoue, garantissant la continuite de service. |
| **Rate Limiting** | Technique de limitation du nombre de requetes qu'un client peut effectuer dans un intervalle de temps donne. |
| **CORS (Cross-Origin Resource Sharing)** | Mecanisme de securite du navigateur controlant les requetes HTTP entre origines differentes. |
| **Docker Compose** | Outil de definition et d'orchestration de conteneurs multi-services a partir d'un fichier YAML. |
| **Gunicorn** | Serveur WSGI de production pour applications Python, capable de gerer des requetes concurrentes via des workers. |
| **Blueprint (Flask)** | Module de routage permettant d'organiser les endpoints en groupes logiques au sein d'une application Flask. |
| **SQLAlchemy** | ORM (Object-Relational Mapping) Python permettant d'interagir avec la base de donnees via des objets Python. |
| **Alembic** | Outil de gestion de migrations de schema de base de donnees, fonctionnant avec SQLAlchemy. |
| **Marshmallow** | Bibliotheque Python de serialisation/deserialisation et validation de donnees, utilisee pour les schemas de requete et de reponse. |
| **Vite** | Bundler JavaScript nouvelle generation, utilisant le module natif ES (ESM) pour des builds rapides. |
| **Tailwind CSS** | Framework CSS base sur des classes utilitaires, permettant un styling rapide sans ecrire de CSS personnalise. |
| **Framer Motion** | Bibliotheque React d'animations declaratives basee sur les MotionValues et les transitions physiques. |
| **Lucide** | Collection d'icones SVG open-source, alternative a Heroicons et Feather Icons. |

---

> Document generé le 1 juillet 2026
> ZAWANI v1.0 — Team ZULU
