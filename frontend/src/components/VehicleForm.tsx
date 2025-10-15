import React, { useState } from 'react'
import { useApi } from '../context/ApiContext'

export default function VehicleForm() {
  const { setVehicle, getVehicleInfo } = useApi()
  const [make, setMake] = useState('Toyota')
  const [model, setModel] = useState('Camry')
  const [year, setYear] = useState<number>(2018)
  const [info, setInfo] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function lookup() {
    setError(null)
    setLoading(true)
    try {
      const data = await getVehicleInfo(make, model, year)
      setInfo(data)
      setVehicle({ make, model, year })
    } catch (e: any) {
      setInfo(null)
      setError(e.message || 'Lookup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="border rounded-lg p-4 bg-white shadow-sm">
      <h2 className="font-semibold mb-2">Vehicle Context</h2>
      <div className="space-y-2">
        <input className="w-full border rounded px-3 py-2" placeholder="Make" value={make} onChange={e => setMake(e.target.value)} />
        <input className="w-full border rounded px-3 py-2" placeholder="Model" value={model} onChange={e => setModel(e.target.value)} />
        <input className="w-full border rounded px-3 py-2" placeholder="Year" type="number" value={year} onChange={e => setYear(parseInt(e.target.value || '0'))} />
        <button className="bg-green-600 text-white px-4 py-2 rounded w-full" onClick={lookup} disabled={loading}>{loading ? 'Loading…' : 'Set & Fetch Specs'}</button>
      </div>
      {info && (
        <div className="mt-3 text-sm">
          <div className="font-semibold">Specs</div>
          <pre className="bg-gray-100 p-2 rounded overflow-x-auto">{JSON.stringify(info.specs || info, null, 2)}</pre>
        </div>
      )}
      {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
    </div>
  )
}
