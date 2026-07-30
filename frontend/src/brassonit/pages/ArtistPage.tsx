import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { fetchArtistDetail } from '../api'
import type { BrArtist } from '../data'
import { catIdByName, fmt, genreIdByName } from '../data'
import { useBrass } from '../store'
import { CartIcon, ChevronLeft, ChevronRight, EyeIcon, ShareIcon } from '../icons'

const PF_ORDER = ['주요활동', '앨범', '수상내역', '경력사항']

export default function ArtistPage() {
  const navigate = useNavigate()
  const { id } = useParams<{ id: string }>()
  const { artists, categories, loading, liked, carted, toggleLiked, toggleCarted, requireLogin } = useBrass()
  const [detail, setDetail] = useState<BrArtist | null>(null)
  const [slide, setSlide] = useState(0)
  const [pfOpen, setPfOpen] = useState(false)
  const [vidOpen, setVidOpen] = useState(false)
  const [shared, setShared] = useState(false)

  useEffect(() => {
    setSlide(0)
    setPfOpen(false)
    setVidOpen(false)
    setShared(false)
    setDetail(null)
    if (id) fetchArtistDetail(id).then(setDetail).catch(() => {}) // 조회수 증가 포함
  }, [id])

  const cur = detail || artists.find((a) => a.id === id)
  if (!cur) return <div className="empty">{loading ? '불러오는 중…' : '아티스트를 찾을 수 없습니다.'}</div>
  const n = cur.images.length

  const flat: typeof cur.portfolio = []
  PF_ORDER.forEach((t) =>
    cur.portfolio
      .filter((p) => p.tag === t)
      .sort((a, b) => b.year - a.year)
      .forEach((p) => flat.push(p)),
  )
  const capped = pfOpen ? flat : flat.slice(0, 5)
  const pfGroups = PF_ORDER.map((t) => ({ tag: t, items: capped.filter((p) => p.tag === t) })).filter((g) => g.items.length)
  const vids = vidOpen ? cur.videos : cur.videos.slice(0, 5)

  const share = () => {
    const url = `${location.origin}/artist/${cur.id}`
    const done = () => {
      setShared(true)
      setTimeout(() => setShared(false), 2000)
    }
    if (navigator.clipboard?.writeText) navigator.clipboard.writeText(url).then(done, done)
    else done()
  }

  return (
    <section>
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        <button onClick={() => navigate(`/category/${catIdByName(categories, cur.cat)}`)}>{cur.cat}</button>
        <span>›</span>
        <button
          className="fw6"
          style={{ color: '#000' }}
          onClick={() => navigate(`/category/${catIdByName(categories, cur.cat)}/${genreIdByName(categories, cur.cat, cur.sub)}`)}
        >
          {cur.sub}
        </button>
      </div>
      <div className="dtl">
        <div className="slider">
          <img src={cur.images[slide % n]} alt={cur.name} />
          {n > 1 && (
            <>
              <button className="snav" style={{ left: 0 }} onClick={() => setSlide((s) => (s + n - 1) % n)}>
                <ChevronLeft />
              </button>
              <button className="snav" style={{ right: 0 }} onClick={() => setSlide((s) => (s + 1) % n)}>
                <ChevronRight />
              </button>
              <div className="dots">
                {cur.images.map((_, i) => (
                  <button key={i} className={`dot2${i === slide % n ? ' on' : ''}`} onClick={() => setSlide(i)} />
                ))}
              </div>
            </>
          )}
        </div>
        <div>
          <div className="kick">
            {cur.cat} · {cur.sub}
          </div>
          <h1 className="dname">{cur.name}</h1>
          <div className="fx dstats">
            <span className="fx ac stat">♥ 좋아요 {fmt(cur.likes)}</span>
            <span className="fx ac stat">
              <EyeIcon /> 조회 {fmt(cur.views)}
            </span>
          </div>
          <div className="fx drow">
            <span className="dlab">장르</span>
            <span>{cur.sub}</span>
          </div>
          <div className="fx drow">
            <span className="dlab">인원</span>
            <span>{cur.members}</span>
          </div>
          <div className="fx drow" style={{ borderBottom: '1px solid #ddd' }}>
            <span className="dlab">소개</span>
            <span style={{ lineHeight: 1.7 }}>{cur.desc}</span>
          </div>
          <div className="fx gap12 mt16" style={{ marginTop: 28 }}>
            <button
              className="bigbtn"
              onClick={() => {
                if (!requireLogin()) return
                navigate('/quote', { state: { qfIds: [cur.id], qfShow: '' } })
              }}
            >
              섭외 견적 요청
            </button>
            {/* 모바일(≤620px)에서는 아이콘만 표시(btxt 숨김) */}
            <button className="bigbtn ghost fx ac gap8" onClick={() => toggleCarted(cur.id)}>
              <CartIcon size={18} />
              <span className="btxt">{carted[cur.id] ? '장바구니에 담김 ✓' : '장바구니 담기'}</span>
            </button>
            <button className="bigbtn ghost fx ac gap8" style={{ flex: 'none' }} onClick={share}>
              <ShareIcon />
              <span className="btxt">{shared ? '링크 복사됨 ✓' : '공유하기'}</span>
            </button>
            <button className="bigbtn ghost" style={{ flex: 'none' }} onClick={() => toggleLiked(cur.id)}>
              <span style={{ color: liked[cur.id] ? 'var(--color-accent)' : '#bbb' }}>♥</span>
            </button>
          </div>
        </div>
      </div>

      <div className="sect" style={{ paddingTop: 0 }}>
        <div className="fx jb sechd">
          <h2 className="sech2">포트폴리오</h2>
        </div>
        {pfGroups.map((g) => (
          <div key={g.tag}>
            <div className="pfgh">{g.tag}</div>
            {g.items.map((p, i) => (
              <div className="fx pfrow" key={i}>
                <span className="pftag">{p.year}</span>
                <span>{p.text}</span>
              </div>
            ))}
          </div>
        ))}
        {cur.portfolio.length > 5 && (
          <button className="moreb" onClick={() => setPfOpen((v) => !v)}>
            {pfOpen ? '접기 ↑' : `더보기 (${cur.portfolio.length - 5}) ↓`}
          </button>
        )}
      </div>

      <div className="sect" style={{ paddingTop: 0 }}>
        <div className="fx jb sechd">
          <h2 className="sech2">영상</h2>
        </div>
        <div className="vidg">
          {vids.map((v) => (
            <div className="vitem" key={v.title}>
              <iframe src={v.src} title={v.title} allowFullScreen loading="lazy" />
            </div>
          ))}
        </div>
        {cur.videos.length > 5 && (
          <button className="moreb" onClick={() => setVidOpen((v) => !v)}>
            {vidOpen ? '접기 ↑' : `더보기 (${cur.videos.length - 5}) ↓`}
          </button>
        )}
      </div>
    </section>
  )
}
