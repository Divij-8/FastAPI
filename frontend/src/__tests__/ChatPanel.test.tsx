import { render, screen } from '@testing-library/react'
import React from 'react'
import ChatPanel from '../components/ChatPanel'
import { ApiProvider } from '../context/ApiContext'

test('renders chat panel heading', () => {
  render(<ApiProvider><ChatPanel /></ApiProvider>)
  expect(screen.getByText(/Chat/i)).toBeInTheDocument()
})
