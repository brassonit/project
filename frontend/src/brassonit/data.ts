// 브라소닛 타입/상수 — 데이터는 API에서 로딩 (store.tsx)

export const SUBS: Record<string, string[]> = {
  대중가수: ['아이돌', '발라드', '트로트', '힙합'],
  음악: ['재즈', '클래식', '뮤지컬', '국악'],
  강연: ['셀럽', '배우'],
  사회자: ['전문MC', '아나운서'],
  퍼포먼스: ['마술', '무용', '댄스'],
}
export const MENU_ORDER = ['대중가수', '음악', '강연', '사회자', '퍼포먼스']

export interface BrCategory {
  id: number
  name: string
  genres: { id: number; name: string }[]
}

// URL(/category/:catId/:genreId)과 카테고리명 사이 변환 — categories는 store에서 API로 로딩
export const catIdByName = (categories: BrCategory[], name: string): number | undefined =>
  categories.find((c) => c.name === name)?.id

export const genreIdByName = (categories: BrCategory[], catName: string, subName: string): number | undefined =>
  categories.find((c) => c.name === catName)?.genres.find((g) => g.name === subName)?.id

export const catNameById = (categories: BrCategory[], id: number): string =>
  categories.find((c) => c.id === id)?.name || ''

export const genreNameById = (categories: BrCategory[], id: number): string => {
  for (const c of categories) {
    const g = c.genres.find((g) => g.id === id)
    if (g) return g.name
  }
  return ''
}

export interface PortfolioItem {
  tag: string
  year: number
  text: string
}
export interface ArtistVideo {
  src: string
  title: string
}
export interface BrArtist {
  id: string // CHAR(8)
  name: string
  cat: string
  sub: string
  members: string
  desc: string
  likes: number
  views: number
  images: string[]
  portfolio: PortfolioItem[]
  videos: ArtistVideo[]
}
export interface BrShow {
  id: string // CHAR(8)
  title: string
  date: string // "2026. 08. 15 · 올림픽공원"
  line: string
  img: string
  cat: string
  lineup: string[] // 출연진 이름
  lineupIds: string[]
  tickets: { label: string; url: string }[]
  likes: number
  views: number
  upcoming: boolean
  intro: string[] // 공연 소개 문단
  videos: ArtistVideo[] // 공연 영상
}

export function fmt(n: number): string {
  return n >= 1000 ? (n / 1000).toFixed(1).replace(/\.0$/, '') + '천' : String(n)
}

// 전화번호 자동 하이픈 포맷
export function fmtPhone(v: string): string {
  const d = (v || '').replace(/\D/g, '').slice(0, 11)
  if (d.length < 4) return d
  if (d.startsWith('02')) {
    if (d.length < 6) return d.slice(0, 2) + '-' + d.slice(2)
    if (d.length < 10) return d.slice(0, 2) + '-' + d.slice(2, d.length - 4) + '-' + d.slice(-4)
    return d.slice(0, 2) + '-' + d.slice(2, 6) + '-' + d.slice(6, 10)
  }
  if (d.length < 8) return d.slice(0, 3) + '-' + d.slice(3)
  if (d.length < 11) return d.slice(0, 3) + '-' + d.slice(3, d.length - 4) + '-' + d.slice(-4)
  return d.slice(0, 3) + '-' + d.slice(3, 7) + '-' + d.slice(7)
}

export const REGIONS = ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원특별자치도', '충청북도', '충청남도', '전북특별자치도', '전라남도', '경상북도', '경상남도', '제주특별자치도']

export const HISTORY = [
  { y: '2026', t: '누적 섭외 3,000건 돌파 · 브라소닛 썸머 스테이지 개최' },
  { y: '2024', t: '공연기획 사업부 신설 · 자체 기획공연 시즌제 시작' },
  { y: '2023', t: '등록 아티스트 300팀 돌파 · 온라인 섭외 플랫폼 오픈' },
  { y: '2021', t: '기업 행사 전문 섭외 서비스 개시' },
  { y: '2019', t: '주식회사 브라소닛 법인 설립' },
]

export const SHOWS = [
  { date: '2026. 08', title: '브라소닛 썸머 스테이지', line: '여름 야외 페스티벌' },
  { date: '2026. 03', title: '봄날의 재즈나이트', line: '재즈 아티스트 합동 공연' },
  { date: '2025. 12', title: '연말 갈라 콘서트', line: '기업 송년회 특별 공연' },
  { date: '2025. 05', title: '뮤직 인 더 파크', line: '대형 야외 음악 축제' },
  { date: '2024. 10', title: '어텀 클래식 시리즈', line: '클래식·국악 크로스오버' },
]
