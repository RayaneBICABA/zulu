import { useState, useCallback } from 'react'

const useApi = (apiFunc) => {
  const [data,    setData]    = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState(null)

  const execute = useCallback(async (...args) => {
    setLoading(true)
    setError(null)
    try {
      const result = await apiFunc(...args)
      setData(result)
      return result
    } catch (err) {
      setError(err.message || 'Une erreur est survenue')
      throw err
    } finally {
      setLoading(false)
    }
  }, [apiFunc])

  const reset = () => {
    setData(null)
    setError(null)
    setLoading(false)
  }

  return { data, loading, error, execute, reset }
}

export default useApi
