import apiClient from '../../../services/apiClient'
import { ENDPOINTS } from '../../../constants/api'
import { CATEGORIES } from '../constants'

// Le backend a livré les modèles (Business / BusinessHour / BusinessPhoto)
// mais pas encore les routes HTTP. On simule en attendant.
// POUR BRANCHER LE BACKEND (supprimer le mock) : mettre VITE_USE_MOCK=false
// dans frontend/.env — aucun autre changement de code nécessaire.
const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'

export const fetchCategories = async () => {
  if (USE_MOCK) return CATEGORIES
  return apiClient.get(ENDPOINTS.categories.list)
}

export const createBusiness = async (payload) => {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 900))
    return { id: Math.floor(Math.random() * 1000), status: 'pending', ...payload }
  }
  return apiClient.post(ENDPOINTS.business.create, payload)
}
