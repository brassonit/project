import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useBrass, type Quote } from '../store'
import { DownloadIcon } from '../icons'

const PAGE = 10

function downloadQuote(q: Quote) {
  if (q.docUrl) {
    window.open(q.docUrl, '_blank')
    return
  }
  const html = `<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8"><title>견적서 - ${q.title}</title></head><body style="font-family:sans-serif;max-width:640px;margin:40px auto;line-height:1.7"><h1 style="border-bottom:2px solid #000;padding-bottom:12px">견 적 서</h1><p><b>제목</b> : ${q.title}<br><b>요청일</b> : ${q.date}<br><b>상태</b> : ${q.status}</p><p><b>아티스트</b> : ${q.artists.join(', ')}${q.show ? '<br><b>공연</b> : ' + q.show : ''}</p><p style="color:#888">세부 출연 조건 및 금액은 담당자 회신 메일을 참조해 주세요.<br>BRASSONIT — 연예인 섭외대행 · 공연기획</p></body></html>`
  const url = URL.createObjectURL(new Blob([html], { type: 'text/html' }))
  const a = document.createElement('a')
  a.href = url
  a.download = `견적서_${q.title}.html`
  a.click()
  setTimeout(() => URL.revokeObjectURL(url), 1000)
}

export default function QuotesPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { quotes, refreshQuotes } = useBrass()
  const qSent = !!(location.state as { qSent?: boolean } | null)?.qSent
  const [pageNo, setPageNo] = useState(1)

  useEffect(() => {
    refreshQuotes()
  }, [refreshQuotes])

  // 페이지당 10행 + 숫자 페이징
  const pageCount = Math.max(1, Math.ceil(quotes.length / PAGE))
  const shown = quotes.slice((pageNo - 1) * PAGE, pageNo * PAGE)
  const goPage = (n: number) => {
    setPageNo(n)
    window.scrollTo(0, 0)
  }

  return (
    <section className="mypg">
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        <span className="fw6" style={{ color: '#000' }}>
          견적내역
        </span>
      </div>
      <h1 className="lth">견적내역</h1>
      {qSent && <p className="aok">견적서가 접수되었습니다. 24시간 이내에 회신드리겠습니다.</p>}
      {quotes.length > 0 ? (
        <>
          <div className="fx qhead">
            <span className="qcold">일자</span>
            <span className="qcols">상태</span>
            <span className="f1">제목</span>
            <span className="qcolw">견적서</span>
          </div>
          {shown.map((q, i) => {
            const meta = [q.artists.length ? `아티스트 ${q.artists.length}팀` : '', q.show ? `공연 첨부 : ${q.show}` : '']
              .filter(Boolean)
              .join(' · ')
            return (
              <div className="fx ac qrow" key={i}>
                <span className="qcold fs13">{q.date}</span>
                <span className="qcols">
                  <span className="qtag">{q.status}</span>
                </span>
                <span className="f1">
                  <span className="fw6 fs14">{q.title}</span>
                  <span className="qmeta">{meta}</span>
                </span>
                <span className="qcolw">
                  {q.doc ? (
                    <button className="qdl" onClick={() => downloadQuote(q)}>
                      <DownloadIcon />
                      다운로드
                    </button>
                  ) : (
                    <span className="fs12" style={{ color: '#bbb' }}>
                      대기중
                    </span>
                  )}
                </span>
              </div>
            )
          })}
          {pageCount > 1 && (
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
        </>
      ) : (
        <div className="empty">
          견적 내역이 없습니다.
          <br />
          장바구니에서 아티스트를 선택해 견적서를 보내보세요.
        </div>
      )}
    </section>
  )
}
