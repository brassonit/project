import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useBrass } from '../store'

export default function CartPage() {
  const navigate = useNavigate()
  const { artists, carted, removeCarted } = useBrass()
  const rows = artists.filter((a) => carted[a.id])
  // 진입 시 전체 선택이 기본
  const [sel, setSel] = useState<Record<string, boolean>>(() => Object.fromEntries(rows.map((a) => [a.id, true])))
  // 직접 URL 진입(새로고침) 시 데이터가 마운트 이후 로드되므로, 처음 행이 나타날 때 전체 선택 적용
  const selInited = useRef(rows.length > 0)
  useEffect(() => {
    if (!selInited.current && rows.length > 0) {
      selInited.current = true
      setSel(Object.fromEntries(rows.map((a) => [a.id, true])))
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [rows.length])

  const selRows = rows.filter((a) => sel[a.id])
  const allCk = rows.length > 0 && rows.every((a) => sel[a.id])

  return (
    <section className="mypg">
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        <span className="fw6" style={{ color: '#000' }}>
          장바구니
        </span>
      </div>
      <h1 className="lth">장바구니</h1>
      {rows.length > 0 ? (
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
            <span className="qcol">카테고리</span>
            <span className="qcol2"></span>
          </div>
          {rows.map((a) => (
            <div className="fx ac qrow" key={a.id}>
              <span className="qcolck">
                <input type="checkbox" className="ckb" checked={!!sel[a.id]} onChange={() => setSel((m) => ({ ...m, [a.id]: !m[a.id] }))} />
              </span>
              <div className="fx ac gap12 f1 pointer" onClick={() => navigate(`/artist/${a.id}`)}>
                <img className="qimg" src={a.images[0]} alt={a.name} />
                <span className="fw6 fs14">{a.name}</span>
              </div>
              <span className="qcol fs13">
                {a.cat} · {a.sub}
              </span>
              <span className="qcol2">
                <button className="qdel" onClick={() => removeCarted([a.id])}>
                  삭제
                </button>
              </span>
            </div>
          ))}
          <div className="fx ac jb cartft">
            <button className="qdel" onClick={() => removeCarted(selRows.map((a) => a.id))}>
              선택 삭제
            </button>
            <button
              className="bigbtn"
              style={{ flex: 'none' }}
              onClick={() => {
                if (!selRows.length) return
                navigate('/quote', { state: { qfIds: selRows.map((a) => a.id), qfShow: '' } })
              }}
            >
              총 {selRows.length}팀 아티스트로 견적 요청
            </button>
          </div>
        </>
      ) : (
        <div className="empty">
          장바구니가 비어 있습니다.
          <br />
          아티스트 카드의 장바구니 버튼을 눌러 담아보세요.
        </div>
      )}
    </section>
  )
}
