import { Link } from 'react-router-dom'
import { useFeaturedPerformances } from '../../../application/hooks/usePerformances'
import { ARTIST_CATEGORY_LABELS, ARTIST_CATEGORY_PATHS, type ArtistCategory } from '../../../domain/models/types'
import { CATEGORY_GRADIENTS, CATEGORY_ICONS, formatDate } from '../../../domain/models/utils'

const CATEGORIES = Object.entries(ARTIST_CATEGORY_LABELS) as [ArtistCategory, string][]

export default function HomePage() {
  const { data: featured } = useFeaturedPerformances()

  return (
    <div>
      {/* Hero Banner */}
      <section className="relative bg-navy-950 text-white overflow-hidden">
        {/* Decorative elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-40 -right-40 w-96 h-96 rounded-full bg-gold-500/10 blur-3xl" />
          <div className="absolute bottom-0 -left-20 w-80 h-80 rounded-full bg-blue-500/10 blur-3xl" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 py-24 md:py-36">
          <p className="text-gold-400 font-medium tracking-widest text-sm mb-4">BRASS ON IT</p>
          <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
            최고의 아티스트를<br />섭외해 드립니다
          </h1>
          <p className="text-lg md:text-xl text-navy-300 mb-10 max-w-xl leading-relaxed">
            대중가수, 댄서, 뮤지션, 연주자, 오케스트라까지
            공연 기획부터 섭외까지 원스톱 서비스
          </p>
          <div className="flex flex-wrap gap-4">
            <Link
              to="/inquiry"
              className="px-8 py-3.5 bg-gold-500 text-navy-950 font-semibold rounded-xl hover:bg-gold-400 transition-colors shadow-lg shadow-gold-500/25"
            >
              섭외 요청하기
            </Link>
            <Link
              to="/booking/singers"
              className="px-8 py-3.5 border border-white/20 text-white font-medium rounded-xl hover:bg-white/10 transition-colors"
            >
              아티스트 둘러보기
            </Link>
          </div>
        </div>
      </section>

      {/* Categories */}
      <section className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center mb-14">
          <p className="text-gold-600 font-medium tracking-widest text-sm mb-2">CATEGORIES</p>
          <h2 className="text-3xl font-bold text-navy-900">섭외대행 카테고리</h2>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-5">
          {CATEGORIES.map(([cat, label]) => (
            <Link
              key={cat}
              to={`/booking/${ARTIST_CATEGORY_PATHS[cat]}`}
              className="group bg-white rounded-2xl p-6 text-center hover:shadow-xl transition-all duration-300 hover:-translate-y-1 border border-gray-100"
            >
              <div className={`w-16 h-16 mx-auto mb-4 rounded-2xl bg-gradient-to-br ${CATEGORY_GRADIENTS[cat]} flex items-center justify-center shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 24 24">
                  <path d={CATEGORY_ICONS[cat]} />
                </svg>
              </div>
              <p className="font-semibold text-gray-800 group-hover:text-navy-700 transition-colors">{label}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* Featured Performances */}
      {featured && featured.performances.length > 0 && (
        <section className="bg-navy-950 py-20">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-end justify-between mb-12">
              <div>
                <p className="text-gold-400 font-medium tracking-widest text-sm mb-2">FEATURED</p>
                <h2 className="text-3xl font-bold text-white">주요 공연</h2>
              </div>
              <Link
                to="/performances"
                className="hidden md:flex items-center gap-1 text-sm text-navy-300 hover:text-white transition-colors"
              >
                전체보기
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {featured.performances.slice(0, 3).map((perf) => (
                <Link
                  key={perf.id}
                  to={`/performances/${perf.id}`}
                  className="group rounded-2xl overflow-hidden bg-navy-900 hover:bg-navy-800 transition-colors"
                >
                  <div className="relative h-52 overflow-hidden">
                    {perf.image_url ? (
                      <img
                        src={perf.image_url}
                        alt={perf.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    ) : (
                      <div className="w-full h-full bg-gradient-to-br from-navy-700 to-navy-900 flex items-center justify-center">
                        <svg className="w-14 h-14 text-navy-600" fill="currentColor" viewBox="0 0 24 24">
                          <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z" />
                        </svg>
                      </div>
                    )}
                    <div className="absolute top-3 left-3">
                      <span className="bg-gold-500 text-white text-xs font-bold px-2.5 py-0.5 rounded-full">
                        FEATURED
                      </span>
                    </div>
                  </div>
                  <div className="p-5">
                    <h3 className="font-bold text-lg text-white mb-2 group-hover:text-gold-300 transition-colors">
                      {perf.title}
                    </h3>
                    <div className="flex items-center gap-4 text-sm text-navy-300">
                      <span className="flex items-center gap-1">
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                        {formatDate(perf.event_date)}
                      </span>
                      <span className="flex items-center gap-1">
                        <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        </svg>
                        {perf.venue}
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>

            <div className="text-center mt-8 md:hidden">
              <Link to="/performances" className="text-sm text-navy-300 hover:text-white transition-colors">
                전체보기 →
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-r from-gold-500 to-gold-600" />
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute -top-20 -right-20 w-60 h-60 rounded-full bg-white/10" />
          <div className="absolute -bottom-10 -left-10 w-40 h-40 rounded-full bg-white/10" />
        </div>

        <div className="relative max-w-7xl mx-auto px-4 py-16 md:py-20 text-center">
          <h2 className="text-2xl md:text-3xl font-bold text-navy-950 mb-3">섭외가 필요하신가요?</h2>
          <p className="text-navy-800/70 mb-8 text-lg">원하시는 아티스트에 대해 문의해 주세요</p>
          <Link
            to="/inquiry"
            className="inline-block px-8 py-3.5 bg-navy-950 text-white font-semibold rounded-xl hover:bg-navy-900 transition-colors shadow-lg"
          >
            문의하기
          </Link>
        </div>
      </section>
    </div>
  )
}
