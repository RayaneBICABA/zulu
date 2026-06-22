import { API_URL } from '../constants/api'

const getAuthHeader = () => {
  const token = localStorage.getItem('token')
  return token ? { Authorization: `Bearer ${token}` } : {}
}

const handleResponse = async (res) => {
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    const message = data?.message || `Erreur ${res.status}`
    throw new Error(message)
  }
  return data
}

const apiClient = {
  get: (endpoint) =>
    fetch(`${API_URL}${endpoint}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
    }).then(handleResponse),

  post: (endpoint, body) =>
    fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(body),
    }).then(handleResponse),

  put: (endpoint, body) =>
    fetch(`${API_URL}${endpoint}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
      body: JSON.stringify(body),
    }).then(handleResponse),

  delete: (endpoint) =>
    fetch(`${API_URL}${endpoint}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
      },
    }).then(handleResponse),
}

export default apiClient
