// Catégories métier de l'annuaire (mock tant que le backend n'expose pas /categories).
// Les `id` correspondront aux `category_id` attendus par le modèle Business.
export const CATEGORIES = [
  { id: 1, name: 'Mécanicien', icon: '🔧' },
  { id: 2, name: 'Couturier', icon: '🧵' },
  { id: 3, name: 'Coiffeur', icon: '✂️' },
  { id: 4, name: 'Soudeur', icon: '🔩' },
  { id: 5, name: 'Menuisier', icon: '🪚' },
  { id: 6, name: 'Électricien', icon: '💡' },
  { id: 7, name: 'Plombier', icon: '🚿' },
  { id: 8, name: 'Réparateur de téléphones', icon: '📱' },
]

export const WEEKDAYS = [
  { key: 'monday', label: 'Lundi' },
  { key: 'tuesday', label: 'Mardi' },
  { key: 'wednesday', label: 'Mercredi' },
  { key: 'thursday', label: 'Jeudi' },
  { key: 'friday', label: 'Vendredi' },
  { key: 'saturday', label: 'Samedi' },
  { key: 'sunday', label: 'Dimanche' },
]

// Créneaux horaires proposés dans les menus déroulants (toutes les 30 min, format 24h).
export const TIME_OPTIONS = Array.from({ length: 48 }, (_, i) => {
  const h = String(Math.floor(i / 2)).padStart(2, '0')
  const m = i % 2 === 0 ? '00' : '30'
  return `${h}:${m}`
})
