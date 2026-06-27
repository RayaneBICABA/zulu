import apiClient from '../../../services/apiClient'
import { API_URL, ENDPOINTS } from '../../../constants/api'
import { CATEGORIES } from '../constants'

// Bascule mock → réel : VITE_USE_MOCK=false dans frontend/.env pour parler au vrai backend.
const USE_MOCK = import.meta.env.VITE_USE_MOCK !== 'false'
const TOKEN_KEY = 'access_token'

export const fetchCategories = async () => {
  const mock = CATEGORIES.map((c) => ({ id: c.id, nom: c.name }))
  if (USE_MOCK) return mock
  try {
    return await apiClient.get(ENDPOINTS.categories.list)
  } catch {
    // Backend pas encore prêt sur cette route → on garde le stepper utilisable.
    return mock
  }
}

// Step 1 — crée le brouillon de commerce, renvoie { id, ... }
const createCommerce = (step1) => apiClient.post(ENDPOINTS.commerce.create, step1)

// Step 2 — localisation + 7 horaires
const updateLocalisation = (id, step2) => apiClient.put(ENDPOINTS.commerce.localisation(id), step2)

// Step 3 — upload multipart vers Cloudinary (apiClient est JSON-only, donc fetch dédié ici)
const uploadPhotos = async (id, files) => {
  const form = new FormData()
  files.forEach((file) => form.append('photos', file))
  const res = await fetch(`${API_URL}${ENDPOINTS.commerce.photos(id)}`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${localStorage.getItem(TOKEN_KEY)}` },
    body: form,
  })
  if (!res.ok) {
    const data = await res.json().catch(() => ({}))
    throw new Error(data.message || `Erreur upload photos (${res.status})`)
  }
  return res.json()
}

// Étape finale — publie le commerce (is_active = true)
const publishCommerce = (id) => apiClient.patch(ENDPOINTS.commerce.publish(id), {})

// Orchestrateur : enchaîne les 4 appels du stepper dans l'ordre.
export const submitCommerce = async ({ step1, step2, photos }) => {
  if (USE_MOCK) {
    await new Promise((resolve) => setTimeout(resolve, 900))
    return { id: Math.floor(Math.random() * 1000), is_active: true, ...step1 }
  }
  const commerce = await createCommerce(step1)
  await updateLocalisation(commerce.id, step2)
  if (photos.length) await uploadPhotos(commerce.id, photos.map((p) => p.file))
  return publishCommerce(commerce.id)
}
