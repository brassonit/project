import { useState, type CSSProperties } from 'react'
import { useNavigate } from 'react-router-dom'
import { fmtPhone } from '../data'
import { useBrass } from '../store'

const sectionTitle: CSSProperties = { fontSize: 18, margin: '40px 0 16px', paddingTop: 32, borderTop: '1px solid #ddd' }

export default function ProfilePage() {
  const navigate = useNavigate()
  const { userEmail, userName, userPhone, updateProfile, withdraw } = useBrass()
  const [name, setName] = useState(userName)
  const [phone, setPhone] = useState(userPhone)
  const [err, setErr] = useState('')
  const [ok, setOk] = useState('')
  const [busy, setBusy] = useState(false)
  // 비밀번호 변경 — 회원정보 저장과 독립 처리
  const [pw, setPw] = useState('')
  const [pw2, setPw2] = useState('')
  const [pwErr, setPwErr] = useState('')
  const [pwOk, setPwOk] = useState('')
  const [pwBusy, setPwBusy] = useState(false)
  const [withdrawAsk, setWithdrawAsk] = useState(false)

  const save = async () => {
    setBusy(true)
    setErr('')
    try {
      await updateProfile(name, phone)
      setOk('저장되었습니다.')
    } catch (e) {
      setOk('')
      setErr((e as Error).message)
    } finally {
      setBusy(false)
    }
  }

  const savePw = async () => {
    if (pw.length < 8) {
      setPwOk('')
      return setPwErr('비밀번호는 8자 이상이어야 합니다.')
    }
    if (pw !== pw2) {
      setPwOk('')
      return setPwErr('비밀번호가 일치하지 않습니다.')
    }
    setPwBusy(true)
    setPwErr('')
    try {
      await updateProfile(userName, userPhone, pw)
      setPw('')
      setPw2('')
      setPwOk('비밀번호가 변경되었습니다.')
    } catch (e) {
      setPwOk('')
      setPwErr((e as Error).message)
    } finally {
      setPwBusy(false)
    }
  }

  const doWithdraw = async () => {
    try {
      await withdraw()
      navigate('/')
    } catch (e) {
      setWithdrawAsk(false)
      setErr((e as Error).message)
    }
  }

  return (
    <section className="mypg">
      <div className="fx ac crumb">
        <button onClick={() => navigate('/')}>홈</button>
        <span>›</span>
        <span className="fw6" style={{ color: '#000' }}>
          회원정보 수정
        </span>
      </div>
      {/* 페이지 h1 없음 — 폼은 브레드크럼에서 32px 아래 시작 */}
      <div className="qform" style={{ marginTop: 32 }}>
        <h2 className="sech2" style={{ fontSize: 18, marginBottom: 16 }}>
          회원정보
        </h2>
        <div className="mfield">
          <label className="flab">이메일 (가입정보)</label>
          <input value={userEmail} readOnly style={{ background: '#eceae9', color: '#888' }} />
        </div>
        <div className="mfield">
          <label className="flab">이름</label>
          <input value={name} onChange={(e) => setName(e.target.value)} placeholder="이름" />
        </div>
        <div className="mfield">
          <label className="flab">휴대폰번호</label>
          <input value={phone} onChange={(e) => setPhone(fmtPhone(e.target.value))} placeholder="010-0000-0000" />
        </div>
        {err && <p className="aerr">{err}</p>}
        {ok && <p className="aok">{ok}</p>}
        <div className="fx mt16" style={{ justifyContent: 'flex-end' }}>
          <button className="bigbtn" style={{ flex: 'none' }} onClick={save} disabled={busy}>
            {busy ? '저장 중…' : '저장'}
          </button>
        </div>

        <h2 className="sech2" style={sectionTitle}>
          비밀번호 변경
        </h2>
        <div className="mfield">
          <label className="flab">비밀번호 변경</label>
          <input type="password" value={pw} onChange={(e) => setPw(e.target.value)} placeholder="새 비밀번호 (8자 이상)" />
        </div>
        <div className="mfield">
          <label className="flab">비밀번호 변경 확인</label>
          <input type="password" value={pw2} onChange={(e) => setPw2(e.target.value)} placeholder="새 비밀번호 확인" />
        </div>
        {pwErr && <p className="aerr">{pwErr}</p>}
        {pwOk && <p className="aok">{pwOk}</p>}
        <div className="fx mt16" style={{ justifyContent: 'flex-end' }}>
          <button className="bigbtn" style={{ flex: 'none' }} onClick={savePw} disabled={pwBusy}>
            {pwBusy ? '변경 중…' : '비밀번호 변경'}
          </button>
        </div>

        <h2 className="sech2" style={sectionTitle}>
          회원탈퇴
        </h2>
        <p className="fs14" style={{ color: '#666', lineHeight: 1.7, margin: 0 }}>
          기존 견적내역이 모두 삭제됩니다.
          <br />
          탈퇴 시 계정 정보, 찜리스트, 장바구니, 견적 내역이 즉시 삭제되며 복구할 수 없습니다.
        </p>
        <div className="fx mt16" style={{ justifyContent: 'flex-end' }}>
          <button className="bigbtn ghost" style={{ flex: 'none', color: '#888', borderColor: '#ccc' }} onClick={() => setWithdrawAsk(true)}>
            회원탈퇴
          </button>
        </div>
      </div>
      {withdrawAsk && (
        <div className="mbk">
          <div className="modal">
            <h2 className="fs20 fw7 m0">회원탈퇴</h2>
            <p className="fs14 mt12" style={{ lineHeight: 1.6 }}>
              정말로 탈퇴하시겠습니까?
            </p>
            <div className="fx ac jb mt16 gap10">
              <button className="bigbtn ghost" style={{ flex: 1 }} onClick={() => setWithdrawAsk(false)}>
                아니오
              </button>
              <button className="bigbtn" style={{ flex: 1 }} onClick={doWithdraw}>
                예, 탈퇴합니다
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  )
}
