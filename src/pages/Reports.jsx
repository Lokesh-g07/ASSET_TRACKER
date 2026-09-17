import { useState } from 'react'
import { Download } from 'lucide-react'

const INCIDENTS = [
  { id:'i1', asset:'MacBook #MB-04',   event:'Left campus boundary', zone:'Admin Gate', time:'2026-04-14 13:45', severity:'critical' },
  { id:'i2', asset:'Projector #PJ-12', event:'Geofence breach',      zone:'Main Hall',  time:'2026-04-14 13:39', severity:'warning'  },
  { id:'i3', asset:'Beacon GW-07',     event:'Low battery (18%)',    zone:'Eng Block',  time:'2026-04-14 13:32', severity:'info'     },
]

function exportCSV(rows) {
  const headers = ['Asset','Event','Zone','Time','Severity']
  const csv = [headers, ...rows.map(r => [r.asset, r.event, r.zone, r.time, r.severity])]
    .map(r => r.join(',')).join('\n')
  const a = Object.assign(document.createElement('a'), {
    href: URL.createObjectURL(new Blob([csv], { type:'text/csv' })),
    download: `incident_log_${Date.now()}.csv`,
  })
  a.click()
}

export default function Reports() {
  const [range, setRange] = useState('today')

  return (
    <div className="page">
      <div className="page-header">
        <h2>Reports &amp; Incident Log</h2>
        <div className="page-controls">
          <select className="filter-select" value={range} onChange={e => setRange(e.target.value)}>
            <option value="today">Today</option>
            <option value="week">This Week</option>
            <option value="month">This Month</option>
          </select>
          <button className="btn-primary small" onClick={() => exportCSV(INCIDENTS)}>
            <Download size={14} /> Export CSV
          </button>
        </div>
      </div>

      <div className="table-wrap">
        <table className="asset-table">
          <thead>
            <tr><th>Asset</th><th>Event</th><th>Zone</th><th>Time</th><th>Severity</th></tr>
          </thead>
          <tbody>
            {INCIDENTS.map(inc => (
              <tr key={inc.id}>
                <td><strong>{inc.asset}</strong></td>
                <td>{inc.event}</td>
                <td>{inc.zone}</td>
                <td style={{ color: 'var(--text-2)', fontSize: 12 }}>{inc.time}</td>
                <td><span className={`status-badge ${inc.severity}`}>{inc.severity}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}