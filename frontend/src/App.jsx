import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import Farmers from './pages/Farmers'
import AddFarmer from './pages/AddFarmer'
import FarmProfile from './pages/FarmProfile'
import FarmerSearch from './pages/FarmerSearch'
import FarmerDigitalTwin from './pages/FarmerDigitalTwin'
import VerificationDashboard from './pages/VerificationDashboard'
import Loans from './pages/Loans'
import Harvest from './pages/Harvest'
import Reports from './pages/Reports'
import Map from './pages/Map'
import NotFound from './pages/NotFound'
import MainLayout from './layouts/MainLayout'
import AuthLayout from './layouts/AuthLayout'

function App() {
  return (
    <Router>
      <Routes>
        {/* Auth routes (no navbar) */}
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<Login />} />
        </Route>

        {/* Main routes (with navbar) */}
        <Route element={<MainLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/farmers" element={<Farmers />} />
          <Route path="/farmers/add" element={<AddFarmer />} />
          <Route path="/farmers/search" element={<FarmerSearch />} />
          <Route path="/farmers/:id/twin" element={<FarmerDigitalTwin />} />
          <Route path="/farmers/:id" element={<FarmProfile />} />
          <Route path="/farmers/:id/verification" element={<VerificationDashboard />} />
          <Route path="/loans" element={<Loans />} />
          <Route path="/harvest" element={<Harvest />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/map" element={<Map />} />
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </Router>
  )
}

export default App