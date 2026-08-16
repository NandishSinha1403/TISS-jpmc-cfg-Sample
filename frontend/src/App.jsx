import { useEffect, useState } from 'react'
import tissLogo from './assets/tiss-logo.svg'
import { apiFetch } from './api/client'
import './App.css'

function App() {
  const [status, setStatus] = useState('checking...')

  useEffect(() => {
    apiFetch('/health')
      .then((data) => setStatus(data.status))
      .catch(() => setStatus('unreachable'))
  }, [])

  return (
    <section id="center">
      <img src={tissLogo} alt="TISS logo" width="120" />
      <h1>TISS Learning Platform</h1>
      <p>Backend status: <strong>{status}</strong></p>
    </section>
  )
}

export default App
