import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'

function Navbar() {
  const navigate = useNavigate()
  const [isOpen, setIsOpen] = useState(false)
  
  const handleLogout = () => {
    localStorage.removeItem('token')
    navigate('/login')
  }

  return (
    <nav style={{
      position: 'sticky',
      top: 0,
      zIndex: 50,
      background: 'rgba(241,234,216,.92)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid var(--line)'
    }}>
      <div style={{
        maxWidth: 1200,
        margin: '0 auto',
        padding: '16px 32px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: 10, fontWeight: 700, fontSize: 18 }}>
          <span style={{
            width: 28,
            height: 28,
            borderRadius: 4,
            background: 'linear-gradient(135deg, var(--soil) 50%, var(--twin) 50%)',
            flex: 'none'
          }}></span>
          Digital Twin Farmer
        </Link>

        <div style={{ display: 'flex', gap: 24, alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: 24, fontSize: 14 }}>
            <Link to="/dashboard" style={{ color: 'var(--ink-soft)' }}>Dashboard</Link>
            <Link to="/farmers" style={{ color: 'var(--ink-soft)' }}>Farmers</Link>
            <Link to="/loans" style={{ color: 'var(--ink-soft)' }}>Loans</Link>
            <Link to="/harvest" style={{ color: 'var(--ink-soft)' }}>Harvest</Link>
            <Link to="/map" style={{ color: 'var(--ink-soft)' }}>Map</Link>
          </div>
          <button 
            onClick={handleLogout}
            style={{
              background: 'var(--danger)',
              color: '#fff',
              border: 'none',
              padding: '8px 16px',
              borderRadius: 4,
              cursor: 'pointer',
              fontSize: 14
            }}
          >
            Logout
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar