import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useBrass } from '../store'

export default function WishlistPage() {
  const navigate = useNavigate()
  const { artists, shows, liked, carted, showLiked, toggleCarted, removeLiked, removeShowLiked, addToCart, requireLogin } = useBrass()
  const rows = artists.filter((a) => liked[a.id])
  const showRows = shows.filter((s) => showLiked[s.id])
  const [sel, setSel] = useState<Record<string, boolean>>({})
  const [showSel, setShowSel] = useState<Record<string, boolean>>({})

  const selRows = rows.filter((a) => sel[a.id])
  const allCk = rows.length > 0 && rows.every((a) => sel[a.id])
  const showAllCk = showRows.length > 0 && showRows.every((s) => showSel[s.id])

  return (
    <section className="mypg">
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        <span className="fw6" style={{ color: '#000' }}>
          찜리스트
        </span>
      </div>
      <h1 className="lth">찜리스트</h1>
      {rows.length > 0 && (
        <>
          <div className="fx ac qhead">
            <label className="fx ac gap8 qcolck pointer">
              <input
                type="checkbox"
                className="ckb"
                checked={allCk}
                onChange={() => {
                  const on = !allCk
                  setSel(Object.fromEntries(rows.map((a) => [a.id, on])))
                }}
              />
              전체
            </label>
            <span className="f1">아티스트</span>
            <span className="qcol3"></span>
          </div>
          {rows.map((a) => (
            <div className="fx ac qrow" key={a.id}>
              <span className="qcolck">
                <input type="checkbox" className="ckb" checked={!!sel[a.id]} onChange={() => setSel((m) => ({ ...m, [a.id]: !m[a.id] }))} />
              </span>
              <div className="fx ac gap12 f1 pointer" onClick={() => navigate(`/artist/${a.id}`)}>
                <img className="qimg" src={a.images[0]} alt={a.name} />
                <span className="col gap4">
                  <span className="fw6 fs14">{a.name}</span>
                  <span className="fs13" style={{ color: '#666' }}>
                    {a.cat} · {a.sub}
                  </span>
                </span>
              </div>
              <span className="qcol3">
                <button className={`qdel${carted[a.id] ? ' on' : ''}`} onClick={() => toggleCarted(a.id)}>
                  {carted[a.id] ? '담김' : '장바구니'}
                </button>
                <button
                  className="qdel"
                  onClick={() => {
                    removeLiked([a.id])
                    setSel((m) => {
                      const n = { ...m }
                      delete n[a.id]
                      return n
                    })
                  }}
                >
                  삭제
                </button>
              </span>
            </div>
          ))}
          <div className="fx ac jb cartft">
            <button
              className="qdel"
              onClick={() => {
                removeLiked(selRows.map((a) => a.id))
                setSel({})
              }}
            >
              선택 삭제
            </button>
            {selRows.length > 0 && (
              <button
                className="bigbtn"
                style={{ flex: 'none' }}
                onClick={() => {
                  addToCart(selRows.map((a) => a.id))
                  setSel({})
                }}
              >
                총 {selRows.length}팀 아티스트 장바구니 담기
              </button>
            )}
          </div>
        </>
      )}
      {showRows.length > 0 && (
        <>
          <div className="fx ac qhead" style={{ marginTop: 36 }}>
            <label className="fx ac gap8 qcolck pointer">
              <input
                type="checkbox"
                className="ckb"
                checked={showAllCk}
                onChange={() => {
                  const on = !showAllCk
                  setShowSel(Object.fromEntries(showRows.map((s) => [s.id, on])))
                }}
              />
              전체
            </label>
            <span className="f1">공연</span>
            <span className="qcol3"></span>
          </div>
          {showRows.map((s) => (
            <div className="fx ac qrow" key={s.id}>
              <span className="qcolck">
                <input type="checkbox" className="ckb" checked={!!showSel[s.id]} onChange={() => setShowSel((m) => ({ ...m, [s.id]: !m[s.id] }))} />
              </span>
              <div className="fx ac gap12 f1 pointer" onClick={() => navigate(`/shows/${s.id}`)}>
                <img className="qimg" src={s.img} alt={s.title} />
                <span className="col gap4">
                  <span className="fw6 fs14">{s.title}</span>
                  <span className="fs13" style={{ color: '#666' }}>
                    {s.lineup.filter(Boolean).join(', ')}
                  </span>
                </span>
              </div>
              <span className="qcol3">
                <button
                  className="qdel"
                  onClick={() => {
                    if (!requireLogin()) return
                    navigate('/quote', { state: { qfIds: [], qfShow: s.id } })
                  }}
                >
                  문의하기
                </button>
                <button
                  className="qdel"
                  onClick={() => {
                    removeShowLiked([s.id])
                    setShowSel((m) => {
                      const n = { ...m }
                      delete n[s.id]
                      return n
                    })
                  }}
                >
                  삭제
                </button>
              </span>
            </div>
          ))}
          <div className="fx ac jb cartft">
            <button
              className="qdel"
              onClick={() => {
                removeShowLiked(showRows.filter((s) => showSel[s.id]).map((s) => s.id))
                setShowSel({})
              }}
            >
              선택 삭제
            </button>
          </div>
        </>
      )}
      {rows.length === 0 && showRows.length === 0 && (
        <div className="empty">
          찜한 아티스트나 공연이 없습니다.
          <br />
          마음에 드는 아티스트와 공연의 하트를 눌러 찜해 보세요.
        </div>
      )}
    </section>
  )
}
