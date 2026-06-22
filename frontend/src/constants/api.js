const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

export const API_URL = BASE_URL

export const ENDPOINTS = {
  health:   '/health',
  auth: {
    login:    '/auth/login',
    register: '/auth/register',
    logout:   '/auth/logout',
    me:       '/auth/me',
  },
}
