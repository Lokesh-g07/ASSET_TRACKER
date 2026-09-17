import { useEffect, useState } from 'react'
import { ref, onValue } from 'firebase/database'
import { db } from '../firebase/config'

// Mock data — swap useMock to false once your Firebase DB is live
const MOCK = [
  { id:'L-22',  name:'Laptop #L-22',     category:'Electronics', location:'Eng Block',  status:'online',  battery:87,  lat:11.0168, lng:76.9558 },
  { id:'MB-04', name:'MacBook #MB-04',   category:'Electronics', location:'Off Campus', status:'alert',   battery:23,  lat:11.0180, lng:76.9570 },
  { id:'PJ-12', name:'Projector #PJ-12', category:'Equipment',   location:'Main Hall',  status:'breach',  battery:100, lat:11.0155, lng:76.9545 },
  { id:'SV-01', name:'Server #SV-01',    category:'Electronics', location:'Labs',       status:'online',  battery:100, lat:11.0162, lng:76.9552 },
  { id:'T-08',  name:'Tablet #T-08',     category:'Electronics', location:'Library',    status:'online',  battery:61,  lat:11.0170, lng:76.9562 },
  { id:'C-03',  name:'Camera #C-03',     category:'Equipment',   location:'Admin',      status:'online',  battery:45,  lat:11.0175, lng:76.9568 },
  { id:'SC-03', name:'Scanner #SC-03',   category:'Equipment',   location:'Library',    status:'idle',    battery:72,  lat:11.0171, lng:76.9563 },
]

export function useAssets(useMock = true) {
  const [assets, setAssets]   = useState(useMock ? MOCK : [])
  const [loading, setLoading] = useState(!useMock)

  useEffect(() => {
    if (useMock) return
    const unsub = onValue(ref(db, 'assets'), (snap) => {
      const data = snap.val()
      if (data) setAssets(Object.entries(data).map(([id, v]) => ({ id, ...v })))
      setLoading(false)
    })
    return unsub
  }, [useMock])

  return { assets, loading }
}