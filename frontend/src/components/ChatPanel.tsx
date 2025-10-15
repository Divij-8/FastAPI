import React, { useState } from 'react'
import { useApi } from '../context/ApiContext'

export default function ChatPanel() {
  const { queryRag } = useApi()
  const [input, setInput] = useState('Explain P0300 misfire diagnosis for 2018 Camry')
  const [messages, setMessages] = useState<{ role: 'user'|'assistant', content: string, sources?: any[] }[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function send() {
    if (!input.trim()) return
    setError(null)
    const userMsg = { role: 'user' as const, content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const res = await queryRag(userMsg.content)
      setMessages(prev => [...prev, { role: 'assistant', content: res.answer, sources: res.sources }])
    } catch (e: any) {
      setError(e.message || 'Failed to query')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="border rounded-lg p-4 bg-white shadow-sm">
      <h2 className="font-semibold mb-2">Chat</h2>
      <div className="h-64 overflow-y-auto space-y-3 border rounded p-3 bg-gray-50">
        {messages.map((m, i) => (
          <div key={i} className={m.role === 'user' ? 'text-right' : 'text-left'}>
            <div className={m.role === 'user' ? 'inline-block bg-blue-600 text-white px-3 py-2 rounded-lg' : 'inline-block bg-gray-200 px-3 py-2 rounded-lg'}>
              {m.content}
            </div>
            {m.role === 'assistant' && m.sources && m.sources.length > 0 && (
              <div className="mt-1 text-xs text-gray-600">
                Sources:
                <ul className="list-disc ml-5">
                  {m.sources.map((s: any, idx: number) => (
                    <li key={idx}>{s.source} p.{s.page} ({s.score?.toFixed?.(2) ?? '—'})</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
        {messages.length === 0 && (
          <div className="text-gray-500">Ask about a repair or upload a manual.</div>
        )}
      </div>
      {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
      <div className="mt-3 flex gap-2">
        <input className="flex-1 border rounded px-3 py-2" value={input} onChange={e => setInput(e.target.value)} placeholder="Describe the issue or ask a question" onKeyDown={e => e.key==='Enter' && send()} />
        <button className="bg-blue-600 text-white px-4 py-2 rounded" onClick={send} disabled={loading}>{loading ? 'Thinking…' : 'Send'}</button>
      </div>
    </div>
  )
}
