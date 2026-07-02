import { useState, useEffect } from 'react'

const STORAGE_KEY = 'zawani_location'

const useUserLocation = () => {
  const [location, setLocation] = useState(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      return stored ? JSON.parse(stored) : null
    } catch { return null }
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!navigator.geolocation) { setLoading(false); return }

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude } = pos.coords
        const loc = { latitude, longitude, adresse: '' }

        try {
          const res = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&accept-language=fr`,
            { headers: { 'User-Agent': 'ZawaniApp/1.0' } }
          )
          const data = await res.json()
          loc.adresse = data.display_name?.split(',')?.slice(0, 3)?.join(',') || ''
          loc.ville = data.address?.city || data.address?.town || data.address?.village || ''
          loc.quartier = data.address?.suburb || data.address?.neighbourhood || ''
        } catch {}

        localStorage.setItem(STORAGE_KEY, JSON.stringify(loc))
        setLocation(loc)
        setLoading(false)
      },
      () => { setLoading(false) },
      { enableHighAccuracy: true, timeout: 10000 }
    )
  }, [])

  return { location, loading }
}

export default useUserLocation