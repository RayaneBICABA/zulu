import { Home, Store, User, MessageCircle } from 'lucide-react'
import { motion } from 'framer-motion'
import { useLocation, useNavigate } from 'react-router-dom'
import { ROUTES } from '../../constants/routes'

const navItems = [
  { label: 'Home',     icon: Home,          to: ROUTES.artisanHome },
  { label: 'Avis',     icon: MessageCircle, to: ROUTES.artisanComments },
  { label: 'Commerce', icon: Store,         to: ROUTES.commerces },
  { label: 'Profil',   icon: User,          to: ROUTES.artisanProfile },
]

const ArtisanBottomNav = () => {
  const location = useLocation()
  const navigate = useNavigate()

  return (
    <motion.nav
      initial={{ y: 100 }}
      animate={{ y: 0 }}
      transition={{ delay: 0.25, type: 'spring', stiffness: 120 }}
      className="fixed bottom-0 left-0 right-0 z-50 border-t border-blue-50 bg-white px-6 py-3 shadow-lg"
    >
      <div className="mx-auto flex max-w-md items-center justify-around">
        {navItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.to
          return (
            <motion.button
              key={item.to}
              whileTap={{ scale: 0.9 }}
              onClick={() => navigate(item.to)}
              className={`flex min-w-14 flex-col items-center gap-1 rounded-full transition-all ${
                isActive
                  ? 'bg-blue-500 px-5 py-2 text-white shadow-lg'
                  : 'text-slate-400'
              }`}
            >
              <Icon size={22} />
              <span className={`text-xs ${isActive ? 'font-bold' : 'font-medium'}`}>
                {item.label}
              </span>
            </motion.button>
          )
        })}
      </div>
    </motion.nav>
  )
}

export default ArtisanBottomNav
