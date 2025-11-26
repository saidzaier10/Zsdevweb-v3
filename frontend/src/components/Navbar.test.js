import { mount } from '@vue/test-utils'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import Navbar from './Navbar.vue'
import { useAuthStore } from '../stores/auth'

// Mock router
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/login', component: { template: '<div>Login</div>' } },
        { path: '/register', component: { template: '<div>Register</div>' } },
        { path: '/portfolio', component: { template: '<div>Portfolio</div>' } },
        { path: '/devis', component: { template: '<div>Devis</div>' } },
        { path: '/mes-devis', component: { template: '<div>Mes Devis</div>' } },
        { path: '/admin/devis', component: { template: '<div>Admin Devis</div>' } },
        { path: '/contact', component: { template: '<div>Contact</div>' } },
    ]
})

describe('Navbar', () => {
    beforeEach(() => {
        setActivePinia(createPinia())
    })

    it('shows login/register when not authenticated', async () => {
        const wrapper = mount(Navbar, {
            global: {
                plugins: [router]
            }
        })

        expect(wrapper.text()).toContain('Connexion')
        expect(wrapper.text()).toContain('Inscription')
        expect(wrapper.text()).not.toContain('Déconnexion')
    })

    it('shows user info and logout when authenticated', async () => {
        const store = useAuthStore()
        store.user = { username: 'TestUser' }
        store.isAuthenticated = true

        const wrapper = mount(Navbar, {
            global: {
                plugins: [router]
            }
        })

        expect(wrapper.text()).toContain('TestUser')
        expect(wrapper.text()).toContain('Déconnexion')
        expect(wrapper.text()).not.toContain('Connexion')
    })

    it('toggles mobile menu', async () => {
        const wrapper = mount(Navbar, {
            global: {
                plugins: [router]
            }
        })

        // Menu should be closed initially (hidden on desktop, but we check state)
        // Note: visibility checks are hard in jsdom without real layout, so we check v-if existence
        expect(wrapper.find('.md\\:hidden.border-t').exists()).toBe(false)

        // Click toggle button
        await wrapper.find('button[aria-label="Menu"]').trigger('click')

        // Menu should be open
        expect(wrapper.find('.md\\:hidden.border-t').exists()).toBe(true)
    })
})
