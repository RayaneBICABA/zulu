import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { Eye, EyeOff, CheckCircle2, UserPlus, Mail, Lock, User, Phone } from 'lucide-react'
import { ROUTES } from '../../../constants/routes'
import useAuth from '../hooks/useAuth'
import AuthLayout from '../../../components/layout/AuthLayout'
import Input from '../../../components/ui/Input'
import Button from '../../../components/ui/Button'
import { AuthAlert, AuthSuccess } from '../components/AuthUI'

const RegisterPage = () => {
  const { register } = useAuth()
  const navigate = useNavigate()

  const [form, setForm] = useState({
    email: '',
    password: '',
    confirm_password: '',
    first_name: '',
    last_name: '',
    telephone: '',
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [fieldErrors, setFieldErrors] = useState({})
  const [success, setSuccess] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
    setFieldErrors(prev => ({ ...prev, [e.target.name]: null }))
  }

  const validate = () => {
    const errors = {}
    if (!form.email) errors.email = 'Email requis'
    if (!form.password) errors.password = 'Mot de passe requis'
    if (form.password && form.password.length < 8) errors.password = 'Minimum 8 caractères'
    if (form.password !== form.confirm_password) errors.confirm_password = 'Les mots de passe ne correspondent pas'
    if (!form.first_name) errors.first_name = 'Prénom requis'
    if (!form.last_name) errors.last_name = 'Nom requis'
    if (!form.telephone) errors.telephone = 'Téléphone requis'
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
        nom: form.last_name,
        prenom: form.first_name,
        telephone: form.telephone,
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
      <AuthLayout title="Compte créé !" subtitle="Bienvenue dans la communauté Zulu">
        <AuthSuccess icon={<CheckCircle2 size={26} className="text-success" />}>
          <p className="text-muted text-xs sm:text-sm mb-5 leading-relaxed">
            Votre compte est prêt. Connectez-vous pour découvrir les artisans près de chez vous.
          </p>
          <Button fullWidth onClick={() => navigate(ROUTES.login)}>
            Se connecter
          </Button>
        </AuthSuccess>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout
      title="Créer un compte"
      subtitle="Rejoignez Zulu en quelques secondes"
      icon={<UserPlus size={18} strokeWidth={2.5} />}
      footer={
        <>
          Déjà inscrit ?{' '}
          <Link to={ROUTES.login} className="text-primary-600 font-semibold hover:text-primary-700 transition-colors">
            Se connecter
          </Link>
        </>
      }
    >
      {error && (
        <div className="mb-5">
          <AuthAlert>{error}</AuthAlert>
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <p className="auth-form-group-label">Identité</p>
          <div className="grid grid-cols-1 min-[360px]:grid-cols-2 gap-3">
            <Input
              auth
              label="Prénom"
              name="first_name"
              placeholder="Jean"
              value={form.first_name}
              onChange={handleChange}
              error={fieldErrors.first_name}
              leftElement={<User size={15} />}
            />
            <Input
              auth
              label="Nom"
              name="last_name"
              placeholder="Traoré"
              value={form.last_name}
              onChange={handleChange}
              error={fieldErrors.last_name}
              leftElement={<User size={15} />}
            />
          </div>
          <div className="mt-3.5">
            <Input
              auth
              label="Téléphone"
              name="telephone"
              type="tel"
              placeholder="+226 70 00 00 00"
              value={form.telephone}
              onChange={handleChange}
              error={fieldErrors.telephone}
              leftElement={<Phone size={16} />}
            />
          </div>
        </div>

        <div>
          <p className="auth-form-group-label">Connexion</p>
          <div className="space-y-3.5">
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
              placeholder="8 caractères minimum"
              value={form.password}
              onChange={handleChange}
              error={fieldErrors.password}
              leftElement={<Lock size={16} />}
              rightElement={
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="text-secondary-200 hover:text-primary-600 transition-colors p-1"
                >
                  {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
                </button>
              }
            />

            <Input
              auth
              label="Confirmer le mot de passe"
              name="confirm_password"
              type={showConfirm ? 'text' : 'password'}
              placeholder="Répétez le mot de passe"
              value={form.confirm_password}
              onChange={handleChange}
              error={fieldErrors.confirm_password}
              leftElement={<Lock size={16} />}
              rightElement={
                <button
                  type="button"
                  onClick={() => setShowConfirm(!showConfirm)}
                  className="text-secondary-200 hover:text-primary-600 transition-colors p-1"
                >
                  {showConfirm ? <EyeOff size={17} /> : <Eye size={17} />}
                </button>
              }
            />
          </div>
        </div>

        <Button type="submit" fullWidth loading={loading}>
          Créer mon compte
        </Button>
      </form>
    </AuthLayout>
  )
}

export default RegisterPage
