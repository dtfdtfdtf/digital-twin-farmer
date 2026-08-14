import React from 'react'

function Footer() {
  return (
    <footer style={{
      background: 'var(--canopy)',
      color: 'var(--parchment)',
      padding: '40px 32px',
      borderTop: '1px solid var(--line-dark)'
    }}>
      <div style={{ maxWidth: 1200, margin: '0 auto', textAlign: 'center' }}>
        <h3 style={{ fontSize: 16, marginBottom: 8 }}>THE TEAM</h3>
        <p style={{ color: 'rgba(241,234,216,.6)', fontSize: 14, marginBottom: 8 }}>
          A Malawian team building agricultural finance infrastructure.
        </p>
        <p style={{ fontSize: 14, color: 'var(--parchment)' }}>
          Emmanuel Zutha · Young Chirwa · Juma Milu · Misheck Nzondo · Clement Mughogho · Radson Kayira
        </p>
        <div style={{ marginTop: 16, fontStyle: 'italic', color: 'rgba(241,234,216,.7)' }}>
          "Turning a farmer's potential into verifiable collateral."
        </div>
        <div style={{ marginTop: 16 }}>
          <a href="#" className="btn btn-primary" style={{ fontSize: 14 }}>
            Request a pilot →
          </a>
        </div>
        <div style={{ marginTop: 24, fontSize: 12, color: 'rgba(241,234,216,.4)' }}>
          © {new Date().getFullYear()} Digital Twin Farmer — Government of Malawi
        </div>
      </div>
    </footer>
  )
}

export default Footer