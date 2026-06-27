import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { User, Mail, LogOut, ChevronRight, Shield, Store, Hammer, Check } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import authService from '../services/authService'
import { ROUTES } from '../constants/routes'
import PageWrapper from '../components/layout/PageWrapper'

const ClientProfilePage = () => {
  const { user, logout, hasRole, setUser } = useAuth()
  const navigate = useNavigate()
  const isArtisan = hasRole('artisan')
  const [upgrading, setUpgrading] = useState(false)
  const [upgraded, setUpgraded] = useState(false)

  const handleLogout = () => {
    logout()
    navigate(ROUTES.login, { replace: true })
  }

  const handleBecomeArtisan = async () => {
    setUpgrading(true)
    try {
      const data = await authService.becomeArtisan()
      if (data.user) setUser(data.user)
      setUpgraded(true)
    } catch (err) {
      // silent
    } finally {
      setUpgrading(false)
    }
  }

  return (
    <PageWrapper className="pb-24">
      <div className="px-5 pt-4">
        <h1 className="text-xl font-bold text-gray-900 mb-6">Mon profil</h1>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden mb-4"
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
              <div className="flex gap-1 mt-1">
                {(user?.roles || []).map((role) => (
                  <span
                    key={role}
                    className={`text-[10px] px-2 py-0.5 rounded-full font-medium ${
                      role === 'artisan'
                        ? 'bg-primary-50 text-primary-600'
                        : 'bg-gray-100 text-gray-500'
                    }`}
                  >
                    {role}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="divide-y divide-gray-100">
            {isArtisan && (
              <button
                onClick={() => navigate(ROUTES.dashboard)}
                className="flex items-center justify-between w-full p-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <Store size={18} className="text-primary-500" />
                  <span className="text-sm text-gray-700">Mon commerce</span>
                </div>
                <ChevronRight size={16} className="text-gray-300" />
              </button>
            )}

            {!isArtisan && !upgraded && (
              <button
                onClick={handleBecomeArtisan}
                disabled={upgrading}
                className="flex items-center justify-between w-full p-4 hover:bg-gray-50 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <Hammer size={18} className="text-primary-500" />
                  <div className="text-left">
                    <span className="text-sm text-gray-700 font-medium">Devenir Artisan</span>
                    <p className="text-xs text-gray-400">Creez votre commerce et recevez des clients</p>
                  </div>
                </div>
                {upgrading ? (
                  <div className="w-5 h-5 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
                ) : (
                  <ChevronRight size={16} className="text-gray-300" />
                )}
              </button>
            )}

            {upgraded && (
              <div className="flex items-center gap-3 p-4 bg-green-50">
                <Check size={18} className="text-green-600" />
                <span className="text-sm text-green-700 font-medium">
                  Vous etes maintenant artisan ! Creez votre commerce.
                </span>
              </div>
            )}

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
              <LogOut size={18} className="text-red-500" />
              <span className="text-sm text-red-500 font-medium">Se deconnecter</span>
            </button>
          </div>
        </motion.div>
      </div>
    </PageWrapper>
  )
}

export default ClientProfilePage
