import { MapContainer, TileLayer } from 'react-leaflet'

const ZONES = [
  { id:'z1', name:'Main Hall',           color:'#6366f1', assets:12 },
  { id:'z2', name:'Engineering Block',   color:'#22c55e', assets:8  },
  { id:'z3', name:'Labs (Restricted)',   color:'#ef4444', assets:5  },
  { id:'z4', name:'Library',             color:'#f59e0b', assets:7  },
  { id:'z5', name:'Admin Block',         color:'#8b5cf6', assets:3  },
]

export default function Geofences() {
  return (
    <div className="page">
      <div className="page-header">
        <h2>Geofence Manager</h2>
        <button className="btn-primary small">+ New Zone</button>
      </div>

      <div className="geofence-layout">
        <div className="zone-list">
          {ZONES.map(z => (
            <div key={z.id} className="zone-card">
              <span className="zone-color" style={{ background: z.color }} />
              <div className="zone-info">
                <span className="zone-name">{z.name}</span>
                <span className="zone-assets">{z.assets} assets tracked</span>
              </div>
              <button className="btn-ghost small">Edit</button>
            </div>
          ))}
        </div>

        <div className="geofence-map">
          <MapContainer
            center={[11.0168, 76.9558]} zoom={17}
            style={{ height: '100%', width: '100%', borderRadius: '8px' }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="© OpenStreetMap"
            />
          </MapContainer>
        </div>
      </div>
    </div>
  )
}