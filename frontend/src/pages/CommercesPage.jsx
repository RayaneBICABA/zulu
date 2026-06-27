import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Plus, Share2, Store } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../constants/routes'
import ArtisanBottomNav from '../components/layout/ArtisanBottomNav'

const MOCK_COMMERCES = [
  {
    id: 1,
    name: 'Atelier Soudure Alpha',
    description: 'Spécialiste en soudure et ferronnerie à Ouagadougou.',
    published: false,
    image: null,
  },
  {
    id: 2,
    name: 'Menuiserie Kaboré',
    description: 'Fabrication de meubles sur mesure.',
    published: true,
    image: null,
  },
]

const CommercesPage = () => {
  const navigate = useNavigate()
  const [commerces, setCommerces] = useState([])

  const togglePublish = (id) => {
    setCommerces(prev =>
      prev.map(c => c.id === id ? { ...c, published: !c.published } : c)
    )
  }

  return (
    <div className="min-h-screen pb-24 max-w-md mx-auto" style={{ background: 'linear-gradient(180deg, #EEF4FF 0%, #F8F9FF 100%)' }}>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="px-5 pt-10">

        {/* Header */}
        <motion.h1 initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="text-3xl font-black text-amber-500 leading-tight mb-6">
          Les commerces
        </motion.h1>

        {/* Bouton ajouter */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.97 }}
          onClick={() => navigate(ROUTES.newCommerce)}
          className="w-full flex items-center justify-center gap-2 h-14 rounded-2xl bg-white border-2 border-dashed border-blue-200 text-blue-400 font-bold text-sm shadow-sm hover:bg-blue-50 transition-colors mb-6"
        >
          <Plus size={20} />
          Ajouter un commerce
        </motion.button>

        {/* Liste des commerces */}
        <AnimatePresence>
          <div className="space-y-4">
            {commerces.map((commerce, i) => (
              <motion.div
                key={commerce.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="bg-white rounded-3xl overflow-hidden shadow-sm border border-blue-50"
              >
                {/* Image */}
                <div className="w-full h-40 bg-slate-200 flex items-center justify-center">
                  {commerce.image ? (
                    <img src={commerce.image} alt={commerce.name} className="w-full h-full object-cover" />
                  ) : (
                    <Store size={40} className="text-slate-300" />
                  )}
                </div>

                {/* Infos */}
                <div className="p-4">
                  <p className="font-bold text-slate-700 text-base">{commerce.name}</p>
                  <p className="text-sm text-slate-400 mt-1">{commerce.description}</p>

                  <div className="flex items-center justify-between mt-4">
                    {/* Bouton partage */}
                    <motion.a
                      whileTap={{ scale: 0.9 }}
                      href={`https://wa.me/?text=Découvrez ${encodeURIComponent(commerce.name)} sur Zulu !`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="w-10 h-10 bg-blue-50 rounded-xl flex items-center justify-center"
                    >
                      <Share2 size={16} className="text-blue-400" />
                    </motion.a>

                    {/* Bouton publier/retirer */}
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.97 }}
                      onClick={() => togglePublish(commerce.id)}
                      className={`px-5 py-2 rounded-xl text-xs font-black uppercase tracking-wider transition-colors ${
                        commerce.published
                          ? 'bg-red-50 text-red-400 border border-red-100'
                          : 'bg-blue-600 text-white shadow-md shadow-blue-200'
                      }`}
                    >
                      {commerce.published ? 'Retirer' : 'Publier la boutique'}
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </AnimatePresence>
      </motion.div>

      <ArtisanBottomNav />
    </div>
  )
}

export default CommercesPage
