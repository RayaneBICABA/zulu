import apiClient from './apiClient'

const authService = {
  me: () => apiClient.get('/auth/me'),
  becomeArtisan: () => apiClient.post('/auth/become-artisan'),
}

export default authService
