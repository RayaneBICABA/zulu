import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Eye, Heart, Share2, Star, Plus } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import ArtisanBottomNav from '../components/layout/ArtisanBottomNav'

const MOCK_BUSINESS = {
  name: 'Atelier Soudure Alpha',
  rating: 4.6,
  views: 248,
  favorites: 36,
  description: 'Spécialiste en soudure et ferronnerie depuis 12 ans à Ouagadougou.',
}

const ArtisanHomePage = () => {
  const { user } = useAuth()
  const firstName = user?.first_name || 'Artisan'
  const business = MOCK_BUSINESS
  const [photos, setPhotos] = useState([])
  const whatsappUrl = `https://wa.me/?text=Découvrez ${encodeURIComponent(business.name)} sur Zulu !`

  const handleAddPhoto = () => {
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.multiple = true
    input.onchange = (e) => {
      const files = Array.from(e.target.files).slice(0, 3 - photos.length)
      const urls = files.map(f => URL.createObjectURL(f))
      setPhotos(prev => [...prev, ...urls].slice(0, 3))
    }
    input.click()
  }

  return (
    <div className="min-h-screen pb-24 max-w-md mx-auto" style={{ background: 'linear-gradient(180deg, #EEF4FF 0%, #F8F9FF 100%)' }}>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="px-5 pt-10">

        {/* Header */}
        <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="flex items-start justify-between mb-4">
          <div>
            <h1 className="text-3xl font-black text-amber-500 leading-tight">Artisans Home</h1>
            <p className="text-sm text-slate-400 mt-1">Bonjour {firstName}</p>
            <p className="text-base font-bold text-slate-700 mt-1">{business.name}</p>
          </div>
          <div className="flex flex-col items-end gap-2">
            <motion.div whileHover={{ scale: 1.05 }} className="flex items-center gap-1 bg-white rounded-full px-3 py-1 shadow-md border border-blue-50">
              <Star size={14} className="text-amber-400 fill-amber-400" />
              <span className="text-sm font-bold text-slate-700">{business.rating}</span>
            </motion.div>
            <motion.a whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }} href={whatsappUrl} target="_blank" rel="noopener noreferrer" className="w-10 h-10 bg-white rounded-full shadow-md border border-blue-50 flex items-center justify-center">
              <Share2 size={18} className="text-slate-500" />
            </motion.a>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }} className="flex gap-6 mb-6 bg-white rounded-2xl px-5 py-3 shadow-sm border border-blue-50">
          <div className="flex items-center gap-2">
            <Eye size={16} className="text-blue-400" />
            <span className="text-sm text-slate-600 font-semibold">{business.views} vues</span>
          </div>
          <div className="flex items-center gap-2">
            <Heart size={16} className="text-rose-400" />
            <span className="text-sm text-slate-600 font-semibold">{business.favorites} favoris</span>
          </div>
        </motion.div>

        {/* Carte présentation */}
        <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.3 }} className="bg-blue-100 rounded-3xl p-6 mb-6 shadow-lg">
          <p className="text-blue-800 font-bold text-base mb-2">Présentation de notre APP</p>
          <p className="text-blue-600 text-sm leading-relaxed">{business.description}</p>
        </motion.div>

        {/* Photos */}
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}>
          <p className="text-sm text-slate-500 mb-4">Vous avez des produits ? Ajouter une image</p>

          {/* Bouton ajouter — visible seulement si moins de 3 photos */}
          {photos.length < 3 && (
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.97 }}
              onClick={handleAddPhoto}
              className="w-full flex items-center justify-center gap-2 h-12 rounded-2xl bg-white border-2 border-dashed border-blue-200 text-blue-400 font-semibold text-sm shadow-sm hover:bg-blue-50 transition-colors mb-4"
            >
              <Plus size={18} />
              Ajouter une image
            </motion.button>
          )}

          {/* Cards photos — visibles seulement après ajout */}
          <AnimatePresence>
            {photos.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0 }}
                className="grid grid-cols-3 gap-3"
              >
                {photos.map((photo, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: i * 0.1 }}
                    className="aspect-square rounded-2xl overflow-hidden shadow-md"
                  >
                    <img src={photo} alt={`Photo ${i + 1}`} className="w-full h-full object-cover" />
                  </motion.div>
                ))}
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>

      </motion.div>
      <ArtisanBottomNav />
    </div>
  )
}

export default ArtisanHomePage
