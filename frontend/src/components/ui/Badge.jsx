import { COLORS } from '../../constants/colors'

const variantStyles = {
  primary:   { backgroundColor: COLORS.primary[100],   color: COLORS.primary[500] },
  secondary: { backgroundColor: COLORS.secondary[100], color: COLORS.secondary[500] },
  success:   { backgroundColor: COLORS.successLight,   color: COLORS.success },
  warning:   { backgroundColor: COLORS.warningLight,   color: COLORS.warning },
  error:     { backgroundColor: COLORS.errorLight,     color: COLORS.error },
  gray:      { backgroundColor: COLORS.gray[100],      color: COLORS.gray[600] },
}

const Badge = ({ children, variant = 'primary', className = '' }) => (
  <span
    style={variantStyles[variant]}
    className={`
      inline-flex items-center px-2.5 py-0.5
      rounded-full text-xs font-medium
      ${className}
    `}
  >
    {children}
  </span>
)

export default Badge
