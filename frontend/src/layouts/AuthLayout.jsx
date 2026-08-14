import React from 'react'
import { Outlet } from 'react-router-dom'

function AuthLayout() {
  return (
    <div style={{ 
      minHeight: '100vh', 
      display: 'flex', 
      alignItems: 'center', 
      justifyContent: 'center',
      background: '#141F0F'
    }}>
      <Outlet />
    </div>
  )
}

export default AuthLayout