import { useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { Eye, EyeOff, CheckCircle2, AlertCircle } from 'lucide-react'
import { ROUTES } from '../../../constants/routes'
import authService from '../../../services/authService'
import AuthLayout from '../../../components/layout/AuthLayout'
import Input from '../../../components/ui/Input'
import Button from '../../../components/ui/Button'

const ResetPasswordPage = () => {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)
  const [success, setSuccess] = useState(false)
  const [fieldErrors, setFieldErrors] = useState({})
  const [showPassword, setShowPassword] = useState(false)

  const validate = () => {
    const errors = {}
    if (!password) errors.password = 'Mot de passe requis'
    if (password && password.length < 8) errors.password = 'Minimum 8 caractères'
    if (password !== confirmPassword) errors.confirmPassword = 'Les mots de passe ne correspondent pas'
    setFieldErrors(errors)
    return Object.keys(errors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!token) {
      setError('Lien de réinitialisation invalide ou expiré')
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
      <AuthLayout title="Lien invalide" subtitle="Ce lien a expiré ou est incorrect">
        <div className="text-center py-2">
          <div className="w-14 h-14 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-5">
            <AlertCircle size={28} className="text-error" />
          </div>
          <p className="text-muted text-sm mb-6 leading-relaxed">
            Veuillez refaire une demande de réinitialisation de mot de passe.
          </p>
          <Link to={ROUTES.forgotPassword}>
            <Button fullWidth>Refaire une demande</Button>
          </Link>
        </div>
      </AuthLayout>
    )
  }

  if (success) {
    return (
      <AuthLayout title="Mot de passe modifié" subtitle="Vous pouvez maintenant vous connecter">
        <div className="text-center py-2">
          <div className="w-14 h-14 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-5">
            <CheckCircle2 size={28} className="text-success" />
          </div>
          <p className="text-muted text-sm mb-6 leading-relaxed">
            Votre mot de passe a été réinitialisé avec succès.
          </p>
          <Link to={ROUTES.login}>
            <Button fullWidth>Se connecter</Button>
          </Link>
        </div>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout title="Nouveau mot de passe" subtitle="Choisissez un mot de passe sécurisé">
      {error && (
        <div className="mb-5 p-3 rounded-xl bg-red-50 text-error text-sm border border-red-100">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="space-y-4">
        <Input
          label="Nouveau mot de passe"
          name="password"
          type={showPassword ? 'text' : 'password'}
          placeholder="8 caractères minimum"
          value={password}
          onChange={(e) => { setPassword(e.target.value); setFieldErrors(p => ({ ...p, password: null })) }}
          error={fieldErrors.password}
          rightElement={
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="text-secondary-200 hover:text-primary-600 transition-colors p-1"
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          }
        />

        <Input
          label="Confirmer le mot de passe"
          name="confirmPassword"
          type="password"
          placeholder="Répétez le mot de passe"
          value={confirmPassword}
          onChange={(e) => { setConfirmPassword(e.target.value); setFieldErrors(p => ({ ...p, confirmPassword: null })) }}
          error={fieldErrors.confirmPassword}
        />

        <Button type="submit" fullWidth loading={loading} className="mt-2">
          Changer le mot de passe
        </Button>
      </form>
    </AuthLayout>
  )
}

export default ResetPasswordPage
