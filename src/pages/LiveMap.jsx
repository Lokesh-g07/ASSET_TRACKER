import { useState } from 'react'
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import { useAssets } from '../hooks/useAssets'
import { useAlerts } from '../hooks/useAlerts'

// Fix Leaflet icon paths broken by Vite
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl:       'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl:     'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
})

const STATUS_COLOR = {
  online: '#22c55e', alert: '#ef4444',
  breach: '#f59e0b', idle:  '#64748b',
}

function colorIcon(color) {
  return L.divIcon({
    className: '',
    html: `<div style="width:12px;height:12px;border-radius:50%;
            background:${color};border:2px solid #fff;
            box-shadow:0 0 8px ${color}"></div>`,
    iconSize: [12, 12], iconAnchor: [6, 6],
  })
}

const ALERT_BULLET = { critical: '🔴', warning: '🟡', info: '🔵' }

export default function LiveMap() {
  const { assets }  = useAssets()
  const { alerts }  = useAlerts()
  const [tab, setTab]         = useState('all')
  const [mapMode, setMapMode] = useState('map')

  const onlineCount = assets.filter(a => a.status === 'online').length
  const alertCount  = alerts.length
  const breachCount = assets.filter(a => a.status === 'breach').length

  const listAssets = tab === 'alerts'
    ? assets.filter(a => a.status === 'alert' || a.status === 'breach')
    : assets

  return (
    <div className="livemap-page">

      {/* ── Stat bar ── */}
      <div className="stat-bar">
        <div className="stat-card">
          <span className="stat-label">Total Assets</span>
          <span className="stat-value">{assets.length}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Online Now</span>
          <span className="stat-value green">{onlineCount}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Active Alerts</span>
          <span className="stat-value red">{alertCount}</span>
        </div>
        <div className="stat-card">
          <span className="stat-label">Geofence Breaches</span>
          <span className="stat-value amber">{breachCount}</span>
        </div>
        <div className="stat-right">
          <span className="live-badge">● Live</span>
          <span className="campus-label">IIT Campus</span>
        </div>
      </div>

      {/* ── Split view ── */}
      <div className="map-split">

        {/* Map column */}
        <div className="map-container-wrap">
          <div className="map-view-tabs">
            {['map', 'heatmap', 'floorplan'].map(m => (
              <button
                key={m}
                className={`map-tab${mapMode === m ? ' active' : ''}`}
                onClick={() => setMapMode(m)}
              >
                {m.charAt(0).toUpperCase() + m.slice(1)}
              </button>
            ))}
          </div>

          <MapContainer
            center={[11.0168, 76.9558]}
            zoom={17}
            zoomControl={false}
            style={{ flex: 1, height: '100%' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="© OpenStreetMap"
            />
            {assets.map(a => (
              <Marker
                key={a.id}
                position={[a.lat, a.lng]}
                icon={colorIcon(STATUS_COLOR[a.status] || '#64748b')}
              >
                <Popup>
                  <strong>{a.name}</strong><br />
                  Location: {a.location}<br />
                  Status: {a.status}<br />
                  Battery: {a.battery}%
                </Popup>
              </Marker>
            ))}
          </MapContainer>
        </div>

        {/* Right panel */}
        <div className="asset-panel">
          <div className="panel-header">
            <span className="panel-title">Assets</span>
            <div className="panel-tabs">
              {['all', 'alerts', 'nearby'].map(t => (
                <button
                  key={t}
                  className={`panel-tab${tab === t ? ' active' : ''}`}
                  onClick={() => setTab(t)}
                >
                  {t.charAt(0).toUpperCase() + t.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Alert rows */}
          {tab === 'all' && alerts.length > 0 && (
            <div className="alert-summary">
              {alerts.map(al => (
                <div key={al.id} className={`alert-row ${al.type}`}>
                  <span>{ALERT_BULLET[al.type]}</span>
                  <div className="alert-info">
                    <span className="alert-title">{al.title}</span>
                    <span className="alert-detail">{al.detail} · {al.time}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {/* Asset list */}
          <div className="asset-list">
            {listAssets.map(a => (
              <div key={a.id} className={`asset-row ${a.status}`}>
                <div className="asset-avatar">{a.name[0]}</div>
                <div className="asset-info">
                  <span className="asset-name">{a.name}</span>
                  <span className="asset-loc">{a.location}</span>
                </div>
                <span className={`asset-status-dot ${a.status}`} />
              </div>
            ))}
          </div>

          {/* Footer */}
          <div className="panel-footer">
            <span>Total {assets.length}</span>
            <span className="green">Online {onlineCount}</span>
            <span className="red">Alerts {alertCount}</span>
            <span className="amber">Breaches {breachCount}</span>
          </div>
        </div>
      </div>
    </div>
  )
}