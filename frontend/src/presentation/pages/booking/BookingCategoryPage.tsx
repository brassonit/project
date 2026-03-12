import { useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useArtists } from '../../../application/hooks/useArtists'
import {
  PATH_TO_CATEGORY,
  ARTIST_CATEGORY_LABELS,
  ARTIST_CATEGORY_PATHS,
  type ArtistCategory,
} from '../../../domain/models/types'
import { CATEGORY_GRADIENTS, CATEGORY_DESCRIPTIONS, CATEGORY_ICONS } from '../../../domain/models/utils'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import ErrorMessage from '../../components/common/ErrorMessage'

const ALL_CATEGORIES = Object.entries(ARTIST_CATEGORY_LABELS) as [ArtistCategory, string][]

export default function BookingCategoryPage() {
  const { categoryPath } = useParams<{ categoryPath: string }>()
  const category = categoryPath ? PATH_TO_CATEGORY[categoryPath] : undefined
  const label = category ? ARTIST_CATEGORY_LABELS[category] : '섭외대행'
  const gradient = category ? CATEGORY_GRADIENTS[category] : 'from-navy-700 to-navy-900'
  const description = category ? CATEGORY_DESCRIPTIONS[category] : ''
  const iconPath = category ? CATEGORY_ICONS[category] : ''

  const [page, setPage] = useState(0)
  const limit = 12
  const { data, isLoading, error, refetch } = useArtists({
    category,
    skip: page * limit,
    limit,
  })

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage message="아티스트 목록을 불러올 수 없습니다." onRetry={refetch} />

  const artists = data?.artists ?? []
  const total = data?.total ?? 0
  const totalPages = Math.ceil(total / limit)

  return (
    <div>
      {/* Hero */}
      <section className={`bg-gradient-to-br ${gradient} text-white`}>
        <div className="max-w-7xl mx-auto px-4 py-16 md:py-24">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 rounded-2xl bg-white/15 backdrop-blur flex items-center justify-center">
              <svg className="w-7 h-7 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d={iconPath} />
              </svg>
            </div>
            <div>
              <p className="text-white/60 font-medium tracking-widest text-xs">ARTIST BOOKING</p>
              <h1 className="text-3xl md:text-4xl font-bold">{label}</h1>
            </div>
          </div>
          <p className="text-white/70 text-lg max-w-2xl mt-4 leading-relaxed">{description}</p>
        </div>
      </section>

      {/* Category Tabs */}
      <div className="bg-white border-b border-gray-200 sticky top-16 z-40">
        <div className="max-w-7xl mx-auto px-4">
          <div className="flex gap-0.5 overflow-x-auto -mb-px">
            {ALL_CATEGORIES.map(([cat, catLabel]) => {
              const isActive = category === cat
              return (
                <Link
                  key={cat}
                  to={`/booking/${ARTIST_CATEGORY_PATHS[cat]}`}
                  onClick={() => setPage(0)}
                  className={`px-4 md:px-5 py-3.5 text-sm font-medium whitespace-nowrap border-b-2 transition-colors ${
                    isActive
                      ? 'border-navy-900 text-navy-900'
                      : 'border-transparent text-gray-400 hover:text-gray-600 hover:border-gray-300'
                  }`}
                >
                  {catLabel}
                </Link>
              )
            })}
          </div>
        </div>
      </div>

      {/* Artist Grid */}
      <section className="max-w-7xl mx-auto px-4 py-12">
        <div className="flex items-center justify-between mb-8">
          <p className="text-gray-500">
            총 <span className="font-semibold text-navy-900">{total}</span>명의 아티스트
          </p>
        </div>

        {artists.length === 0 ? (
          <div className="text-center py-24">
            <div className={`w-20 h-20 mx-auto rounded-full bg-gradient-to-br ${gradient} flex items-center justify-center mb-5 opacity-30`}>
              <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d={iconPath} />
              </svg>
            </div>
            <p className="text-gray-400 text-lg">등록된 아티스트가 없습니다.</p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {artists.map((artist) => (
                <Link
                  key={artist.id}
                  to={`/booking/artist/${artist.id}`}
                  className="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1"
                >
                  {/* Photo */}
                  <div className="relative h-56 overflow-hidden">
                    {artist.profile_image_url ? (
                      <img
                        src={artist.profile_image_url}
                        alt={artist.name}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    ) : (
                      <div className={`w-full h-full bg-gradient-to-br ${CATEGORY_GRADIENTS[artist.category] || gradient} flex items-center justify-center`}>
                        <span className="text-white/30 text-7xl font-bold select-none">
                          {artist.name[0]}
                        </span>
                      </div>
                    )}
                    {/* Overlay on hover */}
                    <div className="absolute inset-0 bg-navy-950/0 group-hover:bg-navy-950/20 transition-colors duration-300" />
                  </div>

                  {/* Info */}
                  <div className="p-5">
                    <span className={`inline-block text-xs font-medium px-2.5 py-1 rounded-full bg-gradient-to-r ${CATEGORY_GRADIENTS[artist.category] || gradient} text-white`}>
                      {artist.category_label}
                    </span>
                    <h3 className="text-lg font-bold text-gray-900 mt-3 mb-1 group-hover:text-navy-700 transition-colors">
                      {artist.name}
                    </h3>
                    <p className="text-sm text-gray-500 line-clamp-2 leading-relaxed">
                      {artist.description}
                    </p>
                  </div>
                </Link>
              ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
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
