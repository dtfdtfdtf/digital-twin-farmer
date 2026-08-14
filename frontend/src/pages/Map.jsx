import React, { useState, useEffect } from 'react'
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet'
import 'leaflet/dist/leaflet.css'
import { getFarmers } from '../services/api'
import L from 'leaflet'

// Fix for Leaflet default markers
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
})

// Malawi center coordinates
const MALAWI_CENTER = [-13.5, 34.0]
const MALAWI_BOUNDS = [
  [-17.5, 32.5],
  [-9.0, 36.0]
]

function Map() {
  const [farmers, setFarmers] = useState([])
  const [loading, setLoading] = useState(true)
  const [selectedStatus, setSelectedStatus] = useState('all')

  useEffect(() => {
    fetchFarmers()
  }, [])

  const fetchFarmers = async () => {
    try {
      const data = await getFarmers()
      const farmersWithGPS = (data.farmers || []).filter(
        f => f.latitude && f.longitude && f.status !== 'inactive'
      )
      setFarmers(farmersWithGPS)
    } catch (error) {
      console.error('Error fetching farmers:', error)
    } finally {
      setLoading(false)
    }
  }

  const getMarkerColor = (farmer) => {
    if (farmer.is_verified && farmer.status === 'active') return '#28a745'
    if (farmer.is_verified) return '#17a2b8'
    if (farmer.status === 'pending') return '#ffc107'
    return '#dc3545'
  }

  const getStatusLabel = (farmer) => {
    if (farmer.is_verified && farmer.status === 'active') return '✅ Active & Verified'
    if (farmer.is_verified) return '🔵 Verified'
    if (farmer.status === 'pending') return '⏳ Pending'
    return '🔴 ' + farmer.status
  }

  const filteredFarmers = selectedStatus === 'all'
    ? farmers
    : farmers.filter(f => {
        if (selectedStatus === 'active') return f.is_verified && f.status === 'active'
        if (selectedStatus === 'verified') return f.is_verified
        if (selectedStatus === 'pending') return f.status === 'pending'
        return true
      })

  const statusCounts = {
    all: farmers.length,
    active: farmers.filter(f => f.is_verified && f.status === 'active').length,
    verified: farmers.filter(f => f.is_verified).length,
    pending: farmers.filter(f => f.status === 'pending').length,
  }

  if (loading) {
    return <div className="wrap" style={{ textAlign: 'center', paddingTop: 60 }}>Loading map data...</div>
  }

  if (farmers.length === 0) {
    return (
      <div className="wrap">
        <h2>Farmer Map</h2>
        <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <p style={{ fontSize: 18, color: 'var(--ink-soft)' }}>
            No farmers with GPS coordinates found.
          </p>
          <p style={{ fontSize: 14, color: 'var(--ink-soft)' }}>
            Register a farmer with GPS coordinates to see them on the map.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="wrap">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, flexWrap: 'wrap', gap: 10 }}>
        <div>
          <h2 style={{ marginBottom: 4 }}>Farmer Map</h2>
          <p style={{ color: 'var(--ink-soft)', fontSize: 14 }}>
            {farmers.length} farmers with GPS locations
          </p>
        </div>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
          <button
            onClick={() => setSelectedStatus('all')}
            style={{
              padding: '6px 14px',
              borderRadius: '20px',
              border: selectedStatus === 'all' ? '2px solid var(--twin)' : '1px solid var(--line)',
              background: selectedStatus === 'all' ? 'rgba(31,158,140,0.1)' : 'transparent',
              cursor: 'pointer',
              fontSize: 12,
              fontWeight: selectedStatus === 'all' ? 600 : 400
            }}
          >
            All ({statusCounts.all})
          </button>
          <button
            onClick={() => setSelectedStatus('active')}
            style={{
              padding: '6px 14px',
              borderRadius: '20px',
              border: selectedStatus === 'active' ? '2px solid #28a745' : '1px solid var(--line)',
              background: selectedStatus === 'active' ? 'rgba(40,167,69,0.1)' : 'transparent',
              cursor: 'pointer',
              fontSize: 12,
              color: '#28a745',
              fontWeight: selectedStatus === 'active' ? 600 : 400
            }}
          >
            ✅ Active ({statusCounts.active})
          </button>
          <button
            onClick={() => setSelectedStatus('verified')}
            style={{
              padding: '6px 14px',
              borderRadius: '20px',
              border: selectedStatus === 'verified' ? '2px solid #17a2b8' : '1px solid var(--line)',
              background: selectedStatus === 'verified' ? 'rgba(23,162,184,0.1)' : 'transparent',
              cursor: 'pointer',
              fontSize: 12,
              color: '#17a2b8',
              fontWeight: selectedStatus === 'verified' ? 600 : 400
            }}
          >
            🔵 Verified ({statusCounts.verified})
          </button>
          <button
            onClick={() => setSelectedStatus('pending')}
            style={{
              padding: '6px 14px',
              borderRadius: '20px',
              border: selectedStatus === 'pending' ? '2px solid #ffc107' : '1px solid var(--line)',
              background: selectedStatus === 'pending' ? 'rgba(255,193,7,0.1)' : 'transparent',
              cursor: 'pointer',
              fontSize: 12,
              color: '#856404',
              fontWeight: selectedStatus === 'pending' ? 600 : 400
            }}
          >
            ⏳ Pending ({statusCounts.pending})
          </button>
        </div>
      </div>

      <div style={{
        height: '600px',
        borderRadius: '12px',
        overflow: 'hidden',
        border: '1px solid var(--line)',
        background: '#f0f0f0'
      }}>
        <MapContainer
          center={MALAWI_CENTER}
          zoom={7}
          minZoom={6}
          maxBounds={MALAWI_BOUNDS}
          style={{ height: '100%', width: '100%' }}
          scrollWheelZoom={true}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          
          {filteredFarmers.map((farmer) => (
            <CircleMarker
              key={farmer.id}
              center={[farmer.latitude, farmer.longitude]}
              radius={8}
              fillColor={getMarkerColor(farmer)}
              color="#fff"
              weight={2}
              opacity={1}
              fillOpacity={0.8}
            >
              <Popup>
                <div style={{ minWidth: '200px' }}>
                  <h4 style={{ margin: '0 0 4px 0' }}>
                    {farmer.first_name} {farmer.last_name}
                  </h4>
                  <p style={{ margin: '2px 0', fontSize: '13px' }}>
                    <strong>District:</strong> {farmer.district}
                  </p>
                  <p style={{ margin: '2px 0', fontSize: '13px' }}>
                    <strong>Status:</strong> {getStatusLabel(farmer)}
                  </p>
                  <p style={{ margin: '2px 0', fontSize: '13px' }}>
                    <strong>Credit Score:</strong> {Math.round((farmer.credit_score || 0) / 10)}%
                  </p>
                  <p style={{ margin: '2px 0', fontSize: '13px' }}>
                    <strong>Phone:</strong> {farmer.phone}
                  </p>
                  <a 
                    href={`/farmers/${farmer.id}/twin`}
                    style={{ 
                      color: '#1F9E8C', 
                      textDecoration: 'none',
                      fontSize: '13px',
                      fontWeight: 600
                    }}
                  >
                    View Twin →
                  </a>
                </div>
              </Popup>
            </CircleMarker>
          ))}
        </MapContainer>
      </div>

      <div style={{
        display: 'flex',
        gap: 20,
        marginTop: 16,
        padding: '12px 20px',
        background: '#fff',
        borderRadius: '8px',
        border: '1px solid var(--line)',
        flexWrap: 'wrap'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#28a745' }}></span>
          <span style={{ fontSize: 13 }}>Active & Verified</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#17a2b8' }}></span>
          <span style={{ fontSize: 13 }}>Verified</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#ffc107' }}></span>
          <span style={{ fontSize: 13 }}>Pending</span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
          <span style={{ width: 12, height: 12, borderRadius: '50%', background: '#dc3545' }}></span>
          <span style={{ fontSize: 13 }}>Suspended/Inactive</span>
        </div>
      </div>
    </div>
  )
}

export default Map