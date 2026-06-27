import apiClient from './apiClient'
import { ENDPOINTS } from '../constants/api'

const TOKEN_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'

const authService = {
  login: (credentials) =>
    apiClient.post(ENDPOINTS.auth.login, credentials)
      .then((data) => {
        if (data.access_token) authService.saveTokens(data.access_token, data.refresh_token)
        return data
      }),

  register: (data) =>
    apiClient.post(ENDPOINTS.auth.register, data),

  logout: () => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
  },

  me: () =>
    apiClient.get(ENDPOINTS.auth.me),

  verifyEmail: (token) =>
    apiClient.post(ENDPOINTS.auth.verifyEmail, { token }),

  resendVerification: () =>
    apiClient.post(ENDPOINTS.auth.resendVerification),

  forgotPassword: (email) =>
    apiClient.post(ENDPOINTS.auth.forgotPassword, { email }),

  resetPassword: (token, password) =>
    apiClient.post(ENDPOINTS.auth.resetPassword, { token, password }),

  saveTokens: (access, refresh) => {
    localStorage.setItem(TOKEN_KEY, access)
    if (refresh) localStorage.setItem(REFRESH_KEY, refresh)
  },

  getToken: () =>
    localStorage.getItem(TOKEN_KEY),

  getRefreshToken: () =>
    localStorage.getItem(REFRESH_KEY),

  isAuthenticated: () =>
    !!localStorage.getItem(TOKEN_KEY),
}

export default authService
