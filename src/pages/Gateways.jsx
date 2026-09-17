import { Radio } from 'lucide-react'
import { useGateways } from '../hooks/useGateways'

export default function Gateways() {
  const { gateways } = useGateways()
  const online = gateways.filter(g => g.status === 'online').length

  return (
    <div className="page">
      <div className="page-header">
        <h2>Gateway Health</h2>
        <span className="green" style={{ fontSize: 13 }}>{online} / {gateways.length} Online</span>
      </div>

      <div className="gateway-grid">
        {gateways.map(gw => (
          <div key={gw.id} className={`gateway-card ${gw.status}`}>
            <div className="gw-header">
              <Radio size={16} />
              <span className="gw-name">{gw.name}</span>
              <span className={`status-dot ${gw.status}`} />
            </div>
            <div className="gw-stats">
              <div className="gw-stat">
                <span className="gw-stat-label">RSSI</span>
                <span className="gw-stat-value">{gw.rssi != null ? `${gw.rssi} dBm` : '—'}</span>
              </div>
              <div className="gw-stat">
                <span className="gw-stat-label">Zone</span>
                <span className="gw-stat-value">{gw.zone}</span>
              </div>
              <div className="gw-stat">
                <span className="gw-stat-label">Last Ping</span>
                <span className="gw-stat-value">{gw.lastPing}</span>
              </div>
            </div>
            {gw.rssi != null && (
              <div className="rssi-bar">
                <div className="rssi-fill" style={{
                  width: `${Math.min(100, Math.max(0, (gw.rssi + 100) / 60 * 100))}%`,
                  background: gw.rssi > -60 ? '#22c55e' : gw.rssi > -80 ? '#f59e0b' : '#ef4444',
                }} />
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}