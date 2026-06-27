import apiClient from './apiClient'
import { ENDPOINTS } from '../constants/api'

const TOKEN_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'

const authService = {
  // Backend renvoie { success, data: { user, token } } — un seul token.
  login: (credentials) =>
    apiClient.post(ENDPOINTS.auth.login, credentials)
      .then((res) => {
        const payload = res?.data || res
        if (payload?.token) localStorage.setItem(TOKEN_KEY, payload.token)
        return payload
      }),

  register: (data) =>
    apiClient.post(ENDPOINTS.auth.register, data),

  refresh: () => {
    const refresh = localStorage.getItem(REFRESH_KEY)
    if (!refresh) return Promise.reject(new Error('No refresh token'))
    return apiClient.post(ENDPOINTS.auth.refresh, { refresh_token: refresh })
      .then((data) => {
        authService.saveTokens(data.access_token, data.refresh_token)
        return data
      })
  },

  logout: () => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(REFRESH_KEY)
  },

  // Backend renvoie { success, data: { ...user } } → on renvoie l'objet user.
  me: () =>
    apiClient.get(ENDPOINTS.auth.me).then((res) => res?.data || res),

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
