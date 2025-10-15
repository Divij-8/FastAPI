import { render, screen } from '@testing-library/react'
import React from 'react'
import DiagnosticLookup from '../components/DiagnosticLookup'
import { ApiProvider } from '../context/ApiContext'

test('renders diagnostic lookup inputs', () => {
  render(<ApiProvider><DiagnosticLookup /></ApiProvider>)
  expect(screen.getByText(/Diagnostic Code Lookup/i)).toBeInTheDocument()
})
