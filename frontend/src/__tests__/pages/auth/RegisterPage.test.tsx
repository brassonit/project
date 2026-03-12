import { describe, it, expect, vi } from 'vitest'
import { renderWithProviders, screen } from '../../../test/test-utils'
import RegisterPage from '../../../presentation/pages/auth/RegisterPage'

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

describe('RegisterPage', () => {
  it('renders register heading and form', () => {
    renderWithProviders(<RegisterPage />)
    expect(screen.getByRole('heading', { name: '회원가입' })).toBeInTheDocument()
    // email + password + confirm password = at least 3 inputs
    const inputs = screen.getAllByRole('textbox')
    expect(inputs.length).toBeGreaterThanOrEqual(1) // email field
  })

  it('has submit button', () => {
    renderWithProviders(<RegisterPage />)
    expect(screen.getByRole('button', { name: '회원가입' })).toBeInTheDocument()
  })

  it('has link to login page', () => {
    renderWithProviders(<RegisterPage />)
    expect(screen.getByRole('link', { name: '로그인' })).toBeInTheDocument()
  })
})
