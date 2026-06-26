const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api'

export const API_URL = BASE_URL

export const ENDPOINTS = {
  health:   '/health',
  auth: {
    login:            '/auth/login',
    register:         '/auth/register',
    refresh:          '/auth/refresh',
    logout:           '/auth/logout',
    me:               '/auth/me',
    verifyEmail:      '/auth/verify-email',
    resendVerification:'/auth/resend-verification',
    forgotPassword:   '/auth/forgot-password',
    resetPassword:    '/auth/reset-password',
    googleLogin:      '/auth/google/login',
    googleCallback:   '/auth/google/callback',
  },
  // Endpoints annuaire — prêts pour quand le backend exposera les routes Business.
  categories: {
    list: '/categories',
  },
  business: {
    list:    '/businesses',
    create:  '/businesses',
    mine:    '/businesses/mine',
    detail:  (id) => `/businesses/${id}`,
    publish: (id) => `/businesses/${id}/publish`,
  },
}
