import { useState, useEffect, useCallback, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { AuthContext } from './AuthContext'
import { auth, onAuthStateChanged, signOut as fbSignOut } from '../../../firebase'
import { API_URL } from '../../../constants/api'

export const AuthProvider = ({ children }) => {
  const navigate = useNavigate()
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [sessionExpired, setSessionExpired] = useState(false)
  const [jwt, setJwt] = useState(null)
  const initialised = useRef(false)
  const syncPromiseRef = useRef(null)
  const deepLinkRef = useRef(false)

  const syncUserWithBackend = useCallback(async (firebaseUser) => {
    if (!firebaseUser) {
      if (!deepLinkRef.current) {
        setUser(null)
        setLoading(false)
      }
      return null
    }

    // Éviter les appels parallèles
    if (syncPromiseRef.current) {
      return syncPromiseRef.current
    }

    syncPromiseRef.current = (async () => {
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
        if (data.access_token) {
          setJwt(data.access_token)
          localStorage.setItem('zawani_jwt', data.access_token)
          if (data.refresh_token) localStorage.setItem('zawani_refresh_token', data.refresh_token)
        }
        return data.user
      } catch (e) {
        console.error('Failed to sync user with backend:', e)
        if (e.message === 'Failed to fetch' || e instanceof TypeError) {
          console.warn('Network error during sync — user may be offline')
        }
        setUser(null)
        return null
      } finally {
        syncPromiseRef.current = null
        setLoading(false)
      }
    })()

    return syncPromiseRef.current
  }, [])

  useEffect(() => {
    if (initialised.current) return
    initialised.current = true

    // Web : traiter le résultat de signInWithRedirect
    if (!window.Capacitor?.isNativePlatform?.()) {
      ;(async () => {
        try {
          const { getRedirectResult } = await import('../../../firebase')
          const result = await getRedirectResult(auth)
          if (result?.user) {
            // syncUserWithBackend va aussi être appelé par onAuthStateChanged
            // (déduplié par syncPromiseRef). Pas besoin de naviguer ici,
            // le useEffect de LoginPage s'en charge.
            await syncUserWithBackend(result.user)
          }
        } catch (e) {
          console.error('getRedirectResult error:', e)
        }
      })()
    }

    // Mobile : écouter les deep links
    if (window.Capacitor?.isNativePlatform?.()) {
      import('@capacitor/app').then(({ App }) => {
        App.addListener('appUrlOpen', async (data) => {
          const url = data.url

          // Reset password (App Links ou custom scheme)
          if (url.includes('/reinitialiser-mot-de-passe')) {
            const params = new URLSearchParams(url.split('?')[1] || '')
            const token = params.get('token')
            if (token) {
              navigate(`/reinitialiser-mot-de-passe?token=${token}`)
            }
            return
          }

          if (!url.startsWith('zawani://auth')) return

          try {
            const { Browser } = await import('@capacitor/browser')
            await Browser.close()
          } catch {
            // Pas de navigation en cours — rien à fermer
          }

          console.log('[DEEPLINK] Received URL:', url.substring(0, 80) + '...')
          const params = new URLSearchParams(url.split('?')[1] || '')
          const idToken = params.get('token')
          if (!idToken || idToken.length < 10) {
            console.log('[DEEPLINK] Token invalide, ignoré')
            return
          }
          console.log('[DEEPLINK] Token extrait, longueur:', idToken.length)

          deepLinkRef.current = true
          try {
            const { signInWithCustomToken } = await import('../../../firebase')
            await signInWithCustomToken(auth, idToken)
            deepLinkRef.current = false
            // onAuthStateChanged va trigger -> syncUserWithBackend(firebaseUser)
            // -> getIdToken() (vrai Firebase ID token) -> POST /auth/firebase-login -> OK
          } catch (err) {
            console.error('[DEEPLINK] signInWithCustomToken echoue:', err)
            deepLinkRef.current = false
            setLoading(false)
          }
        })
      })
    }

    // Écouter les changements d'état Firebase (toujours actif)
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
    try {
      const res = await fetch(`${API_URL}/auth/firebase-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token, first_name, last_name }),
      })
      if (res.ok) {
        const data = await res.json()
        if (data.access_token) {
          setJwt(data.access_token)
          localStorage.setItem('zawani_jwt', data.access_token)
          if (data.refresh_token) localStorage.setItem('zawani_refresh_token', data.refresh_token)
        }
      }
    } catch (e) {
      console.warn('Backend sync after register failed:', e)
    }
    return await syncUserWithBackend(cred.user)
  }, [syncUserWithBackend])

  const logout = useCallback(async () => {
    deepLinkRef.current = false
    await fbSignOut(auth)
    setUser(null)
    setJwt(null)
    setSessionExpired(false)
    localStorage.removeItem('zawani_jwt')
    localStorage.removeItem('zawani_refresh_token')
  }, [])

  const refreshUser = useCallback(async () => {
    const currentUser = auth.currentUser
    if (!currentUser) {
      setUser(null)
      setJwt(null)
      localStorage.removeItem('zawani_jwt')
      localStorage.removeItem('zawani_refresh_token')
      return
    }
    try {
      const token = await currentUser.getIdToken(true)
      const res = await fetch(`${API_URL}/auth/firebase-login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token }),
      })
      if (res.ok) {
        const data = await res.json()
        setUser(data.user)
        if (data.access_token) {
          setJwt(data.access_token)
          localStorage.setItem('zawani_jwt', data.access_token)
          if (data.refresh_token) localStorage.setItem('zawani_refresh_token', data.refresh_token)
        }
      }
    } catch (e) {
      console.error('refreshUser failed:', e)
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
    jwt,
    getFirebaseToken: () => {
      const u = auth.currentUser
      return u ? u.getIdToken() : null
    },
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}