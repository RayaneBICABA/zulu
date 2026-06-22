import { motion } from 'framer-motion'

const Card = ({
  children,
  className = '',
  hoverable = false,
  padding = 'md',
}) => {
  const paddings = { sm: 'p-3', md: 'p-5', lg: 'p-8' }

  return (
    <motion.div
      whileHover={hoverable ? { y: -2, boxShadow: '0 8px 30px rgba(0,0,0,0.12)' } : {}}
      className={`
        bg-white rounded-xl border border-gray-200 shadow-sm
        ${paddings[padding]}
        ${hoverable ? 'cursor-pointer transition-shadow duration-200' : ''}
        ${className}
      `}
    >
      {children}
    </motion.div>
  )
}

export default Card
