import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Eye, EyeOff, LogIn, Mail, Lock } from 'lucide-react'
import { ROUTES } from '../../../constants/routes'
import { API_URL, ENDPOINTS } from '../../../constants/api'
import useAuth from '../hooks/useAuth'
import AuthLayout from '../../../components/layout/AuthLayout'
import Input from '../../../components/ui/Input'
import Button from '../../../components/ui/Button'
import { AuthDivider, AuthAlert, AuthGoogleButton } from '../components/AuthUI'

const LoginPage = () => {
  const { login } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState({ email: '', password: '' })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [fieldErrors, setFieldErrors] = useState({})
  const [showPassword, setShowPassword] = useState(false)

  const handleGoogleLogin = () => {
    window.location.href = `${API_URL}${ENDPOINTS.auth.googleLogin}`
  }

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
    setFieldErrors(prev => ({ ...prev, [e.target.name]: null }))
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
      navigate(ROUTES.dashboard)
    } catch (err) {
      setError(err.message || 'Identifiants invalides')
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout
      title="Bon retour !"
      subtitle="Connectez-vous pour accéder à votre espace Zulu"
      icon={<LogIn size={18} strokeWidth={2.5} />}
      footer={
        <>
          Pas encore de compte ?{' '}
          <Link to={ROUTES.register} className="text-primary-600 font-semibold hover:text-primary-700 transition-colors">
            Créer un compte
          </Link>
        </>
      }
    >
      {error && (
        <div className="mb-5">
          <AuthAlert>{error}</AuthAlert>
        </div>
      )}

      <form onSubmit={handleSubmit} className="auth-form-section">
        <Input
          auth
          label="Adresse email"
          name="email"
          type="email"
          placeholder="vous@exemple.com"
          value={form.email}
          onChange={handleChange}
          error={fieldErrors.email}
          leftElement={<Mail size={16} />}
        />

        <Input
          auth
          label="Mot de passe"
          name="password"
          type={showPassword ? 'text' : 'password'}
          placeholder="••••••••"
          value={form.password}
          onChange={handleChange}
          error={fieldErrors.password}
          leftElement={<Lock size={16} />}
          rightElement={
            <button
              type="button"
              onClick={() => setShowPassword(p => !p)}
              className="text-secondary-200 hover:text-primary-600 transition-colors p-1"
              aria-label={showPassword ? 'Masquer' : 'Afficher'}
            >
              {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
            </button>
          }
        />

        <div className="flex justify-end -mt-1">
          <Link
            to={ROUTES.forgotPassword}
            className="text-sm text-primary-600 hover:text-primary-700 font-medium transition-colors"
          >
            Mot de passe oublié ?
          </Link>
        </div>

        <Button type="submit" fullWidth loading={loading}>
          Se connecter
        </Button>
      </form>

      <AuthDivider />
      <AuthGoogleButton onClick={handleGoogleLogin} />
    </AuthLayout>
  )
}

export default LoginPage
