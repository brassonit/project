import { useEffect, useRef, useState } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { useBrass } from '../store'

export default function VerifyEmailPage() {
  const navigate = useNavigate()
  const { verifyToken } = useBrass()
  const [searchParams] = useSearchParams()
  const token = searchParams.get('token')
  const ran = useRef(false)

  const [status, setStatus] = useState<'pending' | 'success' | 'error'>(token ? 'pending' : 'error')
  const [message, setMessage] = useState(token ? '' : '유효하지 않은 인증 링크입니다.')

  useEffect(() => {
    if (!token || ran.current) return
    ran.current = true
    verifyToken(token)
      .then(() => {
        setStatus('success')
        setMessage('이메일 인증이 완료되었습니다. 이제 로그인할 수 있습니다.')
      })
      .catch((e) => {
        setStatus('error')
        setMessage((e as Error).message || '인증에 실패했습니다. 링크가 만료되었거나 유효하지 않습니다.')
      })
  }, [token, verifyToken])

  return (
    <section>
      <div className="authpg" style={{ textAlign: 'center' }}>
        <h1 className="atitle">이메일 인증</h1>
        {status === 'pending' && <p className="mnote">인증 처리 중입니다…</p>}
        {status === 'success' && <p className="aok">{message}</p>}
        {status === 'error' && <p className="aerr">{message}</p>}
        <button className="bigbtn w100 bbox" style={{ marginTop: 18 }} onClick={() => navigate('/login')}>
          로그인 페이지로 이동
        </button>
      </div>
    </section>
  )
}
