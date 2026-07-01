import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Plus, Pencil, Trash2, X, Check, ArrowLeft } from 'lucide-react'
import apiClient from '../services/apiClient'
import { ENDPOINTS } from '../constants/api'

const AdminCategoriesPage = () => {
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(null)
  const [newNom, setNewNom] = useState('')
  const [editNom, setEditNom] = useState('')
  const navigate = useNavigate()

  const fetch = async () => {
    setLoading(true)
    try {
      const data = await apiClient.get(ENDPOINTS.categories)
      setCategories(Array.isArray(data) ? data : [])
    } catch {
      setCategories([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { fetch() }, [])

  const handleCreate = async () => {
    if (!newNom.trim()) return
    try {
      await apiClient.post(ENDPOINTS.categories, { nom: newNom.trim() })
      setNewNom('')
      fetch()
    } catch {}
  }

  const handleUpdate = async (id) => {
    if (!editNom.trim()) return
    try {
      await apiClient.put(`${ENDPOINTS.categories}/${id}`, { nom: editNom.trim() })
      setEditing(null)
      setEditNom('')
      fetch()
    } catch {}
  }

  const handleDelete = async (id) => {
    if (!confirm('Desactiver cette categorie ?')) return
    try {
      await apiClient.delete(`${ENDPOINTS.categories}/${id}`)
      fetch()
    } catch {}
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-lg mx-auto px-4 py-16">
        <button onClick={() => navigate(-1)} className="mb-4">
          <ArrowLeft size={20} className="text-gray-600" />
        </button>
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Categories</h1>

        <div className="flex gap-2 mb-6">
          <input
            type="text"
            value={newNom}
            onChange={(e) => setNewNom(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleCreate()}
            placeholder="Nouvelle categorie..."
            className="flex-1 h-11 px-4 rounded-xl border border-gray-200 text-sm focus:outline-none focus:border-primary-500"
          />
          <button
            onClick={handleCreate}
            className="h-11 px-4 bg-primary-500 text-white rounded-xl hover:bg-primary-600 transition-colors"
          >
            <Plus size={20} />
          </button>
        </div>

        {loading ? (
          <div className="space-y-3">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded-xl animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="space-y-2">
            {categories.map((cat) => (
              <div key={cat.id} className="bg-white rounded-xl p-4 flex items-center justify-between shadow-sm">
                {editing === cat.id ? (
                  <div className="flex-1 flex items-center gap-2">
                    <input
                      type="text"
                      value={editNom}
                      onChange={(e) => setEditNom(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && handleUpdate(cat.id)}
                      className="flex-1 h-10 px-3 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-primary-500"
                      autoFocus
                    />
                    <button onClick={() => handleUpdate(cat.id)} className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors">
                      <Check size={18} />
                    </button>
                    <button onClick={() => { setEditing(null); setEditNom('') }} className="p-2 text-gray-400 hover:bg-gray-100 rounded-lg transition-colors">
                      <X size={18} />
                    </button>
                  </div>
                ) : (
                  <>
                    <span className="text-sm font-medium text-gray-700">{cat.nom}</span>
                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => { setEditing(cat.id); setEditNom(cat.nom) }}
                        className="p-2 text-gray-400 hover:text-primary-500 hover:bg-primary-50 rounded-lg transition-colors"
                      >
                        <Pencil size={16} />
                      </button>
                      <button
                        onClick={() => handleDelete(cat.id)}
                        className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default AdminCategoriesPage