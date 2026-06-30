import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Eye, EyeOff, Check } from 'lucide-react'
import { ROUTES } from '../../../constants/routes'
import useAuth from '../hooks/useAuth'
import Button from '../../../components/ui/Button'
import Input from '../../../components/ui/Input'
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
    if (!form.first_name) errors.first_name = 'Prenom requis'
    if (!form.last_name) errors.last_name = 'Nom requis'
    if (!form.email) errors.email = 'Email requis'
    if (!form.password) errors.password = 'Mot de passe requis'
    if (form.password && form.password.length < 8) errors.password = 'Minimum 8 caracteres'
    if (form.password !== form.confirm_password) errors.confirm_password = 'Les mots de passe ne correspondent pas'
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
      const code = err.code
      if (code === 'auth/email-already-in-use') {
        setError('Un compte avec cet email existe deja.')
      } else if (code === 'auth/weak-password') {
        setError('Le mot de passe est trop faible.')
      } else if (code === 'auth/invalid-email') {
        setError('Email invalide.')
      } else {
        setError(err.message || "Erreur lors de l'inscription.")
      }
    } finally {
      setLoading(false)
    }
  }

   const handleGoogleLogin = async () => {
    if (window.Capacitor?.isNativePlatform?.()) {
      const { Browser } = await import("@capacitor/browser");
      const { API_URL } = await import("../../../constants/api");
      await Browser.open({ url: `${API_URL}/auth/google/mobile` });
    } else {
      const { signInWithRedirect, googleProvider, auth } =
        await import("../../../firebase");
      await signInWithRedirect(auth, googleProvider);
    }
  }

  if (success) {
    return (
      <PageWrapper className="flex flex-col items-center justify-center min-h-screen px-5">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="w-full text-center"
        >
          <div className="w-14 h-14 rounded-full bg-successLight flex items-center justify-center mx-auto mb-5">
            <Check size={28} className="text-success" />
          </div>
          <h1 className="text-xl font-bold text-gray-900 mb-2">
            Inscription reussie
          </h1>
          <p className="text-sm text-gray-400 mb-8">
            Bienvenue sur Zawani ! Vous pouvez des maintenant vous connecter.
          </p>
          <Button onClick={() => navigate(ROUTES.login)} fullWidth>
            Se connecter
          </Button>
        </motion.div>
      </PageWrapper>
    )
  }

  return (
    <PageWrapper className="flex flex-col min-h-screen px-5 pt-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="w-full"
      >
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900 mb-1">
            Creer un compte
          </h1>
          <p className="text-sm text-gray-400">
            Rejoignez la communaute Zawani
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
                {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
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
                {showConfirm ? <EyeOff size={18} /> : <Eye size={18} />}
              </button>
            }
          />
          <Button type="submit" fullWidth loading={loading}>
            S'inscrire
          </Button>
        </form>

        <p className="text-center text-sm text-gray-400 mt-8">
          Deja un compte ?{' '}
          <Link
            to={ROUTES.login}
            className="text-primary-500 hover:text-primary-600 font-medium transition-colors"
          >
            Se connecter
          </Link>
        </p>

        <div className="relative my-8">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-200" />
          </div>
          <div className="relative flex justify-center text-xs">
            <span className="px-3 bg-white text-gray-400">ou</span>
          </div>
        </div>

        <button
          onClick={handleGoogleLogin}
          className="flex items-center justify-center w-full h-12 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer"
        >
          <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
            <path
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
              fill="#4285F4"
            />
            <path
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              fill="#34A853"
            />
            <path
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              fill="#FBBC05"
            />
            <path
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              fill="#EA4335"
            />
          </svg>
          Continuer avec Google
        </button>
      </motion.div>
    </PageWrapper>
  )
}

export default RegisterPage
