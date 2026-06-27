import { Link, useLocation } from 'react-router-dom'
import { Home, Search, Map, Heart, User } from 'lucide-react'
import { motion } from 'framer-motion'
import { ROUTES } from '../../constants/routes'

const NavItem = ({ to, icon: Icon, label, active }) => (
  <Link
    to={to}
    className={`relative flex flex-col items-center justify-center gap-0.5 min-w-0 flex-1 py-1 transition-colors duration-200 ${
      active ? 'text-primary-600' : 'text-muted hover:text-primary-500'
    }`}
  >
    {active && (
      <motion.div
        layoutId="nav-indicator"
        className="absolute -top-0.5 w-8 h-0.5 rounded-full bg-primary-500"
        transition={{ type: 'spring', stiffness: 400, damping: 30 }}
      />
    )}
    <div className={`p-1.5 rounded-xl transition-all duration-200 ${
      active ? 'bg-primary-100 text-primary-600' : ''
    }`}>
      <Icon size={20} strokeWidth={active ? 2.5 : 2} />
    </div>
    <span className="text-[9px] font-medium truncate w-full text-center">{label}</span>
  </Link>
)

const MobileNav = () => {
  const location = useLocation()

  const navItems = [
    { to: ROUTES.home, icon: Home, label: 'Accueil' },
    { to: '/search', icon: Search, label: 'Découvrir' },
    { to: '/map', icon: Map, label: 'Carte' },
    { to: '/favorites', icon: Heart, label: 'Favoris' },
    { to: ROUTES.dashboard, icon: User, label: 'Profil' },
  ]

  return (
    <nav className="nav-floating">
      <div className="flex items-center justify-between">
        {navItems.map((item) => (
          <NavItem
            key={item.to}
            to={item.to}
            icon={item.icon}
            label={item.label}
            active={location.pathname === item.to}
          />
        ))}
      </div>
    </nav>
  )
}

export default MobileNav
