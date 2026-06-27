import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { CheckCircle2, AlertCircle, Loader2 } from 'lucide-react'
import { ROUTES } from '../../../constants/routes'
import authService from '../../../services/authService'
import AuthLayout from '../../../components/layout/AuthLayout'
import Button from '../../../components/ui/Button'

const VerifyEmailPage = () => {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [status, setStatus] = useState(token ? 'verifying' : 'error')
  const [error, setError] = useState(token ? null : 'Lien de vérification invalide ou expiré')

  useEffect(() => {
    if (!token) return
    authService.verifyEmail(token)
      .then(() => setStatus('success'))
      .catch((err) => {
        setStatus('error')
        setError(err.message)
      })
  }, [token])

  if (status === 'verifying') {
    return (
      <AuthLayout title="Vérification" subtitle="Confirmation de votre adresse email">
        <div className="flex flex-col items-center gap-4 py-6">
          <Loader2 size={32} className="text-primary-500 animate-spin" />
          <p className="text-sm text-muted">Vérification en cours...</p>
        </div>
      </AuthLayout>
    )
  }

  if (status === 'success') {
    return (
      <AuthLayout title="Email vérifié" subtitle="Votre compte est maintenant actif">
        <div className="text-center py-2">
          <div className="w-14 h-14 bg-green-50 rounded-full flex items-center justify-center mx-auto mb-5">
            <CheckCircle2 size={28} className="text-success" />
          </div>
          <p className="text-muted text-sm mb-6 leading-relaxed">
            Votre adresse email a été confirmée. Vous pouvez vous connecter.
          </p>
          <Link to={ROUTES.login}>
            <Button fullWidth>Se connecter</Button>
          </Link>
        </div>
      </AuthLayout>
    )
  }

  return (
    <AuthLayout title="Échec de vérification" subtitle="Le lien n'est plus valide">
      <div className="text-center py-2">
        <div className="w-14 h-14 bg-red-50 rounded-full flex items-center justify-center mx-auto mb-5">
          <AlertCircle size={28} className="text-error" />
        </div>
        <p className="text-error text-sm mb-2">{error}</p>
        <p className="text-muted text-sm mb-6 leading-relaxed">
          Le lien a peut-être expiré. Essayez de vous reconnecter pour recevoir un nouvel email.
        </p>
        <Link to={ROUTES.login}>
          <Button fullWidth variant="secondary">Retour à la connexion</Button>
        </Link>
      </div>
    </AuthLayout>
  )
}

export default VerifyEmailPage
