import { motion } from 'framer-motion'
import { Award, LogOut, Mail, Phone, Store, User, MessageCircle } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import ArtisanBottomNav from '../components/layout/ArtisanBottomNav'
import useAuth from '../features/auth/hooks/useAuth'
import { ROUTES } from '../constants/routes'

const ArtisanProfilePage = () => {
  const navigate = useNavigate()
  const { user, logout } = useAuth()

  const firstName = user?.first_name || 'Priscilla'
  const lastName = user?.last_name || 'Traore'
  const email = user?.email || 'priscilla.traore@gmail.com'

  const handleLogout = () => {
    logout()
    navigate(ROUTES.login)
  }

  const details = [
    { label: 'Nom du commerce', value: 'Atelier Soudure Alpha', icon: Store },
    { label: 'Prénom', value: firstName, icon: User },
    { label: 'Nom', value: lastName, icon: User },
    { label: 'Email', value: email, icon: Mail },
    { label: 'WhatsApp', value: '+226 70 00 00 00', icon: MessageCircle },
    { label: 'Téléphone', value: '+226 70 00 00 00', icon: Phone },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-blue-50 to-slate-50 pb-24">
      <main className="relative mx-auto min-h-screen max-w-lg overflow-hidden px-6 py-8">
        <div
          className="absolute inset-0 opacity-[0.08]"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='84' height='84' viewBox='0 0 84 84' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23d97706' stroke-width='1'%3E%3Cpath d='M8 8h20v20H8zM56 8h20v20H56zM8 56h20v20H8zM56 56h20v20H56zM42 18l10 10-10 10-10-10zM18 42l10 10-10 10L8 52zM66 42l10 10-10 10-10-10z'/%3E%3Cpath d='M0 42h84M42 0v84' opacity='.35'/%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />

        <motion.section
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          className="relative overflow-hidden rounded-[2rem] bg-white/84 p-5 shadow-xl ring-1 ring-orange-100"
        >
          <div className="absolute inset-x-0 bottom-0 h-36 bg-gradient-to-t from-orange-200/70 to-transparent" />

          <div className="relative">
            <h1 className="mb-7 max-w-[12rem] text-3xl font-black leading-tight text-orange-500">
              Profile DE aRTISAN
            </h1>

            <motion.div
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.08 }}
              className="mb-7 overflow-hidden rounded-xl bg-gradient-to-r from-black via-stone-800 to-orange-950 p-4 text-white shadow-lg"
            >
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-full bg-pink-600 text-white ring-4 ring-pink-500/30">
                  <Award size={20} />
                </div>
                <div>
                  <p className="text-[10px] font-bold uppercase tracking-wider text-orange-300">
                    Compte pro
                  </p>
                  <p className="text-sm font-bold">Tableau de bord Artisan</p>
                  <p className="text-[10px] text-white/60">120 nouveaux avis</p>
                </div>
              </div>
            </motion.div>

            <div className="space-y-3">
              {details.map((item, index) => {
                const Icon = item.icon
                return (
                  <motion.div
                    key={item.label}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.12 + index * 0.04 }}
                    className="flex items-center gap-3 rounded-2xl bg-white/70 p-3 shadow-sm ring-1 ring-orange-100/70"
                  >
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-orange-100 text-orange-500">
                      <Icon size={18} />
                    </div>
                    <div className="min-w-0">
                      <p className="text-[11px] font-bold uppercase tracking-wide text-orange-500">
                        {item.label}
                      </p>
                      <p className="truncate text-sm font-semibold text-gray-700">{item.value}</p>
                    </div>
                  </motion.div>
                )
              })}
            </div>

            <motion.button
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.42 }}
              whileTap={{ scale: 0.96 }}
              onClick={handleLogout}
              className="mt-7 flex h-11 w-full items-center justify-center gap-2 rounded-xl bg-white text-sm font-bold text-red-500 shadow-md ring-1 ring-red-100"
            >
              <LogOut size={16} />
              Se déconnecter
            </motion.button>
          </div>
        </motion.section>
      </main>

      <ArtisanBottomNav />
    </div>
  )
}

export default ArtisanProfilePage
