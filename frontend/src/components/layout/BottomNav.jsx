import { NavLink } from 'react-router-dom'
import { Home, Heart, User, Plus } from 'lucide-react'
import { ROUTES } from '../../constants/routes'
import useAuth from '../../features/auth/hooks/useAuth'

const BottomNav = () => {
  const { hasRole } = useAuth()
  const isArtisan = hasRole('artisan')

  const links = [
    { to: ROUTES.home, icon: Home, label: 'Accueil' },
    ...(isArtisan ? [{ to: ROUTES.dashboard, icon: Plus, label: 'Commerce', isPrimary: true }] : []),
    { to: ROUTES.favoris, icon: Heart, label: 'Favoris' },
    { to: ROUTES.profile, icon: User, label: 'Profil' },
  ]

  return (
    <nav className="fixed bottom-0 left-1/2 -translate-x-1/2 w-full max-w-[430px] bg-white border-t border-gray-200 z-50">
      <div className="flex items-center justify-around h-16">
        {links.map(({ to, icon: Icon, label, isPrimary }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              `flex flex-col items-center justify-center gap-0.5 w-full h-full transition-colors ${
                isPrimary
                  ? 'text-primary-500'
                  : isActive
                    ? 'text-primary-500'
                    : 'text-gray-400'
              }`
            }
          >
            {({ isActive }) => (
              <>
                {isPrimary ? (
                  <div className="w-10 h-10 -mt-4 bg-primary-500 rounded-full flex items-center justify-center shadow-lg shadow-primary-500/30">
                    <Icon size={20} className="text-white" />
                  </div>
                ) : (
                  <Icon size={22} strokeWidth={isActive ? 2.5 : 1.5} />
                )}
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
