import { Navigate, useLocation } from 'react-router-dom'
import { ROUTES } from '../../../constants/routes'
import Spinner from '../../../components/ui/Spinner'
import useAuth from '../hooks/useAuth'

const ProtectedRoute = ({ children, role, permission }) => {
  const { user, loading, hasRole, hasPermission } = useAuth()
  const location = useLocation()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <Spinner size="lg" />
      </div>
    )
  }

  if (!user) {
    return <Navigate to={ROUTES.login} state={{ from: location }} replace />
  }

  if (role && !hasRole(role)) {
    return <Navigate to={ROUTES.home} replace />
  }

  if (permission && !hasPermission(permission)) {
    return <Navigate to={ROUTES.home} replace />
  }

  return children
}

export default ProtectedRoute
