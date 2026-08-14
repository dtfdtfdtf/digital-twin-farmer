import React from 'react'
import { Link } from 'react-router-dom'
import DigitalTwinCard from '../components/DigitalTwinCard'

function Home() {
  return (
    <div>
      {/* Hero Section */}
      <section style={{
        background: 'radial-gradient(1200px 500px at 15% -10%, var(--canopy-2), var(--canopy) 60%)',
        color: 'var(--parchment)',
        padding: '80px 0',
        overflow: 'hidden'
      }}>
        <div className="wrap">
          <div style={{
            display: 'grid',
            gridTemplateColumns: '1.05fr .95fr',
            gap: 56,
            alignItems: 'center'
          }}>
            {/* Left side - Text */}
            <div>
              <span style={{
                fontFamily: "'IBM Plex Mono', monospace",
                fontSize: 12.5,
                letterSpacing: '.14em',
                textTransform: 'uppercase',
                color: 'var(--twin)',
                display: 'flex',
                alignItems: 'center',
                gap: 10,
                marginBottom: 22
              }}>
                <span style={{
                  width: 7,
                  height: 7,
                  borderRadius: '50%',
                  background: 'var(--twin)',
                  boxShadow: '0 0 0 4px var(--twin-dim)'
                }}></span>
                Agricultural Finance Platform · Malawi
              </span>
              <h1 style={{
                fontSize: 'clamp(34px, 4.6vw, 58px)',
                lineHeight: 1.04,
                fontWeight: 600
              }}>
                What a farmer can<br /><em style={{ fontStyle: 'normal', color: 'var(--twin)' }}>produce</em> matters more<br />than what they <em style={{ fontStyle: 'normal', color: 'var(--twin)' }}>own</em>.
              </h1>
              <p style={{
                marginTop: 22,
                fontSize: 17,
                lineHeight: 1.65,
                maxWidth: '46ch',
                color: 'rgba(241,234,216,.78)'
              }}>
                Digital Twin Farmer turns satellite data, soil sensors and repayment history into a verifiable, portable credit identity — so smallholders can borrow against their potential, not their title deed.
              </p>
              <div style={{ display: 'flex', gap: 14, marginTop: 32 }}>
                <Link to="/farmers/search" className="btn btn-primary">View the live twin →</Link>
                <Link to="#" className="btn btn-ghost" style={{ borderColor: 'rgba(241,234,216,.3)', color: 'var(--parchment)' }}>Read the case for financing</Link>
              </div>
            </div>

            {/* Right side - Physical Farm + Digital Twin Card */}
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: 16,
              alignItems: 'stretch'
            }}>
              {/* Physical Farm - Left */}
              <div style={{
                background: 'linear-gradient(180deg, #2b3a1f, #1a2712)',
                borderRadius: '12px',
                border: '1px solid rgba(241,234,216,.14)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                overflow: 'hidden',
                position: 'relative',
                aspectRatio: '1/1',
                minHeight: '380px',
                maxHeight: '380px'
              }}>
                <svg viewBox="0 0 300 300" style={{ width: '100%', height: '100%' }}>
                  <rect width="300" height="300" fill="#233420"/>
                  <circle cx="240" cy="55" r="26" fill="#d4a63a" opacity="0.85"/>
                  {Array.from({length:7}).map((_, i) => (
                    <rect key={i} x="20" y={90+i*24} width="220" height="14" rx="2" fill={i%2===0?'#3c5a2e':'#456a34'}/>
                  ))}
                  <rect x="30" y="240" width="46" height="34" fill="#5a4632"/>
                  <polygon points="26,240 53,218 80,240" fill="#7a5a36"/>
                </svg>

                {/* Scanline Animation - moving from top to bottom */}
                <div style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  height: '2px',
                  background: 'var(--twin)',
                  boxShadow: '0 0 18px 3px rgba(31,158,140,.65)',
                  animation: 'sweepVertical 6s ease-in-out infinite'
                }}></div>

                <span style={{
                  position: 'absolute',
                  bottom: 12,
                  fontFamily: "'IBM Plex Mono', monospace",
                  fontSize: 10,
                  letterSpacing: '.08em',
                  textTransform: 'uppercase',
                  padding: '4px 12px',
                  background: 'rgba(0,0,0,.5)',
                  borderRadius: 2,
                  color: '#cfe6bd'
                }}>Physical farm</span>
              </div>

              {/* Digital Twin Card - Right */}
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                minHeight: '380px',
                maxHeight: '380px'
              }}>
                <DigitalTwinCard />
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section style={{ padding: '60px 0', background: 'var(--parchment-2)' }}>
        <div className="wrap">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 24 }}>
            <div className="card text-center">
              <div style={{ fontSize: 36, fontWeight: 700, color: 'var(--twin)' }}>+40%</div>
              <div style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Projected farmer income increase</div>
            </div>
            <div className="card text-center">
              <div style={{ fontSize: 36, fontWeight: 700, color: 'var(--soil)' }}>1,000+</div>
              <div style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Farmers with formal credit history</div>
            </div>
            <div className="card text-center">
              <div style={{ fontSize: 36, fontWeight: 700, color: 'var(--gold)' }}>MWK 50bn</div>
              <div style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Agricultural credit unlocked nationally</div>
            </div>
            <div className="card text-center">
              <div style={{ fontSize: 36, fontWeight: 700, color: 'var(--twin)' }}>15</div>
              <div style={{ color: 'var(--ink-soft)', fontSize: 14 }}>Districts Covered</div>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home