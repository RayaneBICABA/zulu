import { useEffect, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { ROUTES } from '../../../constants/routes'
import useAuth from '../hooks/useAuth'
import Spinner from '../../../components/ui/Spinner'

const TOKEN_KEY = 'access_token'
const REFRESH_KEY = 'refresh_token'

const GoogleCallbackPage = () => {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const { refreshUser } = useAuth()
  const [error, setError] = useState(null)

  useEffect(() => {
    const accessToken = searchParams.get('access_token')
    const refreshToken = searchParams.get('refresh_token')
    const errorParam = searchParams.get('error')

    if (errorParam) {
      setError('Authentification Google echouee.')
      return
    }

    if (!accessToken) {
      setError('Token manquant.')
      return
    }

    localStorage.setItem(TOKEN_KEY, accessToken)
    if (refreshToken) localStorage.setItem(REFRESH_KEY, refreshToken)

    refreshUser()
      .then(() => navigate(ROUTES.home, { replace: true }))
      .catch(() => {
        localStorage.removeItem(TOKEN_KEY)
        localStorage.removeItem(REFRESH_KEY)
        setError('Session invalide.')
      })
  }, [searchParams, navigate, refreshUser])

  if (error) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center px-5">
        <p className="text-error text-sm mb-4">{error}</p>
        <button
          onClick={() => navigate(ROUTES.login, { replace: true })}
          className="text-primary-500 text-sm font-medium"
        >
          Retour a la connexion
        </button>
      </div>
    )
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <Spinner size="lg" />
    </div>
  )
}

export default GoogleCallbackPage
