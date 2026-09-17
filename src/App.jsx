import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom'
import Sidebar   from './components/layout/Sidebar'
import Login     from './pages/Login'
import LiveMap   from './pages/LiveMap'
import Assets    from './pages/Assets'
import Alerts    from './pages/Alerts'
import Geofences from './pages/Geofences'
import Gateways  from './pages/Gateways'
import Reports   from './pages/Reports'
function ProtectedLayout() {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="page-content">
        <Outlet />
      </div>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<ProtectedLayout />}>
          <Route index element={<Navigate to="/map" replace />} />
          <Route path="/map"        element={<LiveMap />} />
          <Route path="/assets"     element={<Assets />} />
          <Route path="/alerts"     element={<Alerts />} />
          <Route path="/geofences"  element={<Geofences />} />
          <Route path="/gateways"   element={<Gateways />} />
          <Route path="/reports"    element={<Reports />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}