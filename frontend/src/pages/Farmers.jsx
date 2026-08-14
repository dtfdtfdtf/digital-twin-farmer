import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getFarmers, deleteFarmer } from '../services/api'

function Farmers() {
  const navigate = useNavigate()
  const [farmers, setFarmers] = useState([])
  const [loading, setLoading] = useState(true)
  const [deletingId, setDeletingId] = useState(null)

  useEffect(() => {
    fetchFarmers()
  }, [])

  const fetchFarmers = async () => {
    try {
      const data = await getFarmers()
      // Filter out inactive farmers (soft deleted)
      const activeFarmers = (data.farmers || []).filter(f => f.status !== 'inactive')
      setFarmers(activeFarmers)
    } catch (error) {
      console.error('Error fetching farmers:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id, name) => {
    if (!window.confirm(`Are you sure you want to delete ${name}?`)) {
      return
    }

    setDeletingId(id)
    try {
      await deleteFarmer(id)
      // Refresh the list
      await fetchFarmers()
    } catch (error) {
      console.error('Error deleting farmer:', error)
      alert('Failed to delete farmer. Please try again.')
    } finally {
      setDeletingId(null)
    }
  }

  return (
    <div className="wrap">
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 24
      }}>
        <div>
          <h2 style={{ marginBottom: 4 }}>Farmers</h2>
          <p style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Manage registered farmers</p>
        </div>
        <button
          onClick={() => navigate('/farmers/add')}
          className="btn btn-primary"
        >
          + Register Farmer
        </button>
      </div>

      {loading ? (
        <p>Loading farmers...</p>
      ) : farmers.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
          <p style={{ color: 'var(--ink-soft)' }}>No farmers registered yet.</p>
          <button
            onClick={() => navigate('/farmers/add')}
            className="btn btn-primary"
            style={{ marginTop: 16 }}
          >
            Register Your First Farmer
          </button>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: 12 }}>
          {farmers.map((farmer) => (
            <div
              key={farmer.id}
              className="card"
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                padding: '16px 20px'
              }}
            >
              <div>
                <div style={{ fontWeight: 600 }}>
                  {farmer.first_name} {farmer.last_name}
                </div>
                <div style={{ fontSize: 13, color: 'var(--ink-soft)' }}>
                  {farmer.district} · {farmer.phone}
                </div>
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                <span style={{
                  fontSize: 12,
                  padding: '4px 12px',
                  borderRadius: '20px',
                  background: farmer.is_verified ? 'rgba(31,158,140,0.15)' : 'rgba(168,72,28,0.15)',
                  color: farmer.is_verified ? 'var(--twin)' : 'var(--soil)'
                }}>
                  {farmer.is_verified ? 'Verified' : 'Pending'}
                </span>
                <span style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color: 'var(--twin)'
                }}>
                  {Math.round((farmer.credit_score || 0) / 10)}%
                </span>
                <Link
                  to={`/farmers/${farmer.id}/twin`}
                  style={{
                    fontSize: 13,
                    color: 'var(--twin)',
                    textDecoration: 'none'
                  }}
                >
                  View Twin →
                </Link>
                <button
                  onClick={() => handleDelete(farmer.id, `${farmer.first_name} ${farmer.last_name}`)}
                  disabled={deletingId === farmer.id}
                  style={{
                    background: 'var(--danger)',
                    color: '#fff',
                    border: 'none',
                    padding: '4px 12px',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontSize: 12,
                    opacity: deletingId === farmer.id ? 0.5 : 1
                  }}
                >
                  {deletingId === farmer.id ? '...' : 'Delete'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default Farmers