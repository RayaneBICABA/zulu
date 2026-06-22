import { Link } from 'react-router-dom'
import { ROUTES } from '../constants/routes'
import PageWrapper from '../components/layout/PageWrapper'
import Button from '../components/ui/Button'

const NotFoundPage = () => (
  <PageWrapper className="flex items-center justify-center">
    <div className="text-center px-4">
      <h1 className="text-7xl sm:text-8xl font-bold text-primary-500 mb-4">404</h1>
      <p className="text-gray-500 mb-8">Page introuvable.</p>
      <Link to={ROUTES.home}><Button>Retour à l'accueil</Button></Link>
    </div>
  </PageWrapper>
)

export default NotFoundPage
