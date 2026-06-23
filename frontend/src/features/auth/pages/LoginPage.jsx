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
  const [showPassword, setShowPassword] = useState(false)

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
              type={showPassword ? 'text' : 'password'}
              placeholder="Votre mot de passe"
              value={form.password}
              onChange={handleChange}
              error={fieldErrors.password}
              required
              rightElement={
                <button
                  type="button"
                  onClick={() => setShowPassword((p) => !p)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                  tabIndex={-1}
                >
                  {showPassword ? (
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  )}
                </button>
              }
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
