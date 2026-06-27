import { motion } from 'framer-motion'
import PageWrapper from './PageWrapper'

// Mise en page commune des écrans d'authentification : carte centrée sur fond crème.
const AuthLayout = ({ title, subtitle, icon, footer, children }) => (
  <PageWrapper className="min-h-screen flex items-center justify-center px-4 py-10">
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="w-full max-w-md"
    >
      <div className="text-center mb-8">
        {icon && (
          <div className="w-12 h-12 rounded-2xl bg-secondary-500 text-white flex items-center justify-center mx-auto mb-4">
            {icon}
          </div>
        )}
        {title && <h1 className="text-3xl font-bold text-secondary-500">{title}</h1>}
        {subtitle && (
          <p className="mt-2 text-xs font-semibold tracking-widest uppercase text-primary-600">
            {subtitle}
          </p>
        )}
      </div>
      <div className="bg-white rounded-3xl shadow-sm p-6 sm:p-8">{children}</div>
      {footer && <p className="text-center text-sm text-gray-500 mt-6">{footer}</p>}
    </motion.div>
  </PageWrapper>
)

export default AuthLayout
