import { AlertTriangle, AlertCircle, Info, CheckCircle } from 'lucide-react'
import { useAlerts } from '../hooks/useAlerts'

const ICON = { critical: AlertTriangle, warning: AlertCircle, info: Info }

export default function Alerts() {
  const { alerts } = useAlerts()

  return (
    <div className="page">
      <div className="page-header">
        <h2>Active Alerts</h2>
        {alerts.length > 0 && <span className="badge-count">{alerts.length}</span>}
      </div>

      <div className="alerts-list">
        {alerts.length === 0 && (
          <div className="empty-state">
            <CheckCircle size={48} color="#22c55e" />
            <p>No active alerts — all clear</p>
          </div>
        )}
        {alerts.map(al => {
          const Icon = ICON[al.type] || Info
          return (
            <div key={al.id} className={`alert-card ${al.type}`}>
              <div className={`alert-icon-wrap ${al.type}`}><Icon size={20} /></div>
              <div className="alert-body">
                <span className="alert-title">{al.title}</span>
                <span className="alert-detail">{al.detail}</span>
                <span className="alert-time">{al.time}</span>
              </div>
              <button className="btn-acknowledge">Acknowledge</button>
            </div>
          )
        })}
      </div>
    </div>
  )
}