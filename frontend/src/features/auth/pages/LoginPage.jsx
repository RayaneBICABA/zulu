import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ROUTES } from '../../../constants/routes'
import useAuth from '../hooks/useAuth'
import Button from '../../../components/ui/Button'
import Input from '../../../components/ui/Input'
import Card from '../../../components/ui/Card'
import PageWrapper from '../../../components/layout/PageWrapper'
import SocialLoginButton from '../components/SocialLoginButton'

const LoginPage = () => {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from = location.state?.from?.pathname || ROUTES.home

  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [fieldErrors, setFieldErrors] = useState({})

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
    setFieldErrors((prev) => ({ ...prev, [e.target.name]: null }))
  }

  const validate = () => {
    const errors = {}
    if (!form.email) errors.email = 'Email requis'
    if (!form.password) errors.password = 'Mot de passe requis'
    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return
    setError(null)
    setLoading(true)
    try {
      await login(form)
      navigate(from, { replace: true })
    } catch (err) {
      setError(err.message)
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
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold text-secondary-500 mb-1">
              Connexion
            </h1>
            <p className="text-sm text-gray-400">
              Accedez a votre compte
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
              value={form.email}
              onChange={handleChange}
              error={fieldErrors.email}
              required
            />
            <Input
              label="Mot de passe"
              name="password"
              type="password"
              placeholder="Votre mot de passe"
              value={form.password}
              onChange={handleChange}
              error={fieldErrors.password}
              required
            />
            <div className="flex justify-end">
              <Link
                to={ROUTES.forgotPassword}
                className="text-sm text-primary-500 hover:text-primary-600 transition-colors"
              >
                Mot de passe oublie ?
              </Link>
            </div>
            <Button type="submit" fullWidth loading={loading}>
              Se connecter
            </Button>
          </form>

          <div className="mt-6">
            <div className="relative mb-6">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-200" />
              </div>
              <div className="relative flex justify-center text-xs">
                <span className="bg-white px-2 text-gray-400">
                  Ou continuer avec
                </span>
              </div>
            </div>
            <SocialLoginButton provider="google" />
          </div>

          <p className="text-center text-sm text-gray-400 mt-6">
            Pas encore de compte ?{' '}
            <Link
              to={ROUTES.register}
              className="text-primary-500 hover:text-primary-600 font-medium transition-colors"
            >
              S'inscrire
            </Link>
          </p>
        </Card>
      </motion.div>
    </PageWrapper>
  )
}

export default LoginPage
