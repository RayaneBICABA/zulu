import Input from '../../../components/ui/Input'
import { CATEGORIES } from '../constants'

// Style commun (reprend celui de <Input/>) pour le <select> et le <textarea> natifs.
const fieldBase =
  'w-full px-3 py-2 rounded-lg border text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-colors duration-200'

const StepBusinessInfo = ({ data, update, errors }) => (
  <div className="space-y-4">
    <Input
      label="Nom du commerce / de l'artisan"
      name="business_name"
      placeholder="Ex: Élec Sawadogo & Fils"
      value={data.business_name}
      onChange={(e) => update({ business_name: e.target.value })}
      error={errors.business_name}
      required
    />

    <Input
      label="Numéro WhatsApp"
      name="whatsapp"
      placeholder="Ex: +226 70 00 00 00"
      value={data.whatsapp}
      onChange={(e) => update({ whatsapp: e.target.value })}
      error={errors.whatsapp}
      required
    />

    <div className="flex flex-col gap-1">
      <label className="text-sm font-medium text-gray-700">
        Catégorie métier <span className="text-primary-500 ml-1">*</span>
      </label>
      <select
        value={data.category_id}
        onChange={(e) => update({ category_id: e.target.value })}
        className={`${fieldBase} ${errors.category_id ? 'border-error bg-red-50' : 'border-gray-300 bg-white'}`}
      >
        <option value="">— Choisir un métier —</option>
        {CATEGORIES.map((c) => (
          <option key={c.id} value={c.id}>
            {c.icon} {c.name}
          </option>
        ))}
      </select>
      {errors.category_id && <span className="text-xs text-error">{errors.category_id}</span>}
    </div>

    <div className="flex flex-col gap-1">
      <label className="text-sm font-medium text-gray-700">
        Description de l'activité <span className="text-primary-500 ml-1">*</span>
      </label>
      <textarea
        rows={4}
        placeholder="Décrivez vos services en quelques mots..."
        value={data.description}
        onChange={(e) => update({ description: e.target.value })}
        className={`${fieldBase} resize-none ${errors.description ? 'border-error bg-red-50' : 'border-gray-300 bg-white'}`}
      />
      {errors.description && <span className="text-xs text-error">{errors.description}</span>}
    </div>
  </div>
)

export default StepBusinessInfo
