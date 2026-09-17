import { useEffect, useState } from 'react'
import { ref, onValue } from 'firebase/database'
import { db } from '../firebase/config'

const MOCK = [
  { id:'a1', type:'critical', title:'Asset left campus',  detail:'MacBook #MB-04 · Admin gate',   time:'2m ago'  },
  { id:'a2', type:'warning',  title:'Geofence breach',    detail:'Projector #PJ-12 · Main Hall',  time:'8m ago'  },
  { id:'a3', type:'info',     title:'Battery low',        detail:'Beacon GW-07 · Eng Block',      time:'15m ago' },
]

export function useAlerts(useMock = true) {
  const [alerts, setAlerts] = useState(MOCK)

  useEffect(() => {
    if (useMock) return
    const unsub = onValue(ref(db, 'alerts'), (snap) => {
      const data = snap.val()
      if (data) {
        const list = Object.entries(data).map(([id, v]) => ({ id, ...v }))
        setAlerts(list.filter(a => !a.acknowledged))
      }
    })
    return unsub
  }, [useMock])

  return { alerts }
}