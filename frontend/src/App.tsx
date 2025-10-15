import React from 'react'
import { ApiProvider } from './context/ApiContext'
import ChatPanel from './components/ChatPanel'
import FileUpload from './components/FileUpload'
import VehicleForm from './components/VehicleForm'
import DiagnosticLookup from './components/DiagnosticLookup'

export default function App() {
  return (
    <ApiProvider>
      <div className="min-h-screen w-full max-w-6xl mx-auto p-4 space-y-4">
        <header className="flex items-center justify-between">
          <h1 className="text-2xl font-bold">Vehicle Service RAG Assistant</h1>
        </header>
        <section className="grid md:grid-cols-3 gap-4">
          <div className="md:col-span-2 space-y-4">
            <ChatPanel />
            <FileUpload />
          </div>
          <div className="space-y-4">
            <VehicleForm />
            <DiagnosticLookup />
          </div>
        </section>
      </div>
    </ApiProvider>
  )
}
