import { useState } from 'react'
import Input from '../../../components/ui/Input'
import Button from '../../../components/ui/Button'
import { WEEKDAYS, TIME_OPTIONS } from '../constants'

const dayLabel = (key) => WEEKDAYS.find((d) => d.key === key)?.label ?? key

const StepLocation = ({ data, update, errors }) => {
  const [locating, setLocating] = useState(false)
  const [geoError, setGeoError] = useState(null)

  // Saisie d'un nouveau créneau horaire à ajouter.
  const [newDay, setNewDay] = useState('')
  const [newOpen, setNewOpen] = useState('08:00')
  const [newClose, setNewClose] = useState('18:00')

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
        update({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
          accuracy: pos.coords.accuracy,
        })
        setLocating(false)
      },
      () => {
        setGeoError('Impossible de récupérer la position. Autorise la localisation.')
        setLocating(false)
      },
      { enableHighAccuracy: true, timeout: 10000 }
    )
  }

  // Jours pas encore ajoutés → l'artisan ne choisit que parmi ceux qui restent.
  const usedDays = data.hours.map((h) => h.day)
  const availableDays = WEEKDAYS.filter((d) => !usedDays.includes(d.key))

  const addHour = () => {
    const day = newDay || availableDays[0]?.key
    if (!day) return
    update({ hours: [...data.hours, { day, opening_time: newOpen, closing_time: newClose }] })
    setNewDay('')
  }
  const removeHour = (idx) => update({ hours: data.hours.filter((_, i) => i !== idx) })

  const located = data.latitude != null && data.longitude != null

  return (
    <div className="space-y-5">
      <div>
        <label className="text-sm font-medium text-gray-700">
          Localisation GPS <span className="text-primary-500 ml-1">*</span>
        </label>
        <div className="mt-1 p-3 rounded-lg border border-gray-300 bg-gray-50">
          {located ? (
            <div className="text-sm text-secondary-500">
              <p className="font-medium">📍 Position réelle détectée (GPS de l'appareil)</p>
              <p className="text-xs text-gray-500 mt-0.5">
                lat {data.latitude.toFixed(5)}, lng {data.longitude.toFixed(5)}
                {data.accuracy != null && ` · précision ±${Math.round(data.accuracy)} m`}
              </p>
              <a
                href={`https://www.openstreetmap.org/?mlat=${data.latitude}&mlon=${data.longitude}#map=18/${data.latitude}/${data.longitude}`}
                target="_blank"
                rel="noreferrer"
                className="inline-block mt-1 text-xs text-primary-600 hover:underline"
              >
                Voir sur la carte ↗
              </a>
            </div>
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
        <p className="text-xs text-gray-500 mt-0.5">
          Ajoute uniquement les jours et heures où tu es ouvert.
        </p>

        {data.hours.length > 0 && (
          <div className="mt-2 space-y-1.5">
            {data.hours.map((h, i) => (
              <div
                key={i}
                className="flex items-center justify-between bg-gray-50 rounded-lg px-3 py-2 text-sm"
              >
                <span className="text-secondary-500">
                  <span className="font-medium">{dayLabel(h.day)}</span> · {h.opening_time} – {h.closing_time}
                </span>
                <button
                  type="button"
                  onClick={() => removeHour(i)}
                  className="text-xs text-error hover:underline"
                >
                  Retirer
                </button>
              </div>
            ))}
          </div>
        )}

        {availableDays.length > 0 ? (
          <div className="mt-2 p-3 rounded-lg border border-dashed border-gray-300 space-y-2">
            <select
              value={newDay || availableDays[0].key}
              onChange={(e) => setNewDay(e.target.value)}
              className="w-full px-2 py-1.5 rounded border border-gray-300 text-sm bg-white"
            >
              {availableDays.map((d) => (
                <option key={d.key} value={d.key}>
                  {d.label}
                </option>
              ))}
            </select>
            <div className="flex items-center gap-2">
              <select
                value={newOpen}
                onChange={(e) => setNewOpen(e.target.value)}
                className="flex-1 min-w-0 px-2 py-1.5 rounded border border-gray-300 text-sm bg-white"
              >
                {TIME_OPTIONS.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
              <span className="text-gray-400">—</span>
              <select
                value={newClose}
                onChange={(e) => setNewClose(e.target.value)}
                className="flex-1 min-w-0 px-2 py-1.5 rounded border border-gray-300 text-sm bg-white"
              >
                {TIME_OPTIONS.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
              <Button type="button" size="sm" onClick={addHour}>
                Ajouter
              </Button>
            </div>
          </div>
        ) : (
          <p className="mt-2 text-xs text-gray-400 italic">
            Tous les jours de la semaine sont configurés.
          </p>
        )}
      </div>
    </div>
  )
}

export default StepLocation
