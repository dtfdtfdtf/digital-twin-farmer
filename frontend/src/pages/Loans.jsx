import React, { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { getLoans, getFarmers, createLoan, approveLoan } from '../services/api'

function Loans() {
  const navigate = useNavigate()
  const [loans, setLoans] = useState([])
  const [farmers, setFarmers] = useState([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('active')
  const [showApplyModal, setShowApplyModal] = useState(false)
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedFarmer, setSelectedFarmer] = useState(null)
  const [loanForm, setLoanForm] = useState({
    amount_requested: '',
    purpose: 'seeds',
    term_months: '6',
    repayment_frequency: 'seasonal'
  })
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState('')

  const purposes = ['seeds', 'fertilizer', 'pesticides', 'irrigation', 'equipment', 'labor', 'transport', 'livestock_feed', 'animal_health', 'other']
  const frequencies = ['monthly', 'quarterly', 'seasonal', 'harvest']

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [loansData, farmersData] = await Promise.all([
        getLoans(),
        getFarmers()
      ])
      setLoans(loansData.loans || [])
      setFarmers(farmersData.farmers || [])
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  const activeLoans = loans.filter(l => 
    l.status === 'active' || l.status === 'disbursed' || l.status === 'approved'
  )
  
  const paidLoans = loans.filter(l => 
    l.status === 'completed'
  )

  const pendingLoans = loans.filter(l => 
    l.status === 'pending' || l.status === 'under_review'
  )

  const getStatusBadge = (status) => {
    const styles = {
      'pending': { color: '#856404', bg: '#fff3cd' },
      'approved': { color: '#0c5460', bg: '#d1ecf1' },
      'disbursed': { color: '#004085', bg: '#cce5ff' },
      'active': { color: '#155724', bg: '#d4edda' },
      'completed': { color: '#155724', bg: '#d4edda' },
      'defaulted': { color: '#721c24', bg: '#f8d7da' },
      'rejected': { color: '#721c24', bg: '#f8d7da' }
    }
    const style = styles[status] || { color: '#383d41', bg: '#e2e3e5' }
    return (
      <span style={{
        padding: '2px 10px',
        borderRadius: '12px',
        fontSize: '11px',
        fontWeight: 600,
        color: style.color,
        background: style.bg
      }}>
        {status.toUpperCase()}
      </span>
    )
  }

  const getFarmerName = (farmerId) => {
    const farmer = farmers.find(f => f.id === farmerId)
    return farmer ? `${farmer.first_name} ${farmer.last_name}` : `Farmer #${farmerId}`
  }

  const getFarmerDistrict = (farmerId) => {
    const farmer = farmers.find(f => f.id === farmerId)
    return farmer?.district || '—'
  }

  const handleApplyLoan = () => {
    setShowApplyModal(true)
    setSearchTerm('')
    setSelectedFarmer(null)
    setError('')
    setLoanForm({
      amount_requested: '',
      purpose: 'seeds',
      term_months: '6',
      repayment_frequency: 'seasonal'
    })
  }

  const filteredFarmers = farmers.filter(f =>
    f.status !== 'inactive' &&
    (f.first_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
     f.last_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
     f.national_id?.includes(searchTerm) ||
     f.phone?.includes(searchTerm))
  )

  const handleSubmitLoan = async () => {
    if (!selectedFarmer) {
      setError('Please select a farmer')
      return
    }

    if (!loanForm.amount_requested || parseFloat(loanForm.amount_requested) <= 0) {
      setError('Please enter a valid loan amount')
      return
    }

    setSubmitting(true)
    setError('')

    try {
      const data = {
        farmer_id: selectedFarmer.id,
        loan_type: 'input_financing',
        purpose: loanForm.purpose,
        amount_requested: parseFloat(loanForm.amount_requested),
        term_months: parseInt(loanForm.term_months),
        repayment_frequency: loanForm.repayment_frequency
      }

      console.log('📤 Submitting loan:', data)  // Add debug log

      await createLoan(data)
      await fetchData()
      setShowApplyModal(false)
      alert('✅ Loan application submitted successfully!')
    } catch (err) {
      console.error('Error applying for loan:', err)
      console.error('Response:', err.response?.data)  // Add debug log
      setError(err.response?.data?.detail || 'Failed to apply for loan. Please try again.')
    } finally {
      setSubmitting(false)
    }
  }

  if (loading) {
    return <div className="wrap" style={{ textAlign: 'center', paddingTop: 60 }}>Loading loans...</div>
  }

  return (
    <div className="wrap">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <h2 style={{ marginBottom: 4 }}>Loans</h2>
          <p style={{ color: 'var(--ink-soft)', fontSize: 14 }}>
            {loans.length} total loans · {activeLoans.length} active · {paidLoans.length} paid
          </p>
        </div>
        <button onClick={handleApplyLoan} className="btn btn-primary">
          + Apply for Loan
        </button>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 24, borderBottom: '1px solid var(--line)', paddingBottom: 8 }}>
        <button
          onClick={() => setActiveTab('active')}
          style={{
            padding: '8px 20px',
            borderRadius: '4px',
            border: 'none',
            background: activeTab === 'active' ? 'var(--twin)' : 'transparent',
            color: activeTab === 'active' ? '#fff' : 'var(--ink-soft)',
            cursor: 'pointer',
            fontWeight: activeTab === 'active' ? 600 : 400
          }}
        >
          Active Loans ({activeLoans.length})
        </button>
        <button
          onClick={() => setActiveTab('pending')}
          style={{
            padding: '8px 20px',
            borderRadius: '4px',
            border: 'none',
            background: activeTab === 'pending' ? 'var(--twin)' : 'transparent',
            color: activeTab === 'pending' ? '#fff' : 'var(--ink-soft)',
            cursor: 'pointer',
            fontWeight: activeTab === 'pending' ? 600 : 400
          }}
        >
          Pending ({pendingLoans.length})
        </button>
        <button
          onClick={() => setActiveTab('paid')}
          style={{
            padding: '8px 20px',
            borderRadius: '4px',
            border: 'none',
            background: activeTab === 'paid' ? 'var(--twin)' : 'transparent',
            color: activeTab === 'paid' ? '#fff' : 'var(--ink-soft)',
            cursor: 'pointer',
            fontWeight: activeTab === 'paid' ? 600 : 400
          }}
        >
          Paid Loans ({paidLoans.length})
        </button>
      </div>

      {/* Active Loans */}
      {activeTab === 'active' && (
        activeLoans.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
            <p style={{ color: 'var(--ink-soft)' }}>No active loans.</p>
            <button onClick={handleApplyLoan} className="btn btn-primary" style={{ marginTop: 16 }}>
              Apply for a Loan
            </button>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: 12 }}>
            {activeLoans.map(loan => (
              <div key={loan.id} className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 600 }}>
                      {getFarmerName(loan.farmer_id)}
                    </div>
                    <div style={{ fontSize: 13, color: 'var(--ink-soft)' }}>
                      {getFarmerDistrict(loan.farmer_id)} · Amount: MWK {loan.amount_requested?.toLocaleString() || 0}
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    {getStatusBadge(loan.status)}
                    <Link
                      to={`/farmers/${loan.farmer_id}/twin`}
                      style={{
                        fontSize: 13,
                        color: 'var(--twin)',
                        textDecoration: 'none'
                      }}
                    >
                      View Farmer →
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      )}

      {/* Pending Loans */}
      {activeTab === 'pending' && (
        pendingLoans.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
            <p style={{ color: 'var(--ink-soft)' }}>No pending loan applications.</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: 12 }}>
            {pendingLoans.map(loan => (
              <div key={loan.id} className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 600 }}>
                      {getFarmerName(loan.farmer_id)}
                    </div>
                    <div style={{ fontSize: 13, color: 'var(--ink-soft)' }}>
                      {getFarmerDistrict(loan.farmer_id)} · Amount: MWK {loan.amount_requested?.toLocaleString() || 0}
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    {getStatusBadge(loan.status)}
                    <Link
                      to={`/farmers/${loan.farmer_id}/twin`}
                      style={{
                        fontSize: 13,
                        color: 'var(--twin)',
                        textDecoration: 'none'
                      }}
                    >
                      View Farmer →
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      )}

      {/* Paid Loans */}
      {activeTab === 'paid' && (
        paidLoans.length === 0 ? (
          <div className="card" style={{ textAlign: 'center', padding: '40px' }}>
            <p style={{ color: 'var(--ink-soft)' }}>No paid loans yet.</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: 12 }}>
            {paidLoans.map(loan => (
              <div key={loan.id} className="card">
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <div>
                    <div style={{ fontWeight: 600 }}>
                      {getFarmerName(loan.farmer_id)}
                    </div>
                    <div style={{ fontSize: 13, color: 'var(--ink-soft)' }}>
                      {getFarmerDistrict(loan.farmer_id)} · Amount: MWK {loan.amount_requested?.toLocaleString() || 0}
                    </div>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                    {getStatusBadge(loan.status)}
                    <Link
                      to={`/farmers/${loan.farmer_id}/twin`}
                      style={{
                        fontSize: 13,
                        color: 'var(--twin)',
                        textDecoration: 'none'
                      }}
                    >
                      View Farmer →
                    </Link>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )
      )}

      {/* Apply for Loan Modal */}
      {showApplyModal && (
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
          zIndex: 100,
          padding: '20px'
        }}>
          <div className="card" style={{ maxWidth: 600, width: '100%', maxHeight: '90vh', overflow: 'auto' }}>
            <h3 style={{ marginBottom: 4 }}>Apply for Loan</h3>
            <p style={{ color: 'var(--ink-soft)', fontSize: 14, marginBottom: 16 }}>
              Search for a farmer and enter loan details
            </p>

            {error && (
              <div style={{
                background: '#f8d7da',
                color: '#721c24',
                padding: '10px 14px',
                borderRadius: 4,
                marginBottom: 16,
                fontSize: 14
              }}>
                {error}
              </div>
            )}

            {/* Search Farmer */}
            <div style={{ marginBottom: 16 }}>
              <label style={{ fontSize: 13, fontWeight: 600 }}>Search Farmer *</label>
              <input
                type="text"
                placeholder="Search by name, ID, or phone..."
                value={searchTerm}
                onChange={(e) => {
                  setSearchTerm(e.target.value)
                  setSelectedFarmer(null)
                }}
                style={{
                  width: '100%',
                  padding: '10px 12px',
                  border: '1px solid var(--line)',
                  borderRadius: 4,
                  fontSize: 14
                }}
              />
              {searchTerm && filteredFarmers.length > 0 && !selectedFarmer && (
                <div style={{
                  border: '1px solid var(--line)',
                  borderRadius: 4,
                  marginTop: 4,
                  maxHeight: 150,
                  overflow: 'auto',
                  background: '#fff'
                }}>
                  {filteredFarmers.map(f => (
                    <div
                      key={f.id}
                      onClick={() => {
                        setSelectedFarmer(f)
                        setSearchTerm(`${f.first_name} ${f.last_name} (${f.national_id})`)
                      }}
                      style={{
                        padding: '8px 12px',
                        cursor: 'pointer',
                        borderBottom: '1px solid var(--line)'
                      }}
                    >
                      {f.first_name} {f.last_name} · {f.district} · {f.national_id}
                    </div>
                  ))}
                </div>
              )}
              {/* Fixed: Only show "No farmers found" if no selected farmer */}
              {searchTerm && filteredFarmers.length === 0 && !selectedFarmer && (
                <div style={{ fontSize: 13, color: 'var(--danger)', marginTop: 4 }}>
                  No farmers found. Farmer must be registered first.
                </div>
              )}
              {selectedFarmer && (
                <div style={{
                  marginTop: 8,
                  padding: '8px 12px',
                  background: 'rgba(31,158,140,0.08)',
                  borderRadius: 4,
                  fontSize: 13
                }}>
                  ✅ Selected: <strong>{selectedFarmer.first_name} {selectedFarmer.last_name}</strong>
                  {' · '}{selectedFarmer.district} · {selectedFarmer.national_id}
                </div>
              )}
            </div>

            {/* Loan Details */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 12 }}>
              <div>
                <label style={{ fontSize: 13, fontWeight: 600 }}>Amount (MWK) *</label>
                <input
                  type="number"
                  value={loanForm.amount_requested}
                  onChange={(e) => setLoanForm({...loanForm, amount_requested: e.target.value})}
                  placeholder="500000"
                  style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
                  required
                />
              </div>
              <div>
                <label style={{ fontSize: 13, fontWeight: 600 }}>Purpose</label>
                <select
                  value={loanForm.purpose}
                  onChange={(e) => setLoanForm({...loanForm, purpose: e.target.value})}
                  style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
                >
                  {purposes.map(p => <option key={p} value={p}>{p.replace('_', ' ').toUpperCase()}</option>)}
                </select>
              </div>
              <div>
                <label style={{ fontSize: 13, fontWeight: 600 }}>Term (months)</label>
                <select
                  value={loanForm.term_months}
                  onChange={(e) => setLoanForm({...loanForm, term_months: e.target.value})}
                  style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
                >
                  <option value="3">3 months</option>
                  <option value="6">6 months</option>
                  <option value="9">9 months</option>
                  <option value="12">12 months</option>
                  <option value="18">18 months</option>
                  <option value="24">24 months</option>
                </select>
              </div>
              <div>
                <label style={{ fontSize: 13, fontWeight: 600 }}>Repayment Frequency</label>
                <select
                  value={loanForm.repayment_frequency}
                  onChange={(e) => setLoanForm({...loanForm, repayment_frequency: e.target.value})}
                  style={{ width: '100%', padding: '8px 12px', border: '1px solid var(--line)', borderRadius: 4 }}
                >
                  {frequencies.map(f => <option key={f} value={f}>{f.toUpperCase()}</option>)}
                </select>
              </div>
            </div>

            <div style={{ marginTop: 20, display: 'flex', gap: 12, justifyContent: 'flex-end' }}>
              <button
                onClick={() => setShowApplyModal(false)}
                className="btn btn-outline"
              >
                Cancel
              </button>
              <button
                onClick={handleSubmitLoan}
                disabled={submitting || !selectedFarmer}
                className="btn btn-primary"
              >
                {submitting ? 'Submitting...' : 'Submit Application'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default Loans