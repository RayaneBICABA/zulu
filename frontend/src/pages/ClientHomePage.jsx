import { useState, useEffect, useCallback } from 'react'
import { motion } from 'framer-motion'
import { Search, MapPin } from 'lucide-react'
import useAuth from '../features/auth/hooks/useAuth'
import commerceService from '../services/commerceService'
import CommerceCard from '../components/ui/CommerceCard'
import PageWrapper from '../components/layout/PageWrapper'

const ClientHomePage = () => {
  const { user } = useAuth()
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
      const data = await commerceService.listPublic(params)
      setCommerces(data.commerces || [])
    } catch {
      setCommerces([])
    } finally {
      setLoading(false)
    }
  }, [search, selectedCategory])

  useEffect(() => {
    const timer = setTimeout(fetchCommerces, search ? 400 : 0)
    return () => clearTimeout(timer)
  }, [fetchCommerces, search])

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
          <p className="text-sm text-gray-400">Bienvenue,</p>
          <h1 className="text-xl font-bold text-gray-900 mb-4">
            {user?.first_name || 'Client'}
          </h1>
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

        <div className="flex gap-2 overflow-x-auto pb-3 -mx-5 px-5" style={{ scrollbarWidth: 'none' }}>
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
        {loading ? (
          <div className="flex justify-center py-12">
            <div className="w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : commerces.length === 0 ? (
          <div className="text-center py-12">
            <MapPin size={40} className="mx-auto text-gray-300 mb-3" />
            <p className="text-gray-400 text-sm">Aucun commerce trouve</p>
          </div>
        ) : (
          <>
            <p className="text-xs text-gray-400 mb-3">
              {commerces.length} commerce{commerces.length !== 1 ? 's' : ''} a proximite
            </p>
            <div className="space-y-4">
              {commerces.map((c, i) => (
                <CommerceCard
                  key={c.id}
                  commerce={c}
                  index={i}
                  isFavorited={favorites.has(c.id)}
                  onToggleFavori={handleToggleFavori}
                />
              ))}
            </div>
          </>
        )}
      </div>
    </PageWrapper>
  )
}

export default ClientHomePage
