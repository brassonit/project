import { describe, it, expect, vi } from 'vitest'
import { renderWithProviders, screen } from '../../../test/test-utils'
import HomePage from '../../../presentation/pages/home/HomePage'

vi.mock('../../../application/hooks/usePerformances', () => ({
  useFeaturedPerformances: () => ({
    data: {
      performances: [
        {
          id: '1',
          title: '봄맞이 콘서트',
          description: '설명',
          event_date: '2026-04-15',
          venue: '예술의전당',
          image_url: null,
          is_featured: true,
          created_at: '2026-01-01',
        },
      ],
      total: 1,
      skip: 0,
      limit: 20,
    },
    isLoading: false,
    error: null,
  }),
}))

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

describe('HomePage', () => {
  it('renders hero banner', () => {
    renderWithProviders(<HomePage />)
    expect(screen.getByText(/최고의 아티스트를/)).toBeInTheDocument()
    expect(screen.getByText(/섭외해 드립니다/)).toBeInTheDocument()
  })

  it('renders category section', () => {
    renderWithProviders(<HomePage />)
    expect(screen.getByText('섭외대행 카테고리')).toBeInTheDocument()
    expect(screen.getByText('대중가수')).toBeInTheDocument()
    expect(screen.getByText('댄서')).toBeInTheDocument()
    expect(screen.getByText('뮤지션')).toBeInTheDocument()
    expect(screen.getByText('연주자')).toBeInTheDocument()
    expect(screen.getByText('오케스트라')).toBeInTheDocument()
  })

  it('renders featured performances', () => {
    renderWithProviders(<HomePage />)
    expect(screen.getByText('주요 공연')).toBeInTheDocument()
    expect(screen.getByText('봄맞이 콘서트')).toBeInTheDocument()
  })

  it('renders CTA section', () => {
    renderWithProviders(<HomePage />)
    expect(screen.getByText('섭외가 필요하신가요?')).toBeInTheDocument()
  })

  it('has inquiry link', () => {
    renderWithProviders(<HomePage />)
    const links = screen.getAllByText('문의하기')
    expect(links.length).toBeGreaterThan(0)
  })
})
