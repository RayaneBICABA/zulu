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
  leftElement,
  rightElement,
  auth = false,
}) => (
  <div className={className}>
    {label && (
      <label htmlFor={name} className="label-field">
        {label}
        {required && <span className="text-primary-500 ml-0.5">*</span>}
      </label>
    )}
    <div className="relative">
      {leftElement && (
        <div className="absolute left-3 top-1/2 -translate-y-1/2 flex items-center pointer-events-none text-primary-400">
          {leftElement}
        </div>
      )}
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
          ${auth ? 'auth-input-field' : 'input-field'}
          ${error ? 'input-field-error border-error/50' : ''}
          ${leftElement ? (auth ? 'pl-10' : 'pl-10') : ''}
          ${rightElement ? 'pr-11' : ''}
        `}
      />
      {rightElement && (
        <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center">
          {rightElement}
        </div>
      )}
    </div>
    {error && (
      <span className="text-xs text-error mt-1.5 flex items-center gap-1">
        <span className="w-1 h-1 rounded-full bg-error inline-block" />
        {error}
      </span>
    )}
  </div>
)

export default Input
