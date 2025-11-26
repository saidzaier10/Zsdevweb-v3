import { setActivePinia, createPinia } from 'pinia'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useAuthStore } from './auth'
import authAPI from '../api/auth'

// Mock the API module
vi.mock('../api/auth', () => ({
    default: {
        login: vi.fn(),
        register: vi.fn(),
        logout: vi.fn(),
        getProfile: vi.fn()
    }
}))

describe('Auth Store', () => {
    beforeEach(() => {
        setActivePinia(createPinia())
        vi.clearAllMocks()
        localStorage.clear()
    })

    it('initializes with no user', () => {
        const store = useAuthStore()
        expect(store.user).toBeNull()
        expect(store.isAuthenticated).toBe(false)
    })

    it('login sets user and tokens', async () => {
        const store = useAuthStore()
        const mockUser = { id: 1, username: 'testuser' }
        const mockTokens = { access: 'access-token', refresh: 'refresh-token' }

        authAPI.login.mockResolvedValue({
            data: {
                user: mockUser,
                tokens: mockTokens
            }
        })

        await store.login({ username: 'testuser', password: 'password' })

        expect(store.user).toEqual(mockUser)
        expect(store.accessToken).toBe(mockTokens.access)
        expect(store.isAuthenticated).toBe(true)
        expect(localStorage.getItem('accessToken')).toBe(mockTokens.access)
    })

    it('logout clears state', async () => {
        const store = useAuthStore()
        store.setTokens({ access: 'token', refresh: 'refresh' })
        store.user = { id: 1 }

        authAPI.logout.mockResolvedValue({})

        await store.logout()

        expect(store.user).toBeNull()
        expect(store.accessToken).toBeNull()
        expect(store.isAuthenticated).toBe(false)
        expect(localStorage.getItem('accessToken')).toBeNull()
    })
})
