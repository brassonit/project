import { Outlet, Link, useLocation, Navigate } from 'react-router-dom'
import { useAuth } from '../../infrastructure/auth/useAuth'
import LoadingSpinner from '../components/common/LoadingSpinner'

const ADMIN_NAV = [
  { path: '/admin', label: '대시보드', exact: true },
  { path: '/admin/artists', label: '아티스트 관리' },
  { path: '/admin/performances', label: '공연 관리' },
  { path: '/admin/inquiries', label: '문의 관리' },
]

export default function AdminLayout() {
  const { user, isAdmin, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) return <LoadingSpinner />
  if (!user) return <Navigate to="/login" replace />
  if (!isAdmin) return <Navigate to="/" replace />

  const isActive = (path: string, exact?: boolean) =>
    exact ? location.pathname === path : location.pathname.startsWith(path)

  return (
    <div className="min-h-screen flex bg-gray-100">
      {/* Sidebar */}
      <aside className="w-60 bg-gray-900 text-white flex-shrink-0 hidden lg:block">
        <div className="p-4">
          <Link to="/" className="text-lg font-bold text-blue-400">BRASS ON IT</Link>
          <p className="text-xs text-gray-400 mt-1">관리자 페이지</p>
        </div>
        <nav className="mt-4">
          {ADMIN_NAV.map(({ path, label, exact }) => (
            <Link
              key={path}
              to={path}
              className={`block px-4 py-3 text-sm transition-colors ${
                isActive(path, exact)
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              {label}
            </Link>
          ))}
        </nav>
        <div className="absolute bottom-0 left-0 w-60 p-4 border-t border-gray-700">
          <Link to="/" className="text-sm text-gray-400 hover:text-white">
            ← 사이트로 돌아가기
          </Link>
        </div>
      </aside>

      {/* Mobile Header + Content */}
      <div className="flex-1 flex flex-col">
        {/* Mobile admin nav */}
        <div className="lg:hidden bg-gray-900 text-white px-4 py-3 flex items-center justify-between">
          <Link to="/" className="font-bold text-blue-400">BRASS ON IT 관리자</Link>
          <Link to="/" className="text-sm text-gray-400">← 사이트</Link>
        </div>
        <div className="lg:hidden bg-gray-800 overflow-x-auto">
          <div className="flex">
            {ADMIN_NAV.map(({ path, label, exact }) => (
              <Link
                key={path}
                to={path}
                className={`px-4 py-2 text-sm whitespace-nowrap ${
                  isActive(path, exact)
                    ? 'text-blue-400 border-b-2 border-blue-400'
                    : 'text-gray-400'
                }`}
              >
                {label}
              </Link>
            ))}
          </div>
        </div>

        <main className="flex-1 p-4 md:p-6 lg:p-8">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
