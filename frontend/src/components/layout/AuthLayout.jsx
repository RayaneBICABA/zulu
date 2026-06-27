import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import logo from '../../assets/fasoConnect.png'

const AuthLayout = ({ title, subtitle, icon, children, footer }) => (
  <div className="min-h-[100dvh] flex flex-col items-center justify-center auth-bg px-4 py-8 sm:px-5 sm:py-12">
    <div className="absolute inset-0 overflow-hidden pointer-events-none">
      <div className="absolute -top-24 -right-24 w-64 h-64 bg-primary-200/40 rounded-full blur-3xl" />
      <div className="absolute -bottom-32 -left-24 w-72 h-72 bg-primary-100/50 rounded-full blur-3xl" />
    </div>

    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.45, ease: [0.22, 1, 0.36, 1] }}
      className="auth-shell relative z-10"
    >
      {/* En-tête compact */}
      <div className="text-center mb-5 sm:mb-6">
        <Link to="/" className="inline-block group">
          <motion.div
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.96 }}
            className="relative w-14 h-14 mx-auto mb-3"
          >
            <div className="absolute inset-0 rounded-xl bg-primary-200/50 blur-md scale-110 opacity-50 group-hover:opacity-70 transition-opacity" />
            <div className="relative w-full h-full bg-surface rounded-xl flex items-center justify-center border border-primary-100 shadow-sm">
              <img src={logo} alt="Zulu" className="w-8 h-8 object-contain" />
            </div>
          </motion.div>
        </Link>

        {icon && (
          <motion.div
            initial={{ scale: 0.85, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.12, duration: 0.3 }}
            className="auth-icon-badge"
          >
            {icon}
          </motion.div>
        )}

        <h1 className="text-xl sm:text-2xl font-bold text-secondary-600 tracking-tight leading-snug">
          {title}
        </h1>
        {subtitle && (
          <p className="text-muted text-xs sm:text-sm mt-1.5 leading-relaxed px-2">
            {subtitle}
          </p>
        )}
      </div>

      {/* Carte */}
      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.08, duration: 0.35 }}
        className="auth-card-wrap"
      >
        <div className="auth-card-body">
          {children}
        </div>
      </motion.div>

      {footer && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mt-5 text-center text-xs sm:text-sm text-muted px-2"
        >
          {footer}
        </motion.div>
      )}
    </motion.div>
  </div>
)

export default AuthLayout
