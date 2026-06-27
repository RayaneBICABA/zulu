import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Heart } from 'lucide-react'
import commerceService from '../services/commerceService'
import CommerceCard from '../components/ui/CommerceCard'
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
            {favoris.map((fav, i) => (
              <CommerceCard
                key={fav.id}
                commerce={fav.commerce}
                index={i}
                isFavorited={true}
                onToggleFavori={handleRemove}
              />
            ))}
          </div>
        )}
      </div>
    </PageWrapper>
  )
}

export default FavorisPage
