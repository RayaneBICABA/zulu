import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ROUTES } from '../../../constants/routes'
import PageWrapper from '../../../components/layout/PageWrapper'
import Card from '../../../components/ui/Card'
import Button from '../../../components/ui/Button'
import Stepper from '../components/Stepper'
import StepBusinessInfo from '../components/StepBusinessInfo'
import StepLocation from '../components/StepLocation'
import StepPhotos from '../components/StepPhotos'
import { createBusiness } from '../services/businessService'

const STEPS = ['Commerce', 'Localisation', 'Photos']

const CompleteProfilePage = () => {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [data, setData] = useState({
    business_name: '',
    whatsapp: '',
    category_id: '',
    description: '',
    latitude: null,
    longitude: null,
    accuracy: null,
    address_description: '',
    hours: [],
    photos: [],
  })
  const [errors, setErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [done, setDone] = useState(false)

  // Fusionne un changement partiel dans `data` et efface l'erreur des champs touchés.
  const update = (patch) => {
    setData((prev) => ({ ...prev, ...patch }))
    setErrors((prev) => {
      const next = { ...prev }
      Object.keys(patch).forEach((key) => delete next[key])
      return next
    })
  }

  const validateStep = () => {
    const e = {}
    if (step === 0) {
      if (!data.business_name.trim()) e.business_name = 'Nom requis'
      if (!data.whatsapp.trim()) e.whatsapp = 'Numéro WhatsApp requis'
      if (!data.category_id) e.category_id = 'Choisis un métier'
      if (!data.description.trim()) e.description = 'Description requise'
    }
    if (step === 1) {
      if (data.latitude == null || data.longitude == null) e.location = 'Détecte ta position GPS'
      if (!data.address_description.trim()) e.address_description = 'Adresse requise'
    }
    if (step === 2) {
      if (data.photos.length < 1) e.photos = 'Ajoute au moins 1 photo'
    }
    setErrors(e)
    return Object.keys(e).length === 0
  }

  const next = () => {
    if (validateStep()) setStep((s) => Math.min(s + 1, STEPS.length - 1))
  }
  const back = () => setStep((s) => Math.max(s - 1, 0))

  // Étape valide ? (sans toucher aux erreurs) → sert à activer le bouton Suivant/Enregistrer.
  const isStepComplete = () => {
    if (step === 0)
      return Boolean(
        data.business_name.trim() && data.whatsapp.trim() && data.category_id && data.description.trim()
      )
    if (step === 1)
      return Boolean(data.latitude != null && data.longitude != null && data.address_description.trim())
    if (step === 2) return data.photos.length >= 1
    return false
  }

  // Met les données du formulaire au format attendu par le modèle Business du backend.
  const buildPayload = () => ({
    business_name: data.business_name.trim(),
    whatsapp: data.whatsapp.trim(),
    category_id: Number(data.category_id),
    description: data.description.trim(),
    latitude: data.latitude,
    longitude: data.longitude,
    address_description: data.address_description.trim(),
    hours: data.hours.map((h) => ({ ...h, is_closed: false })),
    // TODO: remplacer `preview` par l'URL renvoyée par l'endpoint d'upload une fois dispo.
    photos: data.photos.map((p, i) => ({ image_url: p.preview, is_primary: i === 0, sort_order: i })),
  })

  const handleSubmit = async () => {
    if (!validateStep()) return
    setSubmitting(true)
    try {
      await createBusiness(buildPayload())
      setDone(true)
    } catch (err) {
      setErrors({ submit: err.message })
    } finally {
      setSubmitting(false)
    }
  }

  if (done) {
    return (
      <PageWrapper className="flex items-center justify-center min-h-screen px-4">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
          <Card padding="lg">
            <div className="text-center">
              <div className="w-12 h-12 rounded-full bg-successLight flex items-center justify-center mx-auto mb-4">
                <svg className="w-6 h-6 text-success" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h1 className="text-xl font-bold text-secondary-500 mb-2">Commerce enregistré</h1>
              <p className="text-sm text-gray-400 mb-6">
                Votre fiche a été créée. Elle sera visible dans l'annuaire une fois publiée.
              </p>
              <Button onClick={() => navigate(ROUTES.home)}>Retour à l'accueil</Button>
            </div>
          </Card>
        </motion.div>
      </PageWrapper>
    )
  }

  return (
    <PageWrapper className="min-h-screen px-4 py-8 flex justify-center">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.3 }}
        className="w-full max-w-md"
      >
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-secondary-500 mb-1">Complétez votre profil !</h1>
          <p className="text-sm text-gray-400">Renseignez votre commerce pour apparaître dans l'annuaire</p>
        </div>

        <Card padding="lg">
          <Stepper steps={STEPS} current={step} />

          {errors.submit && (
            <div className="mb-4 p-3 rounded-lg bg-errorLight text-error text-sm">{errors.submit}</div>
          )}

          {step === 0 && <StepBusinessInfo data={data} update={update} errors={errors} />}
          {step === 1 && <StepLocation data={data} update={update} errors={errors} />}
          {step === 2 && <StepPhotos data={data} update={update} errors={errors} />}

          <div className="mt-6">
            <div className="flex gap-3">
              {step > 0 && (
                <Button variant="ghost" onClick={back} className="flex-1">
                  Précédent
                </Button>
              )}
              {step < STEPS.length - 1 ? (
                <Button onClick={next} disabled={!isStepComplete()} className="flex-1">
                  Suivant
                </Button>
              ) : (
                <Button onClick={handleSubmit} loading={submitting} disabled={!isStepComplete()} className="flex-1">
                  Enregistrer
                </Button>
              )}
            </div>
            {!isStepComplete() && (
              <p className="text-center text-xs text-gray-400 mt-2">
                Renseigne tous les champs pour continuer.
              </p>
            )}
          </div>
        </Card>
      </motion.div>
    </PageWrapper>
  )
}

export default CompleteProfilePage
