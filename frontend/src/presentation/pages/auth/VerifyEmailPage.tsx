import { useEffect, useState } from 'react'
import { Link, useSearchParams, useLocation } from 'react-router-dom'
import apiClient from '../../../infrastructure/api/client'

export default function VerifyEmailPage() {
  const [searchParams] = useSearchParams()
  const location = useLocation()
  const token = searchParams.get('token')
  const emailFromState = (location.state as { email?: string })?.email

  const [status, setStatus] = useState<'pending' | 'success' | 'error'>(token ? 'pending' : 'success')
  const [message, setMessage] = useState('')

  useEffect(() => {
    if (!token) return
    apiClient
      .get('/auth/verify-email', { params: { token } })
      .then(() => {
        setStatus('success')
        setMessage('이메일 인증이 완료되었습니다!')
      })
      .catch(() => {
        setStatus('error')
        setMessage('인증에 실패했습니다. 토큰이 만료되었거나 유효하지 않습니다.')
      })
  }, [token])

  // Registration success - show "check your email" message
  if (!token) {
    return (
      <div className="min-h-[60vh] flex items-center justify-center px-4">
        <div className="text-center max-w-md">
          <div className="text-5xl mb-4">📧</div>
          <h1 className="text-2xl font-bold mb-3">인증 이메일을 확인해 주세요</h1>
          <p className="text-gray-500 mb-6">
            {emailFromState ? (
              <><strong>{emailFromState}</strong>으로 인증 이메일을 보냈습니다.</>
            ) : (
              '가입하신 이메일로 인증 링크를 보냈습니다.'
            )}
            <br />이메일의 링크를 클릭하면 인증이 완료됩니다.
          </p>
          <Link to="/login" className="text-blue-600 hover:underline">
            로그인 페이지로 이동
          </Link>
        </div>
      </div>
    )
  }

  // Token verification in progress / result
  return (
    <div className="min-h-[60vh] flex items-center justify-center px-4">
      <div className="text-center max-w-md">
        {status === 'pending' && (
          <>
            <div className="animate-spin rounded-full h-10 w-10 border-4 border-gray-300 border-t-blue-600 mx-auto mb-4" />
            <p className="text-gray-500">이메일 인증 중...</p>
          </>
        )}
        {status === 'success' && (
          <>
            <div className="text-5xl mb-4">✅</div>
            <h1 className="text-2xl font-bold mb-3">{message}</h1>
            <Link to="/login" className="text-blue-600 hover:underline">
              로그인하러 가기
            </Link>
          </>
        )}
        {status === 'error' && (
          <>
            <div className="text-5xl mb-4">❌</div>
            <h1 className="text-2xl font-bold mb-3">인증 실패</h1>
            <p className="text-gray-500 mb-6">{message}</p>
            <Link to="/login" className="text-blue-600 hover:underline">
              로그인 페이지로 이동
            </Link>
          </>
        )}
      </div>
    </div>
  )
}
