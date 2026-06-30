import { useState } from 'react'
import { useSearchParams, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ROUTES } from '../../../constants/routes'
import Button from '../../../components/ui/Button'
import Input from '../../../components/ui/Input'
import Card from '../../../components/ui/Card'
import PageWrapper from '../../../components/layout/PageWrapper'
import apiClient from '../../../services/apiClient'
import { useOnlineStatus } from '../../../hooks/useOnlineStatus'

const ResetPasswordPage = () => {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  const isOnline = useOnlineStatus()

  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!token) {
      setError('Lien invalide ou expire.')
      return
    }
    if (password.length < 8) {
      setError('Le mot de passe doit contenir au moins 8 caracteres.')
      return
    }
    if (password !== confirmPassword) {
      setError('Les mots de passe ne correspondent pas.')
      return
    }

    if (!isOnline) {
      setError('Vous semblez hors ligne. Veuillez vérifier votre connexion internet.')
      return
    }
    setError(null)
    setLoading(true)
    try {
      await apiClient.post('/auth/reset-password', { token, password })
      setSuccess(true)
    } catch (err) {
      setError(err.message || 'Erreur lors de la reinitialisation.')
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <PageWrapper className="flex items-center justify-center min-h-screen px-4">
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="w-full max-w-md">
          <Card padding="lg">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-successLight flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h1 className="text-xl font-bold text-secondary-500 mb-2">
                Mot de passe reinitialise
              </h1>
              <p className="text-sm text-gray-400 mb-6">
                Votre mot de passe a ete modifie avec succes.
              </p>
              <Link to={ROUTES.login}>
                <Button>Se connecter</Button>
              </Link>
            </div>
          </Card>
        </motion.div>
      </PageWrapper>
    )
  }

  return (
    <PageWrapper className="flex items-center justify-center min-h-screen px-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="w-full max-w-md"
      >
        <Card padding="lg">
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold text-secondary-500 mb-1">
              Reinitialiser le mot de passe
            </h1>
            <p className="text-sm text-gray-400">
              Choisissez un nouveau mot de passe securise
            </p>
          </div>

          {!token && (
            <div className="mb-4 p-3 rounded-lg bg-errorLight text-error text-sm">
              Lien invalide ou expire. <Link to={ROUTES.forgotPassword} className="underline">Demander un nouveau lien</Link>
            </div>
          )}

          {error && (
            <div className="mb-4 p-3 rounded-lg bg-errorLight text-error text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <Input
              label="Nouveau mot de passe"
              name="password"
              type="password"
              placeholder="Minimum 8 caracteres"
              value={password}
              onChange={(e) => { setPassword(e.target.value); setError(null) }}
              required
            />
            <Input
              label="Confirmer le mot de passe"
              name="confirm_password"
              type="password"
              placeholder="Repeter le mot de passe"
              value={confirmPassword}
              onChange={(e) => { setConfirmPassword(e.target.value); setError(null) }}
              required
            />
            <Button type="submit" fullWidth loading={loading} disabled={!token}>
              Reinitialiser le mot de passe
            </Button>
          </form>

          <p className="text-center text-sm text-gray-400 mt-6">
            <Link
              to={ROUTES.login}
              className="text-primary-500 hover:text-primary-600 font-medium transition-colors"
            >
              Retour a la connexion
            </Link>
          </p>
        </Card>
      </motion.div>
    </PageWrapper>
  )
}

export default ResetPasswordPage