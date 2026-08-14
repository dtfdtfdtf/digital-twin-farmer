import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createFarmer } from '../services/api'

function AddFarmer() {
  const navigate = useNavigate()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    middle_name: '',
    phone: '',
    alternative_phone: '',
    national_id: '',
    gender: '',
    date_of_birth: '',
    village: '',
    district: '',
    region: '',
    traditional_authority: '',
    latitude: '',
    longitude: '',
    farm_area_hectares: ''
  })

  const regions = ['Northern', 'Central', 'Southern']

  const districts = {
    'Northern': ['Chitipa', 'Karonga', 'Likoma', 'Mzimba', 'Nkhata Bay', 'Rumphi'],
    'Central': ['Dedza', 'Dowa', 'Kasungu', 'Lilongwe', 'Mchinji', 'Nkhotakota', 'Ntcheu', 'Ntchisi', 'Salima'],
    'Southern': ['Balaka', 'Blantyre', 'Chikwawa', 'Chiradzulu', 'Machinga', 'Mangochi', 'Mulanje', 'Mwanza', 'Neno', 'Nsanje', 'Phalombe', 'Thyolo', 'Zomba']
  }

  // Malawi boundaries
  const MALAWI_BOUNDS = {
    minLat: -17.5,
    maxLat: -9.0,
    minLng: 32.5,
    maxLng: 36.0
  }

  // Region-specific approximate boundaries
  const REGION_BOUNDS = {
    'Northern': { minLat: -12.0, maxLat: -9.0, minLng: 33.0, maxLng: 35.5 },
    'Central': { minLat: -15.0, maxLat: -12.0, minLng: 33.0, maxLng: 35.0 },
    'Southern': { minLat: -17.5, maxLat: -15.0, minLng: 34.0, maxLng: 36.0 }
  }

  const validatePhone = (phone) => {
    return /^[0-9]{10}$/.test(phone)
  }

  const validateGPS = (lat, lng, region) => {
    if (!lat || !lng) return true // Allow empty fields (optional)
    
    const latNum = parseFloat(lat)
    const lngNum = parseFloat(lng)
    
    // Check if within Malawi
    if (latNum < MALAWI_BOUNDS.minLat || latNum > MALAWI_BOUNDS.maxLat ||
        lngNum < MALAWI_BOUNDS.minLng || lngNum > MALAWI_BOUNDS.maxLng) {
      return { valid: false, message: 'Coordinates must be within Malawi' }
    }
    
    // Check if within region
    if (region && REGION_BOUNDS[region]) {
      const bounds = REGION_BOUNDS[region]
      if (latNum < bounds.minLat || latNum > bounds.maxLat ||
          lngNum < bounds.minLng || lngNum > bounds.maxLng) {
        return { valid: false, message: `Coordinates must be within the ${region} region` }
      }
    }
    
    return { valid: true, message: '' }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Validate phone
    if (!validatePhone(formData.phone)) {
      setError('Phone number must be exactly 10 digits (e.g., 0888123456)')
      setLoading(false)
      return
    }

    // Validate alternative phone (if provided)
    if (formData.alternative_phone && !validatePhone(formData.alternative_phone)) {
      setError('Alternative phone number must be exactly 10 digits')
      setLoading(false)
      return
    }

    // Validate GPS within region
    if (formData.latitude && formData.longitude) {
      const gpsValidation = validateGPS(formData.latitude, formData.longitude, formData.region)
      if (!gpsValidation.valid) {
        setError(gpsValidation.message)
        setLoading(false)
        return
      }
    }

    try {
      const data = {
        ...formData,
        latitude: formData.latitude ? parseFloat(formData.latitude) : null,
        longitude: formData.longitude ? parseFloat(formData.longitude) : null,
        farm_area_hectares: formData.farm_area_hectares ? parseFloat(formData.farm_area_hectares) : null,
        date_of_birth: formData.date_of_birth ? new Date(formData.date_of_birth).toISOString() : null
      }

      console.log('📤 Sending data:', data)

      const response = await createFarmer(data)
      navigate('/farmers')
    } catch (err) {
      console.error('❌ Error:', err)
      console.error('❌ Response:', err.response?.data)
      setError(err.response?.data?.detail || 'Failed to register farmer. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="wrap">
      <div style={{ maxWidth: 700, margin: '0 auto' }}>
        <h2 style={{ marginBottom: 4 }}>Register New Farmer</h2>
        <p style={{ color: 'var(--ink-soft)', marginBottom: 24 }}>
          Enter the farmer's details to create their Digital Twin profile
        </p>

        {error && (
          <div style={{
            background: '#f8d7da',
            color: '#721c24',
            padding: '12px 16px',
            borderRadius: 4,
            marginBottom: 16,
            border: '1px solid #f5c6cb'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="card">
          {/* Personal Information */}
          <h4 style={{ fontSize: 14, marginBottom: 12, color: 'var(--soil)' }}>Personal Information</h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>First Name *</label>
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                required
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              />
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Last Name *</label>
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                required
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              />
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Middle Name</label>
              <input
                type="text"
                name="middle_name"
                value={formData.middle_name}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              />
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Gender</label>
              <select
                name="gender"
                value={formData.gender}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              >
                <option value="">Select</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Date of Birth</label>
              <input
                type="date"
                name="date_of_birth"
                value={formData.date_of_birth}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              />
            </div>
          </div>

          {/* Contact & ID */}
          <h4 style={{ fontSize: 14, marginTop: 16, marginBottom: 12, color: 'var(--soil)' }}>Contact & Identification</h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Phone *</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleChange}
                required
                maxLength="10"
                placeholder="0888123456"
                style={{ 
                  width: '100%', 
                  padding: '8px 12px', 
                  border: `1px solid ${formData.phone && !validatePhone(formData.phone) ? 'var(--danger)' : 'var(--line)'}`,
                  borderRadius: 4 
                }}
              />
              {formData.phone && !validatePhone(formData.phone) && (
                <div style={{ fontSize: 12, color: 'var(--danger)', marginTop: 4 }}>
                  Phone must be exactly 10 digits
                </div>
              )}
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Alternative Phone</label>
              <input
                type="tel"
                name="alternative_phone"
                value={formData.alternative_phone}
                onChange={handleChange}
                maxLength="10"
                placeholder="0999123456"
                style={{ 
                  width: '100%', 
                  padding: '8px 12px', 
                  border: `1px solid ${formData.alternative_phone && !validatePhone(formData.alternative_phone) ? 'var(--danger)' : 'var(--line)'}`,
                  borderRadius: 4 
                }}
              />
              {formData.alternative_phone && !validatePhone(formData.alternative_phone) && (
                <div style={{ fontSize: 12, color: 'var(--danger)', marginTop: 4 }}>
                  Alternative phone must be exactly 10 digits
                </div>
              )}
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>National ID *</label>
              <input
                type="text"
                name="national_id"
                value={formData.national_id}
                onChange={handleChange}
                required
                placeholder="AB123456789"
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              />
            </div>
          </div>

          {/* Location */}
          <h4 style={{ fontSize: 14, marginTop: 16, marginBottom: 12, color: 'var(--soil)' }}>Location</h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Region *</label>
              <select
                name="region"
                value={formData.region}
                onChange={handleChange}
                required
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              >
                <option value="">Select Region</option>
                {regions.map(r => <option key={r} value={r}>{r}</option>)}
              </select>
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>District *</label>
              <select
                name="district"
                value={formData.district}
                onChange={handleChange}
                required
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              >
                <option value="">Select District</option>
                {formData.region && districts[formData.region]?.map(d => (
                  <option key={d} value={d}>{d}</option>
                ))}
              </select>
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Village *</label>
              <input
                type="text"
                name="village"
                value={formData.village}
                onChange={handleChange}
                required
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              />
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Traditional Authority</label>
              <input
                type="text"
                name="traditional_authority"
                value={formData.traditional_authority}
                onChange={handleChange}
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              />
            </div>
          </div>

          {/* Farm Details with GPS Validation */}
          <h4 style={{ fontSize: 14, marginTop: 16, marginBottom: 12, color: 'var(--soil)' }}>Farm Details</h4>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12 }}>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Latitude</label>
              <input
                type="number"
                name="latitude"
                value={formData.latitude}
                onChange={handleChange}
                step="any"
                placeholder="-13.9833"
                style={{ 
                  width: '100%', 
                  padding: '8px 12px', 
                  border: `1px solid ${formData.latitude && formData.longitude && formData.region ? 
                    (validateGPS(formData.latitude, formData.longitude, formData.region).valid ? 'var(--twin)' : 'var(--danger)') 
                    : 'var(--line)'}`,
                  borderRadius: 4 
                }}
              />
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Longitude</label>
              <input
                type="number"
                name="longitude"
                value={formData.longitude}
                onChange={handleChange}
                step="any"
                placeholder="33.7833"
                style={{ 
                  width: '100%', 
                  padding: '8px 12px', 
                  border: `1px solid ${formData.latitude && formData.longitude && formData.region ? 
                    (validateGPS(formData.latitude, formData.longitude, formData.region).valid ? 'var(--twin)' : 'var(--danger)') 
                    : 'var(--line)'}`,
                  borderRadius: 4 
                }}
              />
            </div>
            <div>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Farm Area (ha)</label>
              <input
                type="number"
                name="farm_area_hectares"
                value={formData.farm_area_hectares}
                onChange={handleChange}
                step="0.1"
                placeholder="2.5"
                style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
              />
            </div>
          </div>
          
          {/* GPS Validation Message */}
          {formData.latitude && formData.longitude && formData.region && (
            <div style={{ marginTop: 8 }}>
              {(() => {
                const result = validateGPS(formData.latitude, formData.longitude, formData.region)
                return result.valid ? (
                  <div style={{ fontSize: 12, color: 'var(--twin)' }}>
                    ✅ GPS coordinates are valid for {formData.region} region
                  </div>
                ) : (
                  <div style={{ fontSize: 12, color: 'var(--danger)' }}>
                    ❌ {result.message}
                  </div>
                )
              })()}
            </div>
          )}

          {/* Submit */}
          <div style={{ marginTop: 20, display: 'flex', gap: 12 }}>
            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
            >
              {loading ? 'Registering...' : 'Register Farmer'}
            </button>
            <button
              type="button"
              onClick={() => navigate('/farmers')}
              className="btn btn-outline"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default AddFarmer