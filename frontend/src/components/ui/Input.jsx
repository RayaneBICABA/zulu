const Input = ({
  label,
  name,
  type = 'text',
  placeholder = '',
  value,
  onChange,
  error,
  disabled = false,
  required = false,
  className = '',
  rightElement,
}) => (
  <div className={`flex flex-col gap-1 ${className}`}>
    {label && (
      <label htmlFor={name}
        className="text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-primary-500 ml-1">*</span>}
      </label>
    )}
    <div className="relative">
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        disabled={disabled}
        required={required}
        className={`
          w-full px-3 py-2 rounded-lg border text-sm
          focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent
          disabled:bg-gray-100 disabled:cursor-not-allowed
          transition-colors duration-200
          ${error
            ? 'border-error bg-red-50'
            : 'border-gray-300 bg-white hover:border-gray-400'}
          ${rightElement ? 'pr-10' : ''}
        `}
      />
      {rightElement && (
        <div className="absolute right-2 top-1/2 -translate-y-1/2 flex items-center">
          {rightElement}
        </div>
      )}
    </div>
    {error && (
      <span className="text-xs text-error">{error}</span>
    )}
  </div>
)

export default Input
