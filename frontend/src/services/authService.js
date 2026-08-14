import api from './api'

export const login = async (username, password) => {
  const response = await api.post('/api/auth/login', { username, password })
  return response.data
}

export const register = async (userData) => {
  const response = await api.post('/api/auth/register', userData)
  return response.data
}

export const logout = () => {
  localStorage.removeItem('token')
}

export const getToken = () => {
  return localStorage.getItem('token')
}

export const isAuthenticated = () => {
  return !!localStorage.getItem('token')
}