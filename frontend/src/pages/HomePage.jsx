import { motion } from 'framer-motion'
import PageWrapper from '../components/layout/PageWrapper'
import Navbar from '../components/layout/Navbar'
import Button from '../components/ui/Button'
import Card from '../components/ui/Card'
import { Zap, Shield, Smartphone } from 'lucide-react'

const features = [
  { icon: Zap,        title: 'Rapide',  desc: 'Flask + Vite pour un démarrage immédiat.' },
  { icon: Shield,     title: 'Sécurisé', desc: 'JWT auth prêt à l\'emploi.' },
  { icon: Smartphone, title: 'Mobile',  desc: 'Capacitor pour wrapper en app mobile.' },
]

const HomePage = () => (
  <PageWrapper>
    <Navbar />
    <main className="max-w-5xl mx-auto px-4 py-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="text-center mb-16"
      >
        <h1 className="text-4xl font-bold mb-4 text-secondary-500">
          Zulu Starter
        </h1>
        <p className="text-gray-500 text-lg mb-8">
          Base solide pour hackathon &mdash; Flask &middot; React &middot; PostgreSQL &middot; Docker
        </p>
        <Button size="lg">Commencer</Button>
      </motion.div>

      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {features.map(({ icon: Icon, title, desc }, i) => (
          <motion.div
            key={title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <Card hoverable>
              <Icon size={28} className="text-primary-500 mb-3" />
              <h3 className="font-semibold mb-1 text-secondary-500">
                {title}
              </h3>
              <p className="text-sm text-gray-500">{desc}</p>
            </Card>
          </motion.div>
        ))}
      </div>
    </main>
  </PageWrapper>
)

export default HomePage
