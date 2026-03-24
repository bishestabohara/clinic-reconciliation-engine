import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'x-api-key': import.meta.env.VITE_API_KEY || 'dev-api-key',
  },
})

export async function reconcileMedication(payload) {
  const { data } = await apiClient.post('/api/reconcile/medication', payload)
  return data
}

export async function validateDataQuality(payload) {
  const { data } = await apiClient.post('/api/validate/data-quality', payload)
  return data
}
