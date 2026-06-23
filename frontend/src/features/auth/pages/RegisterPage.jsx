import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ROUTES } from '../../../constants/routes'
import useAuth from '../hooks/useAuth'
import Button from '../../../components/ui/Button'
import Input from '../../../components/ui/Input'
import Card from '../../../components/ui/Card'
import PageWrapper from '../../../components/layout/PageWrapper'

const RegisterPage = () => {
  const { register } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState({
    email: '',
    password: '',
    confirm_password: '',
    first_name: '',
    last_name: '',
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [fieldErrors, setFieldErrors] = useState({})
  const [success, setSuccess] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
    setFieldErrors((prev) => ({ ...prev, [e.target.name]: null }))
  }

  const validate = () => {
    const errors = {}
    if (!form.email) errors.email = 'Email requis'
    if (!form.password) errors.password = 'Mot de passe requis'
    if (form.password && form.password.length < 8) errors.password = 'Minimum 8 caracteres'
    if (form.password !== form.confirm_password) errors.confirm_password = 'Les mots de passe ne correspondent pas'
    if (!form.first_name) errors.first_name = 'Prenom requis'
    if (!form.last_name) errors.last_name = 'Nom requis'
    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!validate()) return
    setError(null)
    setLoading(true)
    try {
      await register({
        email: form.email,
        password: form.password,
        first_name: form.first_name,
        last_name: form.last_name,
      })
      setSuccess(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <PageWrapper className="flex items-center justify-center min-h-screen px-4">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md"
        >
          <Card padding="lg">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-successLight flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h1 className="text-xl font-bold text-secondary-500 mb-2">
                Inscription reussie
              </h1>
              <p className="text-sm text-gray-400 mb-6">
                Un email de verification vous a ete envoye. Veuillez cliquer sur le lien pour activer votre compte.
              </p>
              <Button onClick={() => navigate(ROUTES.login)}>
                Se connecter
              </Button>
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
              Creation de compte
            </h1>
            <p className="text-sm text-gray-400">
              Remplissez le formulaire pour vous inscrire
            </p>
          </div>

          {error && (
            <div className="mb-4 p-3 rounded-lg bg-errorLight text-error text-sm">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-2 gap-3">
              <Input
                label="Prenom"
                name="first_name"
                placeholder="John"
                value={form.first_name}
                onChange={handleChange}
                error={fieldErrors.first_name}
                required
              />
              <Input
                label="Nom"
                name="last_name"
                placeholder="Doe"
                value={form.last_name}
                onChange={handleChange}
                error={fieldErrors.last_name}
                required
              />
            </div>
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
              placeholder="Minimum 8 caracteres"
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
            <Input
              label="Confirmer le mot de passe"
              name="confirm_password"
              type={showConfirm ? 'text' : 'password'}
              placeholder="Repetez le mot de passe"
              value={form.confirm_password}
              onChange={handleChange}
              error={fieldErrors.confirm_password}
              required
              rightElement={
                <button
                  type="button"
                  onClick={() => setShowConfirm((p) => !p)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                  tabIndex={-1}
                >
                  {showConfirm ? (
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
            <Button type="submit" fullWidth loading={loading}>
              S'inscrire
            </Button>
          </form>

          <p className="text-center text-sm text-gray-400 mt-6">
            Deja un compte ?{' '}
            <Link
              to={ROUTES.login}
              className="text-primary-500 hover:text-primary-600 font-medium transition-colors"
            >
              Se connecter
            </Link>
          </p>
        </Card>
      </motion.div>
    </PageWrapper>
  )
}

export default RegisterPage
