import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { App as CapApp } from '@capacitor/app'
import { Browser } from '@capacitor/browser'
import { ROUTES } from '../../constants/routes'
import useAuth from '../../features/auth/hooks/useAuth'

const DeepLinkHandler = () => {
  const navigate = useNavigate()
  const { refreshUser } = useAuth()

  useEffect(() => {
    const handler = CapApp.addListener('appUrlOpen', async (event) => {
      const url = event.url
      if (url.startsWith('zawani://auth')) {
        try {
          // Safe URL parsing regardless of non-standard protocol support in the browser's URL constructor
          const standardUrl = url.replace('zawani://auth', 'https://localhost/auth')
          const parsed = new URL(standardUrl)
          const accessToken = parsed.searchParams.get('access_token')
          const refreshToken = parsed.searchParams.get('refresh_token')

          if (accessToken) {
            localStorage.setItem('access_token', accessToken)
            if (refreshToken) localStorage.setItem('refresh_token', refreshToken)

            // Close the native custom tab if open
            await Browser.close().catch(() => {})

            // Refresh user details and redirect
            await refreshUser()
            navigate(ROUTES.home, { replace: true })
          } else {
            navigate(ROUTES.login, { replace: true })
          }
        } catch (err) {
          console.error('Failed to parse deep link or authenticate user:', err)
          navigate(ROUTES.login, { replace: true })
        }
      }
    })

    return () => {
      handler.remove()
    }
  }, [navigate, refreshUser])

  return null
}

export default DeepLinkHandler
