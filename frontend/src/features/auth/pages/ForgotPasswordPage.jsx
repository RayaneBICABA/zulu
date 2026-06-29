import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ROUTES } from '../../../constants/routes'
import Button from '../../../components/ui/Button'
import Input from '../../../components/ui/Input'
import Card from '../../../components/ui/Card'
import PageWrapper from '../../../components/layout/PageWrapper'
import apiClient from '../../../services/apiClient'

const ForgotPasswordPage = () => {
  const [email, setEmail] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [sent, setSent] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email) {
      setError('Veuillez entrer votre email')
      return
    }
    setError(null)
    setLoading(true)
    try {
      await apiClient.post('/auth/forgot-password', { email })
      setSent(true)
    } catch (err) {
      setSent(true)
    } finally {
      setLoading(false)
    }
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
          {sent ? (
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-successLight flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h1 className="text-xl font-bold text-secondary-500 mb-2">
                Email envoye
              </h1>
              <p className="text-sm text-gray-400 mb-6">
                Si un compte existe avec cette adresse, vous recevrez un lien de reinitialisation.
              </p>
              <Link to={ROUTES.login}>
                <Button>Retour a la connexion</Button>
              </Link>
            </div>
          ) : (
            <>
              <div className="text-center mb-6">
                <h1 className="text-2xl font-bold text-secondary-500 mb-1">
                  Mot de passe oublie
                </h1>
                <p className="text-sm text-gray-400">
                  Saisissez votre email et recevez un lien de reinitialisation
                </p>
              </div>

              {error && (
                <div className="mb-4 p-3 rounded-lg bg-errorLight text-error text-sm">
                  {error}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <Input
                  label="Email"
                  name="email"
                  type="email"
                  placeholder="vous@exemple.com"
                  value={email}
                  onChange={(e) => { setEmail(e.target.value); setError(null) }}
                  required
                />
                <Button type="submit" fullWidth loading={loading}>
                  Envoyer le lien
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
            </>
          )}
        </Card>
      </motion.div>
    </PageWrapper>
  )
}

export default ForgotPasswordPage