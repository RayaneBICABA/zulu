import { useState } from 'react'
import { Link } from 'react-router-dom'
import { CheckCircle2, KeyRound, Mail } from 'lucide-react'
import { ROUTES } from '../../../constants/routes'
import authService from '../../../services/authService'
import AuthLayout from '../../../components/layout/AuthLayout'
import Input from '../../../components/ui/Input'
import Button from '../../../components/ui/Button'
import { AuthAlert, AuthSuccess } from '../components/AuthUI'

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
      await authService.forgotPassword(email)
      setSent(true)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (sent) {
    return (
      <AuthLayout title="Email envoyé !" subtitle="Consultez votre boîte de réception">
        <AuthSuccess icon={<CheckCircle2 size={26} className="text-success" />}>
          <p className="text-muted text-xs sm:text-sm mb-2 leading-relaxed">
            Si un compte existe pour
          </p>
          <p className="text-secondary-600 font-semibold text-xs sm:text-sm mb-4 break-all">
            {email}
          </p>
          <p className="text-muted text-[11px] sm:text-xs mb-5 leading-relaxed">
            Vous recevrez un lien dans les prochaines minutes. Pensez à vérifier vos spams.
          </p>
          <Link to={ROUTES.login}>
            <Button fullWidth variant="secondary">
              Retour à la connexion
            </Button>
          </Link>
        </AuthSuccess>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout
      title="Mot de passe oublié"
      subtitle="Pas de panique, on s'en occupe"
      icon={<KeyRound size={18} strokeWidth={2.5} />}
      footer={
        <Link to={ROUTES.login} className="text-primary-600 font-semibold hover:text-primary-700 transition-colors">
          ← Retour à la connexion
        </Link>
      }
    >
      <div className="mb-5">
        <AuthAlert variant="info">
          Entrez l'email associé à votre compte. Nous vous enverrons un lien sécurisé pour choisir un nouveau mot de passe.
        </AuthAlert>
      </div>

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
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          leftElement={<Mail size={16} />}
        />

        <Button type="submit" fullWidth loading={loading}>
          Envoyer le lien
        </Button>
      </form>
    </AuthLayout>
  )
}

export default ForgotPasswordPage
