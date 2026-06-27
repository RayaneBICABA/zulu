import { motion } from 'framer-motion'
import Spinner from './Spinner'

const sizes = {
  sm: 'h-9 px-3 text-xs',
  md: 'h-12 px-5 text-sm',
  lg: 'h-14 px-6 text-base',
}

const variantClasses = {
  primary: 'text-white font-semibold bg-gradient-to-r from-primary-400 to-primary-600 hover:from-primary-300 hover:to-primary-500 shadow-[var(--shadow-btn)] hover:shadow-[var(--shadow-glow)] hover:-translate-y-0.5',
  secondary: 'bg-surface text-primary-700 font-semibold border border-primary-200 hover:bg-primary-50 hover:border-primary-300 shadow-[var(--shadow-card)]',
  outline: 'border-2 border-primary-400 text-primary-600 font-semibold hover:bg-primary-50',
  ghost: 'bg-transparent text-secondary-600 hover:bg-primary-50',
  danger: 'bg-error text-white font-semibold hover:opacity-90 shadow-sm',
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
    whileTap={{ scale: disabled || loading ? 1 : 0.98 }}
    className={`
      inline-flex items-center justify-center gap-2
      rounded-xl transition-all duration-200
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
