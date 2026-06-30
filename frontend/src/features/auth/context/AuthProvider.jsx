import { useState, useEffect, useCallback, useRef } from 'react'
import { AuthContext } from './AuthContext'
import { auth, onAuthStateChanged, signOut as fbSignOut } from '../../../firebase'
import apiClient from '../../../services/apiClient'
import { API_URL } from '../../../constants/api'

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [sessionExpired, setSessionExpired] = useState(false)
  const initialised = useRef(false)

  const syncUserWithBackend = useCallback(async (firebaseUser) => {
    if (!firebaseUser) {
      setUser(null)
      setLoading(false)
      return null
    }

    try {
      const token = await firebaseUser.getIdToken()
      const res = await fetch(`${API_URL}/auth/firebase-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token }),
      })
      if (!res.ok) {
        const err = await res.json()
        throw new Error(err.error || 'Sync failed')
      }
      const data = await res.json()
      setUser(data.user)
      return data.user
    } catch (e) {
      console.error('Failed to sync user with backend:', e)
      setUser(null)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (initialised.current) return
    initialised.current = true

    ;(async () => {
      try {
        const { getRedirectResult } = await import('../../../firebase')
        const result = await getRedirectResult(auth)
        if (result?.user) {
          await syncUserWithBackend(result.user)
        }
      } catch { }
    })()

    if (window.Capacitor?.isNativePlatform?.()) {
      import('@capacitor/app').then(({ App }) => {
        App.addListener('appUrlOpen', async (data) => {
          if (!data.url.startsWith('zawani://auth')) return
          const params = new URLSearchParams(data.url.split('?')[1] || '')
          const idToken = params.get('token')
          if (!idToken) return
          try {
            const { signInWithCredential, GoogleAuthProvider } = await import('../../../firebase')
            const credential = GoogleAuthProvider.credential(idToken)
            await signInWithCredential(auth, credential)
          } catch { }
        })
      })
    }

    const unsubscribe = onAuthStateChanged(auth, (firebaseUser) => {
      syncUserWithBackend(firebaseUser)
    })

    return () => unsubscribe()
  }, [syncUserWithBackend])

  const login = useCallback(async ({ email, password }) => {
    const { signInWithEmailAndPassword } = await import('../../../firebase')
    const cred = await signInWithEmailAndPassword(auth, email, password)
    return await syncUserWithBackend(cred.user)
  }, [syncUserWithBackend])

  const register = useCallback(async ({ email, password, first_name, last_name }) => {
    const { createUserWithEmailAndPassword } = await import('../../../firebase')
    const cred = await createUserWithEmailAndPassword(auth, email, password)
    const token = await cred.user.getIdToken()
    await fetch(`${API_URL}/auth/firebase-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, first_name, last_name }),
    })
    return await syncUserWithBackend(cred.user)
  }, [syncUserWithBackend])

  const logout = useCallback(async () => {
    await fbSignOut(auth)
    setUser(null)
    setSessionExpired(false)
  }, [])

  const refreshUser = useCallback(async () => {
    const currentUser = auth.currentUser
    if (!currentUser) {
      setUser(null)
      return
    }
    const token = await currentUser.getIdToken(true)
    const res = await fetch(`${API_URL}/auth/firebase-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token }),
    })
    if (res.ok) {
      const data = await res.json()
      setUser(data.user)
    }
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
    setUser,
    loading,
    sessionExpired,
    setSessionExpired,
    clearSessionExpired: () => setSessionExpired(false),
    login,
    register,
    logout,
    refreshUser,
    hasRole,
    hasPermission,
    isAuthenticated: !!user,
    getFirebaseToken: () => {
      const u = auth.currentUser
      return u ? u.getIdToken() : null
    },
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}