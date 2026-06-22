import { Link } from 'react-router-dom'
import { Menu, X } from 'lucide-react'
import { useState } from 'react'
import { ROUTES } from '../../constants/routes'
import Button from '../ui/Button'

const Navbar = () => {
  const [open, setOpen] = useState(false)

  return (
    <nav className="bg-secondary-500 text-white shadow-md">
      <div className="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
        <Link to={ROUTES.home} className="text-xl font-bold tracking-tight text-white">
          Zulu<span className="text-primary-500">.</span>
        </Link>

        <div className="hidden md:flex items-center gap-4">
          <Link to={ROUTES.home}
            className="text-sm text-white/80 hover:text-white transition-colors">
            Accueil
          </Link>
          <Button variant="primary" size="sm">
            Connexion
          </Button>
        </div>

        <button className="md:hidden" onClick={() => setOpen(!open)}>
          {open ? <X size={22} /> : <Menu size={22} />}
        </button>
      </div>

      {open && (
        <div className="bg-secondary-500 md:hidden px-4 pb-4 flex flex-col gap-3">
          <Link to={ROUTES.home} className="text-sm text-white/80 hover:text-white">
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