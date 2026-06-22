import { useState, useEffect } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ROUTES } from '../../../constants/routes'
import authService from '../../../services/authService'
import Button from '../../../components/ui/Button'
import Card from '../../../components/ui/Card'
import Spinner from '../../../components/ui/Spinner'
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

  const renderContent = () => {
    if (status === 'verifying') {
      return (
        <div className="flex flex-col items-center gap-4">
          <Spinner size="lg" />
          <p className="text-sm text-gray-400">Verification de votre email...</p>
        </div>
      )
    }

    if (status === 'success') {
      return (
        <>
          <div className="w-12 h-12 rounded-full bg-successLight flex items-center justify-center mx-auto mb-4">
            <svg className="w-6 h-6 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <h1 className="text-xl font-bold text-secondary-500 mb-2">
            Email verifie
          </h1>
          <p className="text-sm text-gray-400 mb-6">
            Votre adresse email a ete confirmee avec succes.
          </p>
          <Link to={ROUTES.login}>
            <Button>Se connecter</Button>
          </Link>
        </>
      )
    }

    return (
      <>
        <div className="w-12 h-12 rounded-full bg-errorLight flex items-center justify-center mx-auto mb-4">
          <svg className="w-6 h-6 text-error" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h1 className="text-xl font-bold text-secondary-500 mb-2">
          Verification echouee
        </h1>
        <p className="text-sm text-gray-400 mb-2">{error}</p>
        <p className="text-sm text-gray-400 mb-6">
          Le lien a peut-etre expire ou est invalide.
        </p>
        <Link to={ROUTES.login}>
          <Button variant="outline">Retour a la connexion</Button>
        </Link>
      </>
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
        <Card padding="lg" className="text-center">
          {renderContent()}
        </Card>
      </motion.div>
    </PageWrapper>
  )
}

export default VerifyEmailPage
