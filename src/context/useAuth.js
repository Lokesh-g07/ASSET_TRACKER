import { useContext } from 'react'
import { AuthContext } from './authContextObject'

/**
 * Hook to access the authentication context.
 * Must be used inside an AuthProvider.
 */
export const useAuth = () => useContext(AuthContext)
