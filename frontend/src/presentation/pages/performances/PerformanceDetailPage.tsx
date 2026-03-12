import { useParams, Link } from 'react-router-dom'
import { usePerformance } from '../../../application/hooks/usePerformances'
import { formatDateFull } from '../../../domain/models/utils'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import ErrorMessage from '../../components/common/ErrorMessage'

export default function PerformanceDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data: perf, isLoading, error, refetch } = usePerformance(id!)

  if (isLoading) return <LoadingSpinner />
  if (error || !perf) return <ErrorMessage message="공연 정보를 불러올 수 없습니다." onRetry={refetch} />

  return (
    <div>
      {/* Hero Image */}
      <section className="relative h-[50vh] md:h-[60vh] min-h-[400px]">
        {perf.image_url ? (
          <img src={perf.image_url} alt={perf.title} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-navy-800 via-navy-900 to-navy-950" />
        )}
        {/* Overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-navy-950/90 via-navy-950/40 to-transparent" />

        {/* Content on overlay */}
        <div className="absolute bottom-0 left-0 right-0">
          <div className="max-w-5xl mx-auto px-4 pb-10 md:pb-16">
            <Link
              to="/performances"
              className="inline-flex items-center gap-1 text-sm text-white/70 hover:text-white mb-6 transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              공연 목록
            </Link>

            {perf.is_featured && (
              <span className="inline-block bg-gold-500 text-white text-xs font-bold px-3 py-1 rounded-full mb-4">
                FEATURED
              </span>
            )}

            <h1 className="text-3xl md:text-5xl font-bold text-white mb-4 leading-tight">
              {perf.title}
            </h1>

            <div className="flex flex-wrap gap-6 text-white/80 text-sm">
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                {formatDateFull(perf.event_date)}
              </div>
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gold-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {perf.venue}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Detail Content */}
      <section className="max-w-5xl mx-auto px-4 py-12 md:py-16">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
          {/* Description */}
          <div className="lg:col-span-2">
            <h2 className="text-xl font-bold text-navy-900 mb-6">공연 소개</h2>
            <div className="prose prose-lg max-w-none">
              <p className="text-gray-600 whitespace-pre-line leading-relaxed text-base">
                {perf.description}
              </p>
            </div>
          </div>

          {/* Sidebar Info */}
          <div>
            <div className="bg-gray-50 rounded-2xl p-6 sticky top-24">
              <h3 className="font-bold text-navy-900 mb-5">공연 정보</h3>

              <div className="space-y-4 mb-6">
                <div>
                  <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">일시</p>
                  <p className="font-medium text-gray-900">{formatDateFull(perf.event_date)}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-400 uppercase tracking-wider mb-1">장소</p>
                  <p className="font-medium text-gray-900">{perf.venue}</p>
                </div>
              </div>

              <Link
                to="/inquiry"
                className="block w-full text-center py-3 bg-navy-900 text-white font-medium rounded-xl hover:bg-navy-800 transition-colors"
              >
                이 공연에 대해 문의하기
              </Link>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}
