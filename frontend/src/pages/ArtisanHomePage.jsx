import { motion } from 'framer-motion'
import { Eye, Heart, Store, User, ImageIcon, TrendingUp, Camera, Edit3 } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import { ROUTES } from '../constants/routes'
import { useNavigate } from 'react-router-dom'

/* Animation variants */
const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.15 },
  },
}

const fadeInUp = {
  hidden: { opacity: 0, y: 30 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.6, ease: [0.25, 0.46, 0.45, 0.94] },
  },
}

const scaleIn = {
  hidden: { opacity: 0, scale: 0.9 },
  visible: {
    opacity: 1,
    scale: 1,
    transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] },
  },
}

/* Données mock */
const MOCK_BUSINESS = {
  name: 'Atelier Soudure Alpha',
  views: 248,
  favorites: 36,
  description:
    'Spécialiste en soudure et ferronnerie depuis 12 ans à Ouagadougou. Réparations, portails, grilles et structures métalliques sur mesure.',
  photos: [
    'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?q=80&w=400&auto=format&fit=crop',
    null,
    null,
  ],
}

/* Stat Card avec gradient */
const StatCard = ({ icon: Icon, label, value, gradient, delay }) => (
  <motion.div
    variants={scaleIn}
    whileHover={{ y: -6, scale: 1.02 }}
    className="relative overflow-hidden rounded-3xl p-5 bg-white shadow-lg hover:shadow-2xl transition-all duration-300"
  >
    <div className={`absolute inset-0 opacity-10 ${gradient}`} />
    <div className="relative">
      <div className="flex items-center justify-between mb-3">
        <div className={`w-12 h-12 rounded-2xl ${gradient} flex items-center justify-center text-white shadow-lg`}>
          <Icon size={22} />
        </div>
        <TrendingUp size={16} className="text-green-500" />
      </div>
      <p className="text-3xl font-bold text-gray-800 mb-1">{value}</p>
      <p className="text-sm text-gray-500 font-medium">{label}</p>
    </div>
  </motion.div>
)

/* Photo Card */
const PhotoCard = ({ photo, index }) => (
  <motion.div
    variants={scaleIn}
    whileHover={{ scale: 1.05 }}
    className="aspect-square rounded-3xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-300"
  >
    {photo ? (
      <motion.img
        src={photo}
        alt={`Photo ${index + 1}`}
        className="w-full h-full object-cover"
        whileHover={{ scale: 1.1 }}
        transition={{ duration: 0.4 }}
      />
    ) : (
      <div className="w-full h-full bg-gradient-to-br from-gray-100 to-gray-200 flex flex-col items-center justify-center gap-2">
        <div className="w-16 h-16 rounded-2xl bg-white/80 flex items-center justify-center shadow-md">
          <Camera size={28} className="text-gray-400" />
        </div>
        <span className="text-xs text-gray-500 font-medium">Ajouter</span>
      </div>
    )}
  </motion.div>
)

const ArtisanHomePage = () => {
  const { user } = useAuth()
  const navigate = useNavigate()
  const business = MOCK_BUSINESS
  const firstName = user?.first_name || 'Artisan'

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 pb-24">
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8"
      >
        {/* Header avec salutation */}
        <motion.header variants={fadeInUp} className="mb-8">
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-sm sm:text-base text-gray-500 font-medium mb-1">Bonjour 👋</p>
              <h1 className="text-3xl sm:text-4xl lg:text-5xl font-bold bg-gradient-to-r from-amber-600 via-orange-500 to-amber-600 bg-clip-text text-transparent">
                {firstName}
              </h1>
            </div>
            <motion.button
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              onClick={() => navigate(ROUTES.dashboard)}
              className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl bg-white shadow-lg flex items-center justify-center hover:shadow-xl transition-shadow"
            >
              <User size={22} className="text-gray-600" />
            </motion.button>
          </div>
          
          {/* Badge commerce */}
          <motion.div
            variants={fadeInUp}
            className="inline-flex items-center gap-3 px-4 sm:px-5 py-3 rounded-2xl bg-white shadow-lg"
          >
            <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-xl bg-gradient-to-br from-amber-400 to-orange-500 flex items-center justify-center shadow-md">
              <Store size={20} className="text-white" />
            </div>
            <div>
              <p className="text-xs text-gray-500 font-medium">Votre commerce</p>
              <p className="text-base sm:text-lg font-bold text-gray-800">{business.name}</p>
            </div>
          </motion.div>
        </motion.header>

        {/* Stats Grid */}
        <motion.section variants={fadeInUp} className="mb-8">
          <div className="grid grid-cols-2 gap-4 sm:gap-6">
            <StatCard
              icon={Eye}
              label="Vues totales"
              value={business.views}
              gradient="bg-gradient-to-br from-blue-500 to-blue-600"
              delay={0.2}
            />
            <StatCard
              icon={Heart}
              label="Favoris"
              value={business.favorites}
              gradient="bg-gradient-to-br from-pink-500 to-rose-600"
              delay={0.3}
            />
          </div>
        </motion.section>

        {/* Carte présentation */}
        <motion.section variants={fadeInUp} className="mb-8">
          <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-amber-500 via-orange-500 to-yellow-500 p-6 sm:p-8 shadow-2xl">
            {/* Decorations */}
            <div className="absolute top-0 right-0 w-32 h-32 sm:w-48 sm:h-48 bg-white/10 rounded-full blur-3xl -mr-16 -mt-16" />
            <div className="absolute bottom-0 left-0 w-24 h-24 sm:w-40 sm:h-40 bg-white/10 rounded-full blur-2xl -ml-10 -mb-10" />
            
            <div className="relative">
              <div className="flex items-center gap-2 mb-4">
                <Edit3 size={18} className="text-white" />
                <h3 className="text-white text-lg sm:text-xl font-bold">Présentation</h3>
              </div>
              <p className="text-white/90 text-sm sm:text-base lg:text-lg leading-relaxed mb-4">
                {business.description}
              </p>
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                <span className="text-white/80 text-xs sm:text-sm font-medium">Commerce actif</span>
              </div>
            </div>
          </div>
        </motion.section>

        {/* Photos Grid */}
        <motion.section variants={fadeInUp}>
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg sm:text-xl font-bold text-gray-800">Photos du commerce</h3>
            <button className="text-sm text-amber-600 font-semibold hover:text-amber-700">
              Voir tout
            </button>
          </div>
          <motion.div
            variants={containerVariants}
            className="grid grid-cols-3 gap-3 sm:gap-4 lg:gap-6"
          >
            {business.photos.map((photo, i) => (
              <PhotoCard key={i} photo={photo} index={i} />
            ))}
          </motion.div>
        </motion.section>
      </motion.div>

      {/* Navigation bottom */}
      <motion.nav
        initial={{ y: 100 }}
        animate={{ y: 0 }}
        transition={{ delay: 0.6, type: 'spring', stiffness: 120 }}
        className="fixed bottom-0 left-0 right-0 bg-white/95 backdrop-blur-xl border-t border-gray-200 shadow-2xl px-6 py-3"
      >
        <div className="max-w-md mx-auto flex items-center justify-around">
          <motion.button
            whileTap={{ scale: 0.9 }}
            className="flex flex-col items-center gap-1 px-6 py-2 rounded-2xl bg-gradient-to-r from-amber-500 to-orange-500 text-white shadow-lg"
          >
            <Store size={24} />
            <span className="text-xs font-semibold">Commerce</span>
          </motion.button>
          <motion.button
            whileTap={{ scale: 0.9 }}
            onClick={() => navigate(ROUTES.dashboard)}
            className="flex flex-col items-center gap-1 px-6 py-2 rounded-2xl text-gray-400 hover:text-gray-600 transition-colors"
          >
            <User size={24} />
            <span className="text-xs font-semibold">Profil</span>
          </motion.button>
        </div>
      </motion.nav>
    </div>
  )
}

export default ArtisanHomePage
