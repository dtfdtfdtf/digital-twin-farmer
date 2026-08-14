import React, { useState, useEffect } from 'react'
import { getDashboardStats } from '../services/api'

function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      const data = await getDashboardStats()
      setStats(data)
    } catch (error) {
      console.error('Error fetching stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="wrap" style={{ textAlign: 'center', paddingTop: 60 }}>Loading dashboard...</div>
  }

  return (
    <div className="wrap">
      <h2 style={{ marginBottom: 24 }}>Dashboard</h2>
      
      <div className="grid grid-cols-4" style={{ gap: 16, marginBottom: 32 }}>
        <div className="card">
          <div style={{ fontSize: 28, fontWeight: 700, color: 'var(--twin)' }}>{stats?.farmers?.total || 0}</div>
          <div style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Total Farmers</div>
        </div>
        <div className="card">
          <div style={{ fontSize: 28, fontWeight: 700, color: 'var(--soil)' }}>{stats?.farmers?.verified || 0}</div>
          <div style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Verified Farmers</div>
        </div>
        <div className="card">
          <div style={{ fontSize: 28, fontWeight: 700, color: 'var(--gold)' }}>{stats?.loans?.total || 0}</div>
          <div style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Total Loans</div>
        </div>
        <div className="card">
          <div style={{ fontSize: 28, fontWeight: 700, color: 'var(--success)' }}>{stats?.loans?.approved || 0}</div>
          <div style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Approved Loans</div>
        </div>
      </div>

      <div className="grid grid-cols-2" style={{ gap: 24 }}>
        <div className="card">
          <h3 style={{ fontSize: 16, marginBottom: 16 }}>Financial Summary</h3>
          <div><strong>Total Requested:</strong> MWK {stats?.financial?.total_requested?.toLocaleString() || 0}</div>
          <div><strong>Total Disbursed:</strong> MWK {stats?.financial?.total_disbursed?.toLocaleString() || 0}</div>
          <div><strong>Total Repaid:</strong> MWK {stats?.financial?.total_repaid?.toLocaleString() || 0}</div>
          <div><strong>Outstanding:</strong> MWK {stats?.financial?.outstanding?.toLocaleString() || 0}</div>
        </div>
        <div className="card">
          <h3 style={{ fontSize: 16, marginBottom: 16 }}>Recent Activity</h3>
          <div><strong>New Farmers (7 days):</strong> {stats?.farmers?.new_this_week || 0}</div>
          <div><strong>New Loans (7 days):</strong> {stats?.loans?.new_this_week || 0}</div>
          <div><strong>Pending Farmers:</strong> {stats?.farmers?.pending || 0}</div>
          <div><strong>Pending Loans:</strong> {stats?.loans?.pending || 0}</div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
{/* SDG & MW2063 Section */}
<div className="card" style={{ marginTop: 24 }}>
  <h3 style={{ fontSize: 16, marginBottom: 16 }}>Alignment with National & Global Goals</h3>
  <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
    <span className="sdg-chip" style={{ background: '#1a3a1a', color: '#fff', padding: '6px 14px', borderRadius: 20, fontSize: 13 }}>
      🇲🇼 MW2063 - Pillar 1: Agricultural Productivity
    </span>
    <span className="sdg-chip" style={{ background: '#1a3a6a', color: '#fff', padding: '6px 14px', borderRadius: 20, fontSize: 13 }}>
      SDG 9 - Industry & Innovation
    </span>
    <span className="sdg-chip" style={{ background: '#6a1a1a', color: '#fff', padding: '6px 14px', borderRadius: 20, fontSize: 13 }}>
      SDG 1 - No Poverty
    </span>
    <span className="sdg-chip" style={{ background: '#1a6a1a', color: '#fff', padding: '6px 14px', borderRadius: 20, fontSize: 13 }}>
      SDG 2 - Zero Hunger
    </span>
  </div>
</div>