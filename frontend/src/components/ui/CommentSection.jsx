import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Send, Trash2, MessageCircle } from 'lucide-react'
import useAuth from '../../features/auth/hooks/useAuth'
import commerceService from '../../services/commerceService'

const CommentSection = ({ commerceId }) => {
  const { user } = useAuth()
  const [comments, setComments] = useState([])
  const [text, setText] = useState('')
  const [loading, setLoading] = useState(true)
  const [sending, setSending] = useState(false)
  const [submitError, setSubmitError] = useState(null)

  useEffect(() => {
    commerceService.listComments(commerceId)
      .then((data) => setComments(data.commentaires || []))
      .catch((err) => {
        console.error('Erreur chargement commentaires:', err)
        setComments([])
      })
      .finally(() => setLoading(false))
  }, [commerceId])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!text.trim() || sending) return
    setSending(true)
    setSubmitError(null)
    try {
      const result = await commerceService.addComment(commerceId, text.trim())
      setComments((prev) => [result, ...prev])
      setText('')
    } catch (err) {
      setSubmitError(err?.message || 'Erreur lors de l\'envoi du commentaire.')
    }
    finally { setSending(false) }
  }

  const handleDelete = async (commentId) => {
    try {
      await commerceService.deleteComment(commerceId, commentId)
      setComments((prev) => prev.filter((c) => c.id !== commentId))
    } catch (err) {
      console.error('Erreur suppression commentaire:', err)
      setSubmitError('Impossible de supprimer le commentaire.')
    }
  }

  return (
    <div>
      <div className="flex items-center gap-2 mb-3">
        <MessageCircle size={16} className="text-gray-400" />
        <h3 className="text-sm font-semibold text-gray-900">
          Commentaires ({comments.length})
        </h3>
      </div>

      {user && (
        <form onSubmit={handleSubmit} className="flex gap-2 mb-4">
          <input
            type="text"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Ajouter un commentaire..."
            className="flex-1 h-10 px-3 rounded-xl border border-gray-200 text-sm bg-gray-50 focus:outline-none focus:border-primary-500 transition-colors"
          />
          <button
            type="submit"
            disabled={!text.trim() || sending}
            className="w-10 h-10 bg-primary-500 text-white rounded-xl flex items-center justify-center disabled:opacity-40 transition-opacity"
          >
            <Send size={16} />
          </button>
        </form>
      )}

      {submitError && (
        <p className="text-xs text-red-500 mb-3">{submitError}</p>
      )}

      {loading ? (
        <div className="flex justify-center py-6">
          <div className="w-6 h-6 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
        </div>
      ) : comments.length === 0 ? (
        <p className="text-sm text-gray-400 text-center py-6">
          Aucun commentaire pour le moment
        </p>
      ) : (
        <div className="space-y-3">
          <AnimatePresence>
            {comments.map((c) => (
              <motion.div
                key={c.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, height: 0 }}
                className="bg-gray-50 rounded-xl p-3"
              >
                <div className="flex items-start justify-between">
                  <div>
                    <p className="text-xs font-semibold text-gray-900">
                      {c.auteur?.first_name} {c.auteur?.last_name}
                    </p>
                    <p className="text-sm text-gray-600 mt-0.5">{c.contenu}</p>
                  </div>
                  {user && user.id === c.auteur?.id && (
                    <button onClick={() => handleDelete(c.id)} className="text-gray-300 hover:text-red-500 transition-colors">
                      <Trash2 size={14} />
                    </button>
                  )}
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  )
}

export default CommentSection
