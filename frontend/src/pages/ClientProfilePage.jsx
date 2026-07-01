import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { User, Mail, LogOut, Store, ChevronRight } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import commerceService from '../services/commerceService'
import { ROUTES } from '../constants/routes'
import PageWrapper from '../components/layout/PageWrapper'

const ClientProfilePage = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [commerceCount, setCommerceCount] = useState(null)

  useEffect(() => {
    commerceService.artisanProfile()
      .then((data) => setCommerceCount(data.commerces?.length ?? data.nb_commerces ?? 0))
      .catch(() => setCommerceCount(0))
  }, [])

  const handleLogout = async () => {
    await logout()
    navigate(ROUTES.login, { replace: true })
  }

  return (
    <PageWrapper className="pb-24">
      <div className="px-5 pt-14">
        <h1 className="text-xl font-bold text-gray-900 mb-6">Mon profil</h1>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden mb-4"
        >
          <div className="flex items-center gap-4 p-5">
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
              {commerceCount !== null && (
                <p className="text-xs text-gray-400 mt-1">
                  {commerceCount} commerce{commerceCount > 1 ? 's' : ''}
                </p>
              )}
            </div>
          </div>

          <div className="border-t border-gray-100">
            <button
              onClick={() => navigate(ROUTES.dashboard)}
              className="flex items-center justify-between w-full p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                <Store size={18} className="text-primary-500" />
                <span className="text-sm text-gray-700">Mes commerces</span>
              </div>
              <ChevronRight size={16} className="text-gray-300" />
            </button>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl p-5 mb-6"
        >
          <p className="text-white text-sm font-medium mb-3">
            Inscrivez votre commerce et recevez de nouveaux clients gratuitement
          </p>
          <button
            onClick={() => navigate(ROUTES.commerceCreate)}
            className="bg-white text-primary-600 font-semibold text-sm px-5 py-2.5 rounded-xl hover:bg-gray-50 transition-colors"
          >
            Commencer &gt;
          </button>
        </motion.div>

        <button
          onClick={handleLogout}
          className="flex items-center justify-center gap-2 w-full py-3 rounded-xl border border-red-200 text-red-500 font-medium text-sm hover:bg-red-50 transition-colors"
        >
          <LogOut size={18} />
          Se deconnecter
        </button>
      </div>
    </PageWrapper>
  )
}

export default ClientProfilePage
