import React, { createContext, useContext, useMemo, useState } from 'react'

export type VehicleContext = { make?: string; model?: string; year?: number }
export type Source = { text: string; source?: string; page?: number; score?: number }
export type QueryResponse = { answer: string; sources: Source[]; suggested_actions?: string[] }

export type ApiCtx = {
  baseUrl: string
  setBaseUrl: (v: string) => void
  vehicle?: VehicleContext
  setVehicle: (v?: VehicleContext) => void
  queryRag: (q: string) => Promise<QueryResponse>
  getDiagnostic: (code: string) => Promise<any>
  getVehicleInfo: (make: string, model: string, year: number) => Promise<any>
  uploadPdfs: (files: File[]) => Promise<{ ingested_count: number; files: string[] }>
}

const Context = createContext<ApiCtx | undefined>(undefined)

export function ApiProvider({ children }: { children: React.ReactNode }) {
  const [baseUrl, setBaseUrl] = useState<string>(
    import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  )
  const [vehicle, setVehicle] = useState<VehicleContext | undefined>(undefined)

  const value = useMemo<ApiCtx>(() => ({
    baseUrl,
    setBaseUrl,
    vehicle,
    setVehicle,
    async queryRag(q: string) {
      const resp = await fetch(`${baseUrl}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: q, top_k: 4, vehicle }),
      })
      if (!resp.ok) throw new Error(await resp.text())
      return resp.json()
    },
    async getDiagnostic(code: string) {
      const resp = await fetch(`${baseUrl}/diagnostic-codes/${encodeURIComponent(code)}`)
      if (!resp.ok) throw new Error(await resp.text())
      return resp.json()
    },
    async getVehicleInfo(make: string, model: string, year: number) {
      const resp = await fetch(`${baseUrl}/vehicle-info/${encodeURIComponent(make)}/${encodeURIComponent(model)}/${year}`)
      if (!resp.ok) throw new Error(await resp.text())
      return resp.json()
    },
    async uploadPdfs(files: File[]) {
      const form = new FormData()
      for (const f of files) form.append('files', f)
      const resp = await fetch(`${baseUrl}/upload-documents`, { method: 'POST', body: form })
      if (!resp.ok) throw new Error(await resp.text())
      return resp.json()
    }
  }), [baseUrl, vehicle])

  return <Context.Provider value={value}>{children}</Context.Provider>
}

export function useApi(): ApiCtx {
  const ctx = useContext(Context)
  if (!ctx) throw new Error('useApi must be used within ApiProvider')
  return ctx
}
