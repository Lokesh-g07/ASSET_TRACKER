import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/useAuth'

export default function Login() {
  const { login }                   = useAuth()
  const navigate                    = useNavigate()
  const [email,    setEmail]        = useState('')
  const [password, setPassword]     = useState('')
  const [error,    setError]        = useState('')
  const [loading,  setLoading]      = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await login(email, password)
      navigate('/map')
    } catch {
      setError('Invalid credentials. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-header">
          <div className="login-logo" />
          <h1>Campus Asset Tracker</h1>
          <p>IIT Campus · Secure Access</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          {error && <div className="login-error">{error}</div>}

          <div className="field-group">
            <label>Email</label>
            <input type="email" placeholder="admin@campus.ac.in"
              value={email} onChange={e => setEmail(e.target.value)} required />
          </div>

          <div className="field-group">
            <label>Password</label>
            <input type="password" placeholder="••••••••"
              value={password} onChange={e => setPassword(e.target.value)} required />
          </div>

          <button className="btn-primary" type="submit" disabled={loading}>
            {loading ? 'Signing in…' : 'Sign In'}
          </button>
        </form>
      </div>
    </div>
  )
}