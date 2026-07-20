import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { apiErrorMessage, apiUploadQuoteFiles } from '../api'
import { fmtPhone, REGIONS } from '../data'
import { useBrass } from '../store'

interface QuoteFormState {
  qfIds?: string[]
  qfShow?: string
}

type FieldErrs = { email?: string; name?: string; phone?: string; title?: string }

export default function QuoteFormPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { artists, shows, user, userEmail, userName, userPhone, sendQuote } = useBrass()
  const init = (location.state as QuoteFormState | null) || {}
  const loggedIn = !!userEmail

  const [qfIds] = useState<string[]>(init.qfIds || [])
  const [emailIn, setEmailIn] = useState('')
  const [name, setName] = useState(userName)
  const [phone, setPhone] = useState(userPhone)
  const [title, setTitle] = useState('')
  const [date, setDate] = useState('')
  const [dateText, setDateText] = useState('')
  const [region, setRegion] = useState('')
  const [body, setBody] = useState('')
  const [files, setFiles] = useState<File[]>([])
  const [show, setShow] = useState(init.qfShow ?? '')
  const [errs, setErrs] = useState<FieldErrs>({})
  const [sendErr, setSendErr] = useState('')
  const [sending, setSending] = useState(false)
  const [updateProfileCk, setUpdateProfileCk] = useState(true)

  // 문의 모드 — 비로그인 진입(홈 히어로 '섭외 문의하기')
  const inquiry = !loggedIn
  const heading = inquiry ? '섭외 견적 문의' : '섭외 견적 요청'

  const selArtists = qfIds.map((id) => artists.find((a) => a.id === id)).filter(Boolean) as typeof artists
  const sh = show !== '' ? shows.find((s) => s.id === show) : null

  const clearErr = (key: keyof FieldErrs) => setErrs((m) => ({ ...m, [key]: '' }))

  const focusField = (id: string) => {
    setTimeout(() => {
      const el = document.getElementById(id)
      if (!el) return
      const y = el.getBoundingClientRect().top + window.scrollY - 140
      window.scrollTo({ top: y < 0 ? 0 : y, behavior: 'smooth' })
      el.focus({ preventScroll: true })
    }, 60)
  }

  const send = async () => {
    const next: FieldErrs = {}
    if (!loggedIn && !emailIn.trim()) next.email = '이메일을 입력해 주세요.'
    if (!name.trim()) next.name = '이름을 입력해 주세요.'
    if (!phone.trim()) next.phone = '전화번호를 입력해 주세요.'
    if (!title.trim()) next.title = '행사명을 입력해 주세요.'
    if (next.email || next.name || next.phone || next.title) {
      setErrs(next)
      focusField(next.email ? 'qf-email' : next.name ? 'qf-name' : next.phone ? 'qf-phone' : 'qf-title')
      return
    }
    setSending(true)
    setSendErr('')
    try {
      // 첨부파일 실제 업로드 후 URL과 함께 견적 저장
      let attachments: { file_name: string; file_url: string }[] = []
      try {
        attachments = await apiUploadQuoteFiles(files)
      } catch (e) {
        throw new Error(apiErrorMessage(e, '첨부파일 업로드에 실패했습니다.'))
      }
      await sendQuote({
        email: loggedIn ? undefined : emailIn.trim(),
        name: name.trim(),
        phone: phone.trim(),
        event_title: title.trim(),
        event_date: date || undefined,
        event_date_text: dateText || undefined,
        region: region || undefined,
        content: body,
        show_id: sh ? sh.id : undefined,
        artist_ids: qfIds,
        attachments,
        update_profile: loggedIn && updateProfileCk,
      })
      if (loggedIn) navigate('/quotes', { state: { qSent: true } })
      else navigate('/', { state: { qSent: true } })
    } catch (e) {
      setSendErr((e as Error).message)
    } finally {
      setSending(false)
    }
  }

  return (
    <section className="mypg">
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        <span className="fw6" style={{ color: '#000' }}>
          {heading}
        </span>
      </div>
      <h1 className="lth">{heading}</h1>
      <div className="qform">
        {loggedIn ? (
          <div className="mfield">
            <label className="flab">이메일 (가입정보)</label>
            <input value={userEmail} readOnly style={{ background: '#eceae9', color: '#888' }} />
          </div>
        ) : (
          <div className="mfield">
            <label className="flab">
              이메일 <span className="req">*</span>
            </label>
            <input
              id="qf-email"
              value={emailIn}
              onChange={(e) => {
                setEmailIn(e.target.value)
                clearErr('email')
              }}
              placeholder="회신 받을 이메일 주소"
            />
            {errs.email && <p className="ferr">{errs.email}</p>}
          </div>
        )}
        <div className="fx gap12">
          <div className="mfield f1">
            <label className="flab">
              이름 <span className="req">*</span>
            </label>
            <input
              id="qf-name"
              value={name}
              onChange={(e) => {
                setName(e.target.value)
                clearErr('name')
              }}
              placeholder="담당자 이름"
            />
            {errs.name && <p className="ferr">{errs.name}</p>}
          </div>
          <div className="mfield f1">
            <label className="flab">
              전화번호 <span className="req">*</span>
            </label>
            <input
              id="qf-phone"
              value={phone}
              onChange={(e) => {
                setPhone(fmtPhone(e.target.value))
                clearErr('phone')
              }}
              placeholder="010-0000-0000"
            />
            {errs.phone && <p className="ferr">{errs.phone}</p>}
          </div>
        </div>
        <div className="mfield">
          <label className="flab">
            행사명 <span className="req">*</span>
          </label>
          <input
            id="qf-title"
            value={title}
            onChange={(e) => {
              setTitle(e.target.value)
              clearErr('title')
            }}
            placeholder="예) 창립 20주년 기념행사 섭외 문의"
          />
          {errs.title && <p className="ferr">{errs.title}</p>}
        </div>
        <div className="mfield">
          <label className="flab">행사일</label>
          <div className="fx gap12">
            <input
              type="date"
              value={date}
              onChange={(e) => {
                setDate(e.target.value)
                setDateText('')
              }}
              style={{ flex: 'none', width: 170 }}
            />
            <input
              className="f1"
              value={dateText}
              onChange={(e) => {
                setDateText(e.target.value)
                setDate('')
              }}
              placeholder="직접 입력 — 예) 미정 또는 2026년 7월 중순"
            />
          </div>
        </div>
        <div className="mfield">
          <label className="flab">행사지역</label>
          <select className="qselect" value={region} onChange={(e) => setRegion(e.target.value)}>
            <option value="">지역 선택</option>
            {REGIONS.map((r) => (
              <option key={r} value={r}>
                {r}
              </option>
            ))}
          </select>
        </div>
        <div className="mfield">
          <label className="flab">내용</label>
          <textarea className="qta" value={body} onChange={(e) => setBody(e.target.value)} placeholder="행사 일시, 장소, 규모, 예산 범위 등을 알려주세요." />
        </div>
        <div className="mfield">
          <label className="flab">첨부파일</label>
          <label className="qfile">
            <input
              type="file"
              multiple
              style={{ display: 'none' }}
              onChange={(e) => {
                const picked = Array.from(e.target.files || [])
                if (picked.length) setFiles((prev) => [...prev, ...picked])
                e.target.value = ''
              }}
            />
            파일 선택
          </label>
          {files.map((f, i) => (
            <div className="fx ac jb qfrow" key={`${f.name}-${i}`}>
              <span className="fs13">{f.name}</span>
              <button className="qdel" onClick={() => setFiles((prev) => prev.filter((_, j) => j !== i))}>
                삭제
              </button>
            </div>
          ))}
        </div>
        <div className="mfield">
          <label className="flab">공연 선택 — 선택 시 공연과 출연진 목록이 함께 첨부됩니다</label>
          <select className="qselect" value={show} onChange={(e) => setShow(e.target.value)}>
            <option value="">선택 안 함</option>
            {shows.map((o) => (
              <option key={o.id} value={o.id}>
                {o.title} — {o.date}
              </option>
            ))}
          </select>
        </div>
        {selArtists.length > 0 && (
          <>
            <h2 className="qsub">선택한 아티스트 {selArtists.length}팀</h2>
            <div className="fx gap8" style={{ flexWrap: 'wrap' }}>
              {selArtists.map((a) => (
                <span className="fx ac gap8 qchip" key={a.id}>
                  <img src={a.images[0]} alt={a.name} />
                  {a.name}
                </span>
              ))}
            </div>
          </>
        )}
        {sh && (
          <>
            <h2 className="qsub">첨부된 공연</h2>
            <div className="qshowbx">
              <div className="fw7 fs14">{sh.title}</div>
              <div className="fs13" style={{ color: '#888', marginTop: 4 }}>
                {sh.date}
              </div>
              <div className="fs13" style={{ marginTop: 8 }}>
                출연진 자동 첨부 — {sh.lineup.join(', ')}
              </div>
            </div>
          </>
        )}
        {sendErr && <p className="aerr">{sendErr}</p>}
        {loggedIn && user && (
          <label className="fx ac gap8 fs14 pointer" style={{ marginTop: 24 }}>
            <input type="checkbox" className="ckb" checked={updateProfileCk} onChange={(e) => setUpdateProfileCk(e.target.checked)} />
            회원정보의 이름, 전화번호를 입력한 정보로 업데이트 하기
          </label>
        )}
        <button className="bigbtn w100 bbox" style={{ marginTop: 16 }} onClick={send} disabled={sending}>
          {sending ? '전송 중…' : inquiry ? '견적 문의하기' : '견적 요청하기'}
        </button>
      </div>
    </section>
  )
}
