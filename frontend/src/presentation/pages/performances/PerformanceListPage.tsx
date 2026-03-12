import { useState } from 'react'
import { Link } from 'react-router-dom'
import { usePerformances, useFeaturedPerformances } from '../../../application/hooks/usePerformances'
import { formatDate } from '../../../domain/models/utils'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import ErrorMessage from '../../components/common/ErrorMessage'

type Tab = 'all' | 'featured'

export default function PerformanceListPage() {
  const [tab, setTab] = useState<Tab>('all')
  const [page, setPage] = useState(0)
  const limit = 9

  const allQuery = usePerformances({ skip: page * limit, limit })
  const featuredQuery = useFeaturedPerformances()

  const isAll = tab === 'all'
  const query = isAll ? allQuery : featuredQuery
  const { isLoading, error } = query

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage message="공연 목록을 불러올 수 없습니다." onRetry={() => query.refetch()} />

  const performances = isAll
    ? (allQuery.data?.performances ?? [])
    : (featuredQuery.data?.performances ?? [])
  const total = isAll ? (allQuery.data?.total ?? 0) : performances.length
  const totalPages = isAll ? Math.ceil(total / limit) : 1

  return (
    <div>
      {/* Hero */}
      <section className="bg-navy-900 text-white">
        <div className="max-w-7xl mx-auto px-4 py-16 md:py-24">
          <p className="text-gold-400 font-medium tracking-widest text-sm mb-3">PERFORMANCES</p>
          <h1 className="text-3xl md:text-5xl font-bold mb-4">주요 공연</h1>
          <p className="text-navy-300 text-lg max-w-xl">
            BRASS ON IT이 기획하고 운영하는 특별한 공연을 확인해 보세요.
          </p>
        </div>
      </section>

      {/* Content */}
      <section className="max-w-7xl mx-auto px-4 py-12">
        {/* Tabs */}
        <div className="flex gap-1 mb-10 border-b border-gray-200">
          {([['all', '전체 공연'], ['featured', '주요 공연']] as const).map(([key, label]) => (
            <button
              key={key}
              onClick={() => { setTab(key); setPage(0) }}
              className={`px-5 py-3 text-sm font-medium border-b-2 transition-colors -mb-px ${
                tab === key
                  ? 'border-navy-900 text-navy-900'
                  : 'border-transparent text-gray-400 hover:text-gray-600'
              }`}
            >
              {label}
            </button>
          ))}
        </div>

        {performances.length === 0 ? (
          <div className="text-center py-24">
            <svg className="w-16 h-16 mx-auto text-gray-300 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 19V6l12-3v13M9 19c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zm12-3c0 1.105-1.343 2-3 2s-3-.895-3-2 1.343-2 3-2 3 .895 3 2zM9 10l12-3" />
            </svg>
            <p className="text-gray-400 text-lg">등록된 공연이 없습니다.</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {performances.map((perf) => (
                <Link
                  key={perf.id}
                  to={`/performances/${perf.id}`}
                  className="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                >
                  {/* Image */}
                  <div className="relative h-56 overflow-hidden">
                    {perf.image_url ? (
                      <img
                        src={perf.image_url}
                        alt={perf.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-navy-800 to-navy-950 flex items-center justify-center">
                        <svg className="w-16 h-16 text-navy-600" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" />
                        </svg>
                      </div>
                    )}
                    {perf.is_featured && (
                      <div className="absolute top-4 left-4">
                        <span className="bg-gold-500 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md">
                          FEATURED
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Info */}
                  <div className="p-5">
                    <div className="flex items-center gap-2 text-sm text-gray-400 mb-2">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      {formatDate(perf.event_date)}
                    </div>
                    <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-navy-700 transition-colors">
                      {perf.title}
                    </h3>
                    <div className="flex items-center gap-1.5 text-sm text-gray-500">
                      <svg className="w-4 h-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      {perf.venue}
                    </div>
                  </div>
                </Link>
              ))}
            </div>

            {/* Pagination */}
            {isAll && totalPages > 1 && (
              <div className="flex justify-center items-center gap-1 mt-14">
                <button
                  onClick={() => setPage(Math.max(0, page - 1))}
                  disabled={page === 0}
                  className="p-2 rounded-lg text-gray-400 hover:text-gray-700 disabled:opacity-30"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
                  </svg>
                </button>
                {Array.from({ length: totalPages }, (_, i) => (
                  <button
                    key={i}
                    onClick={() => setPage(i)}
                    className={`w-10 h-10 rounded-lg text-sm font-medium transition-colors ${
                      page === i
                        ? 'bg-navy-900 text-white'
                        : 'text-gray-500 hover:bg-gray-100'
                    }`}
                  >
                    {i + 1}
                  </button>
                ))}
                <button
                  onClick={() => setPage(Math.min(totalPages - 1, page + 1))}
                  disabled={page === totalPages - 1}
                  className="p-2 rounded-lg text-gray-400 hover:text-gray-700 disabled:opacity-30"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </button>
              </div>
            )}
          </>
        )}
      </section>
    </div>
  )
}
