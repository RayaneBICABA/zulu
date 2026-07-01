import { Link } from 'react-router-dom'
import { ROUTES } from '../constants/routes'
import PageWrapper from '../components/layout/PageWrapper'
import Button from '../components/ui/Button'

const NotFoundPage = () => (
  <PageWrapper className="flex items-center justify-center bg-gradient-to-br from-slate-50 via-white to-slate-100">
    <div className="max-w-xl rounded-[32px] border border-slate-200 bg-white/95 p-10 shadow-2xl shadow-slate-200/70 text-center">
      <div className="mb-8">
        <p className="text-7xl sm:text-8xl font-extrabold text-primary-500">404</p>
        <h1 className="mt-4 text-3xl font-semibold text-slate-900">Page introuvable</h1>
        <p className="mt-3 text-sm leading-6 text-slate-600">
          La page que vous cherchez n'existe pas ou a été déplacée. Retournez à l'accueil pour continuer votre navigation.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2">
        <Link to={ROUTES.home}>
          <Button variant="primary" fullWidth>Retour à l'accueil</Button>
        </Link>
        <Link to={ROUTES.login}>
          <Button variant="outline" fullWidth>Se connecter</Button>
        </Link>
      </div>

      <p className="mt-6 text-sm text-slate-500">
        Si le problème persiste, vérifiez l'URL ou contactez le support.
      </p>
    </div>
  </PageWrapper>
)

export default NotFoundPage
