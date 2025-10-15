import React, { useState } from 'react'
import { useApi } from '../context/ApiContext'

export default function DiagnosticLookup() {
  const { getDiagnostic } = useApi()
  const [code, setCode] = useState('P0300')
  const [data, setData] = useState<any | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function lookup() {
    setError(null)
    setLoading(true)
    try {
      const res = await getDiagnostic(code)
      setData(res)
    } catch (e: any) {
      setData(null)
      setError(e.message || 'Lookup failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="border rounded-lg p-4 bg-white shadow-sm">
      <h2 className="font-semibold mb-2">Diagnostic Code Lookup</h2>
      <div className="flex gap-2">
        <input className="flex-1 border rounded px-3 py-2" placeholder="P0xxx" value={code} onChange={e => setCode(e.target.value.toUpperCase())} />
        <button className="bg-indigo-600 text-white px-4 py-2 rounded" onClick={lookup} disabled={loading}>{loading ? 'Loading…' : 'Lookup'}</button>
      </div>
      {data && (
        <div className="mt-3 text-sm space-y-2">
          <div className="font-semibold">{data.code} - {data.name}</div>
          <div>{data.description}</div>
          <div>
            <div className="font-semibold">Symptoms</div>
            <ul className="list-disc ml-5">{(data.symptoms||[]).map((s: string, i: number) => <li key={i}>{s}</li>)}</ul>
          </div>
          <div>
            <div className="font-semibold">Possible Causes</div>
            <ul className="list-disc ml-5">{(data.possible_causes||[]).map((s: string, i: number) => <li key={i}>{s}</li>)}</ul>
          </div>
          <div>
            <div className="font-semibold">Troubleshooting Steps</div>
            <ol className="list-decimal ml-5">{(data.troubleshooting_steps||[]).map((s: string, i: number) => <li key={i}>{s}</li>)}</ol>
          </div>
        </div>
      )}
      {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
    </div>
  )
}
