import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../services/authService'

function Login() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await login(formData.username, formData.password)
      if (response.access_token) {
        localStorage.setItem('token', response.access_token)
        navigate('/dashboard')
      }
    } catch (err) {
      setError('Invalid username or password')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{
      background: '#fff',
      padding: '40px',
      borderRadius: 8,
      maxWidth: 400,
      width: '100%',
      boxShadow: '0 8px 32px rgba(0,0,0,0.2)'
    }}>
      <div style={{ textAlign: 'center', marginBottom: 32 }}>
        <div style={{
          width: 48,
          height: 48,
          borderRadius: 8,
          background: 'linear-gradient(135deg, var(--soil) 50%, var(--twin) 50%)',
          margin: '0 auto 16px'
        }}></div>
        <h2 style={{ fontSize: 24 }}>Digital Twin Farmer</h2>
        <p style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Government of Malawi</p>
      </div>

      <form onSubmit={handleSubmit}>
        {error && (
          <div style={{
            background: '#f8d7da',
            color: '#721c24',
            padding: '12px',
            borderRadius: 4,
            marginBottom: 16,
            fontSize: 14
          }}>
            {error}
          </div>
        )}

        <div style={{ marginBottom: 16 }}>
          <label style={{ display: 'block', fontSize: 14, fontWeight: 600, marginBottom: 6 }}>Username</label>
          <input
            type="text"
            value={formData.username}
            onChange={(e) => setFormData({...formData, username: e.target.value})}
            style={{
              width: '100%',
              padding: '10px 12px',
              border: '1px solid var(--line)',
              borderRadius: 4,
              fontSize: 14
            }}
            required
          />
        </div>

        <div style={{ marginBottom: 24 }}>
          <label style={{ display: 'block', fontSize: 14, fontWeight: 600, marginBottom: 6 }}>Password</label>
          <input
            type="password"
            value={formData.password}
            onChange={(e) => setFormData({...formData, password: e.target.value})}
            style={{
              width: '100%',
              padding: '10px 12px',
              border: '1px solid var(--line)',
              borderRadius: 4,
              fontSize: 14
            }}
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
            padding: '12px',
            background: 'var(--twin)',
            color: '#fff',
            border: 'none',
            borderRadius: 4,
            fontSize: 16,
            fontWeight: 600,
            cursor: 'pointer'
          }}
        >
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  )
}

export default Login