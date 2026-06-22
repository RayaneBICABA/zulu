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
  const [verificationUrl, setVerificationUrl] = useState(null)

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
      const data = await register({
        email: form.email,
        password: form.password,
        first_name: form.first_name,
        last_name: form.last_name,
      })
      if (data?.verification_url) setVerificationUrl(data.verification_url)
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
              <p className="text-sm text-gray-400 mb-4">
                Un email de verification vous a ete envoye. Veuillez cliquer sur le lien pour activer votre compte.
              </p>
              {verificationUrl && (
                <a
                  href={verificationUrl}
                  className="block mb-6 text-sm text-primary-500 hover:text-primary-600 underline break-all"
                >
                  {verificationUrl}
                </a>
              )}
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
              type="password"
              placeholder="Minimum 8 caracteres"
              value={form.password}
              onChange={handleChange}
              error={fieldErrors.password}
              required
            />
            <Input
              label="Confirmer le mot de passe"
              name="confirm_password"
              type="password"
              placeholder="Repetez le mot de passe"
              value={form.confirm_password}
              onChange={handleChange}
              error={fieldErrors.confirm_password}
              required
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
