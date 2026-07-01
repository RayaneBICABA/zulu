const BASE_URL = import.meta.env.VITE_API_URL || 'https://zawani-api.onrender.com/api'

export const API_URL = BASE_URL

export const ENDPOINTS = {
  commerces: '/commerces',
  categories: '/categories',
  favoris: '/favoris',
}
