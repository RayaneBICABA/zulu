import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Check, X } from 'lucide-react'
import { ROUTES } from '../../../constants/routes'
import authService from '../../../services/authService'
import Button from '../../../components/ui/Button'
import PageWrapper from '../../../components/layout/PageWrapper'

const VerifyEmailPage = () => {
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')

  const [status, setStatus] = useState(token ? 'verifying' : 'error')
  const [error, setError] = useState(token ? null : 'Lien de verification invalide ou expire')

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
      <PageWrapper className="flex items-center justify-center min-h-screen px-5">
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-center">
          <div className="w-14 h-14 border-2 border-primary-500 border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-sm text-gray-400">Verification de votre email...</p>
        </motion.div>
      </PageWrapper>
    )
  }

  if (status === 'success') {
    return (
      <PageWrapper className="flex items-center justify-center min-h-screen px-5">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center"
        >
          <div className="w-16 h-16 rounded-full bg-green-50 flex items-center justify-center mx-auto mb-5">
            <Check size={32} className="text-green-600" />
          </div>
          <h1 className="text-xl font-bold text-gray-900 mb-2">Email verifie</h1>
          <p className="text-sm text-gray-400 mb-8">
            Votre adresse email a ete confirmee avec succes.
          </p>
          <Link to={ROUTES.login}>
            <Button fullWidth>Se connecter</Button>
          </Link>
        </motion.div>
      </PageWrapper>
    )
  }

  return (
    <PageWrapper className="flex items-center justify-center min-h-screen px-5">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="text-center"
      >
        <div className="w-16 h-16 rounded-full bg-red-50 flex items-center justify-center mx-auto mb-5">
          <X size={32} className="text-red-500" />
        </div>
        <h1 className="text-xl font-bold text-gray-900 mb-2">Verification echouee</h1>
        <p className="text-sm text-gray-400 mb-2">{error}</p>
        <p className="text-sm text-gray-400 mb-8">
          Le lien a peut-etre expire ou est invalide.
        </p>
        <Link to={ROUTES.login}>
          <Button fullWidth variant="outline">Retour a la connexion</Button>
        </Link>
      </motion.div>
    </PageWrapper>
  )
}

export default VerifyEmailPage
