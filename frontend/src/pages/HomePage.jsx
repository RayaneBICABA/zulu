import { useState } from 'react'
import { motion } from 'framer-motion'
import {
  Search, MapPin, Star, ChevronRight, Bell, Sparkles,
  Wrench, Scissors, Zap, Hammer, HardHat, Shirt,
} from 'lucide-react'
import MobileNav from '../components/layout/MobileNav'
import logo from '../assets/fasoConnect.png'

const categories = [
  { id: 'mecanicien', name: 'Mécanique', icon: Wrench, bg: 'linear-gradient(135deg, #89c4e8, #5dade2)' },
  { id: 'couturier', name: 'Couture', icon: Shirt, bg: 'linear-gradient(135deg, #a8d4ea, #6bb5df)' },
  { id: 'coiffeur', name: 'Coiffure', icon: Scissors, bg: 'linear-gradient(135deg, #b3daf0, #4a9fd4)' },
  { id: 'soudeur', name: 'Soudure', icon: HardHat, bg: 'linear-gradient(135deg, #7eb8d4, #3d8fbe)' },
  { id: 'menuisier', name: 'Menuiserie', icon: Hammer, bg: 'linear-gradient(135deg, #9ecae8, #5dade2)' },
  { id: 'electricien', name: 'Électricité', icon: Zap, bg: 'linear-gradient(135deg, #c5e4f3, #6bb5df)' },
]

const recentArtisans = [
  { id: 1, name: 'Mécanique Plus', category: 'Mécanicien', rating: 4.8, distance: '0.8 km', image: 'https://images.unsplash.com/photo-1530046339160-ce3e5b0c7a2f?q=80&w=600&auto=format&fit=crop' },
  { id: 2, name: 'Couture d\'Or', category: 'Couturier', rating: 4.9, distance: '1.2 km', image: 'https://images.unsplash.com/photo-1558694440-03ade9215d7b?q=80&w=600&auto=format&fit=crop' },
  { id: 3, name: 'Salon Prestige', category: 'Coiffeur', rating: 4.5, distance: '2.5 km', image: 'https://images.unsplash.com/photo-1585747860715-2ba37e788b70?q=80&w=600&auto=format&fit=crop' },
]

const fadeUp = {
  hidden: { opacity: 0, y: 16 },
  visible: (i) => ({
    opacity: 1, y: 0,
    transition: { delay: i * 0.07, duration: 0.4, ease: [0.22, 1, 0.36, 1] },
  }),
}

const HomePage = () => {
  const [search, setSearch] = useState('')

  return (
    <div className="page-container">
      <div className="header-zone">
        <div className="page-inner">
          <motion.header
            initial="hidden" animate="visible" variants={fadeUp} custom={0}
            className="px-5 sm:px-6 pt-10 sm:pt-12 pb-4 flex items-center justify-between"
          >
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-xl bg-surface flex items-center justify-center border border-secondary-200 shadow-sm overflow-hidden">
                <img src={logo} alt="Zulu" className="w-8 h-8 object-contain" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-secondary-600 leading-none tracking-tight">Zulu</h1>
                <p className="text-xs text-primary-600 font-medium mt-0.5">Burkina Faso</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button className="icon-btn relative">
                <Bell size={18} />
                <span className="absolute top-2 right-2 w-2 h-2 bg-primary-500 rounded-full ring-2 ring-surface" />
              </button>
              <div className="w-11 h-11 rounded-xl overflow-hidden border border-secondary-200 shadow-sm">
                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Salif" alt="Profil" className="w-full h-full object-cover bg-surface" />
              </div>
            </div>
          </motion.header>
        </div>
      </div>

      <div className="page-inner">
        <motion.section
          initial="hidden" animate="visible" variants={fadeUp} custom={1}
          className="px-5 sm:px-6 pt-4"
        >
          <div className="hero-banner mb-5">
            <div className="relative z-10">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-white/60 backdrop-blur-sm border border-white/80 text-primary-700 text-xs font-semibold mb-3">
                <Sparkles size={12} className="text-primary-500" />
                Artisans vérifiés près de vous
              </div>
              <h2 className="text-2xl sm:text-3xl font-bold text-secondary-600 leading-tight mb-1.5">
                Trouvez le bon<br />
                <span className="text-gradient">artisan</span> en un clic
              </h2>
              <p className="text-secondary-500 text-sm">
                Mécanique · Couture · Coiffure · Soudure
              </p>
            </div>
          </div>

          <div className="relative mb-6">
            <div className="absolute left-3.5 top-1/2 -translate-y-1/2 w-8 h-8 rounded-lg bg-primary-500 flex items-center justify-center z-10">
              <Search size={15} className="text-white" />
            </div>
            <input
              type="text"
              placeholder="Rechercher un service, un métier..."
              className="input-field pl-14 h-14 text-base shadow-md border-primary-100"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </motion.section>

        <motion.section initial="hidden" animate="visible" variants={fadeUp} custom={2} className="mb-7">
          <div className="px-5 sm:px-6 flex items-center justify-between mb-4">
            <h3 className="section-title">Catégories</h3>
            <button className="text-xs text-primary-600 font-semibold px-3 py-1 rounded-full bg-primary-50 border border-primary-200 hover:bg-primary-100 transition-colors">
              Voir tout →
            </button>
          </div>
          <div className="flex gap-3 overflow-x-auto px-5 sm:px-6 no-scrollbar pb-2">
            {categories.map((cat) => {
              const Icon = cat.icon
              return (
                <button key={cat.id} className="flex-shrink-0 flex flex-col items-center gap-2 w-[4.5rem] sm:w-20 group">
                  <div
                    className="category-icon text-white group-active:scale-95"
                    style={{ background: cat.bg }}
                  >
                    <Icon size={22} strokeWidth={2} />
                  </div>
                  <span className="text-[11px] font-medium text-secondary-500 text-center leading-tight">
                    {cat.name}
                  </span>
                </button>
              )
            })}
          </div>
        </motion.section>

        <motion.section
          initial="hidden" animate="visible" variants={fadeUp} custom={3}
          className="px-5 sm:px-6 pb-8"
        >
          <div className="flex items-center justify-between mb-4">
            <h3 className="section-title">À proximité</h3>
            <div className="badge-pill">
              <MapPin size={12} className="text-primary-500" />
              Ouagadougou
            </div>
          </div>

          <div className="space-y-3">
            {recentArtisans.map((artisan, i) => (
              <motion.button
                key={artisan.id}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.15 + i * 0.08, duration: 0.35 }}
                whileTap={{ scale: 0.99 }}
                className="artisan-card group w-full text-left"
              >
                <div className="flex gap-0 sm:gap-0">
                  <div className="relative w-28 sm:w-32 flex-shrink-0">
                    <img src={artisan.image} alt={artisan.name} className="w-full h-full min-h-[7rem] object-cover" />
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent to-black/10" />
                  </div>
                  <div className="flex-grow p-3.5 sm:p-4 flex flex-col justify-between min-w-0">
                    <div>
                      <span className="text-[10px] font-semibold text-primary-600 bg-primary-50 px-2 py-0.5 rounded-full border border-primary-100">
                        {artisan.category}
                      </span>
                      <h4 className="font-semibold text-secondary-600 text-sm sm:text-base mt-1.5 truncate group-hover:text-primary-700 transition-colors">
                        {artisan.name}
                      </h4>
                    </div>
                    <div className="flex items-center justify-between mt-2">
                      <div className="flex items-center gap-2.5">
                        <div className="flex items-center gap-1 px-2 py-0.5 rounded-lg bg-primary-50 border border-primary-100">
                          <Star size={11} className="text-primary-500 fill-primary-500" />
                          <span className="text-xs font-semibold text-primary-700">{artisan.rating}</span>
                        </div>
                        <span className="text-xs text-muted flex items-center gap-0.5">
                          <MapPin size={10} /> {artisan.distance}
                        </span>
                      </div>
                      <div className="w-8 h-8 bg-primary-500 rounded-lg flex items-center justify-center text-white shadow-sm group-hover:bg-primary-600 transition-colors">
                        <ChevronRight size={16} />
                      </div>
                    </div>
                  </div>
                </div>
              </motion.button>
            ))}
          </div>
        </motion.section>
      </div>

      <MobileNav />
    </div>
  )
}

export default HomePage
