import apiClient from './apiClient'
import { ENDPOINTS } from '../constants/api'

const authService = {
  login: (credentials) =>
    apiClient.post(ENDPOINTS.auth.login, credentials),

  register: (data) =>
    apiClient.post(ENDPOINTS.auth.register, data),

  logout: () => {
    localStorage.removeItem('token')
  },

  me: () =>
    apiClient.get(ENDPOINTS.auth.me),

  saveToken: (token) =>
    localStorage.setItem('token', token),

  getToken: () =>
    localStorage.getItem('token'),

  isAuthenticated: () =>
    !!localStorage.getItem('token'),
}

export default authService
