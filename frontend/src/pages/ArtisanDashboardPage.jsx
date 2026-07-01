import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Store, Eye, Heart, MessageCircle, Star, MapPin, Share2, Edit3, ExternalLink, Clock } from 'lucide-react'
import commerceService from '../services/commerceService'
import PageWrapper from '../components/layout/PageWrapper'

const StatCard = ({ icon: Icon, label, value, color }) => (
  <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 flex items-center gap-3">
    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${color}`}>
      <Icon size={18} className="text-white" />
    </div>
    <div>
      <p className="text-lg font-bold text-gray-900">{value}</p>
      <p className="text-xs text-gray-400">{label}</p>
    </div>
  </div>
)

const ArtisanDashboardPage = () => {
  const navigate = useNavigate()
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    commerceService.artisanHome().then(setData).catch(() => {})
    setLoading(false)
  }, [])

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

  if (!data) {
    return (
      <PageWrapper>
        <div className="px-5 pt-14">
          <h1 className="text-xl font-bold text-gray-900 mb-2">Mon commerce</h1>
          <p className="text-gray-400 text-sm mb-6">Vous n'avez pas encore de commerce.</p>
          <button
            onClick={() => navigate('/commerce/nouveau')}
            className="w-full py-3 bg-primary-500 text-white rounded-xl font-medium hover:bg-primary-600 transition-colors"
          >
            Creer mon commerce
          </button>
        </div>
      </PageWrapper>
    )
  }

  const { commerce, stats, message } = data
  const statItems = [
    { icon: Eye, label: 'Vues', value: stats?.nb_vues_profile || 0, color: 'bg-blue-500' },
    { icon: Heart, label: 'Favoris', value: stats?.nb_favoris || 0, color: 'bg-red-500' },
    { icon: MessageCircle, label: 'Avis', value: stats?.rating_count || 0, color: 'bg-green-500' },
    { icon: Star, label: 'Note', value: stats?.average_rating ? `${stats.average_rating}/5` : '—', color: 'bg-yellow-500' },
  ]

  return (
    <PageWrapper className="pb-24">
      <div className="px-5 pt-14">
        <motion.div initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between mb-6">
            <div>
              <p className="text-sm text-gray-400">Tableau de bord</p>
              <h1 className="text-xl font-bold text-gray-900">{commerce.nom_commercial}</h1>
            </div>
            <div className="flex items-center gap-1 text-xs">
              <span className={`w-2 h-2 rounded-full ${commerce.is_active ? 'bg-green-500' : 'bg-gray-300'}`} />
              <span className="text-gray-400">{commerce.is_active ? 'Publie' : 'Brouillon'}</span>
            </div>
          </div>
        </motion.div>

        <div className="grid grid-cols-2 gap-3 mb-6">
          {statItems.map((s, i) => (
            <motion.div key={s.label} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.05 }}>
              <StatCard {...s} />
            </motion.div>
          ))}
        </div>

        <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 mb-4">
          <h3 className="text-sm font-semibold text-gray-900 mb-3">Informations</h3>
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-400">Categorie</span>
              <span className="text-gray-700 font-medium">{data.commerce.categorie?.nom || '—'}</span>
            </div>
            {commerce.description && (
              <div className="flex justify-between">
                <span className="text-gray-400">Description</span>
                <span className="text-gray-700 text-right max-w-[200px]">{commerce.description}</span>
              </div>
            )}
            {commerce.adresse_complete && (
              <div className="flex justify-between">
                <span className="text-gray-400">Adresse</span>
                <span className="text-gray-700 text-right max-w-[200px]">{commerce.adresse_complete}</span>
              </div>
            )}
            {commerce.whatsapp_numero && (
              <div className="flex justify-between">
                <span className="text-gray-400">WhatsApp</span>
                <span className="text-gray-700">{commerce.whatsapp_numero}</span>
              </div>
            )}
            {commerce.contact_telephonique && (
              <div className="flex justify-between">
                <span className="text-gray-400">Telephone</span>
                <span className="text-gray-700">{commerce.contact_telephonique}</span>
              </div>
            )}
          </div>
        </div>

        {commerce.horaires?.length > 0 && (
          <div className="bg-white rounded-xl p-4 shadow-sm border border-gray-100 mb-4">
            <div className="flex items-center gap-2 mb-3">
              <Clock size={14} className="text-gray-400" />
              <h3 className="text-sm font-semibold text-gray-900">Horaires</h3>
            </div>
            <div className="space-y-1">
              {commerce.horaires.map((h) => (
                <div key={h.jour} className="flex justify-between text-sm">
                  <span className="text-gray-600 capitalize w-24">{h.jour}</span>
                  {h.est_ferme ? (
                    <span className="text-gray-400">Ferme</span>
                  ) : (
                    <span className="text-gray-700">{h.heure_ouverture} - {h.heure_fermeture}</span>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="flex flex-col gap-2">
          <button
            onClick={() => navigate(`/commerce/${commerce.id}`)}
            className="flex items-center justify-center gap-2 w-full py-3 bg-primary-500 text-white rounded-xl font-medium hover:bg-primary-600 transition-colors"
          >
            <ExternalLink size={16} />
            Voir la fiche publique
          </button>
          <button
            onClick={() => {
              const url = `https://wa.me/${commerce.whatsapp_numero}`
              window.open(url, '_blank')
            }}
            className="flex items-center justify-center gap-2 w-full py-3 bg-green-500 text-white rounded-xl font-medium hover:bg-green-600 transition-colors"
          >
            <Share2 size={16} />
            Partager sur WhatsApp
          </button>
        </div>
      </div>
    </PageWrapper>
  )
}

export default ArtisanDashboardPage