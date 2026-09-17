import { useState } from 'react'
import { Search } from 'lucide-react'
import { useAssets } from '../hooks/useAssets'

export default function Assets() {
  const { assets }          = useAssets()
  const [search, setSearch] = useState('')
  const [filter, setFilter] = useState('all')

  const filtered = assets.filter(a => {
    const q = a.name.toLowerCase().includes(search.toLowerCase())
    const f = filter === 'all' || a.status === filter
    return q && f
  })

  return (
    <div className="page">
      <div className="page-header">
        <h2>Asset Registry</h2>
        <div className="page-controls">
          <div className="search-box">
            <Search size={15} />
            <input placeholder="Search assets…"
              value={search} onChange={e => setSearch(e.target.value)} />
          </div>
          <select className="filter-select" value={filter} onChange={e => setFilter(e.target.value)}>
            <option value="all">All Status</option>
            <option value="online">Online</option>
            <option value="alert">Alert</option>
            <option value="breach">Breach</option>
            <option value="idle">Idle</option>
          </select>
        </div>
      </div>

      <div className="table-wrap">
        <table className="asset-table">
          <thead>
            <tr>
              <th>Asset</th><th>Category</th><th>Location</th>
              <th>Battery</th><th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(a => (
              <tr key={a.id}>
                <td><strong>{a.name}</strong></td>
                <td>{a.category}</td>
                <td>{a.location}</td>
                <td>
                  <div className="battery-bar">
                    <div className="battery-fill" style={{
                      width: `${a.battery}%`,
                      background: a.battery > 50 ? '#22c55e' : a.battery > 20 ? '#f59e0b' : '#ef4444'
                    }} />
                  </div>
                  <span className="battery-label">{a.battery}%</span>
                </td>
                <td><span className={`status-badge ${a.status}`}>{a.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}