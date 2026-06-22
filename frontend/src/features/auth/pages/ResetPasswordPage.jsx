import { useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ROUTES } from '../../../constants/routes'
import authService from '../../../services/authService'
import Button from '../../../components/ui/Button'
import Input from '../../../components/ui/Input'
import Card from '../../../components/ui/Card'
import PageWrapper from '../../../components/layout/PageWrapper'

const ResetPasswordPage = () => {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [fieldErrors, setFieldErrors] = useState({})

  const validate = () => {
    const errors = {}
    if (!password) errors.password = 'Mot de passe requis'
    if (password && password.length < 8) errors.password = 'Minimum 8 caracteres'
    if (password !== confirmPassword) errors.confirmPassword = 'Les mots de passe ne correspondent pas'
    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!token) {
      setError('Lien de reinitialisation invalide ou expire')
      return
    }
    if (!validate()) return
    setError(null)
    setLoading(true)
    try {
      await authService.resetPassword(token, password)
      setSuccess(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (!token) {
    return (
      <PageWrapper className="flex items-center justify-center min-h-screen px-4">
        <Card padding="lg" className="max-w-md w-full text-center">
          <h1 className="text-xl font-bold text-secondary-500 mb-2">Lien invalide</h1>
          <p className="text-sm text-gray-400 mb-6">
            Ce lien de reinitialisation est invalide ou a expire.
          </p>
          <Link to={ROUTES.forgotPassword}>
            <Button>Renouveler la demande</Button>
          </Link>
        </Card>
      </PageWrapper>
    )
  }

  if (success) {
    return (
      <PageWrapper className="flex items-center justify-center min-h-screen px-4">
        <Card padding="lg" className="max-w-md w-full text-center">
          <div className="w-12 h-12 rounded-full bg-successLight flex items-center justify-center mx-auto mb-4">
            <svg className="w-6 h-6 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h1 className="text-xl font-bold text-secondary-500 mb-2">
            Mot de passe reinitialise
          </h1>
          <p className="text-sm text-gray-400 mb-6">
            Vous pouvez desormais vous connecter avec votre nouveau mot de passe.
          </p>
          <Link to={ROUTES.login}>
            <Button>Se connecter</Button>
          </Link>
        </Card>
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
              Nouveau mot de passe
            </h1>
            <p className="text-sm text-gray-400">
              Choisissez un nouveau mot de passe
            </p>
          </div>

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
              onChange={(e) => { setPassword(e.target.value); setFieldErrors((p) => ({ ...p, password: null })) }}
              error={fieldErrors.password}
              required
            />
            <Input
              label="Confirmer le mot de passe"
              name="confirm_password"
              type="password"
              placeholder="Repetez le mot de passe"
              value={confirmPassword}
              onChange={(e) => { setConfirmPassword(e.target.value); setFieldErrors((p) => ({ ...p, confirmPassword: null })) }}
              error={fieldErrors.confirmPassword}
              required
            />
            <Button type="submit" fullWidth loading={loading}>
              Reinitialiser
            </Button>
          </form>
        </Card>
      </motion.div>
    </PageWrapper>
  )
}

export default ResetPasswordPage
