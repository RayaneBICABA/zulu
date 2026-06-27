import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import logo from '../assets/fasoConnect.png'
import { ROUTES } from '../constants/routes'

export default function SplashScreen() {
  const navigate = useNavigate()

  useEffect(() => {
    const timer = setTimeout(() => navigate(ROUTES.login), 3000)
    return () => clearTimeout(timer)
  }, [navigate])

  return (
    <div className="h-[100dvh] w-full auth-bg flex flex-col items-center justify-center relative overflow-hidden">
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 w-72 h-72 bg-primary-200/50 rounded-full blur-3xl pointer-events-none" />

      <motion.div
        initial={{ opacity: 0, y: 16 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
        className="z-10 flex flex-col items-center px-6"
      >
        <motion.div
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="w-28 h-28 bg-surface rounded-3xl flex items-center justify-center p-6 border border-primary-200 shadow-xl mb-8"
        >
          <img src={logo} alt="Zulu" className="w-full h-full object-contain" />
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
          className="text-4xl sm:text-5xl font-bold tracking-tight text-gradient"
        >
          Zulu
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="text-muted text-sm sm:text-base mt-3 text-center max-w-xs"
        >
          L'annuaire des artisans du Burkina Faso
        </motion.p>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.7 }}
          className="mt-10 w-28 h-1 bg-primary-100 rounded-full overflow-hidden"
        >
          <motion.div
            initial={{ x: '-100%' }}
            animate={{ x: '200%' }}
            transition={{ duration: 1.3, repeat: Infinity, ease: 'easeInOut' }}
            className="h-full w-1/2 rounded-full bg-gradient-to-r from-transparent via-primary-400 to-transparent"
          />
        </motion.div>
      </motion.div>

      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 1 }}
        className="absolute bottom-10 text-xs text-muted px-4 py-2 rounded-full bg-surface/80 border border-secondary-200 backdrop-blur-sm"
      >
        Propulsé par <span className="font-semibold text-primary-600">FasoConnect</span>
      </motion.p>
    </div>
  )
}
