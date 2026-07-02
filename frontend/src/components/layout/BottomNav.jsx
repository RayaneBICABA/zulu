import { NavLink } from 'react-router-dom'
import { Home, Heart, Store, User } from 'lucide-react'
import { ROUTES } from '../../constants/routes'

const BottomNav = () => {
  const links = [
    { to: ROUTES.home, icon: Home, label: 'Accueil' },
    { to: ROUTES.favoris, icon: Heart, label: 'Favoris' },
    { to: ROUTES.dashboard, icon: Store, label: 'Commerce' },
    { to: ROUTES.profile, icon: User, label: 'Profil' },
  ]

  return (
    <nav className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[430px] bg-white border-t border-gray-200 z-50">
      <div className="flex items-center justify-around h-16">
        {links.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex flex-col items-center justify-center gap-0.5 w-full h-full transition-colors ${
                isActive ? 'text-primary-500' : 'text-gray-400'
              }`
            }
          >
            {({ isActive }) => (
              <>
                <Icon size={22} strokeWidth={isActive ? 2.5 : 1.5} />
                <span className="text-[10px] font-medium">{label}</span>
              </>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  )
}

export default BottomNav
