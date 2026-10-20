import { useEffect, useState } from 'react'
import { useLocation, useNavigate, useParams, useSearchParams } from 'react-router-dom'
import { useBrass } from '../store'
import { ArtistCard } from '../components'
import { catNameById, genreNameById } from '../data'

const PAGE = 20

// 모바일 무한스크롤 로딩 개수 — URL에 넣으면 router 네비게이션으로 처리되어
// Layout의 '새 페이지 진입 시 맨 위로 스크롤' 로직이 매번 발동해버림.
// 그래서 세션스토리지에 보관해 라우팅과 무관하게 상세페이지 뒤로가기 시에도 유지되게 함.
const mobileCountKey = (pathname: string) => `catScrollCount:${pathname}`

export default function CategoryPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { artists, categories, loading } = useBrass()
  const { cat: rawCat, sub: rawSub } = useParams<{ cat: string; sub?: string }>()
  const catId = rawCat ? Number(rawCat) : null
  const subId = rawSub ? Number(rawSub) : null
  const cat = catId != null ? catNameById(categories, catId) : ''
  const sub = subId != null ? genreNameById(categories, subId) : null
  // 페이지 번호는 URL 쿼리에 보관 — 상세페이지에서 뒤로가기 시 보던 페이지 그대로 복원됨
  const [searchParams, setSearchParams] = useSearchParams()
  const pageNo = Math.max(1, Number(searchParams.get('page')) || 1)
  const [mobileCount, setMobileCount] = useState<number>(() => {
    const saved = Number(sessionStorage.getItem(mobileCountKey(location.pathname)))
    return saved > 20 ? saved : 20
  })
  const [isMobile, setIsMobile] = useState(() => window.matchMedia('(max-width:620px)').matches)

  const cards = artists.filter((a) => a.cat === cat && (!sub || a.sub === sub))
  const pageCount = Math.max(1, Math.ceil(cards.length / PAGE))

  useEffect(() => {
    const saved = Number(sessionStorage.getItem(mobileCountKey(location.pathname)))
    setMobileCount(saved > 20 ? saved : 20)
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cat, sub])

  useEffect(() => {
    const mq = window.matchMedia('(max-width:620px)')
    const onMq = () => setIsMobile(mq.matches)
    mq.addEventListener('change', onMq)
    return () => mq.removeEventListener('change', onMq)
  }, [])

  // 모바일: 무한 스크롤 (+20) — 불러온 개수는 세션스토리지에도 저장해 뒤로가기 시 복원
  useEffect(() => {
    if (!isMobile) return
    const onScroll = () => {
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 400)
        setMobileCount((c) => {
          const next = c < cards.length ? c + 20 : c
          sessionStorage.setItem(mobileCountKey(location.pathname), String(next))
          return next
        })
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [isMobile, cards.length, location.pathname])

  const safePageNo = Math.min(pageNo, pageCount)
  const shown = isMobile ? cards.slice(0, mobileCount) : cards.slice((safePageNo - 1) * PAGE, safePageNo * PAGE)
  const goPage = (n: number) => {
    setSearchParams(n > 1 ? { page: String(n) } : {}, { replace: true })
    window.scrollTo(0, 0)
  }

  return (
    <section>
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        {sub ? (
          <>
            <button onClick={() => navigate(`/category/${catId}`)}>{cat}</button>
            <span>›</span>
            <span className="fw6" style={{ color: '#000' }}>
              {sub}
            </span>
          </>
        ) : (
          <span className="fw6" style={{ color: '#000' }}>
            {cat}
          </span>
        )}
      </div>
      <div className="sect" style={{ paddingTop: 20 }}>
        {cards.length > 0 ? (
          <>
            <div className="grid5">
              {shown.map((a) => (
                <ArtistCard key={a.id} artist={a} />
              ))}
            </div>
            {!isMobile && pageCount > 1 && (
              <div className="pager">
                <button className="pgb" onClick={() => goPage(safePageNo - 1)} disabled={safePageNo <= 1}>
                  ‹
                </button>
                {Array.from({ length: pageCount }, (_, i) => (
                  <button key={i} className={`pgb${i + 1 === safePageNo ? ' on' : ''}`} onClick={() => goPage(i + 1)}>
                    {i + 1}
                  </button>
                ))}
                <button className="pgb" onClick={() => goPage(safePageNo + 1)} disabled={safePageNo >= pageCount}>
                  ›
                </button>
              </div>
            )}
            <div className="mstat">
              {Math.min(mobileCount, cards.length)} / {cards.length}
            </div>
          </>
        ) : (
          <div className="empty">{loading ? '불러오는 중…' : '검색 결과가 없습니다.'}</div>
        )}
      </div>
    </section>
  )
}
