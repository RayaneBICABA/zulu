import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Heart, MapPin, Star } from 'lucide-react'
import commerceService from '../services/commerceService'
import PageWrapper from '../components/layout/PageWrapper'

const FavorisPage = () => {
  const [favoris, setFavoris] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    commerceService.listFavoris()
      .then((data) => setFavoris(data || []))
      .catch(() => setFavoris([]))
      .finally(() => setLoading(false))
  }, [])

  const handleRemove = async (commerceId) => {
    try {
      await commerceService.toggleFavori(commerceId, true)
      setFavoris((prev) => prev.filter((f) => f.commerce_id !== commerceId))
    } catch {}
  }

  return (
    <PageWrapper className="pb-24">
      <div className="px-5 pt-4">
        <h1 className="text-xl font-bold text-gray-900 mb-4">Mes favoris</h1>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : favoris.length === 0 ? (
          <div className="text-center py-12">
            <Heart size={40} className="mx-auto text-gray-300 mb-3" />
            <p className="text-gray-400 text-sm">Aucun favori pour le moment</p>
          </div>
        ) : (
          <div className="space-y-4">
            {favoris.map((fav, i) => {
              const c = fav.commerce
              return (
                <motion.div
                  key={fav.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                  className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm"
                >
                  <div className="relative h-44 bg-gray-100">
                    {c.photo_principale ? (
                      <img src={c.photo_principale} alt={c.nom_commercial} className="w-full h-full object-cover" />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-300">
                        <MapPin size={40} />
                      </div>
                    )}
                    <button
                      onClick={() => handleRemove(c.id)}
                      className="absolute top-3 right-3 w-9 h-9 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-sm"
                    >
                      <Heart size={18} className="fill-error text-error" />
                    </button>
                  </div>
                  <div className="p-3">
                    <div className="flex items-start justify-between mb-1">
                      <h3 className="font-semibold text-gray-900 text-sm">{c.nom_commercial}</h3>
                      <div className="flex items-center gap-1 flex-none">
                        <Star size={12} className="fill-amber-400 text-amber-400" />
                        <span className="text-xs text-gray-600">
                          {c.average_rating > 0 ? c.average_rating.toFixed(1) : '—'}
                        </span>
                      </div>
                    </div>
                    {c.categorie && (
                      <p className="text-xs text-primary-500 mb-1">{c.categorie.nom}</p>
                    )}
                    {c.adresse_complete && (
                      <p className="text-xs text-gray-400 flex items-center gap-1">
                        <MapPin size={10} />
                        {c.adresse_complete}
                      </p>
                    )}
                  </div>
                </motion.div>
              )
            })}
          </div>
        )}
      </div>
    </PageWrapper>
  )
}

export default FavorisPage
