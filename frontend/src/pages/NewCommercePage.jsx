import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ArrowLeft, ArrowRight, MapPin, Camera, Check } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../constants/routes'
import ArtisanBottomNav from '../components/layout/ArtisanBottomNav'

const categories = ['Mécanicien', 'Couturier', 'Coiffeur', 'Soudeur', 'Menuisier', 'Électricien', 'Plombier']

const NewCommercePage = () => {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [photos, setPhotos] = useState([])
  const [form, setForm] = useState({
    name: '', whatsapp: '', category: '', description: '',
    location: '', address: '', openHour: '', closeHour: '',
  })

  const handleChange = (e) => setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))

  const handleLocation = () => {
    navigator.geolocation?.getCurrentPosition(pos => {
      setForm(prev => ({ ...prev, location: `${pos.coords.latitude.toFixed(5)}, ${pos.coords.longitude.toFixed(5)}` }))
    })
  }

  const handlePhoto = () => {
    if (photos.length >= 3) return
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = 'image/*'
    input.onchange = (e) => {
      const url = URL.createObjectURL(e.target.files[0])
      setPhotos(prev => [...prev, url])
    }
    input.click()
  }

  const Field = ({ label, name, placeholder, type = 'text' }) => (
    <div>
      <label className="text-xs font-black text-slate-400 uppercase tracking-wider ml-1">{label}</label>
      <input name={name} type={type} placeholder={placeholder} value={form[name]} onChange={handleChange}
        className="w-full mt-1 h-12 bg-slate-50 border border-blue-50 rounded-2xl px-4 text-sm font-medium text-slate-700 outline-none focus:border-blue-200 shadow-sm" />
    </div>
  )

  return (
    <div className="min-h-screen pb-24 max-w-md mx-auto" style={{ background: 'linear-gradient(180deg, #EEF4FF 0%, #F8F9FF 100%)' }}>
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="px-5 pt-10">

        {/* Header */}
        <div className="flex items-center gap-3 mb-6">
          <motion.button whileTap={{ scale: 0.9 }} onClick={() => step > 1 ? setStep(s => s - 1) : navigate(-1)}
            className="w-10 h-10 bg-white rounded-xl shadow-sm border border-blue-50 flex items-center justify-center">
            <ArrowLeft size={18} className="text-slate-500" />
          </motion.button>
          <h1 className="text-2xl font-black text-amber-500">Nouveau Commerce</h1>
        </div>

        {/* Stepper indicator */}
        <div className="flex items-center gap-2 mb-8">
          {[1, 2, 3].map((s) => (
            <div key={s} className="flex items-center gap-2">
              <motion.div
                animate={{ backgroundColor: s <= step ? '#3B82F6' : '#E2E8F0' }}
                className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-black"
                style={{ color: s <= step ? 'white' : '#94A3B8' }}
              >
                {s < step ? <Check size={14} /> : s}
              </motion.div>
              {s < 3 && <div className={`flex-1 h-1 rounded-full transition-colors ${s < step ? 'bg-blue-400' : 'bg-slate-200'}`} style={{ width: 40 }} />}
            </div>
          ))}
        </div>

        {/* Steps */}
        <AnimatePresence mode="wait">

          {/* STEP 1 */}
          {step === 1 && (
            <motion.div key="step1" initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -40 }} className="space-y-4">
              <p className="text-xs font-black text-blue-400 uppercase tracking-widest mb-2">Informations générales</p>
              <Field label="Nom commercial" name="name" placeholder="Ex: Atelier Soudure Alpha" />
              <Field label="WhatsApp" name="whatsapp" placeholder="+226 XX XX XX XX" />
              <div>
                <label className="text-xs font-black text-slate-400 uppercase tracking-wider ml-1">Catégorie</label>
                <select name="category" value={form.category} onChange={handleChange}
                  className="w-full mt-1 h-12 bg-slate-50 border border-blue-50 rounded-2xl px-4 text-sm font-medium text-slate-700 outline-none focus:border-blue-200 shadow-sm">
                  <option value="">Choisir une catégorie</option>
                  {categories.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-black text-slate-400 uppercase tracking-wider ml-1">Description</label>
                <textarea name="description" value={form.description} onChange={handleChange}
                  placeholder="Décrivez votre activité..."
                  className="w-full mt-1 bg-slate-50 border border-blue-50 rounded-2xl px-4 py-3 text-sm font-medium text-slate-700 outline-none focus:border-blue-200 shadow-sm resize-none h-24" />
              </div>
              <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }} onClick={() => setStep(2)}
                className="w-full h-14 rounded-2xl bg-blue-600 text-white font-black text-sm uppercase tracking-wider shadow-lg flex items-center justify-center gap-2 mt-4">
                Suivant <ArrowRight size={18} />
              </motion.button>
            </motion.div>
          )}

          {/* STEP 2 */}
          {step === 2 && (
            <motion.div key="step2" initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -40 }} className="space-y-4">
              <p className="text-xs font-black text-blue-400 uppercase tracking-widest mb-2">Localisation</p>
              <div>
                <label className="text-xs font-black text-slate-400 uppercase tracking-wider ml-1">Position GPS</label>
                <div className="flex gap-2 mt-1">
                  <input value={form.location} readOnly placeholder="Latitude, Longitude"
                    className="flex-1 h-12 bg-slate-50 border border-blue-50 rounded-2xl px-4 text-sm text-slate-500 shadow-sm" />
                  <motion.button whileTap={{ scale: 0.95 }} onClick={handleLocation}
                    className="w-12 h-12 bg-blue-600 rounded-2xl flex items-center justify-center shadow-md">
                    <MapPin size={18} className="text-white" />
                  </motion.button>
                </div>
              </div>
              <Field label="Description adresse" name="address" placeholder="Ex: Près du marché Rood Woko" />
              <div className="grid grid-cols-2 gap-3">
                <Field label="Ouverture" name="openHour" placeholder="07:00" />
                <Field label="Fermeture" name="closeHour" placeholder="18:00" />
              </div>
              <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }} onClick={() => setStep(3)}
                className="w-full h-14 rounded-2xl bg-blue-600 text-white font-black text-sm uppercase tracking-wider shadow-lg flex items-center justify-center gap-2 mt-4">
                Suivant <ArrowRight size={18} />
              </motion.button>
            </motion.div>
          )}

          {/* STEP 3 */}
          {step === 3 && (
            <motion.div key="step3" initial={{ opacity: 0, x: 40 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -40 }} className="space-y-4">
              <p className="text-xs font-black text-blue-400 uppercase tracking-widest mb-2">Photos (max 3)</p>
              <div className="grid grid-cols-3 gap-3 mb-2">
                {photos.map((p, i) => (
                  <motion.div key={i} initial={{ opacity: 0, scale: 0.8 }} animate={{ opacity: 1, scale: 1 }} className="aspect-square rounded-2xl overflow-hidden shadow-md">
                    <img src={p} alt="" className="w-full h-full object-cover" />
                  </motion.div>
                ))}
              </div>
              {photos.length < 3 && (
                <motion.button whileTap={{ scale: 0.97 }} onClick={handlePhoto}
                  className="w-full h-12 rounded-2xl border-2 border-dashed border-blue-200 bg-blue-50/50 flex items-center justify-center gap-2 text-blue-400 text-sm font-semibold">
                  <Camera size={18} />
                  Ajouter une photo
                </motion.button>
              )}
              <div className="space-y-3 pt-4">
                <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
                  onClick={() => navigate(ROUTES.commerces)}
                  className="w-full h-14 rounded-2xl bg-slate-800 text-white font-black text-sm uppercase tracking-wider shadow-lg">
                  Enregistrer
                </motion.button>
                <motion.button whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.97 }}
                  onClick={() => navigate(ROUTES.commerces)}
                  className="w-full h-14 rounded-2xl bg-white border border-blue-100 text-blue-400 font-black text-sm uppercase tracking-wider shadow-sm">
                  Publier
                </motion.button>
              </div>
            </motion.div>
          )}

        </AnimatePresence>
      </motion.div>
      <ArtisanBottomNav />
    </div>
  )
}

export default NewCommercePage
