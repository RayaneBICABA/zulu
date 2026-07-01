import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import PageWrapper from '../components/layout/PageWrapper'
import Navbar from '../components/layout/Navbar'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { Zap, Shield, Smartphone, Heart, Search, User } from 'lucide-react'
import { ROUTES } from '../constants/routes'

const features = [
  {
    icon: Search,
    title: 'Recherche intelligente',
    desc: 'Trouvez rapidement des commerces et artisans par metier, categorie ou localisation.',
  },
  {
    icon: Heart,
    title: 'Favoris personalises',
    desc: 'Enregistrez vos etablissements preferes pour y revenir plus tard.',
  },
  {
    icon: Shield,
    title: 'Commerces verifies',
    desc: 'Accedez a des profils de commerces controles et des avis transparents.',
  },
  {
    icon: User,
    title: 'Compte securise',
    desc: 'Gestion de profil, mot de passe, verification par email et espace client personnel.',
  },
  {
    icon: Zap,
    title: 'Navigation fluide',
    desc: 'Une experience rapide et moderne, adaptee au mobile et au web.',
  },
  {
    icon: Smartphone,
    title: 'Application hybride',
    desc: 'Disponible sur web et mobile pour rester connecte a tout moment.',
  },
]

const HomePage = () => (
  <PageWrapper>
    <Navbar />
    <main className="max-w-6xl mx-auto px-4 py-16 sm:py-20">
      <div className="grid gap-12 lg:grid-cols-[1.2fr_1fr] items-center">
        <div>
          <motion.h1
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-4xl sm:text-5xl font-extrabold tracking-tight text-slate-900 mb-6"
          >
            Zawani — trouvez et choisissez les meilleurs commerces locaux.
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="text-base sm:text-lg text-slate-600 max-w-xl mb-8"
          >
            Parcourez des artisans et professionnels verifies, sauvegardez vos favoris, consultez des avis reels et gerez votre compte en toute securite.
          </motion.p>

          <div className="flex flex-col gap-4 sm:flex-row sm:items-center">
            <Link to={ROUTES.login}>
              <Button size="lg">Se connecter</Button>
            </Link>
            <Link to={ROUTES.register}>
              <Button variant="outline" size="lg">Creer un compte</Button>
            </Link>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.96 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="rounded-[32px] bg-gradient-to-br from-slate-50 to-white p-8 shadow-xl shadow-slate-200/60 border border-slate-200"
        >
          <div className="grid gap-4">
            {features.slice(0, 3).map(({ icon: Icon, title, desc }) => (
              <div key={title} className="flex gap-4 p-4 rounded-3xl bg-white border border-slate-200">
                <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary-500 text-white">
                  <Icon size={20} />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900">{title}</h3>
                  <p className="text-sm text-slate-500">{desc}</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>
      </div>

      <section className="mt-16">
        <h2 className="text-2xl font-semibold text-slate-900 mb-6">Fonctionnalites principales</h2>
        <div className="grid gap-6 md:grid-cols-2">
          {features.map(({ icon: Icon, title, desc }) => (
            <Card hoverable key={title} className="p-6">
              <div className="flex items-center gap-3 mb-4 text-primary-500">
                <Icon size={24} />
                <h3 className="text-lg font-semibold text-slate-900">{title}</h3>
              </div>
              <p className="text-sm text-slate-600">{desc}</p>
            </Card>
          ))}
        </div>
      </section>

      <section className="mt-16 rounded-[32px] bg-primary-500/5 border border-primary-100 p-8">
        <div className="grid gap-4 sm:grid-cols-2">
          <div>
            <p className="text-sm uppercase tracking-[0.2em] text-primary-500 font-semibold">A propos</p>
            <h3 className="mt-2 text-2xl font-semibold text-slate-900">Une experience de recherche locale simple et moderne</h3>
          </div>
          <p className="text-slate-600 leading-7">
            Zawani aide les clients a trouver des commerçants et artisans de proximite en mettant en avant les profils verifies, les avis, les favorites et un espace client securise. Le tout est accessible sur web via Vercel, et prepare pour integration mobile.
          </p>
        </div>
      </section>
    </main>
  </PageWrapper>
)

export default HomePage
