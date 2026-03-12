import { describe, it, expect, vi } from 'vitest'
import { renderWithProviders, screen } from '../../../test/test-utils'
import LoginPage from '../../../presentation/pages/auth/LoginPage'

vi.mock('../../../infrastructure/auth/useAuth', () => ({
  useAuth: vi.fn().mockReturnValue({
    user: null,
    isLoading: false,
    isAdmin: false,
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
  }),
}))

describe('LoginPage', () => {
  it('renders login heading and form fields', () => {
    renderWithProviders(<LoginPage />)
    expect(screen.getByRole('heading', { name: '로그인' })).toBeInTheDocument()
    expect(screen.getByRole('textbox')).toBeInTheDocument() // email input
  })

  it('has submit button', () => {
    renderWithProviders(<LoginPage />)
    expect(screen.getByRole('button', { name: '로그인' })).toBeInTheDocument()
  })

  it('has link to register page', () => {
    renderWithProviders(<LoginPage />)
    expect(screen.getByRole('link', { name: '회원가입' })).toBeInTheDocument()
  })
})
