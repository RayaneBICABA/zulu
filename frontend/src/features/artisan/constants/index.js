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

// Horaires par défaut : ouvert Lun→Sam 08:00-18:00, fermé le dimanche.
// Fonction (et non constante) pour renvoyer un tableau frais à chaque init de formulaire.
export const defaultHours = () =>
  WEEKDAYS.map((d) => ({
    day: d.key,
    opening_time: d.key === 'sunday' ? '' : '08:00',
    closing_time: d.key === 'sunday' ? '' : '18:00',
    is_closed: d.key === 'sunday',
  }))
