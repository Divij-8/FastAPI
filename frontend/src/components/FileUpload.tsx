import React, { useRef, useState } from 'react'
import { useApi } from '../context/ApiContext'

export default function FileUpload() {
  const { uploadPdfs } = useApi()
  const inputRef = useRef<HTMLInputElement | null>(null)
  const [result, setResult] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function onUpload(files: FileList | null) {
    if (!files || files.length === 0) return
    setLoading(true)
    setError(null)
    try {
      const arr = Array.from(files)
      const res = await uploadPdfs(arr)
      setResult(`Ingested ${res.ingested_count} chunks from ${res.files.join(', ')}`)
    } catch (e: any) {
      setError(e.message || 'Upload failed')
    } finally {
      setLoading(false)
      if (inputRef.current) inputRef.current.value = ''
    }
  }

  return (
    <div className="border rounded-lg p-4 bg-white shadow-sm">
      <h2 className="font-semibold mb-2">Upload PDF Service Manuals</h2>
      <input ref={inputRef} type="file" accept="application/pdf" multiple onChange={e => onUpload(e.target.files)} />
      {loading && <div className="text-sm text-gray-600 mt-2">Uploading…</div>}
      {result && <div className="text-green-700 text-sm mt-2">{result}</div>}
      {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
    </div>
  )
}
