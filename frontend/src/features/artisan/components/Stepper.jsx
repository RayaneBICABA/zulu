// Barre de progression : libellé de l'étape courante + jauge remplie selon l'avancement.
const Stepper = ({ steps, current }) => {
  const pct = ((current + 1) / steps.length) * 100
  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-semibold text-secondary-500">{steps[current]}</span>
        <span className="text-xs text-gray-400">
          Étape {current + 1} sur {steps.length}
        </span>
      </div>
      <div className="h-2 w-full rounded-full bg-gray-200 overflow-hidden">
        <div
          className="h-full rounded-full bg-primary-500 transition-all duration-300"
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}

export default Stepper
