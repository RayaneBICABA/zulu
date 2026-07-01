import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import PageWrapper from '../components/layout/PageWrapper'
import Navbar from '../components/layout/Navbar'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { Globe, Zap, Shield, Smartphone, Heart, Search, User } from 'lucide-react'
import { ROUTES } from '../constants/routes'

const features = [
  {
    icon: Search,
    title: 'Recherche instantanée',
    desc: 'Trouve le commerce ou l’atelier local en quelques secondes, sans perdre de temps.',
    subtitle: 'Recherche localisée et immédiate pour trouver un commerce en un instant.',
  },
  {
    icon: Heart,
    title: 'Favoris stylés',
    desc: 'Sauvegarde tes coups de cœur et retrouve-les directement dans ton espace.',
    subtitle: 'Garde tes favoris à portée de main pour y revenir rapidement.',
  },
  {
    icon: Shield,
    title: 'Avis transparents',
    desc: 'Des notes claires et des retours réels pour choisir en toute confiance.',
    subtitle: 'Des avis authentiques pour des décisions plus sûres.',
  },
  {
    icon: User,
    title: 'Profil sécurisé',
    desc: 'Ton espace perso garde tes préférences, favoris et commandes à portée de main.',
    subtitle: 'Ton profil organise tout et protège tes préférences.',
  },
  {
    icon: Zap,
    title: 'Interface ultra réactive',
    desc: 'Une appli web fluide, rapide et taillée pour les usages mobiles d’aujourd’hui.',
    subtitle: 'Navigation fluide pour une expérience rapide et naturelle.',
  },
  {
    icon: Smartphone,
    title: '100% responsive',
    desc: 'Fonctionne aussi bien sur desktop que sur mobile.',
    subtitle: 'Accessible sur ordinateur et mobile sans compromis.',
  },
]

const HomePage = () => (
  <PageWrapper>
    <Navbar />
    <main className="max-w-6xl mx-auto px-4 py-16 sm:py-20">
      <div className="grid gap-12 lg:grid-cols-1 items-center">
        <div>
          <motion.h1
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-4xl sm:text-5xl font-extrabold tracking-tight text-slate-950 mb-6"
          >
            Zawani : le logiciel qui dynamise le marché local.
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-base sm:text-lg text-slate-600 max-w-xl mb-8"
          >
            Zawani facilite l’accès aux commerçants et aux artisans de ton quartier, simplifie la gestion des favoris et met en valeur les avis locaux. C’est le changement concret pour le marché local.
          </motion.p>

          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <Link to={ROUTES.login}>
              <Button size="lg">Explorer maintenant</Button>
            </Link>
            <Link to={ROUTES.register}>
              <Button variant="outline" size="lg">Rejoins-nous</Button>
            </Link>
          </div>
        </div>
      </div>

      <section className="mt-16">
        <div className="flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
          <div className="flex items-start gap-4">
            <div className="flex h-24 w-24 items-center justify-center rounded-3xl border border-slate-200 bg-slate-950 text-white shadow-lg">
              <Globe size={38} />
            </div>
            <div>
              <h2 className="text-2xl font-semibold text-slate-950">Ce que Zawani apporte</h2>
              <p className="text-sm text-slate-500 mt-2 max-w-xl">
                Le logiciel offre des outils concrets pour structurer l’offre locale, améliorer la visibilité des commerçants et rendre le marché plus fluide.
              </p>
            </div>
          </div>
        </div>

        <div className="grid gap-6 md:grid-cols-2 mt-8">
          {features.map(({ icon: Icon, title, desc, subtitle }, index) => (
            <Card hoverable key={title} className="p-6 border border-slate-200 bg-white shadow-lg shadow-slate-200/50">
              <div className="flex items-center gap-3 mb-4">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-gradient-to-br from-orange-400 to-pink-500 text-white">
                  <Icon size={24} />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-slate-950">{title}</h3>
                </div>
              </div>
              <p className="text-sm text-slate-600 mb-4">{desc}</p>
              <div className="mt-4 rounded-[28px] border border-slate-200 bg-slate-50 p-5">
                <div className="flex items-center gap-3 text-slate-700">
                  <Icon size={22} className="text-primary-500" />
                  <span className="text-sm">{subtitle}</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </section>

      <section className="mt-16">
        <div className="flex flex-col gap-4 md:flex-row md:items-end md:justify-between mb-6">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-slate-500 font-semibold">Impact local</p>
            <h2 className="mt-2 text-2xl sm:text-3xl font-semibold text-slate-950">Une vraie valeur pour le marché</h2>
          </div>
          <p className="text-sm text-slate-500 max-w-xl">
            Zawani aide les commerçants et artisans à mieux se faire connaître, à attirer des clients et à rendre le commerce local plus visible.
          </p>
        </div>

        <div className="grid gap-4 p-8 rounded-[32px] border border-slate-200 bg-slate-100 min-h-[320px]">
          <div className="rounded-[28px] bg-slate-950 p-8 text-white shadow-lg">
            <div className="mb-6 flex h-16 w-16 items-center justify-center rounded-3xl bg-gradient-to-br from-orange-400 to-pink-500">
              <Globe size={32} />
            </div>
            <h3 className="text-xl font-semibold">Visibilité locale plus forte</h3>
            <p className="mt-3 text-sm text-slate-200">Zawani aide les commerçants à être trouvés et recommandés par leurs voisins.</p>
          </div>
          <div className="grid gap-3 sm:grid-cols-3">
            <div className="rounded-3xl bg-white p-4 text-slate-900 shadow-sm">
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-slate-100 text-primary-500">
                <Search size={20} />
              </div>
              <p className="text-sm font-semibold">Recherche claire</p>
            </div>
            <div className="rounded-3xl bg-white p-4 text-slate-900 shadow-sm">
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-slate-100 text-primary-500">
                <Heart size={20} />
              </div>
              <p className="text-sm font-semibold">Favoris simples</p>
            </div>
            <div className="rounded-3xl bg-white p-4 text-slate-900 shadow-sm">
              <div className="mb-3 inline-flex h-12 w-12 items-center justify-center rounded-3xl bg-slate-100 text-primary-500">
                <Shield size={20} />
              </div>
              <p className="text-sm font-semibold">Avis de confiance</p>
            </div>
          </div>
        </div>
      </section>

      <section className="mt-16 rounded-[32px] bg-primary-500/5 border border-primary-100 p-8">
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-primary-500 font-semibold">Expérience web</p>
            <h3 className="mt-2 text-2xl font-semibold text-slate-900">Adapté au navigateur et au mobile</h3>
          </div>
          <p className="text-slate-600 leading-7">
            Zawani est une plateforme en ligne conçue pour vos recherches de commerces locaux. Une application web légère et responsive qui fonctionne aussi bien sur desktop que sur mobile.
          </p>
        </div>
      </section>
    </main>
  </PageWrapper>
)

export default HomePage
