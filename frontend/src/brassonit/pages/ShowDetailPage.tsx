import { useEffect, useState } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { fmt } from '../data'
import { useBrass } from '../store'
import { EyeIcon, ShareIcon } from '../icons'

export default function ShowDetailPage() {
  const navigate = useNavigate()
  const { idx: showId } = useParams<{ idx: string }>()
  const { shows, artists, loading, requireLogin, showLiked, toggleShowLiked } = useBrass()
  const [shared, setShared] = useState(false)
  const [introOpen, setIntroOpen] = useState(false)
  const [vidOpen, setVidOpen] = useState(false)

  useEffect(() => {
    setShared(false)
    setIntroOpen(false)
    setVidOpen(false)
  }, [showId])

  const sh = shows.find((s) => s.id === showId)
  if (!sh) return <div className="empty">{loading ? '불러오는 중…' : '공연을 찾을 수 없습니다.'}</div>

  const openArtist = (name: string, id?: string) => {
    const a = id ? artists.find((x) => x.id === id) : artists.find((x) => x.name === name)
    if (a) navigate(`/artist/${a.id}`)
  }

  const share = () => {
    const url = `${location.origin}/shows/${sh.id}`
    const done = () => {
      setShared(true)
      setTimeout(() => setShared(false), 2000)
    }
    if (navigator.clipboard?.writeText) navigator.clipboard.writeText(url).then(done, done)
    else done()
  }

  const vids = vidOpen ? sh.videos : sh.videos.slice(0, 5)

  return (
    <section>
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        <button className="fw6" style={{ color: '#000' }} onClick={() => navigate('/shows')}>
          기획공연
        </button>
      </div>
      <div className="dtl dtl2">
        <div className="simg m0" style={{ aspectRatio: '16/10' }}>
          <img src={sh.img} alt={sh.title} style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        </div>
        <div>
          <div className="kick">BRASSONIT PRODUCTION</div>
          <h1 className="dname">{sh.title}</h1>
          <div className="fx ac gap16 mb16">
            <span className="fx ac stat">♥ 좋아요 {fmt(sh.likes)}</span>
            <span className="fx ac stat">
              <EyeIcon /> 조회 {fmt(sh.views)}
            </span>
          </div>
          <div className="fx drow">
            <span className="dlab">일시·장소</span>
            <span>{sh.date}</span>
          </div>
          <div className="fx drow">
            <span className="dlab">소개</span>
            <span style={{ lineHeight: 1.7 }}>{sh.line}</span>
          </div>
          <div className="fx drow" style={{ borderBottom: '1px solid #ddd' }}>
            <span className="dlab">출연진</span>
            {/* 출연진 — 칩/보더/밑줄 없는 플레인 텍스트 버튼 */}
            <span className="fx gap12" style={{ flexWrap: 'wrap' }}>
              {sh.lineup.map((nm, i) => (
                <button key={nm} className="castlnk" onClick={() => openArtist(nm, sh.lineupIds[i])}>
                  {nm}
                </button>
              ))}
            </span>
          </div>
          <div className="col gap8" style={{ marginTop: 28 }}>
            {sh.tickets.map((t) => (
              <button key={t.label} className="bigbtn ghost w100 bbox" onClick={() => window.open(t.url, '_blank')}>
                예매 바로가기 · {t.label} ↗
              </button>
            ))}
          </div>
          <div className="fx gap12" style={{ marginTop: 12, justifyContent: 'flex-end' }}>
            <button
              className="bigbtn"
              style={{ flex: 'none' }}
              onClick={() => {
                if (!requireLogin()) return
                navigate('/quote', { state: { qfIds: [], qfShow: sh.id } })
              }}
            >
              공연 문의하기
            </button>
            {/* 모바일(≤620px)에서는 아이콘만 표시(btxt 숨김) */}
            <button className="bigbtn ghost fx ac gap8" style={{ flex: 'none' }} onClick={share}>
              <ShareIcon />
              <span className="btxt">{shared ? '링크 복사됨 ✓' : '공유하기'}</span>
            </button>
            <button className="bigbtn ghost" style={{ flex: 'none' }} onClick={() => toggleShowLiked(sh.id)}>
              <span style={{ color: showLiked[sh.id] ? 'var(--color-accent)' : '#bbb' }}>♥</span>
            </button>
          </div>
        </div>
      </div>

      <div className="sect" style={{ paddingTop: 0 }}>
        <div className="fx jb sechd">
          <h2 className="sech2">공연 소개</h2>
        </div>
        <div className={`introwrap${introOpen ? '' : ' clamp'}`}>
          {sh.intro.map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </div>
        <button className="moreb" style={{ maxWidth: 960 }} onClick={() => setIntroOpen((v) => !v)}>
          {introOpen ? '접기 ↑' : '더보기 ↓'}
        </button>
      </div>

      <div className="sect" style={{ paddingTop: 0 }}>
        <div className="fx jb sechd">
          <h2 className="sech2">공연 영상</h2>
        </div>
        <div className="vidg">
          {vids.map((v) => (
            <div className="vitem" key={v.title}>
              <iframe src={v.src} title={v.title} allowFullScreen loading="lazy" />
            </div>
          ))}
        </div>
        {sh.videos.length > 5 && (
          <button className="moreb" style={{ maxWidth: 960 }} onClick={() => setVidOpen((v) => !v)}>
            {vidOpen ? '접기 ↑' : `더보기 (${sh.videos.length - 5}) ↓`}
          </button>
        )}
      </div>
    </section>
  )
}
