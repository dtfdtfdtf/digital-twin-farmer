import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ==================== FARMER API ====================

export const getFarmers = async (params = {}) => {
  const response = await api.get('/api/farmers', { params })
  return response.data
}

export const getFarmer = async (id) => {
  const response = await api.get(`/api/farmers/${id}`)
  return response.data
}

export const createFarmer = async (data) => {
  const response = await api.post('/api/farmers', data)
  return response.data
}

export const updateFarmer = async (id, data) => {
  const response = await api.put(`/api/farmers/${id}`, data)
  return response.data
}

export const deleteFarmer = async (id) => {
  const response = await api.delete(`/api/farmers/${id}`)
  return response.data
}

// ==================== VERIFICATION API ====================

export const verifyGPS = async (farmerId) => {
  const response = await api.post(`/api/farmers/${farmerId}/verify/gps`)
  return response.data
}

export const verifySatellite = async (farmerId) => {
  const response = await api.post(`/api/farmers/${farmerId}/verify/satellite`)
  return response.data
}

export const verifyOfficer = async (farmerId, officerName) => {
  const response = await api.post(`/api/farmers/${farmerId}/verify/officer`, null, {
    params: { officer_name: officerName }
  })
  return response.data
}

export const verifyCommunity = async (farmerId, verifier) => {
  const response = await api.post(`/api/farmers/${farmerId}/verify/community`, null, {
    params: { verifier }
  })
  return response.data
}

export const verifyHistorical = async (farmerId) => {
  const response = await api.post(`/api/farmers/${farmerId}/verify/historical`)
  return response.data
}

export const runAICheck = async (farmerId) => {
  const response = await api.post(`/api/farmers/${farmerId}/ai-check`)
  return response.data
}

export const getVerificationStatus = async (farmerId) => {
  const response = await api.get(`/api/farmers/${farmerId}/verification-status`)
  return response.data
}

// ==================== HISTORICAL RECORDS API ====================

export const addHistoricalRecord = async (farmerId, data) => {
  const response = await api.post(`/api/farmers/${farmerId}/historical-record`, null, {
    params: data
  })
  return response.data
}

export const getHistoricalRecords = async (farmerId) => {
  const response = await api.get(`/api/farmers/${farmerId}/historical-records`)
  return response.data
}

export const deleteHistoricalRecord = async (recordId) => {
  const response = await api.delete(`/api/historical-record/${recordId}`)
  return response.data
}

// ==================== LOAN API ====================

export const getLoans = async (params = {}) => {
  const response = await api.get('/api/loans', { params })
  return response.data
}

export const createLoan = async (data) => {
  const response = await api.post('/api/loans', data)
  return response.data
}

export const approveLoan = async (id) => {
  const response = await api.post(`/api/loans/${id}/approve`)
  return response.data
}

// ==================== DASHBOARD API ====================

export const getDashboardStats = async () => {
  const response = await api.get('/api/dashboard/stats')
  return response.data
}

// ==================== AI API ====================

export const predictYield = async (farmerId) => {
  const response = await api.get(`/api/ai/predict-yield/${farmerId}`)
  return response.data
}

export const getCreditScore = async (farmerId) => {
  const response = await api.get(`/api/ai/credit-score/${farmerId}`)
  return response.data
}

export const getLoanRecommendation = async (farmerId) => {
  const response = await api.get(`/api/ai/loan-recommendation/${farmerId}`)
  return response.data
}

export default api