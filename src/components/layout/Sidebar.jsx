import { NavLink } from 'react-router-dom'
import { Map, Bell, Package, Shield, Radio, FileText, LogOut, Cpu } from 'lucide-react'
import { useAuth }   from '../../context/useAuth'
import { useAlerts } from '../../hooks/useAlerts'

const NAV = [
  { icon: Map,      label: 'Live Map',   path: '/map'       },
  { icon: Bell,     label: 'Alerts',     path: '/alerts'    },
  { icon: Package,  label: 'Assets',     path: '/assets'    },
  { icon: Shield,   label: 'Geofences',  path: '/geofences' },
  { icon: Radio,    label: 'Gateways',   path: '/gateways'  },
  { icon: FileText, label: 'Reports',    path: '/reports'   },
]

export default function Sidebar() {
  const { logout }  = useAuth()
  const { alerts }  = useAlerts()
  const critCount   = alerts.filter(a => a.type === 'critical').length

  return (
    <aside className="sidebar">
      <div className="sidebar-logo"><Cpu size={20} /></div>

      <nav className="sidebar-nav">
        {NAV.map((item) => {
          const NavIcon = item.icon
          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) => `nav-item${isActive ? ' active' : ''}`}
            >
              <NavIcon size={20} />
              {item.label === 'Alerts' && critCount > 0 && (
                <span className="nav-badge">{critCount}</span>
              )}
              <span className="nav-tooltip">{item.label}</span>
            </NavLink>
          )
        })}
      </nav>

      <button className="nav-item logout-btn" onClick={logout}>
        <LogOut size={20} />
        <span className="nav-tooltip">Logout</span>
      </button>
    </aside>
  )
}