import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { MapPin, Heart } from 'lucide-react'
import StarRating from './StarRating'

const CommerceCard = ({ commerce, isFavorited, onToggleFavori, index = 0 }) => {
  const navigate = useNavigate()

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05 }}
      className="bg-white rounded-2xl border border-gray-100 overflow-hidden shadow-sm cursor-pointer active:scale-[0.98] transition-transform"
      onClick={() => navigate(`/commerce/${commerce.id}`)}
    >
      <div className="relative h-44 bg-gray-100">
        {commerce.photo_principale ? (
          <img src={commerce.photo_principale} alt={commerce.nom_commercial} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-300">
            <MapPin size={40} />
          </div>
        )}
        {onToggleFavori && (
          <button
            onClick={(e) => { e.stopPropagation(); onToggleFavori(commerce.id) }}
            className="absolute top-3 right-3 w-9 h-9 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-sm"
          >
            <Heart
              size={18}
              className={isFavorited ? 'fill-red-500 text-red-500' : 'text-gray-400'}
            />
          </button>
        )}
        {commerce.is_verified && (
          <div className="absolute top-3 left-3 px-2 py-0.5 bg-white/90 backdrop-blur-sm rounded-full text-[10px] font-medium text-primary-500">
            Verifie
          </div>
        )}
      </div>
      <div className="p-3">
        <div className="flex items-start justify-between mb-1">
          <h3 className="font-semibold text-gray-900 text-sm leading-tight">{commerce.nom_commercial}</h3>
        </div>
        {commerce.categorie && (
          <p className="text-xs text-primary-500 mb-1 font-medium">{commerce.categorie.nom}</p>
        )}
        <StarRating rating={commerce.average_rating} count={commerce.rating_count} />
        {commerce.adresse_complete && (
          <p className="text-xs text-gray-400 flex items-center gap-1 mt-1.5 truncate">
            <MapPin size={10} className="flex-none" />
            {commerce.adresse_complete}
          </p>
        )}
      </div>
    </motion.div>
  )
}

export default CommerceCard
