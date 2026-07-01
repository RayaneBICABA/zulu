import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Store, MapPin, Search, Shield } from 'lucide-react'

const features = [
  { icon: Search,  title: 'Trouvez',          desc: 'Decouvrez les commerces et artisans pres de chez vous.' },
  { icon: Store,   title: 'Decouvrez',        desc: 'Explorez les produits et services de votre quartier.' },
  { icon: MapPin,  title: 'Localisez',        desc: 'Trouvez facilement les adresses et horaires.' },
  { icon: Shield,  title: 'Connectez',        desc: 'Echangez directement avec les artisans.' },
]

const LandingPage = () => {
  const navigate = useNavigate()

  useEffect(() => {
    if (window.Capacitor) {
      navigate('/splash', { replace: true })
    }
  }, [navigate])

  if (window.Capacitor) return null

  return (
    <div className="min-h-screen bg-white">
      <header className="max-w-6xl mx-auto px-6 py-6 flex items-center justify-between">
        <img src="/zawani.svg" alt="Zawani" className="h-8" />
        <nav className="flex items-center gap-4">
          <button
            onClick={() => navigate('/login')}
            className="text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            Connexion
          </button>
          <button
            onClick={() => navigate('/register')}
            className="text-sm px-5 py-2.5 bg-primary-500 text-white rounded-full hover:bg-primary-600 transition-colors font-medium"
          >
            Creer un compte
          </button>
        </nav>
      </header>

      <main>
        <section className="max-w-6xl mx-auto px-6 pt-24 pb-20 md:pt-32 md:pb-28">
          <div className="max-w-2xl">
            <motion.h1
              className="text-5xl md:text-6xl font-bold text-gray-900 leading-tight"
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
            >
              Le marche de
              <br />
              <span className="text-primary-500">proximite</span>
            </motion.h1>
            <motion.p
              className="text-lg text-gray-500 mt-6 leading-relaxed"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.2, ease: [0.22, 1, 0.36, 1] }}
            >
              Zawani vous connecte aux commerces et artisans de votre quartier.
              Trouvez, comparez et echanguez en toute simplicite.
            </motion.p>
            <motion.div
              className="flex items-center gap-4 mt-10"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.35, ease: [0.22, 1, 0.36, 1] }}
            >
              <button
                onClick={() => navigate('/register')}
                className="px-8 py-3.5 bg-primary-500 text-white rounded-full hover:bg-primary-600 transition-colors font-medium shadow-lg shadow-primary-500/25"
              >
                Commencer
              </button>
              <button
                onClick={() => navigate('/admin/categories')}
                className="px-8 py-3.5 text-gray-600 hover:text-gray-900 transition-colors font-medium"
              >
                Admin
              </button>
            </motion.div>
          </div>
        </section>

        <section className="max-w-6xl mx-auto px-6 pb-24">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                className="p-6 rounded-2xl bg-gray-50 hover:bg-gray-100 transition-colors"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.4 + i * 0.1, ease: [0.22, 1, 0.36, 1] }}
              >
                <div className="w-10 h-10 rounded-xl bg-primary-100 flex items-center justify-center mb-4">
                  <f.icon size={20} className="text-primary-500" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-1">{f.title}</h3>
                <p className="text-sm text-gray-500 leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </section>
      </main>

      <footer className="border-t border-gray-100 py-8">
        <div className="max-w-6xl mx-auto px-6 flex items-center justify-between text-sm text-gray-400">
          <span>&copy; 2025 Zawani</span>
          <div className="flex items-center gap-6">
            <button onClick={() => navigate('/login')} className="hover:text-gray-600 transition-colors">Connexion</button>
            <button onClick={() => navigate('/admin/categories')} className="hover:text-gray-600 transition-colors">Admin</button>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default LandingPage