import PageWrapper from '../components/layout/PageWrapper'
import Navbar from '../components/layout/Navbar'
import Card from '../components/ui/Card'
import Button from '../components/ui/Button'
import useAuth from '../features/auth/hooks/useAuth'
import { ROUTES } from '../constants/routes'
import { useNavigate } from 'react-router-dom'

const DashboardPage = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate(ROUTES.login)
  }

  return (
    <PageWrapper>
      <Navbar />
      <main className="max-w-lg mx-auto px-4 py-16">
        <Card padding="lg">
          <h1 className="text-2xl font-bold text-gray-900 mb-4">
            Tableau de bord
          </h1>
          <p className="text-gray-500 mb-2">
            Bienvenue, {user?.first_name} {user?.last_name}
          </p>
          <p className="text-sm text-gray-400 mb-6">
            Email : {user?.email}
          </p>
          <div className="flex gap-3">
            <Button variant="outline" onClick={handleLogout}>
              Deconnexion
            </Button>
          </div>
        </Card>
      </main>
    </PageWrapper>
  )
}

export default DashboardPage
