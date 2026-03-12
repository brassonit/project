import { describe, it, expect, vi } from 'vitest'
import { renderWithProviders, screen } from '../../../test/test-utils'
import InquiryPage from '../../../presentation/pages/inquiry/InquiryPage'

vi.mock('../../../application/hooks/useInquiries', () => ({
  useCreateInquiry: () => ({
    mutate: vi.fn(),
    isPending: false,
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

describe('InquiryPage', () => {
  it('renders inquiry form heading and fields', () => {
    renderWithProviders(<InquiryPage />)
    expect(screen.getByRole('heading', { name: '문의하기' })).toBeInTheDocument()
    // Check for form fields by their text content
    expect(screen.getByText('이름 *')).toBeInTheDocument()
    expect(screen.getByText('이메일 *')).toBeInTheDocument()
    expect(screen.getByText('전화번호')).toBeInTheDocument()
    expect(screen.getByText('제목 *')).toBeInTheDocument()
    expect(screen.getByText('내용 *')).toBeInTheDocument()
  })

  it('has submit button', () => {
    renderWithProviders(<InquiryPage />)
    expect(screen.getByRole('button', { name: '문의 보내기' })).toBeInTheDocument()
  })
})
