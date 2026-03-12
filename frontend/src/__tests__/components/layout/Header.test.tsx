import { describe, it, expect, vi, beforeEach } from 'vitest'
import { renderWithProviders, screen, userEvent } from '../../../test/test-utils'
import Header from '../../../presentation/layouts/Header'

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

import { useAuth } from '../../../infrastructure/auth/useAuth'
const mockedUseAuth = vi.mocked(useAuth)

describe('Header', () => {
  beforeEach(() => {
    mockedUseAuth.mockReturnValue({
      user: null,
      isLoading: false,
      isAdmin: false,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
    })
  })

  it('renders navigation links', () => {
    renderWithProviders(<Header />)
    expect(screen.getByText('BRASS ON IT')).toBeInTheDocument()
    expect(screen.getByText('HOME')).toBeInTheDocument()
    expect(screen.getByText('주요공연')).toBeInTheDocument()
    expect(screen.getByText('섭외대행')).toBeInTheDocument()
    expect(screen.getByText('문의하기')).toBeInTheDocument()
  })

  it('shows login/register when not authenticated', () => {
    renderWithProviders(<Header />)
    expect(screen.getByText('로그인')).toBeInTheDocument()
    expect(screen.getByText('회원가입')).toBeInTheDocument()
  })

  it('shows user info and logout when authenticated', () => {
    mockedUseAuth.mockReturnValue({
      user: { id: '1', email: 'test@test.com', role: 'customer', is_verified: true, created_at: '' },
      isLoading: false,
      isAdmin: false,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
    })

    renderWithProviders(<Header />)
    expect(screen.getByText('test@test.com')).toBeInTheDocument()
    expect(screen.getByText('로그아웃')).toBeInTheDocument()
  })

  it('shows admin link for admin users', () => {
    mockedUseAuth.mockReturnValue({
      user: { id: '1', email: 'admin@test.com', role: 'admin', is_verified: true, created_at: '' },
      isLoading: false,
      isAdmin: true,
      login: vi.fn(),
      register: vi.fn(),
      logout: vi.fn(),
    })

    renderWithProviders(<Header />)
    expect(screen.getByText('관리자')).toBeInTheDocument()
  })

  it('toggles mobile menu', async () => {
    renderWithProviders(<Header />)
    const user = userEvent.setup()
    const menuButton = screen.getByLabelText('메뉴 열기')

    await user.click(menuButton)
    expect(screen.getByText('대중가수')).toBeInTheDocument()
    expect(screen.getByText('댄서')).toBeInTheDocument()
    expect(screen.getByText('뮤지션')).toBeInTheDocument()
    expect(screen.getByText('연주자')).toBeInTheDocument()
    expect(screen.getByText('오케스트라')).toBeInTheDocument()
  })
})
