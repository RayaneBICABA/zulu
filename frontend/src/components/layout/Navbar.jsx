import { Link } from 'react-router-dom'
import { Menu, X } from 'lucide-react'
import { useState } from 'react'
import { ROUTES } from '../../constants/routes'
import Button from '../ui/Button'

const Navbar = () => {
  const [open, setOpen] = useState(false)

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-lg mx-auto px-4 h-14 flex items-center justify-between">
        <Link to={ROUTES.home} className="flex items-center gap-2">
          <img src="/logo.png" alt="Zawani" className="h-8 w-8 object-contain" />
          <span className="text-lg font-bold tracking-tight text-primary-500">
            Zawani
          </span>
        </Link>

        <div className="hidden md:flex items-center gap-4">
          <Link to={ROUTES.home}
            className="text-sm text-gray-600 hover:text-primary-500 transition-colors">
            Accueil
          </Link>
          <Button variant="primary" size="sm">
            Connexion
          </Button>
        </div>

        <button className="md:hidden p-2 -mr-2" onClick={() => setOpen(!open)}>
          {open ? <X size={20} className="text-gray-900" /> : <Menu size={20} className="text-gray-900" />}
        </button>
      </div>

      {open && (
        <div className="bg-white md:hidden px-4 pb-4 flex flex-col gap-3 border-b border-gray-200">
          <Link to={ROUTES.home} className="text-sm text-gray-600 hover:text-primary-500 py-2">
            Accueil
          </Link>
          <Button variant="primary" size="sm" fullWidth>
            Connexion
          </Button>
        </div>
      )}
    </nav>
  )
}

export default Navbar
