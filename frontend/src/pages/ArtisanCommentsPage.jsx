import { motion } from 'framer-motion'
import { Star, Store, User, ChevronLeft } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import ArtisanBottomNav from '../components/layout/ArtisanBottomNav'

const comments = [
  {
    id: 1,
    name: 'Moussa K.',
    text: 'Très professionnel, mon portail a été réparé avant midi. Je recommande sans hésiter.',
    date: 'Il y a 2 h',
  },
  {
    id: 2,
    name: 'Fatou D.',
    text: 'Excellent travail sur ma tenue de mariage. Finition impeccable.',
    date: 'Hier',
  },
  {
    id: 3,
    name: 'Salif T.',
    text: 'Bon service mais un peu d’attente. À recommander tout de même.',
    date: 'Il y a 3 jours',
  },
]

const ArtisanCommentsPage = () => {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-b from-orange-50 via-blue-50 to-slate-50 pb-24">
      <main className="relative mx-auto min-h-screen max-w-lg overflow-hidden px-6 py-7">
        <div
          className="absolute inset-0 opacity-[0.08]"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='84' height='84' viewBox='0 0 84 84' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' stroke='%23d97706' stroke-width='1'%3E%3Cpath d='M8 8h20v20H8zM56 8h20v20H56zM8 56h20v20H8zM56 56h20v20H56zM42 18l10 10-10 10-10-10zM18 42l10 10-10 10L8 52zM66 42l10 10-10 10-10-10z'/%3E%3Cpath d='M0 42h84M42 0v84' opacity='.35'/%3E%3C/g%3E%3C/svg%3E")`,
          }}
        />

        <div className="relative">
          <motion.button
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            onClick={() => navigate(-1)}
            className="mb-5 flex h-10 w-10 items-center justify-center rounded-full bg-white/80 text-orange-500 shadow-md"
          >
            <ChevronLeft size={22} />
          </motion.button>

          <motion.h1
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-5 text-3xl font-extrabold text-orange-500"
          >
            Voir les comments
          </motion.h1>

          <motion.section
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.08 }}
            className="rounded-[2rem] bg-white/92 p-5 shadow-xl ring-1 ring-orange-100"
          >
            <div className="mb-5 flex items-start justify-between">
              <div>
                <p className="text-[10px] font-bold uppercase tracking-wider text-gray-400">
                  Avis clients
                </p>
                <div className="mt-1 flex items-center gap-2">
                  <span className="text-2xl font-black text-gray-900">4.8</span>
                  <div className="flex text-orange-400">
                    {[1, 2, 3, 4, 5].map((star) => (
                      <Star key={star} size={13} fill="currentColor" />
                    ))}
                  </div>
                  <span className="text-[11px] font-medium text-gray-400">120 avis</span>
                </div>
              </div>
              <div className="rounded-2xl bg-orange-50 px-3 py-2 text-right">
                <p className="text-[10px] text-orange-500">Satisfaction</p>
                <p className="text-sm font-bold text-orange-600">98%</p>
              </div>
            </div>

            <div className="space-y-3">
              {comments.map((comment, index) => (
                <motion.article
                  key={comment.id}
                  initial={{ opacity: 0, y: 14 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.14 + index * 0.07 }}
                  className="rounded-2xl bg-slate-50 p-4 shadow-sm ring-1 ring-slate-100"
                >
                  <div className="mb-2 flex items-center justify-between">
                    <p className="text-sm font-bold text-gray-800">{comment.name}</p>
                    <div className="flex text-orange-400">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <Star key={star} size={10} fill="currentColor" />
                      ))}
                    </div>
                  </div>
                  <p className="text-xs leading-relaxed text-gray-600">{comment.text}</p>
                  <p className="mt-3 text-[10px] font-medium text-gray-400">{comment.date}</p>
                </motion.article>
              ))}
            </div>
          </motion.section>

          <div className="mt-6 grid grid-cols-2 gap-3">
            <div className="rounded-2xl bg-white/80 p-4 text-center shadow-md">
              <Store size={20} className="mx-auto mb-2 text-blue-500" />
              <p className="text-xs font-semibold text-gray-500">Commerce actif</p>
            </div>
            <div className="rounded-2xl bg-white/80 p-4 text-center shadow-md">
              <User size={20} className="mx-auto mb-2 text-blue-500" />
              <p className="text-xs font-semibold text-gray-500">Profil vérifié</p>
            </div>
          </div>
        </div>
      </main>

      <ArtisanBottomNav />
    </div>
  )
}

export default ArtisanCommentsPage
