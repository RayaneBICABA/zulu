// Indicateur visuel de progression : ① ─ ② ─ ③
const Stepper = ({ steps, current }) => (
  <div className="flex items-center justify-center mb-6">
    {steps.map((label, i) => {
      const done = i < current
      const active = i === current
      return (
        <div key={label} className="flex items-center">
          <div className="flex flex-col items-center">
            <div
              className={`w-9 h-9 rounded-full flex items-center justify-center text-sm font-semibold border-2 transition-colors
                ${active
                  ? 'bg-primary-500 border-primary-500 text-white'
                  : done
                  ? 'bg-primary-100 border-primary-500 text-primary-600'
                  : 'bg-white border-gray-300 text-gray-400'}`}
            >
              {done ? '✓' : i + 1}
            </div>
            <span className={`mt-1 text-xs ${active ? 'text-primary-600 font-medium' : 'text-gray-400'}`}>
              {label}
            </span>
          </div>
          {i < steps.length - 1 && (
            <div className={`w-10 h-0.5 mx-1 mb-5 ${done ? 'bg-primary-500' : 'bg-gray-300'}`} />
          )}
        </div>
      )
    })}
  </div>
)

export default Stepper
