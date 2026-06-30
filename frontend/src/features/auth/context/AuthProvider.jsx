import { useState, useEffect, useCallback, useRef } from 'react'
import { AuthContext } from './AuthContext'
import { auth, onAuthStateChanged, signOut as fbSignOut } from '../../../firebase'
import { API_URL } from '../../../constants/api'

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [sessionExpired, setSessionExpired] = useState(false)
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
        return data.user
      } catch (e) {
        console.error('Failed to sync user with backend:', e)
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

    // Mobile : écouter le deep link zawani://auth?token=xxx
    if (window.Capacitor?.isNativePlatform?.()) {
      import('@capacitor/app').then(({ App }) => {
        App.addListener('appUrlOpen', async (data) => {
          if (!data.url.startsWith('zawani://auth')) return

          try {
            const { Browser } = await import('@capacitor/browser')
            await Browser.close()
          } catch {}

          console.log('[DEEPLINK] Received URL:', data.url.substring(0, 80) + '...')
          const params = new URLSearchParams(data.url.split('?')[1] || '')
          const idToken = params.get('token')
          if (!idToken || idToken.length < 10) {
            console.log('[DEEPLINK] Token invalide, ignoré')
            return
          }
          console.log('[DEEPLINK] Token extrait, longueur:', idToken.length)

          deepLinkRef.current = true
          try {
            const res = await fetch(`${API_URL}/auth/firebase-login`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ token: idToken }),
            })
            if (!res.ok) {
              const err = await res.json().catch(() => ({}))
              throw new Error(err.error || `HTTP ${res.status}`)
            }
            const data = await res.json()
            console.log('[DEEPLINK] Sync reussi, user:', data.user?.email)
            setUser(data.user)
          } catch (err) {
            console.error('[DEEPLINK] Sync echoue:', err)
            deepLinkRef.current = false
          } finally {
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
    await fetch(`${API_URL}/auth/firebase-login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ token, first_name, last_name }),
    })
    return await syncUserWithBackend(cred.user)
  }, [syncUserWithBackend])

  const logout = useCallback(async () => {
    deepLinkRef.current = false
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
    // Forcer un nouveau token (refresh) puis re-sync
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