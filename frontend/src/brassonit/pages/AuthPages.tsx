import { useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'
import { useBrass } from '../store'

export function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const { login } = useBrass()
  const [email, setEmail] = useState('')
  const [pw, setPw] = useState('')
  const [err, setErr] = useState<string>((location.state as { authErr?: string } | null)?.authErr || '')
  const [busy, setBusy] = useState(false)

  const doLogin = async () => {
    const em = email.trim()
    if (!em || !pw) return setErr('이메일과 비밀번호를 입력해 주세요.')
    setBusy(true)
    setErr('')
    try {
      await login(em, pw)
      navigate('/')
    } catch (e) {
      setErr((e as Error).message)
    } finally {
      setBusy(false)
    }
  }

  return (
    <section>
      <div className="authpg">
        <h1 className="atitle">로그인</h1>
        <div className="mfield">
          <input placeholder="이메일" value={email} onChange={(e) => setEmail(e.target.value)} />
        </div>
        <div className="mfield">
          <input type="password" placeholder="비밀번호" value={pw} onChange={(e) => setPw(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && doLogin()} />
        </div>
        {err && <p className="aerr">{err}</p>}
        <button className="bigbtn w100 bbox" onClick={doLogin} disabled={busy}>
          {busy ? '로그인 중…' : '로그인'}
        </button>
        <p className="mnote">
          계정이 없으신가요?{' '}
          <button className="albtn" onClick={() => navigate('/signup')}>
            회원가입
          </button>
        </p>
      </div>
    </section>
  )
}

export function SignupPage() {
  const navigate = useNavigate()
  const { signup, resendVerification } = useBrass()
  const [email, setEmail] = useState('')
  const [pw, setPw] = useState('')
  const [pw2, setPw2] = useState('')
  const [err, setErr] = useState('')
  const [ok, setOk] = useState('')
  const [busy, setBusy] = useState(false)
  const [done, setDone] = useState(false)
  const [resent, setResent] = useState(false)

  const doSignup = async () => {
    const em = email.trim()
    if (!/\S+@\S+\.\S+/.test(em)) return setErr('올바른 이메일 주소를 입력해 주세요.')
    if (pw.length < 8) return setErr('비밀번호는 8자 이상이어야 합니다.')
    if (pw !== pw2) return setErr('비밀번호가 일치하지 않습니다.')
    setBusy(true)
    setErr('')
    try {
      await signup(em, pw)
      setDone(true)
      setOk(`인증 메일을 ${em} 주소로 보냈습니다. 메일의 링크를 눌러 인증을 완료해 주세요.`)
    } catch (e) {
      setErr((e as Error).message)
    } finally {
      setBusy(false)
    }
  }

  const doResend = async () => {
    setErr('')
    setResent(false)
    try {
      await resendVerification(email.trim(), pw)
      setResent(true)
    } catch (e) {
      setErr((e as Error).message)
    }
  }

  return (
    <section>
      <div className="authpg">
        <h1 className="atitle">회원가입</h1>
        {!done ? (
          <>
            <div className="mfield">
              <input placeholder="이메일" value={email} onChange={(e) => setEmail(e.target.value)} />
            </div>
            <div className="mfield">
              <input type="password" placeholder="비밀번호 (8자 이상)" value={pw} onChange={(e) => setPw(e.target.value)} />
            </div>
            <div className="mfield">
              <input type="password" placeholder="비밀번호 확인" value={pw2} onChange={(e) => setPw2(e.target.value)} />
            </div>
            {err && <p className="aerr">{err}</p>}
            <button className="bigbtn w100 bbox" onClick={doSignup} disabled={busy}>
              {busy ? '가입 중…' : '가입하기'}
            </button>
          </>
        ) : (
          <>
            <p className="aok">{ok}</p>
            {err && <p className="aerr">{err}</p>}
            {resent && <p className="aok">인증 메일을 다시 보냈습니다.</p>}
            <button className="moreb" style={{ margin: '0 0 14px' }} onClick={doResend}>
              인증 메일 재발송
            </button>
            <button className="bigbtn w100 bbox" onClick={() => navigate('/login')}>
              로그인 하러 가기
            </button>
          </>
        )}
        <p className="mnote">
          이미 계정이 있으신가요?{' '}
          <button className="albtn" onClick={() => navigate('/login')}>
            로그인
          </button>
        </p>
      </div>
    </section>
  )
}
