import React, { useState, useEffect } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { 
  getFarmer, 
  deleteFarmer, 
  getVerificationStatus, 
  verifyGPS, 
  verifySatellite, 
  verifyOfficer, 
  verifyCommunity, 
  runAICheck,
  getHistoricalRecords,
  addHistoricalRecord,
  deleteHistoricalRecord
} from '../services/api'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

function FarmerDigitalTwin() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [farmer, setFarmer] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showDeleteModal, setShowDeleteModal] = useState(false)
  const [showAddRecord, setShowAddRecord] = useState(false)
  const [verificationStatus, setVerificationStatus] = useState(null)
  const [verifying, setVerifying] = useState(false)
  const [activeTab, setActiveTab] = useState('profile')
  const [historicalRecords, setHistoricalRecords] = useState([])
  
  const [recordForm, setRecordForm] = useState({
    enterprise_type: 'crop',
    crop_name: '',
    bags_per_hectare: '',
    season: new Date().getFullYear().toString()
  })

  const cropSuggestions = ['Maize', 'Groundnuts', 'Soybean', 'Tobacco', 'Cassava', 'Beans', 'Rice', 'Tomatoes', 'Onions', 'Dairy', 'Goats', 'Poultry']

  useEffect(() => {
    fetchFarmer()
    fetchVerificationStatus()
    fetchHistoricalRecords()
  }, [id])

  const fetchFarmer = async () => {
    try {
      const data = await getFarmer(id)
      setFarmer(data)
    } catch (error) {
      console.error('Error fetching farmer:', error)
    } finally {
      setLoading(false)
    }
  }

  const fetchVerificationStatus = async () => {
    try {
      const data = await getVerificationStatus(id)
      setVerificationStatus(data)
    } catch (error) {
      console.error('Error fetching verification status:', error)
    }
  }

  const fetchHistoricalRecords = async () => {
    try {
      const data = await getHistoricalRecords(id)
      setHistoricalRecords(data || [])
    } catch (error) {
      console.error('Error fetching historical records:', error)
    }
  }

  const handleDeleteFarmer = async () => {
    try {
      await deleteFarmer(id)
      navigate('/farmers')
    } catch (error) {
      console.error('Error deleting farmer:', error)
      alert('Failed to delete farmer. Please try again.')
    }
  }

  const handleVerify = async (layer, params = {}) => {
    setVerifying(true)
    try {
      let result
      switch(layer) {
        case 'gps':
          result = await verifyGPS(id)
          break
        case 'satellite':
          result = await verifySatellite(id)
          break
        case 'officer':
          const officerName = prompt('Enter officer name:')
          if (!officerName) { setVerifying(false); return }
          result = await verifyOfficer(id, officerName)
          break
        case 'community':
          const verifier = prompt('Enter community verifier name (e.g., Village Head):')
          if (!verifier) { setVerifying(false); return }
          result = await verifyCommunity(id, verifier)
          break
        default:
          return
      }
      await fetchVerificationStatus()
      await fetchFarmer()
      alert(`✅ ${layer.charAt(0).toUpperCase() + layer.slice(1)} verification successful!`)
    } catch (error) {
      console.error('Error verifying:', error)
      alert('Failed to verify. Please try again.')
    } finally {
      setVerifying(false)
    }
  }

  const handleAICheck = async () => {
    setVerifying(true)
    try {
      const result = await runAICheck(id)
      await fetchVerificationStatus()
      await fetchFarmer()
      if (result.passed) {
        alert('✅ AI consistency check passed! No flags found.')
      } else {
        alert(`⚠️ AI check found ${result.flag_count} issue(s):\n\n${result.flags.join('\n')}`)
      }
    } catch (error) {
      console.error('Error running AI check:', error)
      alert('Failed to run AI check. Please try again.')
    } finally {
      setVerifying(false)
    }
  }

  const handleAddRecord = async (e) => {
    e.preventDefault()
    
    const bags = parseFloat(recordForm.bags_per_hectare)
    const area = farmer?.farm_area_hectares || 1
    
    setVerifying(true)
    try {
      await addHistoricalRecord(id, {
        season: recordForm.season,
        enterprise_type: recordForm.enterprise_type,
        crop_name: recordForm.crop_name,
        area_hectares: area,
        bags_50kg: bags,
        verified_by: 'Officer'
      })
      
      await fetchHistoricalRecords()
      await fetchFarmer()
      setShowAddRecord(false)
      setRecordForm({
        enterprise_type: 'crop',
        crop_name: '',
        bags_per_hectare: '',
        season: new Date().getFullYear().toString()
      })
      alert('✅ Historical record added successfully! Verification score updated.')
    } catch (error) {
      console.error('Error adding record:', error)
      alert('Failed to add record. Please try again.')
    } finally {
      setVerifying(false)
    }
  }

  const handleDeleteRecord = async (recordId) => {
    if (!window.confirm('Are you sure you want to delete this record?')) return
    
    try {
      await deleteHistoricalRecord(recordId)
      await fetchHistoricalRecords()
      await fetchFarmer()
      alert('✅ Record deleted successfully!')
    } catch (error) {
      console.error('Error deleting record:', error)
      alert('Failed to delete record.')
    }
  }

  // Prepare chart data
  const chartData = {
    labels: ['2022', '2023', '2024', '2025', '2026'],
    datasets: [
      {
        label: 'Actual Yield (t/ha)',
        data: historicalRecords.length > 0 
          ? historicalRecords.slice(0, 5).map(r => r.yield_tons || 0)
          : [3.2, 3.8, 3.5, 4.0, 4.2],
        borderColor: '#A8481C',
        backgroundColor: 'rgba(168,72,28,0.1)',
        tension: 0.3,
        fill: true,
        pointRadius: 4,
        pointBackgroundColor: '#A8481C'
      },
      {
        label: 'AI Predicted Yield (t/ha)',
        data: [null, null, null, 3.8, 4.5],
        borderColor: '#1F9E8C',
        backgroundColor: 'rgba(31,158,140,0.1)',
        borderDash: [6, 4],
        tension: 0.3,
        fill: false,
        pointRadius: 4,
        pointBackgroundColor: '#1F9E8C'
      }
    ]
  }

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: { boxWidth: 12, font: { size: 12 } }
      },
      title: {
        display: true,
        text: `${farmer?.first_name || ''} ${farmer?.last_name || ''} - Harvest Performance`,
        font: { size: 14, weight: 'bold' }
      }
    },
    scales: {
      y: {
        title: { display: true, text: 'Yield (tons per hectare)' },
        min: 0,
        max: 6
      },
      x: {
        title: { display: true, text: 'Season' }
      }
    }
  }

  if (loading) {
    return <div className="wrap" style={{ textAlign: 'center', paddingTop: 60 }}>Loading farmer profile...</div>
  }

  if (!farmer) {
    return <div className="wrap" style={{ textAlign: 'center', paddingTop: 60 }}>Farmer not found</div>
  }

  return (
    <div className="wrap">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
        <Link to="/farmers/search" style={{ color: 'var(--twin)', fontSize: 14 }}>← Back to Search</Link>
        <button
          onClick={() => setShowDeleteModal(true)}
          style={{
            background: 'var(--danger)',
            color: '#fff',
            border: 'none',
            padding: '8px 16px',
            borderRadius: 4,
            cursor: 'pointer',
            fontSize: 13
          }}
        >
          🗑️ Delete Farmer
        </button>
      </div>
      
      <h2 style={{ marginTop: 8, marginBottom: 4 }}>Digital Twin Profile</h2>
      <p style={{ color: 'var(--ink-soft)', marginBottom: 24 }}>Complete digital identity for {farmer.first_name} {farmer.last_name}</p>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24, borderBottom: '1px solid var(--line)', paddingBottom: 8 }}>
        <button
          onClick={() => setActiveTab('profile')}
          style={{
            padding: '8px 20px',
            borderRadius: '4px',
            border: 'none',
            background: activeTab === 'profile' ? 'var(--twin)' : 'transparent',
            color: activeTab === 'profile' ? '#fff' : 'var(--ink-soft)',
            cursor: 'pointer',
            fontWeight: activeTab === 'profile' ? 600 : 400
          }}
        >
          Profile
        </button>
        <button
          onClick={() => setActiveTab('verification')}
          style={{
            padding: '8px 20px',
            borderRadius: '4px',
            border: 'none',
            background: activeTab === 'verification' ? 'var(--twin)' : 'transparent',
            color: activeTab === 'verification' ? '#fff' : 'var(--ink-soft)',
            cursor: 'pointer',
            fontWeight: activeTab === 'verification' ? 600 : 400
          }}
        >
          Verification Dashboard
        </button>
      </div>

      {/* Profile Tab */}
      {activeTab === 'profile' && (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
            {/* Left: Digital Twin Card */}
            <div>
              <div style={{
                background: 'linear-gradient(145deg, #0d1a17, #1a2d26)',
                borderRadius: '12px',
                padding: '24px 20px',
                border: '1px solid rgba(31,158,140,0.3)',
                boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
                position: 'relative',
                overflow: 'hidden'
              }}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  borderBottom: '1px solid rgba(31,158,140,0.2)',
                  paddingBottom: 10
                }}>
                  <span style={{
                    fontFamily: "'IBM Plex Mono', monospace",
                    fontSize: 11,
                    letterSpacing: '.12em',
                    color: 'var(--twin)',
                    textTransform: 'uppercase'
                  }}>
                    Digital Twin Farmer
                  </span>
                  <span style={{
                    fontFamily: "'IBM Plex Mono', monospace",
                    fontSize: 10,
                    color: 'rgba(241,234,216,0.4)',
                    background: 'rgba(31,158,140,0.15)',
                    padding: '2px 10px',
                    borderRadius: 12
                  }}>
                    SBT · CELO
                  </span>
                </div>

                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 14,
                  marginTop: 12
                }}>
                  <div style={{
                    width: 50,
                    height: 50,
                    borderRadius: '50%',
                    background: 'linear-gradient(135deg, #2b3a1f, #1a2712)',
                    border: '2px solid rgba(31,158,140,0.3)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}>
                    <svg width="28" height="28" viewBox="0 0 32 32" fill="none">
                      <circle cx="16" cy="10" r="6" stroke="#1f9e8c" strokeWidth="1.5"/>
                      <path d="M4 28C4 22 9 18 16 18C23 18 28 22 28 28" stroke="#1f9e8c" strokeWidth="1.5"/>
                    </svg>
                  </div>
                  <div>
                    <div style={{
                      fontFamily: "'Fraunces', serif",
                      fontSize: 18,
                      fontWeight: 600,
                      color: 'var(--parchment)'
                    }}>
                      {farmer.first_name} {farmer.last_name}
                    </div>
                    <div style={{
                      fontFamily: "'IBM Plex Mono', monospace",
                      fontSize: 10,
                      color: 'rgba(241,234,216,0.4)'
                    }}>
                      DTF-{String(farmer.id).padStart(6, '0')}
                    </div>
                  </div>
                </div>

                <div style={{
                  display: 'grid',
                  gridTemplateColumns: '1fr 1fr',
                  gap: '4px 16px',
                  fontSize: 12,
                  marginTop: 12
                }}>
                  <div>
                    <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>Country</span>
                    <div style={{ color: 'var(--parchment)', fontWeight: 500 }}>Malawi</div>
                  </div>
                  <div>
                    <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>District</span>
                    <div style={{ color: 'var(--parchment)', fontWeight: 500 }}>{farmer.district || '—'}</div>
                  </div>
                  <div>
                    <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>Phone</span>
                    <div style={{ color: 'var(--parchment)', fontWeight: 500 }}>{farmer.phone || '—'}</div>
                  </div>
                  <div>
                    <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>National ID</span>
                    <div style={{ color: 'var(--parchment)', fontWeight: 500 }}>{farmer.national_id || '—'}</div>
                  </div>
                  <div>
                    <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>Enterprise</span>
                    <div style={{ color: 'var(--parchment)', fontWeight: 500 }}>Crop / Livestock</div>
                  </div>
                  <div>
                    <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>Region</span>
                    <div style={{ color: 'var(--parchment)', fontWeight: 500 }}>{farmer.region || '—'}</div>
                  </div>
                </div>

                <div style={{
                  background: 'rgba(31,158,140,0.08)',
                  borderRadius: 6,
                  padding: '8px 14px',
                  marginTop: 12
                }}>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <span style={{ fontSize: 11, color: 'rgba(241,234,216,0.5)' }}>AI Credit Score</span>
                    <span style={{
                      fontFamily: "'IBM Plex Mono', monospace",
                      fontSize: 16,
                      fontWeight: 700,
                      color: 'var(--twin)'
                    }}>{Math.round((farmer.credit_score || 0) / 10)}%</span>
                  </div>
                  <div style={{
                    width: '100%',
                    height: 4,
                    background: 'rgba(255,255,255,0.1)',
                    borderRadius: 2,
                    marginTop: 4,
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${Math.min((farmer.credit_score || 0) / 10, 100)}%`,
                      height: '100%',
                      background: 'linear-gradient(90deg, var(--twin), #28b6a2)',
                      borderRadius: 2
                    }}></div>
                  </div>
                </div>

                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: 8,
                  fontSize: 11,
                  color: 'var(--twin)',
                  marginTop: 10
                }}>
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <circle cx="7" cy="7" r="6" stroke="#1f9e8c" strokeWidth="1.5"/>
                    <path d="M4 7L6 9L10 5" stroke="#1f9e8c" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: 10 }}>
                    {farmer.has_blockchain_identity ? 'Blockchain Verified' : 'Blockchain Pending'}
                  </span>
                  <span style={{
                    marginLeft: 'auto',
                    fontFamily: "'IBM Plex Mono', monospace",
                    fontSize: 9,
                    color: 'rgba(241,234,216,0.25)'
                  }}>
                    • CELO
                  </span>
                </div>
              </div>
            </div>

            {/* Right: Farmer Details + Verification Buttons */}
            <div>
              <div className="card">
                <h3 style={{ fontSize: 16, marginBottom: 12 }}>Personal Details</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px 16px', fontSize: 14 }}>
                  <div><strong>Status</strong></div>
                  <div style={{ color: farmer.is_verified ? 'var(--twin)' : 'var(--soil)' }}>
                    {farmer.is_verified ? '✅ Verified' : '⏳ Pending'}
                  </div>
                  <div><strong>Village</strong></div>
                  <div>{farmer.village || '—'}</div>
                  <div><strong>Traditional Authority</strong></div>
                  <div>{farmer.traditional_authority || '—'}</div>
                  <div><strong>Farm Area</strong></div>
                  <div>{farmer.farm_area_hectares || '—'} ha</div>
                  <div><strong>GPS</strong></div>
                  <div>{farmer.latitude && farmer.longitude ? `${farmer.latitude}, ${farmer.longitude}` : '—'}</div>
                </div>

                {/* Verification Buttons */}
                <div style={{ marginTop: 16, paddingTop: 16, borderTop: '1px solid var(--line)' }}>
                  <h4 style={{ fontSize: 13, marginBottom: 10 }}>Verification Actions</h4>
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                    <button
                      onClick={() => handleVerify('gps')}
                      disabled={verifying || farmer.is_gps_verified}
                      className="btn btn-primary"
                      style={{ 
                        fontSize: 11, 
                        padding: '4px 12px',
                        opacity: farmer.is_gps_verified ? 0.5 : 1
                      }}
                    >
                      {farmer.is_gps_verified ? '✅ GPS Done' : 'Verify GPS'}
                    </button>
                    <button
                      onClick={() => handleVerify('satellite')}
                      disabled={verifying || farmer.is_satellite_verified}
                      className="btn btn-primary"
                      style={{ 
                        fontSize: 11, 
                        padding: '4px 12px',
                        opacity: farmer.is_satellite_verified ? 0.5 : 1
                      }}
                    >
                      {farmer.is_satellite_verified ? '✅ Satellite Done' : 'Verify Satellite'}
                    </button>
                    <button
                      onClick={() => handleVerify('officer')}
                      disabled={verifying || farmer.is_officer_verified}
                      className="btn btn-primary"
                      style={{ 
                        fontSize: 11, 
                        padding: '4px 12px',
                        opacity: farmer.is_officer_verified ? 0.5 : 1
                      }}
                    >
                      {farmer.is_officer_verified ? '✅ Officer Done' : 'Verify Officer'}
                    </button>
                    <button
                      onClick={() => handleVerify('community')}
                      disabled={verifying || farmer.is_community_verified}
                      className="btn btn-primary"
                      style={{ 
                        fontSize: 11, 
                        padding: '4px 12px',
                        opacity: farmer.is_community_verified ? 0.5 : 1
                      }}
                    >
                      {farmer.is_community_verified ? '✅ Community Done' : 'Verify Community'}
                    </button>
                  </div>
                  <div style={{ fontSize: 11, color: 'var(--ink-soft)', marginTop: 8 }}>
                    Score: {farmer.verification_score || 0}% · Level: {farmer.verification_level?.toUpperCase() || 'UNVERIFIED'}
                  </div>
                </div>
              </div>

              {/* Harvest Graph */}
              <div className="card" style={{ marginTop: 16 }}>
                <h3 style={{ fontSize: 16, marginBottom: 8 }}>Harvest Performance</h3>
                <p style={{ fontSize: 13, color: 'var(--ink-soft)', marginBottom: 12 }}>
                  Actual vs AI predicted yield for {farmer.first_name} {farmer.last_name}
                </p>
                <div style={{ height: '180px' }}>
                  <Line data={chartData} options={chartOptions} />
                </div>
              </div>
            </div>
          </div>

          {/* Historical Records Section */}
          <div className="card" style={{ marginTop: 24 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <h3 style={{ fontSize: 16 }}>Farming Records</h3>
              <button
                onClick={() => setShowAddRecord(!showAddRecord)}
                className="btn btn-primary"
                style={{ fontSize: 13 }}
              >
                {showAddRecord ? 'Cancel' : '+ Add Record'}
              </button>
            </div>

            {showAddRecord && (
              <form onSubmit={handleAddRecord} style={{
                background: 'var(--parchment-2)',
                padding: '16px',
                borderRadius: '4px',
                marginBottom: '16px',
                display: 'grid',
                gridTemplateColumns: '1fr 1fr 1fr auto',
                gap: 12,
                alignItems: 'end'
              }}>
                <div>
                  <label style={{ fontSize: 13, fontWeight: 600 }}>Enterprise Type</label>
                  <select
                    value={recordForm.enterprise_type}
                    onChange={(e) => setRecordForm({...recordForm, enterprise_type: e.target.value})}
                    style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
                  >
                    <option value="crop">Crop</option>
                    <option value="livestock">Livestock</option>
                  </select>
                </div>
                <div>
                  <label style={{ fontSize: 13, fontWeight: 600 }}>Crop / Livestock</label>
                  <input
                    type="text"
                    list="cropSuggestions"
                    value={recordForm.crop_name}
                    onChange={(e) => setRecordForm({...recordForm, crop_name: e.target.value})}
                    placeholder="e.g., Maize"
                    style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
                    required
                  />
                  <datalist id="cropSuggestions">
                    {cropSuggestions.map(crop => <option key={crop} value={crop} />)}
                  </datalist>
                </div>
                <div>
                  <label style={{ fontSize: 13, fontWeight: 600 }}>Bags (50kg) per ha</label>
                  <input
                    type="number"
                    value={recordForm.bags_per_hectare}
                    onChange={(e) => setRecordForm({...recordForm, bags_per_hectare: e.target.value})}
                    placeholder="e.g., 30"
                    style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
                    required
                  />
                </div>
                <div>
                  <button type="submit" className="btn btn-primary" style={{ width: '100%' }} disabled={verifying}>
                    {verifying ? 'Saving...' : 'Save Record'}
                  </button>
                </div>
              </form>
            )}

            {historicalRecords.length === 0 ? (
              <p style={{ color: 'var(--ink-soft)', textAlign: 'center', padding: '20px' }}>
                No farming records yet. Add your first record above.
              </p>
            ) : (
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 14 }}>
                  <thead>
                    <tr style={{ borderBottom: '2px solid var(--line)' }}>
                      <th style={{ textAlign: 'left', padding: '8px' }}>Season</th>
                      <th style={{ textAlign: 'left', padding: '8px' }}>Crop</th>
                      <th style={{ textAlign: 'right', padding: '8px' }}>Bags/ha</th>
                      <th style={{ textAlign: 'right', padding: '8px' }}>Area (ha)</th>
                      <th style={{ textAlign: 'right', padding: '8px' }}>Yield (tons)</th>
                      <th style={{ textAlign: 'center', padding: '8px' }}>Action</th>
                    </tr>
                  </thead>
                  <tbody>
                    {historicalRecords.map(record => (
                      <tr key={record.id} style={{ borderBottom: '1px solid var(--line)' }}>
                        <td style={{ padding: '8px' }}>{record.season}</td>
                        <td style={{ padding: '8px' }}>{record.crop_name}</td>
                        <td style={{ textAlign: 'right', padding: '8px' }}>{record.bags_50kg || '-'}</td>
                        <td style={{ textAlign: 'right', padding: '8px' }}>{record.area_hectares || 1}</td>
                        <td style={{ textAlign: 'right', padding: '8px', fontWeight: 600, color: 'var(--twin)' }}>
                          {record.yield_tons || 0}
                        </td>
                        <td style={{ textAlign: 'center', padding: '8px' }}>
                          <button
                            onClick={() => handleDeleteRecord(record.id)}
                            style={{
                              background: 'var(--danger)',
                              color: '#fff',
                              border: 'none',
                              padding: '2px 10px',
                              borderRadius: '4px',
                              cursor: 'pointer',
                              fontSize: 11
                            }}
                          >
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </>
      )}

      {/* Verification Tab */}
      {activeTab === 'verification' && verificationStatus && (
        <div>
          <div className="card" style={{ textAlign: 'center', marginBottom: 24 }}>
            <div style={{ fontSize: 14, color: 'var(--ink-soft)' }}>Verification Score</div>
            <div style={{ 
              fontSize: 72, 
              fontWeight: 700, 
              color: verificationStatus.verification_score >= 90 ? 'var(--twin)' : 
                     verificationStatus.verification_score >= 70 ? 'var(--gold)' : 
                     verificationStatus.verification_score >= 50 ? 'var(--soil)' : 'var(--danger)'
            }}>
              {verificationStatus.verification_score}%
            </div>
            <div style={{ fontSize: 18, fontWeight: 600 }}>
              {verificationStatus.verification_status_text}
            </div>
            <div style={{ fontSize: 13, color: 'var(--ink-soft)', marginTop: 4 }}>
              Level: {verificationStatus.verification_level.toUpperCase()}
            </div>
          </div>

          <div className="card">
            <h3 style={{ fontSize: 16, marginBottom: 16 }}>Verification Layers</h3>
            <div style={{ display: 'grid', gap: 12 }}>
              {Object.entries(verificationStatus.layers || {}).map(([key, layer]) => (
                <div key={key} style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '12px 16px',
                  background: layer.verified ? 'rgba(31,158,140,0.08)' : 'rgba(168,72,28,0.05)',
                  borderRadius: '4px',
                  border: `1px solid ${layer.verified ? 'rgba(31,158,140,0.2)' : 'rgba(168,72,28,0.15)'}`
                }}>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 14, textTransform: 'capitalize' }}>
                      {key.replace('_', ' ')}
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--ink-soft)' }}>
                      Weight: {layer.weight}%
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <span style={{
                      fontSize: 13,
                      color: layer.verified ? 'var(--twin)' : 'var(--soil)'
                    }}>
                      {layer.status}
                    </span>
                    {!layer.verified && key !== 'national_id' && (
                      <button
                        onClick={() => handleVerify(key)}
                        disabled={verifying}
                        className="btn btn-primary"
                        style={{ fontSize: 11, padding: '4px 12px' }}
                      >
                        Verify
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card" style={{ marginTop: 16 }}>
            <h3 style={{ fontSize: 16, marginBottom: 12 }}>AI Consistency Check</h3>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <span style={{ 
                  fontSize: 14, 
                  fontWeight: 600,
                  color: verificationStatus.ai_consistency?.passed ? 'var(--twin)' : 'var(--danger)'
                }}>
                  {verificationStatus.ai_consistency?.passed ? '✅ Passed' : '⚠️ Issues Found'}
                </span>
                {verificationStatus.ai_consistency?.flags?.length > 0 && (
                  <div style={{ fontSize: 13, color: 'var(--danger)', marginTop: 4 }}>
                    {verificationStatus.ai_consistency.flags.map((flag, i) => (
                      <div key={i}>• {flag}</div>
                    ))}
                  </div>
                )}
              </div>
              <button
                onClick={handleAICheck}
                disabled={verifying}
                className="btn btn-primary"
              >
                Run AI Check
              </button>
            </div>
          </div>

          <div className="card" style={{ marginTop: 16 }}>
            <h3 style={{ fontSize: 16, marginBottom: 12 }}>Loan Eligibility</h3>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
              {Object.entries(verificationStatus.loan_eligibility?.requirements || {}).map(([key, value]) => (
                <div key={key} style={{ fontSize: 13 }}>
                  <span style={{ color: 'var(--ink-soft)' }}>{key.replace(/_/g, ' ')}:</span>
                  <span style={{ 
                    marginLeft: 8,
                    fontWeight: 600,
                    color: value ? 'var(--twin)' : 'var(--danger)'
                  }}>
                    {value ? '✅' : '❌'}
                  </span>
                </div>
              ))}
            </div>
            <div style={{ 
              marginTop: 12,
              padding: '8px 16px',
              borderRadius: '4px',
              background: verificationStatus.loan_eligibility?.eligible ? 'rgba(31,158,140,0.1)' : 'rgba(168,72,28,0.1)',
              fontWeight: 600,
              color: verificationStatus.loan_eligibility?.eligible ? 'var(--twin)' : 'var(--soil)'
            }}>
              {verificationStatus.loan_eligibility?.eligible ? '✅ Farmer is eligible for loans' : '❌ Farmer is NOT eligible for loans'}
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.5)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 100
        }}>
          <div className="card" style={{ maxWidth: 400, width: '100%', textAlign: 'center' }}>
            <h3 style={{ color: 'var(--danger)' }}>Confirm Delete</h3>
            <p style={{ color: 'var(--ink-soft)', margin: '16px 0' }}>
              Are you sure you want to delete <strong>{farmer.first_name} {farmer.last_name}</strong>?
              <br />
              <span style={{ fontSize: 13 }}>This action cannot be undone.</span>
            </p>
            <div style={{ display: 'flex', gap: 12, justifyContent: 'center' }}>
              <button
                onClick={() => setShowDeleteModal(false)}
                className="btn btn-outline"
              >
                Cancel
              </button>
              <button
                onClick={handleDeleteFarmer}
                style={{
                  background: 'var(--danger)',
                  color: '#fff',
                  border: 'none',
                  padding: '10px 24px',
                  borderRadius: 4,
                  cursor: 'pointer',
                  fontSize: 14,
                  fontWeight: 600
                }}
              >
                Yes, Delete
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default FarmerDigitalTwin