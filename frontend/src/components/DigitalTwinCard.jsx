import React from 'react'

function DigitalTwinCard() {
  return (
    <div style={{
      background: 'linear-gradient(145deg, #0d1a17, #1a2d26)',
      borderRadius: '12px',
      padding: '24px 20px',
      border: '1px solid rgba(31,158,140,0.3)',
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
      position: 'relative',
      overflow: 'hidden',
      maxWidth: '400px',
      width: '100%',
      height: '380px',
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'space-between'
    }}>
      {/* Background pattern */}
      <div style={{
        position: 'absolute',
        top: -50,
        right: -50,
        width: 200,
        height: 200,
        borderRadius: '50%',
        background: 'rgba(31,158,140,0.05)',
        pointerEvents: 'none'
      }}></div>
      <div style={{
        position: 'absolute',
        bottom: -80,
        left: -80,
        width: 250,
        height: 250,
        borderRadius: '50%',
        background: 'rgba(168,72,28,0.05)',
        pointerEvents: 'none'
      }}></div>

      {/* Header */}
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

      {/* Avatar / Sketch */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 14
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
            fontSize: 16,
            fontWeight: 600,
            color: 'var(--parchment)'
          }}>
            Farmer Identity
          </div>
          <div style={{
            fontFamily: "'IBM Plex Mono', monospace",
            fontSize: 10,
            color: 'rgba(241,234,216,0.4)'
          }}>
            DTF-000001
          </div>
        </div>
      </div>

      {/* Details Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: '4px 16px',
        fontSize: 12
      }}>
        <div>
          <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>Country</span>
          <div style={{ color: 'var(--parchment)', fontWeight: 500 }}>Malawi</div>
        </div>
        <div>
          <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>District</span>
          <div style={{ color: 'var(--parchment)', fontWeight: 500 }}>—</div>
        </div>
        <div>
          <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>Enterprise</span>
          <div style={{ color: 'var(--parchment)', fontWeight: 500 }}>Crop / Livestock</div>
        </div>
        <div>
          <span style={{ color: 'rgba(241,234,216,0.4)', fontSize: 10 }}>Digital ID</span>
          <div style={{ color: 'var(--twin)', fontWeight: 600, fontFamily: "'IBM Plex Mono', monospace" }}>DTF-000001</div>
        </div>
      </div>

      {/* Credit Score - Updated to show percentage */}
      <div style={{
        background: 'rgba(31,158,140,0.08)',
        borderRadius: 6,
        padding: '8px 14px'
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
          }}>82%</span>
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
            width: '82%',
            height: '100%',
            background: 'linear-gradient(90deg, var(--twin), #28b6a2)',
            borderRadius: 2
          }}></div>
        </div>
      </div>

      {/* Blockchain Verified */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: 8,
        fontSize: 11,
        color: 'var(--twin)'
      }}>
        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
          <circle cx="7" cy="7" r="6" stroke="#1f9e8c" strokeWidth="1.5"/>
          <path d="M4 7L6 9L10 5" stroke="#1f9e8c" strokeWidth="1.5" strokeLinecap="round"/>
        </svg>
        <span style={{ fontFamily: "'IBM Plex Mono', monospace", fontSize: 10 }}>
          Blockchain Verified
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
  )
}

export default DigitalTwinCard