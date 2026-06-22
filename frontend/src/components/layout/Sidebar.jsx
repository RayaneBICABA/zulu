import { Link, useLocation } from 'react-router-dom'
import { useState } from 'react'
import { Menu, X } from 'lucide-react'

const Sidebar = ({
  items = [],
  title = '',
  collapsed = false,
  onItemClick,
  className = '',
}) => {
  const location = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)

  const isActive = (path) => location.pathname === path

  const sidebarContent = (
    <>
      {title && !collapsed && (
        <div className="px-4 py-5 text-lg font-semibold border-b border-white/10">
          {title}
        </div>
      )}

      <nav className="flex-1 px-2 py-4 flex flex-col gap-1">
        {items.map(({ to, label, icon: Icon }) => {
          const active = isActive(to)
          return (
            <Link
              key={to}
              to={to}
              onClick={() => { onItemClick?.(); setMobileOpen(false) }}
              className={`
                flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm
                transition-colors duration-150
                ${active
                  ? 'bg-primary-500 text-white'
                  : 'text-white/70 hover:bg-white/10 hover:text-white'}
              `}
            >
              {Icon && <Icon size={20} className="shrink-0" />}
              {!collapsed && <span>{label}</span>}
            </Link>
          )
        })}
      </nav>
    </>
  )

  return (
    <>
      <button
        className="lg:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-secondary-500 text-white shadow-lg"
        onClick={() => setMobileOpen(!mobileOpen)}
      >
        {mobileOpen ? <X size={20} /> : <Menu size={20} />}
      </button>

      <aside
        className={`
          bg-secondary-500 h-screen text-white flex flex-col
          transition-all duration-200
          ${collapsed ? 'w-16' : 'w-64'}
          hidden lg:flex
          ${className}
        `}
      >
        {sidebarContent}
      </aside>

      {mobileOpen && (
        <div className="lg:hidden fixed inset-0 z-40">
          <div className="absolute inset-0 bg-black/50" onClick={() => setMobileOpen(false)} />
          <aside
            className="bg-secondary-500 relative w-64 h-screen flex flex-col"
          >
            {sidebarContent}
          </aside>
        </div>
      )}
    </>
  )
}

export default Sidebar
