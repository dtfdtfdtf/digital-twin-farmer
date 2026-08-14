import React from 'react'
import { Link } from 'react-router-dom'

function NotFound() {
  return (
    <div className="wrap" style={{ textAlign: 'center', padding: '60px 0' }}>
      <h1 style={{ fontSize: '72px', color: 'var(--soil)' }}>404</h1>
      <h2>Page Not Found</h2>
      <p style={{ color: 'var(--ink-soft)' }}>The page you're looking for doesn't exist.</p>
      <Link to="/" className="btn btn-primary" style={{ marginTop: '20px' }}>Go Home</Link>
    </div>
  )
}

export default NotFound