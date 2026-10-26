// 브라소닛 타입/상수 — 데이터는 API에서 로딩 (store.tsx)

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
  thumbnails: string[]
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
  { y: '2026', t: "'원더 X 장영실' 문예회관 특성화 지원사업 선정 · Blue Note Tokyo All-Star Jazz Orchestra 4개 도시 투어" },
  { y: '2025', t: "청주시립예술단 협업 피크닉 콘서트 · 대구 파워풀대구페스티벌 · Compagnie Käfig 'PIXEL' · 김포 명인명무전 '월곶나빌레라'" },
  { y: '2024', t: '전국 문예회관·축제 60여 개 공연 진행 · 최백호·이무진 X 데이브레이크·코요태&케이시·인순이 콘서트 · 부천 K댄스 페스티벌' },
  { y: '2023', t: "윈튼 마살리스 — 경남문화예술회관 · 나윤선·양희은·박정현 & 몽니 콘서트 · 트롯 페스타 '뿅 디스 빠뤼'" },
  { y: '2022', t: "'Beyond the Hip Hop' 시작 — 인천 · 김연자·노브레인 & 레이지본·이은미 콘서트" },
  { y: '2021', t: "'Body & Voice' — 인제 하늘내린센터 · 브라소닛 빅밴드 'Aladdin' — 밀양" },
  { y: '2020', t: "브라소닛 빅밴드 & 앰비규어스댄스컴퍼니 'Body & Voice' 초연 — 밀양아리랑아트센터" },
  { y: '2019', t: '브라소닛 빅밴드 정기공연 with Eric Miyashiro·유태평양·오종대' },
  { y: '2018', t: "'Musical Diva All Stars' · 이은미·YB 콘서트 · 첫 '설렘주의보' 공연 · 빅밴드 with BMK & Crissie 7개 도시 투어" },
  { y: '2017', t: '김태우 & 알리 콘서트 — 포천·군산 · 빅밴드 정기공연 — 홍대 웨스트 브릿지' },
  { y: '2016', t: "(주)온아트 설립 · 브라소닛 빅밴드 'Jazz Party' — 보령·공주·청양" },
  { y: '2015', t: "(주)에이엠지이엔티 설립 · '브라소닛 빅밴드' 창단 · 조수미 콘서트 · 아이돌 대전 슈퍼콘서트(관객 2만 5천여 명)" },
  { y: '2014', t: "브라소닛 설립 · 첫 기획공연 'Jazz All Stars' — 보령·서산 · 수원 광교호수공원 재즈페스티벌" },
]

export const SHOWS = [
  { date: '대중가수 라인업', title: '설렘주의보 콘서트', line: 'K-POP & 대중가수 맞춤형 브랜드 콘서트' },
  { date: '대중가수 라인업', title: 'Beyond the Hip & Pop', line: '힙합·댄스·K-POP·DJ 페스타' },
  { date: '대중가수 라인업', title: '밴드DAY', line: '밴드 페스타 / 락 페스타' },
  { date: '대중가수 라인업', title: '뿅 디스 빠뤼', line: '트롯 페스타' },
  { date: '대중가수 라인업', title: '뮤지컬 & 크로스오버', line: '뮤지컬·크로스오버 갈라 콘서트' },
  { date: '다원예술', title: '타임 매직 유니버스: 원더 X 장영실', line: '최형배 마술사의 과학마술극(뮤지컬)' },
  { date: '다원예술', title: 'Body & Voice', line: '브라소닛 빅밴드 & 앰비규어스댄스컴퍼니' },
  { date: '다원예술', title: '국민뮤지컬 사랑은 비를 타고', line: 'since 1995 · 한국 창작뮤지컬의 대표작' },
  { date: '다원예술', title: '가족뮤지컬 구름빵', line: '백희나 원작 · 대한민국 대표 가족뮤지컬' },
]
