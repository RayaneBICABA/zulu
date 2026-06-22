import { motion } from 'framer-motion'

const PageWrapper = ({ children, className = '' }) => (
  <motion.div
    initial={{ opacity: 0, y: 12 }}
    animate={{ opacity: 1, y: 0 }}
    exit={{ opacity: 0, y: -12 }}
    transition={{ duration: 0.2 }}
    className={`min-h-screen bg-gray-50 ${className}`}
  >
    {children}
  </motion.div>
)

export default PageWrapper
