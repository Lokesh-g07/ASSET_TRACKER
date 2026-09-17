import { createContext } from 'react'

/**
 * The React context object for authentication state.
 * Consumed via the useAuth hook (context/useAuth.js).
 */
export const AuthContext = createContext(null)
