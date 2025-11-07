import React, { useState } from 'react'

type Payload = {
  n: number
  ritual_mu: number
  trade_mu: number
  symbol_mu: number
  hier_mu: number
  sigma: number
  seed: number
}

export default function App() {
  const [state, setState] = useState<Payload>({
    n: 400, ritual_mu: 6.7, trade_mu: 5.9, symbol_mu: 6.3, hier_mu: 6.1, sigma: 1.8, seed: 42
  })
  const [result, setResult] = useState<{nlis_mean:number, crm_mean:number} | null>(null)
  const [loading, setLoading] = useState(false)
  const apiBase = import.meta.env.VITE_API_BASE || "http://localhost:8000"

  const run = async () => {
    setLoading(true)
    try {
      const res = await fetch(`${apiBase}/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(state)
      })
      const data = await res.json()
      setResult(data)
    } finally {
      setLoading(false)
    }
  }

  const ctl = (k: keyof Payload) => (e: React.ChangeEvent<HTMLInputElement>) => {
    const v = e.target.type === 'range' || e.target.type === 'number' ? Number(e.target.value) : e.target.value
    setState(s => ({...s, [k]: v} as any))
  }

  return (
    <div style={{maxWidth: 900, margin: '40px auto', fontFamily: 'system-ui, -apple-system, Segoe UI, Roboto'}}>
      <h1>VerbaTerra Dashboard</h1>
      <p>React + Vite front-end talking to a FastAPI backend. Adjust inputs and run.</p>

      <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:16}}>
        <label>n
          <input type="number" min={50} max={5000} value={state.n} onChange={ctl('n')} />
        </label>
        <label>Ritual μ
          <input type="range" min={1} max={10} step={0.1} value={state.ritual_mu} onChange={ctl('ritual_mu')} />
        </label>
        <label>Trade μ
          <input type="range" min={1} max={10} step={0.1} value={state.trade_mu} onChange={ctl('trade_mu')} />
        </label>
        <label>Symbolism μ
          <input type="range" min={1} max={10} step={0.1} value={state.symbol_mu} onChange={ctl('symbol_mu')} />
        </label>
        <label>Hierarchy μ
          <input type="range" min={1} max={10} step={0.1} value={state.hier_mu} onChange={ctl('hier_mu')} />
        </label>
        <label>σ
          <input type="range" min={0.5} max={3} step={0.1} value={state.sigma} onChange={ctl('sigma')} />
        </label>
        <label>Seed
          <input type="number" min={0} max={10000} value={state.seed} onChange={ctl('seed')} />
        </label>
      </div>

      <button onClick={run} disabled={loading} style={{marginTop:16, padding:'8px 16px'}}>
        {loading ? 'Running…' : 'Run Simulation'}
      </button>

      {result && (
        <div style={{marginTop:24, padding:16, border:'1px solid #ddd', borderRadius:8}}>
          <h3>Results</h3>
          <p><strong>NLIS (mean):</strong> {result.nlis_mean.toFixed(2)}</p>
          <p><strong>CRM (mean):</strong> {result.crm_mean.toFixed(2)}</p>
          <p style={{opacity:0.7}}>Try hovering sliders and re-run to compare.</p>
        </div>
      )}
    </div>
  )
}
