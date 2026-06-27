const BASE_URL = import.meta.env.VITE_API_URL || 'https://zawani-api.onrender.com/api'

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
    becomeArtisan:    '/auth/become-artisan',
  },
  commerces: '/commerces',
  categories: '/categories',
  favoris: '/favoris',
}
