import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useBrass } from '../store'
import { ArtistCard } from '../components'
import { catNameById, genreNameById } from '../data'

const PAGE = 20

export default function CategoryPage() {
  const navigate = useNavigate()
  const { artists, categories, loading } = useBrass()
  const { cat: rawCat, sub: rawSub } = useParams<{ cat: string; sub?: string }>()
  const catId = rawCat ? Number(rawCat) : null
  const subId = rawSub ? Number(rawSub) : null
  const cat = catId != null ? catNameById(categories, catId) : ''
  const sub = subId != null ? genreNameById(categories, subId) : null
  const [pageNo, setPageNo] = useState(1)
  const [mobileCount, setMobileCount] = useState(20)
  const [isMobile, setIsMobile] = useState(() => window.matchMedia('(max-width:620px)').matches)

  const cards = artists.filter((a) => a.cat === cat && (!sub || a.sub === sub))
  const pageCount = Math.max(1, Math.ceil(cards.length / PAGE))

  useEffect(() => {
    setPageNo(1)
    setMobileCount(20)
  }, [cat, sub])

  useEffect(() => {
    const mq = window.matchMedia('(max-width:620px)')
    const onMq = () => setIsMobile(mq.matches)
    mq.addEventListener('change', onMq)
    return () => mq.removeEventListener('change', onMq)
  }, [])

  // 모바일: 무한 스크롤 (+20)
  useEffect(() => {
    if (!isMobile) return
    const onScroll = () => {
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 400)
        setMobileCount((c) => (c < cards.length ? c + 20 : c))
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [isMobile, cards.length])

  const shown = isMobile ? cards.slice(0, mobileCount) : cards.slice((pageNo - 1) * PAGE, pageNo * PAGE)
  const goPage = (n: number) => {
    setPageNo(n)
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
                <button className="pgb" onClick={() => goPage(pageNo - 1)} disabled={pageNo <= 1}>
                  ‹
                </button>
                {Array.from({ length: pageCount }, (_, i) => (
                  <button key={i} className={`pgb${i + 1 === pageNo ? ' on' : ''}`} onClick={() => goPage(i + 1)}>
                    {i + 1}
                  </button>
                ))}
                <button className="pgb" onClick={() => goPage(pageNo + 1)} disabled={pageNo >= pageCount}>
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
