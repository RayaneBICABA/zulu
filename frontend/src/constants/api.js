const BASE_URL = import.meta.env.VITE_API_URL || 'https://zawani-api.onrender.com/api'

export const API_URL = BASE_URL

export const ENDPOINTS = {
  health:   '/health',
  auth: {
    me:               '/auth/me',
    firebaseLogin:    '/auth/firebase-login',
    becomeArtisan:    '/auth/become-artisan',
  },
  commerces: '/commerces',
  categories: '/categories',
  favoris: '/favoris',
}
