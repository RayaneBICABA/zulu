import { motion } from 'framer-motion'
import { Settings, LogOut, ChevronRight, PlusCircle, Store, Mail, Heart, Users } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import { ROUTES } from '../constants/routes'
import { useNavigate } from 'react-router-dom'
import MobileNav from '../components/layout/MobileNav'

const DashboardPage = () => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate(ROUTES.login)
  }

  const userBusinesses = [
    { id: 1, name: 'Soudure de l\'Avenir', status: 'Publié', visitors: 124 },
  ]

  return (
    <div className="page-container">
      <div className="page-inner">
        <section className="profile-header">
          <div className="relative px-5 sm:px-6 pt-12 sm:pt-14 pb-8">
            <motion.div
              initial={{ opacity: 0, y: 16 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.4 }}
              className="flex flex-col items-center text-center"
            >
              <div className="relative mb-4">
                <div className="w-24 h-24 rounded-2xl overflow-hidden ring-4 ring-white shadow-lg border border-primary-100">
                  <img
                    src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${user?.first_name}`}
                    alt="Profil"
                    className="w-full h-full object-cover bg-surface"
                  />
                </div>
                <button className="absolute -bottom-1 -right-1 w-9 h-9 bg-primary-500 text-white rounded-xl flex items-center justify-center border-2 border-white shadow-md hover:bg-primary-600 transition-colors">
                  <Settings size={15} />
                </button>
              </div>

              <h2 className="text-xl sm:text-2xl font-bold text-secondary-600">
                {user?.first_name} {user?.last_name}
              </h2>
              <span className="text-xs text-primary-700 font-medium mt-2 px-3 py-1 bg-primary-50 rounded-full border border-primary-200">
                Membre Zulu
              </span>
            </motion.div>

            <div className="grid grid-cols-2 gap-3 mt-7">
              {[
                { icon: Heart, label: 'Favoris', value: '12' },
                { icon: Users, label: 'Contacts', value: '48' },
              ].map((stat, i) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1 + i * 0.08 }}
                  className="surface-card p-4 text-center"
                >
                  <div className="w-9 h-9 rounded-xl bg-primary-100 text-primary-600 flex items-center justify-center mx-auto mb-2">
                    <stat.icon size={17} />
                  </div>
                  <p className="text-xs text-muted font-medium">{stat.label}</p>
                  <p className="text-2xl font-bold text-gradient mt-0.5">{stat.value}</p>
                </motion.div>
              ))}
            </div>
          </div>
        </section>

        <section className="mt-6 px-5 sm:px-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="section-title">Mes commerces</h3>
            <button
              onClick={() => navigate(ROUTES.addBusiness)}
              className="flex items-center gap-1.5 text-xs font-semibold text-white px-3 py-1.5 rounded-full bg-primary-500 hover:bg-primary-600 transition-colors shadow-sm"
            >
              <PlusCircle size={14} />
              Ajouter
            </button>
          </div>

          {userBusinesses.length > 0 ? (
            <div className="space-y-3">
              {userBusinesses.map((biz) => (
                <motion.div
                  key={biz.id}
                  whileHover={{ y: -2 }}
                  className="surface-card p-4 flex items-center justify-between group cursor-pointer border-l-4 border-l-primary-400"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-11 h-11 rounded-xl bg-primary-100 text-primary-600 flex items-center justify-center">
                      <Store size={20} />
                    </div>
                    <div>
                      <h4 className="font-semibold text-secondary-600 text-sm group-hover:text-primary-700 transition-colors">{biz.name}</h4>
                      <span className="inline-flex items-center gap-1 text-xs text-success font-medium mt-0.5 bg-success-light px-2 py-0.5 rounded-full">
                        {biz.status}
                      </span>
                    </div>
                  </div>
                  <button className="w-8 h-8 rounded-lg bg-primary-50 flex items-center justify-center text-primary-500 group-hover:bg-primary-500 group-hover:text-white transition-all">
                    <ChevronRight size={17} />
                  </button>
                </motion.div>
              ))}
            </div>
          ) : (
            <div className="surface-card p-8 border-dashed border-2 border-primary-200 text-center bg-primary-50/30">
              <div className="w-14 h-14 rounded-2xl bg-primary-100 text-primary-500 flex items-center justify-center mx-auto mb-3">
                <Store size={24} />
              </div>
              <p className="text-sm text-muted leading-relaxed">
                Vous n'avez pas encore enregistré de commerce.
              </p>
            </div>
          )}
        </section>

        <section className="mt-6 px-5 sm:px-6 pb-8">
          <h3 className="section-title mb-3">Paramètres</h3>
          <div className="surface-card overflow-hidden divide-y divide-secondary-100">
            <button className="w-full p-4 flex items-center justify-between hover:bg-primary-50/50 transition-colors group">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-primary-50 text-primary-600 flex items-center justify-center">
                  <Mail size={16} />
                </div>
                <div className="text-left">
                  <p className="text-sm font-medium text-secondary-600">Email</p>
                  <p className="text-xs text-muted truncate max-w-[200px] sm:max-w-xs">{user?.email}</p>
                </div>
              </div>
              <ChevronRight size={16} className="text-secondary-200 group-hover:text-primary-400 transition-colors" />
            </button>
            <button
              className="w-full p-4 flex items-center justify-between hover:bg-red-50/50 transition-colors group"
              onClick={handleLogout}
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-red-50 text-error flex items-center justify-center">
                  <LogOut size={16} />
                </div>
                <div className="text-left">
                  <p className="text-sm font-medium text-error">Déconnexion</p>
                  <p className="text-xs text-error/70">Quitter la session</p>
                </div>
              </div>
            </button>
          </div>
        </section>
      </div>

      <MobileNav />
    </div>
  )
}

export default DashboardPage
