import { motion } from 'framer-motion'
import { Star } from 'lucide-react'
import ArtisanBottomNav from '../components/layout/ArtisanBottomNav'

const comments = [
  { id: 1, name: 'Moussa K.', text: 'Très professionnel, mon véhicule est comme neuf. Je recommande sans hésiter.', date: 'Il y a 2h', rating: 5 },
  { id: 2, name: 'Fatou D.', text: 'Excellent travail sur ma tenue de mariage, finitions impeccables.', date: 'Hier', rating: 5 },
  { id: 3, name: 'Salif T.', text: "Bon service mais un peu d'attente. A recommander tout de même.", date: 'Il y a 3 jours', rating: 4 },
]

const ArtisanCommentsPage = () => {
  return (
    <div className="min-h-screen pb-24 max-w-md mx-auto" style={{ background: 'linear-gradient(180deg, #EEF4FF 0%, #F8F9FF 100%)' }}>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="px-5 pt-10">

        {/* Header */}
        <motion.h1 initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="text-3xl font-black text-amber-500 leading-tight mb-6">
          Voir les comments
        </motion.h1>

        {/* Note globale */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.1 }}
          className="bg-white rounded-3xl p-5 shadow-sm border border-blue-50 mb-6"
        >
          <p className="text-xs font-black uppercase tracking-widest text-slate-400 mb-2">Avis clients</p>
          <div className="flex items-center gap-3">
            <span className="text-4xl font-black text-slate-800">4.8</span>
            <div>
              <div className="flex gap-0.5">
                {[1,2,3,4,5].map(s => (
                  <Star key={s} size={16} className="text-amber-400 fill-amber-400" />
                ))}
              </div>
              <p className="text-xs text-slate-400 font-medium mt-1">+142 avis</p>
            </div>
          </div>
        </motion.div>

        {/* Liste commentaires */}
        <div className="space-y-3">
          {comments.map((comment, i) => (
            <motion.div
              key={comment.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 + i * 0.1 }}
              className="bg-white rounded-3xl p-5 shadow-sm border border-blue-50"
            >
              <div className="flex items-center justify-between mb-2">
                <p className="font-bold text-slate-700 text-sm">{comment.name}</p>
                <div className="flex gap-0.5">
                  {[1,2,3,4,5].map(s => (
                    <Star key={s} size={11} className={s <= comment.rating ? 'text-amber-400 fill-amber-400' : 'text-slate-200 fill-slate-200'} />
                  ))}
                </div>
              </div>
              <p className="text-sm text-slate-500 leading-relaxed">{comment.text}</p>
              <p className="text-xs text-slate-300 font-medium mt-3">{comment.date}</p>
            </motion.div>
          ))}
        </div>

      </motion.div>
      <ArtisanBottomNav />
    </div>
  )
}

export default ArtisanCommentsPage
