import { API_URL } from '../constants/api'

const TOKEN_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'
let isRefreshing = false
let refreshQueue = []

const getAuthHeader = () => {
  const token = localStorage.getItem(TOKEN_KEY)
  return token ? { Authorization: `Bearer ${token}` } : {}
}

const handleResponse = async (res) => {
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    const message = data?.message || `Erreur ${res.status}`
    const error = new Error(message)
    error.status = res.status
    throw error
  }
  return data
}

const refreshToken = async () => {
  const refresh = localStorage.getItem(REFRESH_KEY)
  if (!refresh) throw new Error('No refresh token')
  const res = await fetch(`${API_URL}/auth/refresh`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${refresh}`,
    },
  })
  if (!res.ok) throw new Error('Refresh failed')
  const data = await res.json()
  localStorage.setItem(TOKEN_KEY, data.access_token)
  if (data.refresh_token) localStorage.setItem(REFRESH_KEY, data.refresh_token)
  return data.access_token
}

const authFetch = async (endpoint, options = {}) => {
  const url = `${API_URL}${endpoint}`
  const res = await fetch(url, options)
  if (res.status !== 401) return handleResponse(res)

  const originalRequest = () =>
    fetch(url, { ...options, headers: { ...options.headers, ...getAuthHeader() } })
      .then(handleResponse)

  if (isRefreshing) {
    return new Promise((resolve, reject) => {
      refreshQueue.push({ resolve, reject })
    }).then(() => originalRequest())
  }

  isRefreshing = true
  try {
    await refreshToken()
    isRefreshing = false
    refreshQueue.forEach((q) => q.resolve())
    refreshQueue = []
    return originalRequest()
  } catch (err) {
    isRefreshing = false
    refreshQueue.forEach((q) => q.reject(err))
    refreshQueue = []
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
    window.dispatchEvent(new CustomEvent('auth:logout'))
    const sessionError = new Error('Session expirée, veuillez vous reconnecter', { cause: err })
    throw sessionError
  }
}

const apiClient = {
  get: (endpoint) =>
    authFetch(endpoint, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    }),

  post: (endpoint, body) =>
    authFetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
      body: JSON.stringify(body),
    }),

  postMultipart: (endpoint, formData) =>
    authFetch(endpoint, {
      method: 'POST',
      headers: { ...getAuthHeader() },
      body: formData,
    }),

  put: (endpoint, body) =>
    authFetch(endpoint, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
      body: JSON.stringify(body),
    }),

  patch: (endpoint, body) =>
    authFetch(endpoint, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
      body: body ? JSON.stringify(body) : undefined,
    }),

  delete: (endpoint) =>
    authFetch(endpoint, {
      method: 'DELETE',
      headers: { 'Content-Type': 'application/json', ...getAuthHeader() },
    }),
}

export default apiClient
