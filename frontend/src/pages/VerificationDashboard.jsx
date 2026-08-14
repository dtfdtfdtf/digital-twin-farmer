import React, { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getFarmer, getVerificationStatus, verifyGPS, verifySatellite, verifyOfficer, verifyCommunity, runAICheck } from '../services/api'

function VerificationDashboard() {
  const { id } = useParams()
  const [farmer, setFarmer] = useState(null)
  const [verificationStatus, setVerificationStatus] = useState(null)
  const [loading, setLoading] = useState(true)
  const [verifying, setVerifying] = useState(false)

  useEffect(() => {
    fetchData()
  }, [id])

  const fetchData = async () => {
    setLoading(true)
    try {
      const [farmerData, statusData] = await Promise.all([
        getFarmer(id),
        getVerificationStatus(id)
      ])
      setFarmer(farmerData)
      setVerificationStatus(statusData)
    } catch (error) {
      console.error('Error fetching verification data:', error)
    } finally {
      setLoading(false)
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
      await fetchData()
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
      await fetchData()
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

  if (loading) {
    return <div className="wrap" style={{ textAlign: 'center', paddingTop: 60 }}>Loading verification data...</div>
  }

  if (!farmer || !verificationStatus) {
    return <div className="wrap" style={{ textAlign: 'center', paddingTop: 60 }}>No verification data found</div>
  }

  const getScoreColor = (score) => {
    if (score >= 90) return 'var(--twin)'
    if (score >= 70) return 'var(--gold)'
    if (score >= 50) return 'var(--soil)'
    return 'var(--danger)'
  }

  const getLayerStatusColor = (verified) => {
    return verified ? 'var(--twin)' : 'var(--ink-soft)'
  }

  const getLayerStatusText = (verified) => {
    return verified ? '✅ Verified' : '⏳ Pending'
  }

  return (
    <div className="wrap">
      <Link to={`/farmers/${id}/twin`} style={{ color: 'var(--twin)', fontSize: 14 }}>← Back to Profile</Link>
      
      <h2 style={{ marginTop: 16, marginBottom: 4 }}>Verification Dashboard</h2>
      <p style={{ color: 'var(--ink-soft)', marginBottom: 24 }}>
        {farmer.first_name} {farmer.last_name} - {farmer.district}
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
        {/* Left Column: Verification Score & Loan Eligibility */}
        <div>
          {/* Score Card */}
          <div className="card" style={{ textAlign: 'center' }}>
            <div style={{ fontSize: 14, color: 'var(--ink-soft)' }}>Verification Score</div>
            <div style={{ 
              fontSize: 64, 
              fontWeight: 700, 
              color: getScoreColor(verificationStatus.verification_score)
            }}>
              {verificationStatus.verification_score}%
            </div>
            <div style={{ fontSize: 18, fontWeight: 600, marginTop: 4 }}>
              {verificationStatus.verification_status_text}
            </div>
            <div style={{ fontSize: 13, color: 'var(--ink-soft)' }}>
              Level: <strong>{verificationStatus.verification_level.toUpperCase()}</strong>
            </div>
            <div style={{ 
              marginTop: 16, 
              padding: '8px 16px', 
              borderRadius: '4px',
              background: verificationStatus.loan_eligibility?.eligible ? 'rgba(31,158,140,0.1)' : 'rgba(168,72,28,0.1)',
              fontWeight: 600,
              color: verificationStatus.loan_eligibility?.eligible ? 'var(--twin)' : 'var(--soil)'
            }}>
              {verificationStatus.loan_eligibility?.eligible ? '✅ Eligible for Loans' : '❌ Not Eligible for Loans'}
            </div>
          </div>

          {/* Loan Eligibility Requirements */}
          <div className="card" style={{ marginTop: 16 }}>
            <h4 style={{ fontSize: 14, marginBottom: 12 }}>Eligibility Requirements</h4>
            {Object.entries(verificationStatus.loan_eligibility?.requirements || {}).map(([key, value]) => (
              <div key={key} style={{ 
                display: 'flex', 
                justifyContent: 'space-between', 
                padding: '6px 0',
                borderBottom: '1px solid var(--line)',
                fontSize: 13
              }}>
                <span style={{ color: 'var(--ink-soft)' }}>{key.replace(/_/g, ' ')}</span>
                <span style={{ color: value ? 'var(--twin)' : 'var(--danger)' }}>
                  {value ? '✅' : '❌'}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Right Column: Verification Layers */}
        <div>
          <div className="card">
            <h4 style={{ fontSize: 14, marginBottom: 12 }}>Verification Layers</h4>
            {Object.entries(verificationStatus.layers || {}).map(([key, layer]) => (
              <div key={key} style={{ 
                padding: '10px 12px', 
                marginBottom: 8,
                background: layer.verified ? 'rgba(31,158,140,0.06)' : 'rgba(168,72,28,0.04)',
                borderRadius: '4px',
                border: `1px solid ${layer.verified ? 'rgba(31,158,140,0.15)' : 'rgba(168,72,28,0.1)'}`
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: 14, textTransform: 'capitalize' }}>
                      {key.replace('_', ' ')}
                      <span style={{ fontSize: 11, color: 'var(--ink-soft)', marginLeft: 8 }}>
                        (Weight: {layer.weight}%)
                      </span>
                    </div>
                    {layer.verified_at && (
                      <div style={{ fontSize: 11, color: 'var(--ink-soft)' }}>
                        {new Date(layer.verified_at).toLocaleDateString()}
                      </div>
                    )}
                    {layer.officer_name && (
                      <div style={{ fontSize: 11, color: 'var(--twin)' }}>
                        By: {layer.officer_name}
                      </div>
                    )}
                    {layer.verifier && (
                      <div style={{ fontSize: 11, color: 'var(--twin)' }}>
                        By: {layer.verifier}
                      </div>
                    )}
                    {layer.record_count !== undefined && (
                      <div style={{ fontSize: 11, color: 'var(--ink-soft)' }}>
                        {layer.record_count} records
                      </div>
                    )}
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    <span style={{ 
                      fontSize: 13,
                      fontWeight: 500,
                      color: getLayerStatusColor(layer.verified)
                    }}>
                      {getLayerStatusText(layer.verified)}
                    </span>
                    {!layer.verified && key !== 'national_id' && key !== 'historical_records' && (
                      <button
                        onClick={() => handleVerify(key)}
                        disabled={verifying}
                        className="btn btn-primary"
                        style={{ fontSize: 11, padding: '4px 12px' }}
                      >
                        {verifying ? '...' : 'Verify'}
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          {/* AI Consistency Check */}
          <div className="card" style={{ marginTop: 16 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <h4 style={{ fontSize: 14 }}>AI Consistency Check</h4>
                <span style={{ 
                  fontSize: 14, 
                  fontWeight: 600,
                  color: verificationStatus.ai_consistency?.passed ? 'var(--twin)' : 'var(--danger)'
                }}>
                  {verificationStatus.ai_consistency?.passed ? '✅ Passed' : '⚠️ Issues Found'}
                </span>
                {verificationStatus.ai_consistency?.flags?.length > 0 && (
                  <div style={{ fontSize: 13, color: 'var(--danger)', marginTop: 8 }}>
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
                style={{ fontSize: 12 }}
              >
                {verifying ? 'Running...' : 'Run AI Check'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default VerificationDashboard