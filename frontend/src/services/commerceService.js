import apiClient from './apiClient'
import { ENDPOINTS } from '../constants/api'

const commerceService = {
  listPublic: (params = {}) => {
    const query = new URLSearchParams()
    if (params.q) query.set('q', params.q)
    if (params.categorie_id) query.set('categorie_id', params.categorie_id)
    if (params.page) query.set('page', params.page)
    if (params.per_page) query.set('per_page', params.per_page)
    const qs = query.toString()
    return apiClient.get(`${ENDPOINTS.commerces}${qs ? `?${qs}` : ''}`)
  },

  listCategories: () =>
    apiClient.get(ENDPOINTS.categories),

  toggleFavori: (commerceId, isFavorited) =>
    isFavorited
      ? apiClient.delete(`${ENDPOINTS.commerces}/${commerceId}/favoris`)
      : apiClient.post(`${ENDPOINTS.commerces}/${commerceId}/favoris`),

  listFavoris: () =>
    apiClient.get(ENDPOINTS.favoris),
}

export default commerceService
