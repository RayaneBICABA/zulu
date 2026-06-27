import { motion } from 'framer-motion'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../constants/routes'
import { API_URL } from '../constants/api'

const SplashScreen = () => {
  const navigate = useNavigate()
  const [ready, setReady] = useState(false)

  useEffect(() => {
    fetch(`${API_URL}/health`).catch(() => {})
    const timer = setTimeout(() => setReady(true), 2800)
    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    if (ready) {
      navigate(ROUTES.login, { replace: true })
    }
  }, [ready, navigate])

  return (
    <div className="fixed inset-0 bg-white flex items-center justify-center">
      <div className="flex flex-col items-center gap-4">
        <motion.img
          src="/logo.png"
          alt="Zawani"
          className="w-28 h-28 object-contain"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{
            duration: 0.9,
            ease: [0.22, 1, 0.36, 1],
          }}
        />

        <motion.img
          src="/zawani.svg"
          alt="Zawani"
          className="h-9 object-contain"
          initial={{ opacity: 0, x: 50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{
            duration: 0.9,
            delay: 0.5,
            ease: [0.22, 1, 0.36, 1],
          }}
        />

        <motion.p
          className="text-gray-400 text-sm tracking-wide mt-2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{
            duration: 0.8,
            delay: 1.0,
          }}
        >
          Trouvez, partagez, connectez.
        </motion.p>

        <motion.div
          className="w-10 h-0.5 bg-primary-500 rounded-full mt-6"
          initial={{ scaleX: 0 }}
          animate={{ scaleX: 1 }}
          transition={{
            duration: 1.4,
            delay: 1.2,
            ease: [0.22, 1, 0.36, 1],
          }}
        />
      </div>
    </div>
  )
}

export default SplashScreen
