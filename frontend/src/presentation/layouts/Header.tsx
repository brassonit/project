import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../../infrastructure/auth/useAuth'
import { ARTIST_CATEGORY_LABELS, ARTIST_CATEGORY_PATHS, type ArtistCategory } from '../../domain/models/types'

const CATEGORIES = Object.entries(ARTIST_CATEGORY_LABELS) as [ArtistCategory, string][]

export default function Header() {
  const { user, isAdmin, logout } = useAuth()
  const location = useLocation()
  const [mobileOpen, setMobileOpen] = useState(false)
  const [bookingOpen, setBookingOpen] = useState(false)

  const isActive = (path: string) =>
    location.pathname === path || location.pathname.startsWith(path + '/')

  const navLinkClass = (path: string) =>
    `px-3 py-2 text-sm font-medium tracking-wide transition-colors ${
      isActive(path) ? 'text-navy-900' : 'text-gray-500 hover:text-navy-900'
    }`

  return (
    <header className="bg-white/95 backdrop-blur-md border-b border-gray-100 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="text-lg font-bold tracking-wider text-navy-900">
            BRASS ON IT
          </Link>

          {/* Desktop Nav */}
          <nav className="hidden md:flex items-center gap-1">
            <Link to="/" className={navLinkClass('/')}>HOME</Link>
            <Link to="/performances" className={navLinkClass('/performances')}>주요공연</Link>

            {/* 섭외대행 Dropdown */}
            <div
              className="relative"
              onMouseEnter={() => setBookingOpen(true)}
              onMouseLeave={() => setBookingOpen(false)}
            >
              <button className={`${navLinkClass('/booking')} flex items-center gap-1`}>
                섭외대행
                <svg className={`w-3.5 h-3.5 transition-transform ${bookingOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              {bookingOpen && (
                <div className="absolute top-full left-0 bg-white shadow-xl rounded-xl py-2 min-w-[180px] border border-gray-100 mt-0.5">
                  {CATEGORIES.map(([cat, label]) => (
                    <Link
                      key={cat}
                      to={`/booking/${ARTIST_CATEGORY_PATHS[cat]}`}
                      className="block px-4 py-2.5 text-sm text-gray-600 hover:bg-navy-50 hover:text-navy-900 transition-colors"
                    >
                      {label}
                    </Link>
                  ))}
                </div>
              )}
            </div>

            <Link to="/inquiry" className={navLinkClass('/inquiry')}>문의하기</Link>
          </nav>

          {/* Auth + Admin */}
          <div className="hidden md:flex items-center gap-3">
            {user ? (
              <>
                {isAdmin && (
                  <Link
                    to="/admin"
                    className="px-3.5 py-1.5 text-sm font-medium text-navy-900 border border-navy-200 rounded-lg hover:bg-navy-50 transition-colors"
                  >
                    관리자
                  </Link>
                )}
                <span className="text-sm text-gray-400">{user.email}</span>
                <button
                  onClick={logout}
                  className="px-3 py-1.5 text-sm text-gray-500 hover:text-navy-900 transition-colors"
                >
                  로그아웃
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="px-3 py-1.5 text-sm text-gray-500 hover:text-navy-900 transition-colors">
                  로그인
                </Link>
                <Link
                  to="/register"
                  className="px-4 py-1.5 text-sm font-medium text-white bg-navy-900 rounded-lg hover:bg-navy-800 transition-colors"
                >
                  회원가입
                </Link>
              </>
            )}
          </div>

          {/* Mobile Hamburger */}
          <button
            className="md:hidden p-2 -mr-2"
            onClick={() => setMobileOpen(!mobileOpen)}
            aria-label="메뉴 열기"
          >
            <svg className="w-6 h-6 text-navy-900" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileOpen && (
          <nav className="md:hidden pb-5 pt-2 border-t border-gray-100 space-y-1">
            <Link to="/" className="block px-3 py-2.5 text-sm font-medium text-gray-700 rounded-lg hover:bg-gray-50" onClick={() => setMobileOpen(false)}>HOME</Link>
            <Link to="/performances" className="block px-3 py-2.5 text-sm font-medium text-gray-700 rounded-lg hover:bg-gray-50" onClick={() => setMobileOpen(false)}>주요공연</Link>
            <div className="px-3 pt-3 pb-1 text-xs font-semibold text-gray-400 tracking-wider uppercase">섭외대행</div>
            {CATEGORIES.map(([cat, label]) => (
              <Link
                key={cat}
                to={`/booking/${ARTIST_CATEGORY_PATHS[cat]}`}
                className="block px-6 py-2 text-sm text-gray-600 rounded-lg hover:bg-gray-50"
                onClick={() => setMobileOpen(false)}
              >
                {label}
              </Link>
            ))}
            <Link to="/inquiry" className="block px-3 py-2.5 text-sm font-medium text-gray-700 rounded-lg hover:bg-gray-50" onClick={() => setMobileOpen(false)}>문의하기</Link>
            <div className="border-t border-gray-100 mt-3 pt-3 space-y-1">
              {user ? (
                <>
                  {isAdmin && (
                    <Link to="/admin" className="block px-3 py-2.5 text-sm font-medium text-navy-700 rounded-lg hover:bg-gray-50" onClick={() => setMobileOpen(false)}>관리자</Link>
                  )}
                  <button onClick={() => { logout(); setMobileOpen(false) }} className="block w-full text-left px-3 py-2.5 text-sm text-gray-500 rounded-lg hover:bg-gray-50">로그아웃</button>
                </>
              ) : (
                <>
                  <Link to="/login" className="block px-3 py-2.5 text-sm text-gray-700 rounded-lg hover:bg-gray-50" onClick={() => setMobileOpen(false)}>로그인</Link>
                  <Link to="/register" className="block px-3 py-2.5 text-sm font-medium text-navy-700 rounded-lg hover:bg-gray-50" onClick={() => setMobileOpen(false)}>회원가입</Link>
                </>
              )}
            </div>
          </nav>
        )}
      </div>
    </header>
  )
}
