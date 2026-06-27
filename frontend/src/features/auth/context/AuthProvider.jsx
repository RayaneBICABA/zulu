import { useState, useEffect, useCallback, useRef } from 'react'
import { AuthContext } from './AuthContext'
import authService from '../../../services/authService'

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [sessionExpired, setSessionExpired] = useState(false)
  const initialised = useRef(false)

  const refreshUser = useCallback(async () => {
    if (!authService.isAuthenticated()) {
      setUser(null)
      setLoading(false)
      return
    }
    try {
      const data = await authService.me()
      setUser(data.user || data)
    } catch {
      authService.logout()
      setUser(null)
      setSessionExpired(true)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (!initialised.current) {
      initialised.current = true
      refreshUser()
    }
  }, [refreshUser])

  useEffect(() => {
    const handleForceLogout = () => {
      setUser(null)
      setSessionExpired(true)
    }
    window.addEventListener('auth:logout', handleForceLogout)
    return () => window.removeEventListener('auth:logout', handleForceLogout)
  }, [])

  const login = useCallback(async (credentials) => {
    setError(null)
    setSessionExpired(false)
    const data = await authService.login(credentials)
    const userData = data.user || data
    setUser(userData)
    return userData
  }, [])

  const register = useCallback(async (data) => {
    setError(null)
    setSessionExpired(false)
    return authService.register(data)
  }, [])

  const logout = useCallback(() => {
    authService.logout()
    setUser(null)
    setError(null)
    setSessionExpired(false)
  }, [])

  const clearSessionExpired = useCallback(() => {
    setSessionExpired(false)
  }, [])

  const hasRole = useCallback((role) => {
    if (!user || !user.roles) return false
    return user.roles.some((r) => r.name === role || r === role)
  }, [user])

  const hasPermission = useCallback((permission) => {
    if (!user || !user.roles) return false
    return user.roles.some((role) => {
      if (role.permissions) return role.permissions.some((p) => p.codename === permission || p === permission)
      return false
    })
  }, [user])

  const value = {
    user,
    loading,
    error,
    sessionExpired,
    clearSessionExpired,
    login,
    register,
    logout,
    refreshUser,
    hasRole,
    hasPermission,
    isAuthenticated: !!user,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}
