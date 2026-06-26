const MAX_PHOTOS = 3

const StepPhotos = ({ data, update, errors }) => {
  const onSelect = (e) => {
    const files = Array.from(e.target.files || [])
    const room = MAX_PHOTOS - data.photos.length
    // URL.createObjectURL → aperçu local immédiat (l'upload réel viendra avec le backend).
    const next = files.slice(0, room).map((file) => ({ file, preview: URL.createObjectURL(file) }))
    update({ photos: [...data.photos, ...next] })
    e.target.value = ''
  }

  const remove = (idx) => update({ photos: data.photos.filter((_, i) => i !== idx) })

  return (
    <div className="space-y-4">
      <p className="text-sm text-gray-500">
        Ajoute 1 à 3 photos de ton local (la 1ʳᵉ sera la photo principale de l'annuaire).
      </p>

      <div className="grid grid-cols-3 gap-3">
        {data.photos.map((p, i) => (
          <div key={i} className="relative aspect-square rounded-lg overflow-hidden border border-gray-200">
            <img src={p.preview} alt="" className="w-full h-full object-cover" />
            {i === 0 && (
              <span className="absolute top-1 left-1 px-1.5 py-0.5 rounded bg-primary-500 text-white text-[10px]">
                Principale
              </span>
            )}
            <button
              type="button"
              onClick={() => remove(i)}
              className="absolute top-1 right-1 w-5 h-5 rounded-full bg-black/60 text-white text-xs flex items-center justify-center"
            >
              ×
            </button>
          </div>
        ))}

        {data.photos.length < MAX_PHOTOS && (
          <label className="aspect-square rounded-lg border-2 border-dashed border-gray-300 flex flex-col items-center justify-center cursor-pointer hover:border-primary-500 text-gray-400 hover:text-primary-500 transition-colors">
            <span className="text-2xl leading-none">+</span>
            <span className="text-[11px] mt-1">Ajouter</span>
            <input type="file" accept="image/*" multiple className="hidden" onChange={onSelect} />
          </label>
        )}
      </div>

      {errors.photos && <p className="text-xs text-error">{errors.photos}</p>}
    </div>
  )
}

export default StepPhotos
