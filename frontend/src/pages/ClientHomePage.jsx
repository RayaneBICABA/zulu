import { useState, useEffect, useCallback } from 'react'
import { motion } from 'framer-motion'
import { Search, MapPin, Star, Heart } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import useUserLocation from '../hooks/useUserLocation'
import commerceService from '../services/commerceService'
import PageWrapper from '../components/layout/PageWrapper'

const ClientHomePage = () => {
  const { user } = useAuth()
  const { location: userLocation, loading: locLoading } = useUserLocation()
  const [search, setSearch] = useState('')
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState(null)
  const [commerces, setCommerces] = useState([])
  const [loading, setLoading] = useState(true)
  const [favorites, setFavorites] = useState(new Set())

  useEffect(() => {
    commerceService.listCategories().then(setCategories).catch(() => {})
  }, [])

  const fetchCommerces = useCallback(async () => {
    setLoading(true)
    try {
      const params = { per_page: 50 }
      if (search) params.q = search
      if (selectedCategory) params.categorie_id = selectedCategory
      if (userLocation?.latitude && userLocation?.longitude) {
        params.lat = userLocation.latitude
        params.lng = userLocation.longitude
      }
      const data = await commerceService.listPublic(params)
      setCommerces(data.commerces || [])
    } catch {
      setCommerces([])
    } finally {
      setLoading(false)
    }
  }, [search, selectedCategory, userLocation])

  useEffect(() => {
    fetchCommerces()
  }, [fetchCommerces])

  useEffect(() => {
    commerceService.listFavoris().then((favs) => {
      setFavorites(new Set(favs.map((f) => f.commerce_id)))
    }).catch(() => {})
  }, [])

  const handleToggleFavori = async (commerceId) => {
    const isFavorited = favorites.has(commerceId)
    try {
      await commerceService.toggleFavori(commerceId, isFavorited)
      setFavorites((prev) => {
        const next = new Set(prev)
        isFavorited ? next.delete(commerceId) : next.add(commerceId)
        return next
      })
    } catch {}
  }

  return (
    <PageWrapper className="pb-24">
      <div className="px-5 pt-4">
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-sm text-gray-400">Bienvenue,</p>
              <h1 className="text-xl font-bold text-gray-900">
                {user?.first_name || 'Client'}
              </h1>
            </div>
            {locLoading ? (
              <div className="h-3 w-20 bg-gray-200 rounded animate-pulse" />
            ) : userLocation?.ville ? (
              <div className="flex items-center gap-1 text-xs text-gray-400">
                <MapPin size={12} />
                <span>{userLocation.ville}</span>
                {userLocation.quartier && <span className="text-gray-300">· {userLocation.quartier}</span>}
              </div>
            ) : null}
          </div>
        </motion.div>

        <div className="relative mb-4">
          <Search size={18} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Rechercher un metier ou commerce..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full h-11 pl-10 pr-4 rounded-xl border border-gray-200 text-sm bg-gray-50 focus:outline-none focus:border-primary-500 transition-colors"
          />
        </div>

        <div className="flex gap-2 overflow-x-auto pb-3 -mx-5 px-5 scrollbar-hide">
          <button
            onClick={() => setSelectedCategory(null)}
            className={`flex-none px-4 py-2 rounded-full text-xs font-medium border transition-colors ${
              !selectedCategory
                ? 'bg-primary-500 text-white border-primary-500'
                : 'bg-white text-gray-600 border-gray-200'
            }`}
          >
            Tout
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id === selectedCategory ? null : cat.id)}
              className={`flex-none px-4 py-2 rounded-full text-xs font-medium border transition-colors ${
                selectedCategory === cat.id
                  ? 'bg-primary-500 text-white border-primary-500'
                  : 'bg-white text-gray-600 border-gray-200'
              }`}
            >
              {cat.nom}
            </button>
          ))}
        </div>
      </div>

      <div className="px-5">
        <h2 className="text-sm font-semibold text-gray-900 mb-3">
          {commerces.length} commerce{commerces.length !== 1 ? 's' : ''}
        </h2>

        {loading ? (
          <div className="flex justify-center py-12">
            <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : commerces.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-400 text-sm">Aucun commerce trouve</p>
          </div>
        ) : (
          <div className="space-y-4">
            {commerces.map((c, i) => (
              <motion.div
                key={c.id}
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
                    onClick={() => handleToggleFavori(c.id)}
                    className="absolute top-3 right-3 w-9 h-9 bg-white/90 backdrop-blur-sm rounded-full flex items-center justify-center shadow-sm"
                  >
                    <Heart
                      size={18}
                      className={favorites.has(c.id) ? 'fill-error text-error' : 'text-gray-400'}
                    />
                  </button>
                  {c.is_verified && (
                    <div className="absolute top-3 left-3 px-2 py-0.5 bg-white/90 backdrop-blur-sm rounded-full text-[10px] font-medium text-primary-500">
                      Verifie
                    </div>
                  )}
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
            ))}
          </div>
        )}
      </div>
    </PageWrapper>
  )
}

export default ClientHomePage
