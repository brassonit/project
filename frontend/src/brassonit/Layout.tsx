import { useEffect, useState } from 'react'
import { Outlet, useLocation, useNavigate, useParams } from 'react-router-dom'
import { MENU_ORDER, SUBS } from './data'
import { useBrass } from './store'
import { CartIcon, ChevronUp, HeartIcon, SearchIcon, UserIcon } from './icons'
import './brassonit.css'

export default function BrassLayout() {
  const navigate = useNavigate()
  const location = useLocation()
  const { user, cartCount, logout, requireLogin } = useBrass()
  const [q, setQ] = useState('')
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const [hoverCat, setHoverCat] = useState<string | null>(null)
  // 드롭다운에서 이동 직후에는 메가메뉴를 열지 않음 — 마우스가 GNB를 벗어나면 해제
  const [megaLock, setMegaLock] = useState(false)
  const [showTop, setShowTop] = useState(false)
  const params = useParams()

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [location.pathname, location.search])

  useEffect(() => {
    const onScroll = () => setShowTop(window.scrollY > 400)
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [])

  const goWithLock = (path: string) => {
    setUserMenuOpen(false)
    setMegaLock(true)
    navigate(path)
  }

  const curCat = location.pathname.startsWith('/category/') ? decodeURIComponent(params.cat || location.pathname.split('/')[2] || '') : null

  const isMobileList = location.pathname.startsWith('/category/')
  const catForSub = curCat && SUBS[curCat] ? curCat : null
  const curSub = catForSub ? decodeURIComponent(location.pathname.split('/')[3] || '') : ''

  return (
    <div className="br-root">
      <header className="wrap">
        <div className="fx ac hdr">
          <button className="logo" onClick={() => navigate('/')}>
            brasso<span>nit</span>
            <span className="logosub">공연기획사 브라소닛</span>
          </button>
          <div className="fx ac srch">
            <SearchIcon />
            <input
              placeholder="어떤 아티스트를 찾으세요?"
              value={q}
              onChange={(e) => setQ(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && q.trim()) navigate(`/search?q=${encodeURIComponent(q.trim())}`)
              }}
            />
          </div>
          <div className="fx ac gap12 noshrink authwrap">
            {!user ? (
              <>
                <button className="authb" onClick={() => navigate('/signup')}>
                  회원가입
                </button>
                <button className="authb" style={{ background: '#000', borderColor: '#000', color: '#fff', padding: '8px 16px' }} onClick={() => navigate('/login')}>
                  로그인
                </button>
              </>
            ) : (
              <>
                <div className="posrel" onMouseLeave={() => setUserMenuOpen(false)}>
                  <button className="uicon" onClick={() => setUserMenuOpen((v) => !v)} title="내 계정">
                    <UserIcon />
                  </button>
                  {userMenuOpen && (
                    <div className="umenu">
                      {/* 사용자명 — 링크 없는 플레인 텍스트 */}
                      <span className="uname">{user}님</span>
                      <button onClick={() => goWithLock('/profile')}>회원정보</button>
                      <button onClick={() => goWithLock('/quotes')}>견적내역</button>
                      <button
                        className="uout"
                        onClick={() => {
                          setUserMenuOpen(false)
                          setMegaLock(true)
                          logout()
                          navigate('/')
                        }}
                      >
                        로그아웃
                      </button>
                    </div>
                  )}
                </div>
                <button className="uicon" onClick={() => navigate('/wishlist')} title="찜리스트">
                  <HeartIcon size={22} />
                </button>
                <button
                  className="uicon posrel"
                  onClick={() => {
                    if (requireLogin()) navigate('/cart')
                  }}
                  title="장바구니"
                >
                  <CartIcon />
                  {cartCount > 0 && <span className="fx ac jc cbadge">{cartCount}</span>}
                </button>
              </>
            )}
          </div>
        </div>
      </header>

      <nav
        className={`gnb${megaLock ? ' mega-lock' : ''}`}
        onMouseLeave={() => {
          setHoverCat(null)
          setMegaLock(false)
        }}
      >
        <div className="wrap posrel">
          {/* 메가메뉴는 메뉴 탭 영역(gnbwrap)에 hover했을 때만 열림 — CSS `.gnbwrap:hover + .mega` */}
          <div className="gnbwrap">
            <div className="fx ac gnbrow">
              {MENU_ORDER.map((cat) => (
                <button
                  key={cat}
                  className={`gtab${curCat === cat ? ' on' : ''}${hoverCat === cat ? ' hov' : ''}`}
                  onClick={() => {
                    setMegaLock(true)
                    navigate(`/category/${encodeURIComponent(cat)}`)
                  }}
                  onMouseEnter={() => setHoverCat(cat)}
                >
                  {cat}
                </button>
              ))}
            </div>
          </div>
          <div className="mega">
            <div className="wrap">
              <div className="megagrid">
                {MENU_ORDER.map((cat) => (
                  <div className="mcol" key={cat}>
                    <h3
                      className="mtitle"
                      onClick={() => {
                        setMegaLock(true)
                        navigate(`/category/${encodeURIComponent(cat)}`)
                      }}
                    >
                      {cat}
                    </h3>
                    {SUBS[cat].map((sub) => (
                      <button
                        key={sub}
                        className="msub"
                        onClick={() => {
                          setMegaLock(true)
                          navigate(`/category/${encodeURIComponent(cat)}/${encodeURIComponent(sub)}`)
                        }}
                      >
                        {sub}
                      </button>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </div>
          {isMobileList && catForSub && (
            <div className="subbar">
              {[null, ...SUBS[catForSub]].map((sub) => (
                <button
                  key={sub || '전체'}
                  className={`schip${(curSub || '') === (sub || '') ? ' on' : ''}`}
                  onClick={() => navigate(sub ? `/category/${encodeURIComponent(catForSub)}/${encodeURIComponent(sub)}` : `/category/${encodeURIComponent(catForSub)}`)}
                >
                  {sub || '전체'}
                </button>
              ))}
            </div>
          )}
        </div>
      </nav>

      <main className="wrap">
        <Outlet />
      </main>

      {showTop && (
        <button className="topb" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })} title="맨 위로">
          <ChevronUp />
        </button>
      )}

      <footer>
        <div className="wrap ftr ftgrid">
          <div className="fx ac gap24 ftm">
            <span className="fw7" style={{ color: '#000' }}>
              brassonit
            </span>
            <button className="ftrb" onClick={() => navigate('/about')}>
              브라소닛 소개
            </button>
            <button className="ftrb" onClick={() => navigate('/privacy')}>
              개인정보취급방침
            </button>
            <button className="ftrb" onClick={() => navigate('/terms')}>
              이용약관
            </button>
          </div>
          <span className="ftrc">© 2026 brassonit. All rights reserved.</span>
          <div className="fx ac gap12 snsw">
            <a className="snsb" href="https://www.facebook.com" target="_blank" rel="noopener noreferrer" title="페이스북">
              <svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor">
                <path d="M22 12a10 10 0 1 0-11.56 9.88v-6.99H7.9V12h2.54V9.8c0-2.5 1.49-3.89 3.77-3.89 1.09 0 2.24.2 2.24.2v2.46h-1.26c-1.24 0-1.63.77-1.63 1.56V12h2.78l-.45 2.89h-2.33v6.99A10 10 0 0 0 22 12z" />
              </svg>
            </a>
            <a className="snsb" href="https://www.instagram.com" target="_blank" rel="noopener noreferrer" title="인스타그램">
              <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2">
                <rect width="19" height="19" x="2.5" y="2.5" rx="5.5" />
                <circle cx="12" cy="12" r="4.2" />
                <line x1="17.4" x2="17.41" y1="6.6" y2="6.6" />
              </svg>
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}
