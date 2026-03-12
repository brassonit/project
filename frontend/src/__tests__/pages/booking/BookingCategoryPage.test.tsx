import { describe, it, expect, vi } from 'vitest'
import { render, screen } from '@testing-library/react'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import BookingCategoryPage from '../../../presentation/pages/booking/BookingCategoryPage'

vi.mock('../../../application/hooks/useArtists', () => ({
  useArtists: () => ({
    data: {
      artists: [
        {
          id: '1',
          name: '김가수',
          category: 'singer',
          category_label: '대중가수',
          description: '인기 가수입니다.',
          profile_image_url: null,
          gallery_images: [],
          is_active: true,
          created_at: '2026-01-01',
          updated_at: '2026-01-01',
        },
      ],
      total: 1,
      skip: 0,
      limit: 12,
    },
    isLoading: false,
    error: null,
    refetch: vi.fn(),
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

function renderWithRoute(path: string) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } })
  return render(
    <QueryClientProvider client={qc}>
      <MemoryRouter initialEntries={[path]}>
        <Routes>
          <Route path="/booking/:categoryPath" element={<BookingCategoryPage />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  )
}

describe('BookingCategoryPage', () => {
  it('renders category heading for singers', () => {
    renderWithRoute('/booking/singers')
    expect(screen.getByRole('heading', { name: '대중가수' })).toBeInTheDocument()
  })

  it('renders artist list', () => {
    renderWithRoute('/booking/singers')
    expect(screen.getByText('김가수')).toBeInTheDocument()
  })

  it('shows total count', () => {
    renderWithRoute('/booking/singers')
    expect(screen.getByText((_, el) => el?.tagName === 'P' && el?.textContent === '총 1명의 아티스트')).toBeInTheDocument()
  })
})
