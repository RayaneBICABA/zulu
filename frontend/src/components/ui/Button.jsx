import { motion } from 'framer-motion'
import Spinner from './Spinner'

const sizes = {
  sm: 'px-3 py-1.5 text-sm',
  md: 'px-4 py-2 text-sm',
  lg: 'px-6 py-3 text-base',
}

const variantClasses = {
  primary:
    'bg-primary-500 text-white hover:bg-primary-600 focus:ring-primary-500',
  secondary:
    'bg-secondary-500 text-white hover:bg-secondary-600 focus:ring-secondary-500',
  outline:
    'border-2 border-primary-500 text-primary-500 hover:bg-primary-500 hover:text-white focus:ring-primary-500',
  ghost:
    'bg-transparent text-gray-600 hover:bg-gray-100 focus:ring-gray-400',
  danger:
    'bg-error text-white hover:bg-red-700 focus:ring-error',
}

const Button = ({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  fullWidth = false,
  onClick,
  type = 'button',
  className = '',
}) => (
  <motion.button
    type={type}
    onClick={onClick}
    disabled={disabled || loading}
    whileTap={{ scale: 0.97 }}
    className={`
      inline-flex items-center justify-center gap-2
      rounded-lg font-medium transition-colors duration-200
      focus:outline-none focus:ring-2 focus:ring-offset-2
      disabled:opacity-50 disabled:cursor-not-allowed
      ${variantClasses[variant]}
      ${sizes[size]}
      ${fullWidth ? 'w-full' : ''}
      ${className}
    `}
  >
    {loading && <Spinner size="sm" />}
    {children}
  </motion.button>
)

export default Button
