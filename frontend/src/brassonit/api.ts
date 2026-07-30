// 브라소닛 API 클라이언트 — backend /api 연동
import apiClient from '../infrastructure/api/client'
import type { BrArtist, BrCategory, BrShow } from './data'

// ── 응답 타입 (backend presentation/schemas) ──
interface PortfolioItemDto {
  tag: string
  year: number
  content: string
}
interface VideoItemDto {
  video_url: string
  title: string | null
}
interface ArtistDto {
  id: string
  genre_id: number
  genre_name: string | null
  category_name: string | null
  name: string
  members: string | null
  description: string
  like_count: number
  view_count: number
  images: string[]
  portfolios: PortfolioItemDto[]
  videos: VideoItemDto[]
}
interface ShowDto {
  id: string
  title: string
  event_date: string
  venue: string
  description: string
  intro: string // 공연 소개 본문 (문단은 빈 줄 구분)
  image_url: string | null
  like_count: number
  view_count: number
  is_upcoming: boolean
  lineup: { artist_id: string; artist_name: string | null }[]
  tickets: { label: string; url: string }[]
  videos: VideoItemDto[]
}
export interface UserDto {
  id: string
  email: string
  name: string | null
  phone: string | null
  role: string
  is_verified: boolean
}
export interface QuoteDto {
  id: string
  email: string
  name: string
  phone: string
  event_title: string
  show_title: string | null
  status: string // received | replied
  quote_file_url: string | null
  artists: { artist_id: string; artist_name: string | null }[]
  created_at: string
}

const toArtist = (d: ArtistDto): BrArtist => ({
  id: d.id,
  name: d.name,
  cat: d.category_name || '',
  sub: d.genre_name || '',
  members: d.members || '',
  desc: d.description,
  likes: d.like_count,
  views: d.view_count,
  images: d.images.length ? d.images : [`https://picsum.photos/seed/${d.id}/700/700`],
  portfolio: d.portfolios.map((p) => ({ tag: p.tag, year: p.year, text: p.content })),
  videos: d.videos.map((v) => ({ src: v.video_url, title: v.title || '' })),
})

const toShow = (d: ShowDto): BrShow => {
  const [y, m, dd] = d.event_date.split('-')
  return {
    id: d.id,
    title: d.title,
    date: `${y}. ${m}. ${dd} · ${d.venue}`,
    line: d.description,
    img: d.image_url || `https://picsum.photos/seed/${d.id}/900/560`,
    cat: '',
    lineup: d.lineup.map((l) => l.artist_name || ''),
    lineupIds: d.lineup.map((l) => l.artist_id),
    tickets: d.tickets,
    likes: d.like_count,
    views: d.view_count,
    upcoming: d.is_upcoming,
    // 공연 소개 — 빈 줄로 구분된 본문을 문단 배열로
    intro: d.intro.split(/\n\s*\n/).filter((p) => p.trim()),
    videos: d.videos.map((v) => ({ src: v.video_url, title: v.title || '' })),
  }
}

// ── API ──
export async function fetchArtists(): Promise<BrArtist[]> {
  // 카탈로그 전체 로딩 (100건 초과 대비 페이지네이션)
  const out: ArtistDto[] = []
  let skip = 0
  for (;;) {
    const { data } = await apiClient.get('/artists', { params: { skip, limit: 100 } })
    out.push(...data.artists)
    if (out.length >= data.total || data.artists.length === 0) break
    skip += 100
  }
  return out.map(toArtist)
}

export async function fetchArtistDetail(id: string): Promise<BrArtist> {
  const { data } = await apiClient.get(`/artists/${id}`) // 조회수 증가 포함
  return toArtist(data)
}

export async function fetchShows(): Promise<BrShow[]> {
  const { data } = await apiClient.get('/shows')
  return data.shows.map(toShow)
}

export async function fetchCategories(): Promise<BrCategory[]> {
  const { data } = await apiClient.get('/categories')
  return data.categories
}

export interface PolicyDto {
  policy_type: string
  effective_date: string // "2026-01-01"
  content: string // HTML
  versions: string[] // 시행일 목록 (최신순, "2026-01-01" 포맷)
}

export async function fetchPolicy(type: 'terms' | 'privacy', effectiveDate?: string): Promise<PolicyDto> {
  const { data } = await apiClient.get(`/policies/${type}`, { params: effectiveDate ? { effective_date: effectiveDate } : {} })
  return data
}

// ── auth ──
export async function apiRegister(email: string, password: string): Promise<UserDto> {
  const { data } = await apiClient.post('/auth/register', { email, password })
  return data
}

export async function apiVerifyEmail(token: string): Promise<void> {
  await apiClient.get('/auth/verify-email', { params: { token } })
}

export async function apiResendVerification(email: string, password: string): Promise<void> {
  await apiClient.post('/auth/resend-verification', { email, password })
}

export async function apiLogin(email: string, password: string): Promise<{ token: string; user: UserDto }> {
  const { data } = await apiClient.post('/auth/login', { email, password })
  return { token: data.access_token, user: data.user }
}

export async function apiMe(): Promise<UserDto> {
  const { data } = await apiClient.get('/auth/me')
  return data
}

export async function apiUpdateProfile(body: { name?: string; phone?: string; password?: string }): Promise<UserDto> {
  const { data } = await apiClient.put('/auth/me', body)
  return data
}

export async function apiWithdraw(): Promise<void> {
  await apiClient.delete('/auth/me')
}

// ── wishlist / cart ──
export const apiWishlist = () => apiClient.get('/me/wishlist').then((r) => r.data.artist_ids as string[])
export const apiWishToggle = (id: string) =>
  apiClient.post(`/me/wishlist/${id}/toggle`).then((r) => r.data.active as boolean)
export const apiWishRemove = (ids: string[]) =>
  apiClient.post('/me/wishlist/remove', { artist_ids: ids }).then((r) => r.data.artist_ids as string[])
export const apiShowWishlist = () => apiClient.get('/me/show-wishlist').then((r) => r.data.show_ids as string[])
export const apiShowWishToggle = (id: string) =>
  apiClient.post(`/me/show-wishlist/${id}/toggle`).then((r) => r.data.active as boolean)
export const apiShowWishRemove = (ids: string[]) =>
  apiClient.post('/me/show-wishlist/remove', { show_ids: ids }).then((r) => r.data.show_ids as string[])
export const apiCart = () => apiClient.get('/me/cart').then((r) => r.data.artist_ids as string[])
export const apiCartToggle = (id: string) =>
  apiClient.post(`/me/cart/${id}/toggle`).then((r) => r.data.active as boolean)
export const apiCartAdd = (ids: string[]) =>
  apiClient.post('/me/cart/add', { artist_ids: ids }).then((r) => r.data.artist_ids as string[])
export const apiCartRemove = (ids: string[]) =>
  apiClient.post('/me/cart/remove', { artist_ids: ids }).then((r) => r.data.artist_ids as string[])

// ── quotes ──
export interface QuoteCreateBody {
  email?: string
  name: string
  phone: string
  event_title: string
  event_date?: string
  event_date_text?: string
  region?: string
  content?: string
  show_id?: string
  artist_ids: string[]
  attachments: { file_name: string; file_url: string }[]
  update_profile: boolean
}

// 첨부파일 업로드 — 견적 생성 전에 호출, {file_name, file_url} 목록 반환
export async function apiUploadQuoteFiles(files: File[]): Promise<{ file_name: string; file_url: string }[]> {
  if (!files.length) return []
  const form = new FormData()
  files.forEach((f) => form.append('files', f))
  // 기본 Content-Type(application/json)을 무시하고 multipart로 전송
  const { data } = await apiClient.post('/quotes/attachments', form, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function apiCreateQuote(body: QuoteCreateBody): Promise<QuoteDto> {
  const { data } = await apiClient.post('/quotes', body)
  return data
}

export async function apiMyQuotes(): Promise<QuoteDto[]> {
  const { data } = await apiClient.get('/quotes/me', { params: { limit: 100 } })
  return data.quotes
}

// axios 에러에서 백엔드 detail 메시지 추출
export function apiErrorMessage(e: unknown, fallback: string): string {
  const detail = (e as { response?: { data?: { detail?: unknown } } })?.response?.data?.detail
  return typeof detail === 'string' ? detail : fallback
}
