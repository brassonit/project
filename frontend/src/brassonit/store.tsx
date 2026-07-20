// 브라소닛 전역 상태 — backend API 연동 (인증/카탈로그/찜/장바구니/견적)
import { createContext, useCallback, useContext, useEffect, useMemo, useState, type ReactNode } from 'react'
import { useNavigate } from 'react-router-dom'
import type { BrArtist, BrShow } from './data'
import {
  apiCart,
  apiCartAdd,
  apiCartRemove,
  apiCartToggle,
  apiCreateQuote,
  apiErrorMessage,
  apiLogin,
  apiMe,
  apiMyQuotes,
  apiRegister,
  apiResendVerification,
  apiShowWishlist,
  apiShowWishRemove,
  apiShowWishToggle,
  apiUpdateProfile,
  apiVerifyEmail,
  apiWishlist,
  apiWishRemove,
  apiWishToggle,
  apiWithdraw,
  fetchArtists,
  fetchShows,
  type QuoteCreateBody,
  type QuoteDto,
} from './api'

export interface Quote {
  date: string // "2026. 07. 14"
  status: string // 접수완료 | 회신완료
  title: string
  artists: string[]
  show: string
  doc?: boolean
  docUrl?: string
}

type IdMap = Record<string, boolean>

const TOKEN_KEY = 'access_token'

const fmtDate = (iso: string): string => {
  const d = new Date(iso)
  const pad = (n: number) => (n < 10 ? '0' : '') + n
  return `${d.getFullYear()}. ${pad(d.getMonth() + 1)}. ${pad(d.getDate())}`
}

const toQuote = (q: QuoteDto): Quote => ({
  date: fmtDate(q.created_at),
  status: q.status === 'replied' ? '회신완료' : '접수완료',
  title: q.event_title,
  artists: q.artists.map((a) => a.artist_name || ''),
  show: q.show_title || '',
  doc: q.status === 'replied',
  docUrl: q.quote_file_url || undefined,
})

interface BrassState {
  // 카탈로그
  artists: BrArtist[]
  shows: BrShow[]
  loading: boolean
  // 사용자
  user: string | null
  userEmail: string
  userName: string
  userPhone: string
  liked: IdMap
  carted: IdMap
  showLiked: IdMap // 공연 찜 (id → bool)
  quotes: Quote[]
  cartCount: number
  // auth
  signup: (email: string, pw: string) => Promise<void>
  verifyToken: (token: string) => Promise<void>
  resendVerification: (email: string, pw: string) => Promise<void>
  login: (email: string, pw: string) => Promise<void>
  logout: () => void
  updateProfile: (name: string, phone: string, pw?: string) => Promise<void>
  withdraw: () => Promise<void>
  // 찜/장바구니
  toggleLiked: (id: string) => void
  toggleCarted: (id: string) => void
  toggleShowLiked: (id: string) => void
  removeLiked: (ids: string[]) => void
  removeCarted: (ids: string[]) => void
  removeShowLiked: (ids: string[]) => void
  addToCart: (ids: string[]) => void
  // 견적
  sendQuote: (body: QuoteCreateBody) => Promise<void>
  refreshQuotes: () => Promise<void>
  requireLogin: () => boolean
}

const Ctx = createContext<BrassState | null>(null)

export function BrassProvider({ children }: { children: ReactNode }) {
  const navigate = useNavigate()
  const [artists, setArtists] = useState<BrArtist[]>([])
  const [shows, setShows] = useState<BrShow[]>([])
  const [loading, setLoading] = useState(true)
  const [user, setUser] = useState<string | null>(null)
  const [userEmail, setUserEmail] = useState('')
  const [userName, setUserName] = useState('')
  const [userPhone, setUserPhone] = useState('')
  const [liked, setLiked] = useState<IdMap>({})
  const [carted, setCarted] = useState<IdMap>({})
  const [showLiked, setShowLiked] = useState<IdMap>({})
  const [quotes, setQuotes] = useState<Quote[]>([])

  const applyUser = useCallback((u: { email: string; name: string | null; phone: string | null }) => {
    setUserEmail(u.email)
    setUserName(u.name || '')
    setUserPhone(u.phone || '')
    setUser(u.name || u.email.split('@')[0])
  }, [])

  const loadInteractions = useCallback(async () => {
    const [wish, showWish, cart, qs] = await Promise.all([apiWishlist(), apiShowWishlist(), apiCart(), apiMyQuotes()])
    setLiked(Object.fromEntries(wish.map((id) => [id, true])))
    setShowLiked(Object.fromEntries(showWish.map((id) => [id, true])))
    setCarted(Object.fromEntries(cart.map((id) => [id, true])))
    setQuotes(qs.map(toQuote))
  }, [])

  // 초기 로딩 — 카탈로그 + 세션 복원
  useEffect(() => {
    ;(async () => {
      try {
        const [a, s] = await Promise.all([fetchArtists(), fetchShows()])
        setArtists(a)
        setShows(s)
      } catch {
        /* 서버 미기동 시 빈 카탈로그 */
      } finally {
        setLoading(false)
      }
      if (localStorage.getItem(TOKEN_KEY)) {
        try {
          applyUser(await apiMe())
          await loadInteractions()
        } catch {
          localStorage.removeItem(TOKEN_KEY)
        }
      }
    })()
  }, [applyUser, loadInteractions])

  const requireLogin = useCallback(() => {
    if (user) return true
    navigate('/login', { state: { authErr: '로그인이 필요한 기능입니다.' } })
    return false
  }, [user, navigate])

  const value = useMemo<BrassState>(
    () => ({
      artists,
      shows,
      loading,
      user,
      userEmail,
      userName,
      userPhone,
      liked,
      carted,
      showLiked,
      quotes,
      cartCount: Object.values(carted).filter(Boolean).length,

      signup: async (email, pw) => {
        try {
          await apiRegister(email, pw)
        } catch (e) {
          throw new Error(apiErrorMessage(e, '회원가입에 실패했습니다.'))
        }
      },
      verifyToken: async (token) => {
        try {
          await apiVerifyEmail(token)
        } catch (e) {
          throw new Error(apiErrorMessage(e, '이메일 인증에 실패했습니다.'))
        }
      },
      resendVerification: async (email, pw) => {
        try {
          await apiResendVerification(email, pw)
        } catch (e) {
          throw new Error(apiErrorMessage(e, '인증 메일 재발송에 실패했습니다.'))
        }
      },
      login: async (email, pw) => {
        try {
          const { token, user: u } = await apiLogin(email, pw)
          localStorage.setItem(TOKEN_KEY, token)
          applyUser(u)
          await loadInteractions()
        } catch (e) {
          throw new Error(apiErrorMessage(e, '로그인에 실패했습니다.'))
        }
      },
      logout: () => {
        localStorage.removeItem(TOKEN_KEY)
        setUser(null)
        setUserEmail('')
        setUserName('')
        setUserPhone('')
        setLiked({})
        setCarted({})
        setShowLiked({})
        setQuotes([])
      },
      updateProfile: async (name, phone, pw) => {
        try {
          const u = await apiUpdateProfile({ name, phone, password: pw || undefined })
          applyUser(u)
        } catch (e) {
          throw new Error(apiErrorMessage(e, '저장에 실패했습니다.'))
        }
      },
      withdraw: async () => {
        await apiWithdraw()
        localStorage.removeItem(TOKEN_KEY)
        setUser(null)
        setUserEmail('')
        setUserName('')
        setUserPhone('')
        setLiked({})
        setCarted({})
        setShowLiked({})
        setQuotes([])
      },

      toggleLiked: (id) => {
        if (!requireLogin()) return
        // 낙관적 업데이트 후 서버 동기화
        setLiked((m) => ({ ...m, [id]: !m[id] }))
        setArtists((prev) => prev.map((a) => (a.id === id ? { ...a, likes: a.likes + (liked[id] ? -1 : 1) } : a)))
        apiWishToggle(id).catch(() => setLiked((m) => ({ ...m, [id]: !m[id] })))
      },
      toggleCarted: (id) => {
        if (!requireLogin()) return
        setCarted((m) => ({ ...m, [id]: !m[id] }))
        apiCartToggle(id).catch(() => setCarted((m) => ({ ...m, [id]: !m[id] })))
      },
      toggleShowLiked: (id) => {
        if (!requireLogin()) return
        // 낙관적 업데이트 후 서버 동기화 — 찜 시 좋아요 수 +1 반영 (해제 시 -1)
        setShowLiked((m) => ({ ...m, [id]: !m[id] }))
        setShows((prev) => prev.map((s) => (s.id === id ? { ...s, likes: s.likes + (showLiked[id] ? -1 : 1) } : s)))
        apiShowWishToggle(id).catch(() => setShowLiked((m) => ({ ...m, [id]: !m[id] })))
      },
      removeShowLiked: (ids) => {
        setShowLiked((m) => {
          const n = { ...m }
          ids.forEach((id) => delete n[id])
          return n
        })
        apiShowWishRemove(ids).catch(() => {})
      },
      removeLiked: (ids) => {
        setLiked((m) => {
          const n = { ...m }
          ids.forEach((id) => delete n[id])
          return n
        })
        apiWishRemove(ids).catch(() => {})
      },
      removeCarted: (ids) => {
        setCarted((m) => {
          const n = { ...m }
          ids.forEach((id) => delete n[id])
          return n
        })
        apiCartRemove(ids).catch(() => {})
      },
      addToCart: (ids) => {
        setCarted((m) => {
          const n = { ...m }
          ids.forEach((id) => (n[id] = true))
          return n
        })
        apiCartAdd(ids).catch(() => {})
      },

      sendQuote: async (body) => {
        try {
          await apiCreateQuote(body)
        } catch (e) {
          throw new Error(apiErrorMessage(e, '견적 전송에 실패했습니다.'))
        }
        // 발송된 아티스트는 서버에서 장바구니 제거됨 — 로컬 동기화
        setCarted((m) => {
          const n = { ...m }
          body.artist_ids.forEach((id) => delete n[id])
          return n
        })
        if (user) {
          const qs = await apiMyQuotes().catch(() => null)
          if (qs) setQuotes(qs.map(toQuote))
          if (body.update_profile) applyUser(await apiMe().catch(() => ({ email: userEmail, name: body.name, phone: body.phone })))
        }
      },
      refreshQuotes: async () => {
        const qs = await apiMyQuotes().catch(() => null)
        if (qs) setQuotes(qs.map(toQuote))
      },
      requireLogin,
    }),
    [artists, shows, loading, user, userEmail, userName, userPhone, liked, carted, showLiked, quotes, applyUser, loadInteractions, requireLogin],
  )

  return <Ctx.Provider value={value}>{children}</Ctx.Provider>
}

export function useBrass(): BrassState {
  const ctx = useContext(Ctx)
  if (!ctx) throw new Error('useBrass must be used within BrassProvider')
  return ctx
}
