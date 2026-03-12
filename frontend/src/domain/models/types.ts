/** 아티스트 카테고리 */
export type ArtistCategory = 'singer' | 'dancer' | 'musician' | 'instrumentalist' | 'orchestra'

export const ARTIST_CATEGORY_LABELS: Record<ArtistCategory, string> = {
  singer: '대중가수',
  dancer: '댄서',
  musician: '뮤지션',
  instrumentalist: '연주자',
  orchestra: '오케스트라',
}

export const ARTIST_CATEGORY_PATHS: Record<ArtistCategory, string> = {
  singer: 'singers',
  dancer: 'dancers',
  musician: 'musicians',
  instrumentalist: 'instrumentalists',
  orchestra: 'orchestra',
}

export const PATH_TO_CATEGORY: Record<string, ArtistCategory> = {
  singers: 'singer',
  dancers: 'dancer',
  musicians: 'musician',
  instrumentalists: 'instrumentalist',
  orchestra: 'orchestra',
}

/** 사용자 역할 */
export type UserRole = 'customer' | 'admin'

/** 문의 상태 */
export type InquiryStatus = 'pending' | 'replied' | 'closed'

export const INQUIRY_STATUS_LABELS: Record<InquiryStatus, string> = {
  pending: '대기 중',
  replied: '답변 완료',
  closed: '종료',
}

/** 사용자 */
export interface User {
  id: string
  email: string
  role: UserRole
  is_verified: boolean
  created_at: string
}

/** 아티스트 */
export interface Artist {
  id: string
  name: string
  category: ArtistCategory
  category_label: string
  description: string
  profile_image_url: string | null
  gallery_images: string[]
  is_active: boolean
  created_at: string
  updated_at: string
}

/** 공연 */
export interface Performance {
  id: string
  title: string
  description: string
  event_date: string
  venue: string
  image_url: string | null
  artist_id: string | null
  is_featured: boolean
  created_at: string
}

/** 문의 */
export interface Inquiry {
  id: string
  name: string
  email: string
  phone: string | null
  subject: string
  message: string
  status: InquiryStatus
  admin_reply: string | null
  created_at: string
}

/** 인증 응답 */
export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

/** 목록 응답 */
export interface ArtistListResponse {
  artists: Artist[]
  total: number
  skip: number
  limit: number
}

export interface PerformanceListResponse {
  performances: Performance[]
  total: number
  skip: number
  limit: number
}

export interface InquiryListResponse {
  inquiries: Inquiry[]
  total: number
  skip: number
  limit: number
}

/** 대시보드 통계 */
export interface DashboardStats {
  artists: { total: number; active: number; inactive: number }
  performances: { total: number; featured: number }
  inquiries: { total: number; pending: number; replied: number; closed: number }
}

/** 이미지 업로드 응답 */
export interface ImageUploadResponse {
  url: string
}
