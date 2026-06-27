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

  getOne: (id) =>
    apiClient.get(`${ENDPOINTS.commerces}/${id}`),

  create: (data) =>
    apiClient.post(ENDPOINTS.commerces, data),

  updateLocalisation: (commerceId, data) =>
    apiClient.put(`${ENDPOINTS.commerces}/${commerceId}/localisation`, data),

  uploadPhotos: (commerceId, files) => {
    const formData = new FormData()
    files.forEach((f) => formData.append('photos', f))
    return apiClient.postMultipart(`${ENDPOINTS.commerces}/${commerceId}/photos`, formData)
  },

  publish: (commerceId) =>
    apiClient.patch(`${ENDPOINTS.commerces}/${commerceId}/publish`),

  getRating: (commerceId) =>
    apiClient.get(`${ENDPOINTS.commerces}/${commerceId}/rating`),

  listCategories: () =>
    apiClient.get(ENDPOINTS.categories),

  toggleFavori: (commerceId, isFavorited) =>
    isFavorited
      ? apiClient.delete(`${ENDPOINTS.commerces}/${commerceId}/favoris`)
      : apiClient.post(`${ENDPOINTS.commerces}/${commerceId}/favoris`),

  listFavoris: () =>
    apiClient.get(ENDPOINTS.favoris),

  addComment: (commerceId, contenu) =>
    apiClient.post(`${ENDPOINTS.commerces}/${commerceId}/commentaires`, { contenu }),

  listComments: (commerceId) =>
    apiClient.get(`${ENDPOINTS.commerces}/${commerceId}/commentaires`),

  deleteComment: (commerceId, commentId) =>
    apiClient.delete(`${ENDPOINTS.commerces}/${commerceId}/commentaires/${commentId}`),

  shareWhatsApp: (commerceId) =>
    apiClient.get(`${ENDPOINTS.commerces}/${commerceId}/geolocalisation`),

  recordView: (commerceId) =>
    apiClient.post(`${ENDPOINTS.commerces}/${commerceId}/vues`, {}),

  artisanHome: () =>
    apiClient.get('/artisan/home'),

  artisanProfile: () =>
    apiClient.get('/artisan/profile'),

  switchCommerce: (commerceId) =>
    apiClient.patch('/artisan/active-commerce', { commerce_id: commerceId }),

  artisanCards: () =>
    apiClient.get('/artisan/commerces/cards'),
}

export default commerceService
