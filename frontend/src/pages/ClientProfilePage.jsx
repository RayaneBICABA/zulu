import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { User, Mail, LogOut, ChevronRight, Shield } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import { ROUTES } from '../constants/routes'
import PageWrapper from '../components/layout/PageWrapper'

const ClientProfilePage = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate(ROUTES.login, { replace: true })
  }

  return (
    <PageWrapper className="pb-24">
      <div className="px-5 pt-4">
        <h1 className="text-xl font-bold text-gray-900 mb-6">Mon profil</h1>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden"
        >
          <div className="flex items-center gap-4 p-5 border-b border-gray-100">
            <div className="w-16 h-16 rounded-full bg-primary-50 flex items-center justify-center">
              <User size={28} className="text-primary-500" />
            </div>
            <div>
              <h2 className="font-semibold text-gray-900">
                {user?.first_name} {user?.last_name}
              </h2>
              <p className="text-sm text-gray-400 flex items-center gap-1">
                <Mail size={12} />
                {user?.email}
              </p>
            </div>
          </div>

          <div className="divide-y divide-gray-100">
            <button className="flex items-center justify-between w-full p-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-center gap-3">
                <Shield size={18} className="text-gray-400" />
                <span className="text-sm text-gray-700">Mes informations</span>
              </div>
              <ChevronRight size={16} className="text-gray-300" />
            </button>

            <button
              onClick={handleLogout}
              className="flex items-center gap-3 w-full p-4 hover:bg-gray-50 transition-colors"
            >
              <LogOut size={18} className="text-error" />
              <span className="text-sm text-error font-medium">Se deconnecter</span>
            </button>
          </div>
        </motion.div>
      </div>
    </PageWrapper>
  )
}

export default ClientProfilePage
