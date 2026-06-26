import { useState } from 'react'
import Input from '../../../components/ui/Input'
import Button from '../../../components/ui/Button'
import { WEEKDAYS } from '../constants'

const StepLocation = ({ data, update, errors }) => {
  const [locating, setLocating] = useState(false)
  const [geoError, setGeoError] = useState(null)

  // navigator.geolocation marche en web ET dans Capacitor → aucune adaptation pour le mobile.
  const detectPosition = () => {
    setGeoError(null)
    if (!navigator.geolocation) {
      setGeoError("La géolocalisation n'est pas supportée par cet appareil.")
      return
    }
    setLocating(true)
    navigator.geolocation.getCurrentPosition(
      (pos) => {
        update({ latitude: pos.coords.latitude, longitude: pos.coords.longitude })
        setLocating(false)
      },
      () => {
        setGeoError('Impossible de récupérer la position. Autorise la localisation.')
        setLocating(false)
      },
      { enableHighAccuracy: true, timeout: 10000 }
    )
  }

  const setHour = (idx, patch) => {
    update({ hours: data.hours.map((h, i) => (i === idx ? { ...h, ...patch } : h)) })
  }

  const located = data.latitude != null && data.longitude != null

  return (
    <div className="space-y-5">
      <div>
        <label className="text-sm font-medium text-gray-700">
          Localisation GPS <span className="text-primary-500 ml-1">*</span>
        </label>
        <div className="mt-1 p-3 rounded-lg border border-gray-300 bg-gray-50">
          {located ? (
            <p className="text-sm text-secondary-500">
              📍 Position enregistrée
              <br />
              <span className="text-xs text-gray-500">
                lat {data.latitude.toFixed(5)}, lng {data.longitude.toFixed(5)}
              </span>
            </p>
          ) : (
            <p className="text-sm text-gray-500">Aucune position détectée.</p>
          )}
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="mt-2"
            loading={locating}
            onClick={detectPosition}
          >
            {located ? 'Re-détecter ma position' : 'Détecter ma position'}
          </Button>
          {geoError && <p className="text-xs text-error mt-1">{geoError}</p>}
          {errors.location && <p className="text-xs text-error mt-1">{errors.location}</p>}
        </div>
      </div>

      <Input
        label="Description de l'adresse"
        name="address_description"
        placeholder="Ex: Rue 26.07, Patte d'Oie, près du marché"
        value={data.address_description}
        onChange={(e) => update({ address_description: e.target.value })}
        error={errors.address_description}
        required
      />

      <div>
        <label className="text-sm font-medium text-gray-700">Horaires d'ouverture</label>
        <div className="mt-2 divide-y divide-gray-100">
          {data.hours.map((h, i) => (
            <div key={h.day} className="py-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium text-gray-700">{WEEKDAYS[i].label}</span>
                <button
                  type="button"
                  onClick={() => setHour(i, { is_closed: !h.is_closed })}
                  className="text-xs text-primary-600 hover:underline"
                >
                  {h.is_closed ? 'Fermé · Ouvrir' : 'Ouvert · Fermer'}
                </button>
              </div>
              {!h.is_closed && (
                <div className="flex items-center gap-2 mt-1">
                  <input
                    type="time"
                    value={h.opening_time}
                    onChange={(e) => setHour(i, { opening_time: e.target.value })}
                    className="flex-1 min-w-0 px-2 py-1 rounded border border-gray-300 text-sm"
                  />
                  <span className="text-gray-400">—</span>
                  <input
                    type="time"
                    value={h.closing_time}
                    onChange={(e) => setHour(i, { closing_time: e.target.value })}
                    className="flex-1 min-w-0 px-2 py-1 rounded border border-gray-300 text-sm"
                  />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default StepLocation
