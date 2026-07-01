import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Store, Eye, Heart, MessageCircle, Star, Share2 } from 'lucide-react'
import commerceService from '../services/commerceService'
import PageWrapper from '../components/layout/PageWrapper'

const PRIMARY_VARIANTS = [
  { bg: 'bg-primary-500', light: 'bg-primary-50' },
  { bg: 'bg-primary-600', light: 'bg-primary-100' },
  { bg: 'bg-primary-400', light: 'bg-primary-50' },
  { bg: 'bg-primary-700', light: 'bg-primary-100' },
]

const StatCard = ({ icon: Icon, label, value, variant }) => (
  <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex items-center gap-3">
    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${variant.bg}`}>
      <Icon size={18} className="text-white" />
    </div>
    <div>
      <p className="text-lg font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-400">{label}</p>
    </div>
  </div>
)

const CommerceListItem = ({ item, isSelected, onSelect, data, loadingStats, onDelete, onDraft, onPublish }) => {
  const s = data?.commerce?.stats
  const whatsapp = data?.commerce?.whatsapp_numero
  const statItems = [
    { icon: Eye, label: 'Vues', value: s?.nb_vues_profile ?? '—' },
    { icon: Heart, label: 'Favoris', value: s?.nb_favoris ?? '—' },
    { icon: MessageCircle, label: 'Avis', value: s?.rating_count ?? '—' },
    { icon: Star, label: 'Note', value: s?.average_rating ? `${s.average_rating}/5` : '—' },
  ]

  const handleDelete = () => {
    if (window.confirm(`Supprimer "${item.nom_commercial}" ? Cette action est irreversible.`)) {
      onDelete(item.id)
    }
  }

  return (
    <div>
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        onClick={onSelect}
        className={`bg-white rounded-2xl border overflow-hidden cursor-pointer active:scale-[0.98] transition-all ${
          isSelected ? 'border-primary-500 shadow-md' : 'border-gray-100 shadow-sm'
        }`}
      >
        <div className="flex gap-3 p-3">
          {item.first_image_url ? (
            <div className="w-20 h-20 rounded-xl overflow-hidden flex-none bg-gray-100">
              <img src={item.first_image_url} alt={item.nom_commercial} className="w-full h-full object-cover" />
            </div>
          ) : (
            <div className="w-20 h-20 rounded-xl bg-primary-50 flex items-center justify-center flex-none">
              <Store size={24} className="text-primary-300" />
            </div>
          )}
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h3 className="font-semibold text-sm text-gray-900 truncate">{item.nom_commercial}</h3>
              <span className={`w-2 h-2 rounded-full flex-none ${item.is_active ? 'bg-green-500' : 'bg-gray-300'}`} />
            </div>
            {item.description && (
              <p className="text-xs text-gray-400 mt-0.5 line-clamp-2">{item.description}</p>
            )}
          </div>
        </div>
      </motion.div>

      <AnimatePresence>
        {isSelected && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden"
          >
            <div className="pt-3 pb-2 px-0.5">
              {loadingStats ? (
                <div className="grid grid-cols-2 gap-2">
                  {Array.from({ length: 4 }).map((_, i) => (
                    <div key={i} className="h-16 bg-gray-100 rounded-xl animate-pulse" />
                  ))}
                </div>
              ) : (
                <>
                  <div className="grid grid-cols-2 gap-2 mb-3">
                    {statItems.map((s, i) => (
                      <StatCard key={s.label} {...s} variant={PRIMARY_VARIANTS[i % PRIMARY_VARIANTS.length]} />
                    ))}
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() => {
                        if (whatsapp) window.open(`https://wa.me/${whatsapp.replace(/[^0-9]/g, '')}`, '_blank')
                      }}
                      className="flex-1 h-10 bg-green-500 text-white rounded-xl flex items-center justify-center gap-1.5 text-xs font-medium hover:bg-green-600 transition-colors"
                    >
                      <Share2 size={14} />
                      WhatsApp
                    </button>
                    {item.is_active ? (
                      <button
                        onClick={() => onDraft(item.id)}
                        className="h-10 px-4 bg-primary-100 text-primary-600 rounded-xl text-xs font-medium hover:bg-primary-200 transition-colors"
                      >
                        Brouillon
                      </button>
                    ) : (
                      <button
                        onClick={() => onPublish(item.id)}
                        className="h-10 px-4 bg-green-100 text-green-600 rounded-xl text-xs font-medium hover:bg-green-200 transition-colors"
                      >
                        Publier
                      </button>
                    )}
                    <button
                      onClick={handleDelete}
                      className="h-10 px-4 bg-red-50 text-red-500 rounded-xl text-xs font-medium hover:bg-red-100 transition-colors"
                    >
                      Supprimer
                    </button>
                  </div>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

const ArtisanDashboardPage = () => {
  const navigate = useNavigate()
  const [commerces, setCommerces] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedId, setSelectedId] = useState(null)
  const [selectedStats, setSelectedStats] = useState(null)
  const [loadingStats, setLoadingStats] = useState(false)

  useEffect(() => {
    commerceService.listMyCommerces()
      .then((data) => setCommerces(data.commerces || []))
      .catch(() => setCommerces([]))
      .finally(() => setLoading(false))
  }, [])

  const handleDelete = async (id) => {
    try {
      await commerceService.deleteCommerce(id)
      setCommerces((prev) => prev.filter((c) => c.id !== id))
      if (selectedId === id) {
        setSelectedId(null)
        setSelectedStats(null)
      }
    } catch {}
  }

  const handleDraft = async (id) => {
    try {
      await commerceService.toggleDraft(id)
      setCommerces((prev) => prev.map((c) => c.id === id ? { ...c, is_active: false } : c))
    } catch {}
  }

  const handlePublish = async (id) => {
    try {
      await commerceService.publish(id)
      setCommerces((prev) => prev.map((c) => c.id === id ? { ...c, is_active: true } : c))
    } catch (err) {
      alert(err?.response?.data?.error || "Impossible de publier. Verifie que toutes les etapes sont completes.")
    }
  }

  const handleSelect = async (id) => {
    if (selectedId === id) {
      setSelectedId(null)
      setSelectedStats(null)
      return
    }
    setSelectedId(id)
    setSelectedStats(null)
    setLoadingStats(true)
    try {
      const data = await commerceService.artisanHome(id)
      setSelectedStats(data)
    } catch {
      setSelectedStats(null)
    } finally {
      setLoadingStats(false)
    }
  }

  if (loading) {
    return (
      <PageWrapper>
        <div className="px-5 pt-14 space-y-4">
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-20 bg-gray-200 rounded-xl animate-pulse" />
          ))}
        </div>
      </PageWrapper>
    )
  }

  return (
    <PageWrapper className="pb-24">
      <div className="px-5 pt-14">
        <div className="flex items-center justify-between mb-6">
          <div>
            <p className="text-sm text-gray-400">Mes commerces</p>
            <h1 className="text-xl font-bold text-gray-900">
              {commerces.length} commerce{commerces.length > 1 ? 's' : ''}
            </h1>
          </div>
          <button
            onClick={() => navigate('/commerce/nouveau')}
            className="h-9 px-4 bg-primary-500 text-white rounded-xl text-sm font-medium hover:bg-primary-600 transition-colors"
          >
            + Nouveau
          </button>
        </div>

        {commerces.length === 0 ? (
          <div className="text-center py-16">
            <Store size={48} className="mx-auto text-gray-300 mb-4" />
            <p className="text-gray-400 text-sm mb-6">Vous n'avez pas encore de commerce.</p>
            <button
              onClick={() => navigate('/commerce/nouveau')}
              className="py-3 px-6 bg-primary-500 text-white rounded-xl font-medium hover:bg-primary-600 transition-colors"
            >
              Creer mon commerce
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {commerces.map((item, i) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.05 }}
              >
                <CommerceListItem
                  item={item}
                  isSelected={selectedId === item.id}
                  onSelect={() => handleSelect(item.id)}
                  data={selectedId === item.id ? selectedStats : null}
                  loadingStats={selectedId === item.id && loadingStats}
                  onDelete={handleDelete}
                  onDraft={handleDraft}
                  onPublish={handlePublish}
                />
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </PageWrapper>
  )
}

export default ArtisanDashboardPage