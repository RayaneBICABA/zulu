import { motion } from 'framer-motion'
import { Award, LogOut, User, Store, Mail, Phone, MessageCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import useAuth from '../features/auth/hooks/useAuth'
import { ROUTES } from '../constants/routes'
import ArtisanBottomNav from '../components/layout/ArtisanBottomNav'

const InfoRow = ({ icon: Icon, label, value }) => (
  <motion.div
    initial={{ opacity: 0, x: -10 }}
    animate={{ opacity: 1, x: 0 }}
    className="flex items-center gap-4 bg-white rounded-2xl px-5 py-4 shadow-sm border border-blue-50"
  >
    <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center flex-shrink-0">
      <Icon size={18} className="text-blue-400" />
    </div>
    <div>
      <p className="text-xs text-slate-400 font-medium">{label}</p>
      <p className="text-sm font-bold text-slate-700">{value || '—'}</p>
    </div>
  </motion.div>
)

const ArtisanProfilePage = () => {
  const navigate = useNavigate()
  const { logout, user } = useAuth()

  const handleLogout = () => {
    logout()
    navigate(ROUTES.login)
  }

  return (
    <div className="min-h-screen pb-24 max-w-md mx-auto" style={{ background: 'linear-gradient(180deg, #EEF4FF 0%, #F8F9FF 100%)' }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="px-5 pt-10"
      >
        {/* Header */}
        <motion.h1
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-3xl font-black text-amber-500 leading-tight mb-6"
        >
          Profile de{'\n'}l'Artisan
        </motion.h1>

        {/* Carte Pro */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          whileHover={{ scale: 1.02 }}
          className="mb-6 overflow-hidden rounded-3xl bg-gradient-to-r from-blue-100 via-blue-50 to-slate-100 p-5 shadow-xl"
        >
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-pink-600 flex items-center justify-center shadow-lg ring-4 ring-pink-500/20">
              <Award size={22} className="text-slate-800" />
            </div>
            <div>
              <p className="text-[10px] font-black uppercase tracking-widest text-blue-500 mb-1">Compte Pro</p>
              <p className="text-sm font-bold text-slate-800">Tableau de bord Artisan</p>
              <p className="text-xs text-slate-800/50 mt-0.5">120 nouveaux avis</p>
            </div>
          </div>
        </motion.div>

        {/* Infos utilisateur */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="space-y-3 mb-8"
        >
          <InfoRow icon={Store}          label="Commerce"   value="Atelier Soudure Alpha" />
          <InfoRow icon={User}           label="Prénom"     value={user?.first_name} />
          <InfoRow icon={User}           label="Nom"        value={user?.last_name} />
          <InfoRow icon={Mail}           label="Email"      value={user?.email} />
          <InfoRow icon={MessageCircle}  label="WhatsApp"   value={user?.whatsapp || '+226 XX XX XX XX'} />
          <InfoRow icon={Phone}          label="Téléphone"  value={user?.phone || '+226 XX XX XX XX'} />
        </motion.div>

        {/* Bouton déconnexion */}
        <motion.button
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.97 }}
          onClick={handleLogout}
          className="w-full flex items-center justify-center gap-2 h-14 rounded-2xl bg-white border border-red-100 text-red-500 font-bold text-sm shadow-sm hover:bg-red-50 transition-colors"
        >
          <LogOut size={16} />
          Se déconnecter
        </motion.button>
      </motion.div>

      <ArtisanBottomNav />
    </div>
  )
}

export default ArtisanProfilePage
