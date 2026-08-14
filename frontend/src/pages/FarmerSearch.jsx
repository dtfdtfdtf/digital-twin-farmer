import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getFarmers } from '../services/api'

function FarmerSearch() {
  const navigate = useNavigate()
  const [farmers, setFarmers] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchFarmers()
  }, [])

  const fetchFarmers = async () => {
    try {
      const data = await getFarmers()
      setFarmers(data.farmers || [])
    } catch (error) {
      console.error('Error fetching farmers:', error)
    } finally {
      setLoading(false)
    }
  }

  const filteredFarmers = farmers.filter(farmer =>
    farmer.first_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    farmer.last_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    farmer.district?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    farmer.national_id?.includes(searchTerm)
  )

  const handleSelectFarmer = (farmer) => {
    navigate(`/farmers/${farmer.id}/twin`)
  }

  return (
    <div className="wrap">
      <h2 style={{ marginBottom: 8 }}>Find a Farmer's Digital Twin</h2>
      <p style={{ color: 'var(--ink-soft)', marginBottom: 24 }}>
        Search for a farmer to view their complete digital profile
      </p>

      {/* Search Box */}
      <div style={{
        display: 'flex',
        gap: 12,
        marginBottom: 24,
        flexWrap: 'wrap'
      }}>
        <input
          type="text"
          placeholder="Search by name, district, or ID..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          style={{
            flex: 1,
            minWidth: '250px',
            padding: '12px 16px',
            border: '1px solid var(--line)',
            borderRadius: '4px',
            fontSize: '14px'
          }}
        />
        <button
          onClick={() => setSearchTerm('')}
          className="btn btn-outline"
        >
          Clear
        </button>
      </div>

      {/* Results */}
      {loading ? (
        <p>Loading farmers...</p>
      ) : filteredFarmers.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
          <p style={{ color: 'var(--ink-soft)' }}>No farmers found. Register a farmer first.</p>
          <button
            onClick={() => navigate('/farmers')}
            className="btn btn-primary"
            style={{ marginTop: 16 }}
          >
            Go to Farmers → Register
          </button>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: 12 }}>
          {filteredFarmers.map((farmer) => (
            <div
              key={farmer.id}
              className="card"
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                cursor: 'pointer',
                padding: '16px 20px'
              }}
              onClick={() => handleSelectFarmer(farmer)}
            >
              <div>
                <div style={{ fontWeight: 600 }}>
                  {farmer.first_name} {farmer.last_name}
                </div>
                <div style={{ fontSize: 13, color: 'var(--ink-soft)' }}>
                  {farmer.district} · {farmer.national_id}
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
                <span style={{ fontSize: 20, color: 'var(--ink-soft)' }}>→</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default FarmerSearch