import { useEffect, useState } from 'react'
import { ref, onValue } from 'firebase/database'
import { db } from '../firebase/config'

const MOCK = [
  { id:'GW-01', name:'GW-01 Eng. Block', status:'online',  rssi:-42, lastPing:'5s ago',  zone:'Eng Block' },
  { id:'GW-03', name:'GW-03 Library',    status:'online',  rssi:-71, lastPing:'5s ago',  zone:'Library'   },
  { id:'GW-07', name:'GW-07 Admin',      status:'warning', rssi:-89, lastPing:'12s ago', zone:'Admin'     },
  { id:'GW-09', name:'GW-09 Main Hall',  status:'online',  rssi:-45, lastPing:'5s ago',  zone:'Main Hall' },
  { id:'GW-11', name:'GW-11 Labs',       status:'offline', rssi:null,lastPing:'8m ago',  zone:'Labs'      },
]

export function useGateways(useMock = true) {
  const [gateways, setGateways] = useState(MOCK)

  useEffect(() => {
    if (useMock) return
    const unsub = onValue(ref(db, 'gateways'), (snap) => {
      const data = snap.val()
      if (data) setGateways(Object.entries(data).map(([id, v]) => ({ id, ...v })))
    })
    return unsub
  }, [useMock])

  return { gateways }
}