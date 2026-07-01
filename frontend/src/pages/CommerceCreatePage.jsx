import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { ROUTES } from '../constants/routes'
import { ArrowLeft, ArrowRight, Check, Upload, MapPin, Clock } from 'lucide-react'
import commerceService from '../services/commerceService'
import useUserLocation from '../hooks/useUserLocation'
import Button from '../components/ui/Button'
import Input from '../components/ui/Input'
import PageWrapper from '../components/layout/PageWrapper'

const JOURS = ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche']

const CommerceCreatePage = () => {
  const navigate = useNavigate()
  const { location: userLocation } = useUserLocation()
  const [step, setStep] = useState(1)
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [commerceId, setCommerceId] = useState(null)

  const [step1, setStep1] = useState({
    nom_commercial: '',
    categorie_id: '',
    description: '',
    whatsapp_numero: '',
    contact_telephonique: '',
    is_vendeur_produits: false,
  })

  const [step2, setStep2] = useState({
    adresse_complete: '',
    latitude: null,
    longitude: null,
    horaires: JOURS.map((j) => ({
      jour: j,
      heure_ouverture: '08:00',
      heure_fermeture: '18:00',
      est_ferme: j === 'dimanche',
      est_24h: false,
    })),
  })

  const [photos, setPhotos] = useState([])
  const [photoPreview, setPhotoPreview] = useState([])

  useEffect(() => {
    commerceService.listCategories().then(setCategories).catch(() => {})
  }, [])

  useEffect(() => {
    if (userLocation) {
      setStep2((prev) => ({
        ...prev,
        latitude: userLocation.latitude,
        longitude: userLocation.longitude,
        adresse_complete: prev.adresse_complete || userLocation.adresse || '',
      }))
    }
  }, [userLocation])

  const handlePhotoChange = (e) => {
    const files = Array.from(e.target.files).slice(0, 3)
    setPhotos(files)
    setPhotoPreview(files.map((f) => URL.createObjectURL(f)))
  }

  const handleStep1 = async () => {
    setError(null)
    setLoading(true)
    try {
      const data = {
        nom_commercial: step1.nom_commercial,
        categorie_id: parseInt(step1.categorie_id),
        description: step1.description || undefined,
        whatsapp_numero: step1.whatsapp_numero || undefined,
        contact_telephonique: step1.contact_telephonique || undefined,
        is_vendeur_produits: step1.is_vendeur_produits,
      }
      const result = await commerceService.create(data)
      setCommerceId(result.id || result.commerce?.id)
      setStep(2)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleStep2 = async () => {
    setError(null)
    setLoading(true)
    try {
      await commerceService.updateLocalisation(commerceId, {
        latitude: step2.latitude,
        longitude: step2.longitude,
        adresse_complete: step2.adresse_complete,
        horaires: step2.horaires,
      })
      setStep(3)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleStep3 = async () => {
    setError(null)
    setLoading(true)
    try {
      if (photos.length > 0) {
        await commerceService.uploadPhotos(commerceId, photos)
      }
      await commerceService.publish(commerceId)
      navigate(ROUTES.home, { replace: true })
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const toggleJourFerme = (index) => {
    setStep2((prev) => ({
      ...prev,
      horaires: prev.horaires.map((h, i) => i === index ? { ...h, est_ferme: !h.est_ferme } : h),
    }))
  }

  const updateHoraire = (index, field, value) => {
    setStep2((prev) => ({
      ...prev,
      horaires: prev.horaires.map((h, i) => i === index ? { ...h, [field]: value } : h),
    }))
  }

  const stepLabels = ['Informations', 'Localisation', 'Photos']

  return (
    <PageWrapper className="min-h-screen bg-white">
      <div className="px-5 pt-14">
        <button onClick={() => step > 1 ? setStep(step - 1) : navigate(-1)} className="mb-4">
          <ArrowLeft size={20} className="text-gray-600" />
        </button>

        <h1 className="text-xl font-bold text-gray-900 mb-1">Nouveau commerce</h1>
        <p className="text-sm text-gray-400 mb-6">Etape {step}/3 — {stepLabels[step - 1]}</p>

        <div className="flex gap-2 mb-6">
          {[1, 2, 3].map((s) => (
            <div key={s} className={`h-1.5 flex-1 rounded-full transition-colors ${s <= step ? 'bg-primary-500' : 'bg-gray-200'}`} />
          ))}
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-lg bg-red-50 text-red-600 text-sm">{error}</div>
        )}

        <AnimatePresence mode="wait">
          {step === 1 && (
            <motion.div key="s1" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
              <Input label="Nom du commerce" value={step1.nom_commercial} onChange={(e) => setStep1({ ...step1, nom_commercial: e.target.value })} required />
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1.5">Categorie</label>
                <select value={step1.categorie_id} onChange={(e) => setStep1({ ...step1, categorie_id: e.target.value })} className="w-full h-11 px-3 rounded-xl border border-gray-200 text-sm bg-gray-50 focus:outline-none focus:border-primary-500">
                  <option value="">Selectionner...</option>
                  {categories.map((c) => <option key={c.id} value={c.id}>{c.nom}</option>)}
                </select>
              </div>
              <Input label="Description" value={step1.description} onChange={(e) => setStep1({ ...step1, description: e.target.value })} placeholder="Decrivez votre activite..." />
              <Input label="WhatsApp" value={step1.whatsapp_numero} onChange={(e) => setStep1({ ...step1, whatsapp_numero: e.target.value })} placeholder="+226 XX XX XX XX" />
              <Input label="Telephone" value={step1.contact_telephonique} onChange={(e) => setStep1({ ...step1, contact_telephonique: e.target.value })} placeholder="+226 XX XX XX XX" />
              <Button onClick={handleStep1} fullWidth loading={loading} disabled={!step1.nom_commercial || !step1.categorie_id}>
                Suivant <ArrowRight size={16} className="ml-1" />
              </Button>
            </motion.div>
          )}

          {step === 2 && (
            <motion.div key="s2" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
              <Input label="Adresse complete" value={step2.adresse_complete} onChange={(e) => setStep2({ ...step2, adresse_complete: e.target.value })} placeholder="Quartier, rue, repere..." required />

              {step2.latitude && (
                <div className="flex items-center gap-2 text-xs text-green-600 bg-green-50 p-3 rounded-xl">
                  <MapPin size={14} />
                  Position GPS detectee automatiquement
                </div>
              )}

              <div>
                <div className="flex items-center gap-2 mb-3">
                  <Clock size={16} className="text-gray-400" />
                  <span className="text-sm font-medium text-gray-700">Horaires</span>
                </div>
                <div className="space-y-2">
                  {step2.horaires.map((h, i) => (
                    <div key={h.jour} className={`flex items-center gap-2 p-2 rounded-xl ${h.est_ferme ? 'bg-gray-50 opacity-60' : 'bg-gray-50'}`}>
                      <span className="text-xs font-medium text-gray-600 w-20 capitalize">{h.jour}</span>
                      {h.est_ferme ? (
                        <span className="text-xs text-gray-400">Ferme</span>
                      ) : (
                        <>
                          <input type="time" value={h.heure_ouverture} onChange={(e) => updateHoraire(i, 'heure_ouverture', e.target.value)} className="text-xs border border-gray-200 rounded-lg px-2 py-1 bg-white" />
                          <span className="text-gray-300">—</span>
                          <input type="time" value={h.heure_fermeture} onChange={(e) => updateHoraire(i, 'heure_fermeture', e.target.value)} className="text-xs border border-gray-200 rounded-lg px-2 py-1 bg-white" />
                        </>
                      )}
                      <button onClick={() => toggleJourFerme(i)} className={`ml-auto text-[10px] px-2 py-1 rounded-lg ${h.est_ferme ? 'bg-gray-200 text-gray-500' : 'bg-primary-50 text-primary-500'}`}>
                        {h.est_ferme ? 'Ouvrir' : 'Fermer'}
                      </button>
                    </div>
                  ))}
                </div>
              </div>

              <Button onClick={handleStep2} fullWidth loading={loading} disabled={!step2.adresse_complete}>
                Suivant <ArrowRight size={16} className="ml-1" />
              </Button>
            </motion.div>
          )}

          {step === 3 && (
            <motion.div key="s3" initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -20 }} className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-gray-700 mb-1.5">Photos du local (1 a 3)</label>
                <label className="flex flex-col items-center justify-center h-40 border-2 border-dashed border-gray-200 rounded-2xl cursor-pointer hover:border-primary-400 transition-colors">
                  <Upload size={24} className="text-gray-300 mb-2" />
                  <span className="text-xs text-gray-400">Appuyez pour ajouter</span>
                  <input type="file" accept="image/*" multiple onChange={handlePhotoChange} className="hidden" />
                </label>
              </div>

              {photoPreview.length > 0 && (
                <div className="flex gap-3">
                  {photoPreview.map((url, i) => (
                    <div key={i} className="relative w-24 h-24 rounded-xl overflow-hidden">
                      <img src={url} alt="" className="w-full h-full object-cover" />
                    </div>
                  ))}
                </div>
              )}

              <div className="bg-primary-50 rounded-xl p-4 text-sm text-primary-700">
                Votre commerce sera publie et visible dans l'annuaire apres validation.
              </div>

              <Button onClick={handleStep3} fullWidth loading={loading}>
                <Check size={16} className="mr-1" /> Publier mon commerce
              </Button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </PageWrapper>
  )
}

export default CommerceCreatePage
