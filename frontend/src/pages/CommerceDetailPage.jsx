import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ArrowLeft, MapPin, Phone, MessageCircle, Clock, Heart, Share2, ChevronLeft, ChevronRight, Star } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import commerceService from '../services/commerceService'
import StarRating from '../components/ui/StarRating'
import CommentSection from '../components/ui/CommentSection'

const JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

const CommerceDetailPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { user } = useAuth()

  const [commerce, setCommerce] = useState(null)
  const [rating, setRating] = useState(null)
  const [loading, setLoading] = useState(true)
  const [photoIndex, setPhotoIndex] = useState(0)
  const [isFavorited, setIsFavorited] = useState(false)

  useEffect(() => {
    setLoading(true)
    Promise.all([
      commerceService.getOne(id),
      commerceService.getRating(id).catch(() => null),
    ]).then(([c, r]) => {
      setCommerce(c)
      setRating(r)
      commerceService.recordView(id).catch(() => {})
    }).catch(() => {}).finally(() => setLoading(false))
  }, [id])

  useEffect(() => {
    if (!user || !commerce) return
    commerceService.listFavoris().then((favs) => {
      setIsFavorited(favs.some((f) => f.commerce_id === commerce.id))
    }).catch(() => {})
  }, [user, commerce])

  const handleToggleFavori = async () => {
    if (!user) return navigate('/login')
    try {
      await commerceService.toggleFavori(commerce.id, isFavorited)
      setIsFavorited((p) => !p)
    } catch {}
  }

  const handleShare = async () => {
    try {
      const data = await commerceService.shareWhatsApp(commerce.id)
      if (data.geolocalisation_url) window.open(data.geolocalisation_url, '_blank')
    } catch {}
  }

  const handleCall = () => {
    const phone = commerce?.whatsapp_numero || commerce?.contact_telephonique
    if (phone) window.open(`tel:${phone}`, '_blank')
  }

  const handleWhatsApp = () => {
    const phone = commerce?.whatsapp_numero || commerce?.contact_telephonique
    if (phone) window.open(`https://wa.me/${phone.replace(/[^0-9]/g, '')}`, '_blank')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-white">
        <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
      </div>
    )
  }

  if (!commerce) {
    return (
      <div className="min-h-screen flex flex-col items-center justify-center bg-white px-5">
        <p className="text-gray-400 text-sm mb-4">Commerce introuvable</p>
        <button onClick={() => navigate(-1)} className="text-primary-500 text-sm font-medium">
          Retour
        </button>
      </div>
    )
  }

  const photos = commerce.photos || []
  const horaires = commerce.horaires || []
  const today = new Date().toLocaleDateString('fr-FR', { weekday: 'long' }).toLowerCase()

  return (
    <div className="min-h-screen bg-white pb-8">
      <div className="relative h-64 bg-gray-100">
        {photos.length > 0 ? (
          <>
            <img src={photos[photoIndex]?.url} alt={commerce.nom_commercial} className="w-full h-full object-cover" />
            {photos.length > 1 && (
              <>
                <button onClick={() => setPhotoIndex((p) => (p > 0 ? p - 1 : photos.length - 1))}
                  className="absolute left-3 top-1/2 -translate-y-1/2 w-8 h-8 bg-white/80 rounded-full flex items-center justify-center shadow">
                  <ChevronLeft size={18} />
                </button>
                <button onClick={() => setPhotoIndex((p) => (p < photos.length - 1 ? p + 1 : 0))}
                  className="absolute right-3 top-1/2 -translate-y-1/2 w-8 h-8 bg-white/80 rounded-full flex items-center justify-center shadow">
                  <ChevronRight size={18} />
                </button>
                <div className="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-1.5">
                  {photos.map((_, i) => (
                    <div key={i} className={`w-2 h-2 rounded-full ${i === photoIndex ? 'bg-primary-500' : 'bg-white/60'}`} />
                  ))}
                </div>
              </>
            )}
          </>
        ) : (
          <div className="w-full h-full flex items-center justify-center text-gray-300">
            <MapPin size={50} />
          </div>
        )}
        <button onClick={() => navigate(-1)} className="absolute top-4 left-4 w-9 h-9 bg-white/90 rounded-full flex items-center justify-center shadow">
          <ArrowLeft size={18} />
        </button>
        <div className="absolute top-4 right-4 flex gap-2">
          <button onClick={handleToggleFavori} className="w-9 h-9 bg-white/90 rounded-full flex items-center justify-center shadow">
            <Heart size={18} className={isFavorited ? 'fill-red-500 text-red-500' : 'text-gray-600'} />
          </button>
          <button onClick={handleShare} className="w-9 h-9 bg-white/90 rounded-full flex items-center justify-center shadow">
            <Share2 size={18} className="text-gray-600" />
          </button>
        </div>
      </div>

      <div className="px-5 -mt-4 relative">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-4">
          <div className="flex items-start justify-between mb-2">
            <h1 className="text-lg font-bold text-gray-900">{commerce.nom_commercial}</h1>
            {commerce.is_verified && (
              <span className="px-2 py-0.5 bg-primary-50 text-primary-500 rounded-full text-[10px] font-medium flex-none">
                Verifie
              </span>
            )}
          </div>

          {commerce.categorie && (
            <p className="text-sm text-primary-500 font-medium mb-2">{commerce.categorie.nom}</p>
          )}

          {rating && (
            <div className="mb-3">
              <StarRating rating={rating.average_rating} count={rating.rating_count} size={16} />
            </div>
          )}

          {commerce.description && (
            <p className="text-sm text-gray-500 leading-relaxed mb-4">{commerce.description}</p>
          )}

          <div className="space-y-2">
            {commerce.adresse_complete && (
              <div className="flex items-start gap-2 text-sm text-gray-600">
                <MapPin size={16} className="text-gray-400 mt-0.5 flex-none" />
                <span>{commerce.adresse_complete}</span>
              </div>
            )}
            {commerce.contact_telephonique && (
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Phone size={16} className="text-gray-400 flex-none" />
                <span>{commerce.contact_telephonique}</span>
              </div>
            )}
          </div>
        </div>

        {horaires.length > 0 && (
          <div className="mt-4 bg-white rounded-2xl shadow-sm border border-gray-100 p-4">
            <div className="flex items-center gap-2 mb-3">
              <Clock size={16} className="text-gray-400" />
              <h3 className="text-sm font-semibold text-gray-900">Horaires d'ouverture</h3>
            </div>
            <div className="space-y-1.5">
              {JOURS.map((jour) => {
                const h = horaires.find((hr) => hr.jour === jour)
                const isToday = jour === today
                return (
                  <div key={jour} className={`flex items-center justify-between text-xs ${isToday ? 'font-semibold text-primary-500' : 'text-gray-500'}`}>
                    <span className="capitalize">{jour}</span>
                    {h?.est_ferme ? (
                      <span className="text-gray-400">Ferme</span>
                    ) : h?.est_24h ? (
                      <span className="text-green-600">24h/24</span>
                    ) : h ? (
                      <span>{h.heure_ouverture?.slice(0, 5)} — {h.heure_fermeture?.slice(0, 5)}</span>
                    ) : (
                      <span className="text-gray-300">—</span>
                    )}
                  </div>
                )
              })}
            </div>
          </div>
        )}

        <div className="mt-4 flex gap-3">
          {commerce.contact_telephonique && (
            <button onClick={handleCall} className="flex-1 h-12 bg-gray-100 rounded-xl flex items-center justify-center gap-2 text-sm font-medium text-gray-700">
              <Phone size={16} />
              Appeler
            </button>
          )}
          <button onClick={handleWhatsApp} className="flex-1 h-12 bg-green-500 text-white rounded-xl flex items-center justify-center gap-2 text-sm font-medium">
            <MessageCircle size={16} />
            WhatsApp
          </button>
        </div>

        <div className="mt-6">
          <CommentSection commerceId={commerce.id} />
        </div>
      </div>
    </div>
  )
}

export default CommerceDetailPage
