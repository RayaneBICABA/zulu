import { motion } from 'framer-motion'
import { LogOut, PlusCircle, Store, Mail, Heart } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import { ROUTES } from '../constants/routes'
import { useNavigate } from 'react-router-dom'
import ArtisanBottomNav from '../components/layout/ArtisanBottomNav'

const DashboardPage = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate(ROUTES.login)
  }

  const userBusinesses = [
    { id: 1, name: "Soudure de l'Avenir", status: 'Publié' },
  ]

  return (
    <div className="min-h-screen pb-24 max-w-md mx-auto" style={{ background: 'linear-gradient(180deg, #EEF4FF 0%, #F8F9FF 100%)' }}>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="px-5 pt-10">

        {/* Header */}
        <motion.h1 initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="text-3xl font-black text-amber-500 leading-tight mb-6">
          Mon Tableau{'\n'}de Bord
        </motion.h1>

        {/* Avatar + Nom */}
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.1 }}
          className="bg-white rounded-3xl p-5 shadow-sm border border-blue-50 mb-4 flex items-center gap-4">
          <div className="w-16 h-16 rounded-2xl overflow-hidden border-2 border-blue-50 shadow-sm flex-shrink-0">
            <img src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.first_name}`} alt="Profil" className="w-full h-full object-cover" />
          </div>
          <div>
            <p className="text-lg font-black text-slate-700">{user?.first_name} {user?.last_name}</p>
            <span className="text-xs text-blue-500 font-bold px-3 py-1 bg-blue-50 rounded-full">Membre Zulu</span>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.15 }}
          className="bg-white rounded-3xl p-5 shadow-sm border border-blue-50 mb-6 flex items-center gap-4">
          <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
            <Heart size={18} className="text-rose-400" />
          </div>
          <div>
            <p className="text-xs text-slate-400 font-medium">Favoris</p>
            <p className="text-2xl font-black text-slate-700">12</p>
          </div>
        </motion.div>

        {/* Mes commerces */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="mb-6">
          <div className="flex items-center justify-between mb-3">
            <p className="text-sm font-black text-slate-600 uppercase tracking-wider">Mes commerces</p>
            <motion.button whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}
              onClick={() => navigate(ROUTES.newCommerce)}
              className="flex items-center gap-1 text-xs font-black text-white px-3 py-2 rounded-xl bg-blue-600 shadow-md">
              <PlusCircle size={14} />
              Ajouter
            </motion.button>
          </div>

          <div className="space-y-3">
            {userBusinesses.map((biz, i) => (
              <motion.div key={biz.id} initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 + i * 0.1 }}
                className="bg-white rounded-3xl p-4 shadow-sm border border-blue-50 flex items-center gap-4">
                <div className="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center flex-shrink-0">
                  <Store size={22} className="text-blue-400" />
                </div>
                <div className="flex-1">
                  <p className="font-bold text-slate-700 text-sm">{biz.name}</p>
                  <span className="text-xs text-green-500 font-bold">{biz.status}</span>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Paramètres */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }} className="mb-6">
          <p className="text-sm font-black text-slate-600 uppercase tracking-wider mb-3">Paramètres</p>
          <div className="space-y-3">
            <div className="bg-white rounded-3xl p-4 shadow-sm border border-blue-50 flex items-center gap-4">
              <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
                <Mail size={16} className="text-blue-400" />
              </div>
              <div>
                <p className="text-xs text-slate-400 font-medium">Email</p>
                <p className="text-sm font-bold text-slate-700">{user?.email}</p>
              </div>
            </div>

            <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }} onClick={handleLogout}
              className="w-full flex items-center justify-center gap-2 h-14 rounded-3xl bg-white border border-red-100 text-red-500 font-black text-sm shadow-sm hover:bg-red-50 transition-colors">
              <LogOut size={16} />
              Se déconnecter
            </motion.button>
          </div>
        </motion.div>

      </motion.div>
      <ArtisanBottomNav />
    </div>
  )
}

export default DashboardPage
