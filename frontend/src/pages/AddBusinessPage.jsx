import { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowLeft, Camera, MapPin, Clock, Phone, Info, Store } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../constants/routes'
import Button from '../components/ui/Button'

const categories = [
  { id: 'mecanicien', name: 'Mécanicien' },
  { id: 'couturier', name: 'Couturier' },
  { id: 'coiffeur', name: 'Coiffeur' },
  { id: 'soudeur', name: 'Soudeur' },
  { id: 'menuisier', name: 'Menuisier' },
  { id: 'electricien', name: 'Électricien' },
]

const AddBusinessPage = () => {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [form, setForm] = useState({
    name: '',
    category: '',
    description: '',
    phone: '',
    address: '',
    hours: '',
    latitude: '',
    longitude: '',
  })

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
      navigate(ROUTES.dashboard)
    }, 2000)
  }

  const handleGetLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        setForm(prev => ({
          ...prev,
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
        }))
      })
    }
  }

  return (
    <div className="page-container pb-8">
      <div className="page-inner">
        <div className="profile-header mb-5">
          <motion.header
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            className="relative px-5 sm:px-6 pt-10 sm:pt-12 pb-6 flex items-center gap-3"
          >
            <button onClick={() => navigate(-1)} className="icon-btn bg-surface/80">
              <ArrowLeft size={20} />
            </button>
            <div>
              <h1 className="text-lg sm:text-xl font-bold text-secondary-600">Ajouter un commerce</h1>
              <p className="text-xs text-muted mt-0.5">Enregistrez votre activité sur Zulu</p>
            </div>
          </motion.header>
        </div>

        <main className="px-5 sm:px-6">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="flex gap-3 overflow-x-auto no-scrollbar">
              <button
                type="button"
                className="w-24 h-24 rounded-2xl border-2 border-dashed border-primary-300 bg-primary-50 flex flex-col items-center justify-center text-primary-600 gap-1.5 flex-shrink-0 hover:bg-primary-100 transition-colors active:scale-95"
              >
                <Camera size={22} />
                <span className="text-[10px] font-semibold">Photo</span>
              </button>
            </div>

            <div className="surface-card p-5 sm:p-6 space-y-4 border-l-4 border-l-primary-400">
              {[
                { label: 'Nom du commerce', name: 'name', icon: Store, placeholder: 'Ex: Atelier de Soudure Alpha', required: true },
              ].map((field) => (
                <div key={field.name}>
                  <label className="label-field">{field.label}</label>
                  <div className="relative">
                    <field.icon size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-primary-400" />
                    <input
                      name={field.name}
                      placeholder={field.placeholder}
                      value={form[field.name]}
                      onChange={handleChange}
                      className="input-field pl-10"
                      required={field.required}
                    />
                  </div>
                </div>
              ))}

              <div>
                <label className="label-field">Catégorie</label>
                <select
                  name="category"
                  value={form.category}
                  onChange={handleChange}
                  className="input-field appearance-none cursor-pointer"
                  required
                >
                  <option value="">Sélectionner une catégorie</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.name}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="label-field">Localisation GPS</label>
                <div className="flex flex-col sm:flex-row gap-2">
                  <div className="relative flex-grow">
                    <MapPin size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-primary-400" />
                    <input
                      placeholder="Lat, Long"
                      value={form.latitude ? `${form.latitude.toFixed(4)}, ${form.longitude.toFixed(4)}` : ''}
                      readOnly
                      className="input-field pl-10"
                    />
                  </div>
                  <button type="button" onClick={handleGetLocation} className="btn-secondary px-4 text-xs whitespace-nowrap sm:w-auto w-full">
                    Ma position
                  </button>
                </div>
              </div>

              <div>
                <label className="label-field">Téléphone</label>
                <div className="relative">
                  <Phone size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-primary-400" />
                  <input name="phone" placeholder="+226 XX XX XX XX" value={form.phone} onChange={handleChange} className="input-field pl-10" required />
                </div>
              </div>

              <div>
                <label className="label-field">Horaires</label>
                <div className="relative">
                  <Clock size={15} className="absolute left-3.5 top-1/2 -translate-y-1/2 text-primary-400" />
                  <input name="hours" placeholder="Ex: Lun-Sam, 08h-18h" value={form.hours} onChange={handleChange} className="input-field pl-10" />
                </div>
              </div>

              <div>
                <label className="label-field">Description de l'adresse</label>
                <div className="relative">
                  <Info size={15} className="absolute left-3.5 top-3.5 text-primary-400" />
                  <textarea name="description" placeholder="Ex: Derrière l'école primaire..." value={form.description} onChange={handleChange} rows={3} className="input-field pl-10 h-auto py-3 resize-none" />
                </div>
              </div>
            </div>

            <Button type="submit" fullWidth loading={loading} size="lg">
              Enregistrer mon commerce
            </Button>
          </form>
        </main>
      </div>
    </div>
  )
}

export default AddBusinessPage
