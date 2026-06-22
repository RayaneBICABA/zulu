# Zulu Starter -- Frontend

Base solide pour hackathons et projets full-stack.

**Stack :** React 19 + Vite 8 + Tailwind CSS v4 + Framer Motion + React Router v7

## Prerequisites

- Node.js >= 18

## Installation

```bash
npm install
```

## Scripts

| Commande | Description |
|---|---|
| `npm run dev` | Démarre le serveur de développement local |
| `npm run dev:network` | Démarre le serveur accessible sur le réseau local |
| `npm run build` | Compile l'application pour la production |
| `npm run preview` | Prévisualise le build de production en local |
| `npm run lint` | Vérifie le code avec ESLint |

## Architecture

Voir [ARCHITECTURE.md](../docs/FRONTEND_ARCHITECTURE.md) pour la documentation complète.

## Environnement

Copier `.env.example` vers `.env` et ajuster si nécessaire :

```env
VITE_API_URL=http://localhost:5000/api
```
