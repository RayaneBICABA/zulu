import { API_URL } from '../constants/api'

const REQUEST_TIMEOUT_MS = 90000

const fetchWithTimeout = async (url, options = {}) => {
  const controller = new AbortController()
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS)
  try {
    return await fetch(url, { ...options, signal: controller.signal })
  } catch (err) {
    if (err.name === 'AbortError') {
      throw new Error('Le serveur met trop de temps a repondre. Reessayez dans quelques secondes.')
    }
    if (err.message === 'Failed to fetch' || err instanceof TypeError) {
      throw new Error('Impossible de contacter le serveur. Verifiez votre connexion internet.')
    }
    throw err
  } finally {
    clearTimeout(timeoutId)
  }
}

const getAuthHeader = async () => {
  const jwt = localStorage.getItem('zawani_jwt')
  if (jwt) return { Authorization: `Bearer ${jwt}` }
  try {
    const { auth } = await import('../firebase')
    const user = auth.currentUser
    if (!user) return {}
    const token = await user.getIdToken()
    return { Authorization: `Bearer ${token}` }
  } catch {
    return {}
  }
}

const handleResponse = async (res) => {
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    let message = data?.message || data?.error || `Erreur ${res.status}`
    if (typeof message === 'object') {
      try { message = Object.values(message).flat().join(', ') || JSON.stringify(message) } catch { message = JSON.stringify(message) }
    }
    const error = new Error(message)
    error.status = res.status
    throw error
  }
  return data
}

const tryRefresh = async () => {
  const refreshToken = localStorage.getItem('zawani_refresh_token')
  if (!refreshToken) return null
  try {
    const res = await fetch(`${API_URL}/auth/refresh`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${refreshToken}` },
    })
    if (!res.ok) return null
    const data = await res.json()
    if (data.access_token) {
      localStorage.setItem('zawani_jwt', data.access_token)
      return data.access_token
    }
    return null
  } catch {
    return null
  }
}

let refreshPromise = null

const authFetch = async (endpoint, options = {}) => {
  const url = `${API_URL}${endpoint}`
  const headers = { ...options.headers, ...(await getAuthHeader()) }
  let res = await fetchWithTimeout(url, { ...options, headers })

  if (res.status === 401) {
    const newToken = refreshPromise || tryRefresh()
    refreshPromise = newToken
    const token = await newToken
    refreshPromise = null
    if (token) {
      headers.Authorization = `Bearer ${token}`
      res = await fetchWithTimeout(url, { ...options, headers })
    }
  }

  if (res.status === 401) {
    window.dispatchEvent(new CustomEvent('auth:logout'))
    throw new Error('Session expirée, veuillez vous reconnecter')
  }

  return handleResponse(res)
}

const apiClient = {
  get: (endpoint) =>
    authFetch(endpoint, { method: 'GET', headers: { 'Content-Type': 'application/json' } }),

  post: (endpoint, body) =>
    authFetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }),

  postMultipart: (endpoint, formData) =>
    authFetch(endpoint, { method: 'POST', headers: {}, body: formData }),

  put: (endpoint, body) =>
    authFetch(endpoint, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    }),

  patch: (endpoint, body) =>
    authFetch(endpoint, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: body ? JSON.stringify(body) : undefined,
    }),

  delete: (endpoint) =>
    authFetch(endpoint, { method: 'DELETE', headers: { 'Content-Type': 'application/json' } }),
}

export default apiClient
