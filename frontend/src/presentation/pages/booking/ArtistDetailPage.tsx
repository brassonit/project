import { useParams, Link } from 'react-router-dom'
import { useArtist } from '../../../application/hooks/useArtists'
import { ARTIST_CATEGORY_PATHS } from '../../../domain/models/types'
import { CATEGORY_GRADIENTS } from '../../../domain/models/utils'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import ErrorMessage from '../../components/common/ErrorMessage'

export default function ArtistDetailPage() {
  const { id } = useParams<{ id: string }>()
  const { data: artist, isLoading, error, refetch } = useArtist(id!)

  if (isLoading) return <LoadingSpinner />
  if (error || !artist) return <ErrorMessage message="아티스트 정보를 불러올 수 없습니다." onRetry={refetch} />

  const backPath = `/booking/${ARTIST_CATEGORY_PATHS[artist.category]}`
  const gradient = CATEGORY_GRADIENTS[artist.category] || 'from-navy-700 to-navy-900'

  return (
    <div>
      {/* Hero Section */}
      <section className="relative">
        <div className={`bg-gradient-to-br ${gradient}`}>
          <div className="max-w-6xl mx-auto px-4 py-8">
            <Link
              to={backPath}
              className="inline-flex items-center gap-1 text-sm text-white/70 hover:text-white transition-colors"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              {artist.category_label} 목록
            </Link>
          </div>
        </div>

        {/* Profile Card - overlaps gradient */}
        <div className="max-w-6xl mx-auto px-4 -mt-2">
          <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
            <div className="md:flex">
              {/* Photo */}
              <div className="md:w-2/5 lg:w-1/3">
                <div className={`h-72 md:h-full min-h-[320px] bg-gradient-to-br ${gradient} flex items-center justify-center relative overflow-hidden`}>
                  {artist.profile_image_url ? (
                    <img
                      src={artist.profile_image_url}
                      alt={artist.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <>
                      <div className="absolute inset-0 opacity-10">
                        <div className="absolute top-10 -left-10 w-40 h-40 rounded-full border border-white/30" />
                        <div className="absolute -bottom-5 right-5 w-60 h-60 rounded-full border border-white/20" />
                      </div>
                      <span className="text-white/20 text-[120px] font-bold select-none">
                        {artist.name[0]}
                      </span>
                    </>
                  )}
                </div>
              </div>

              {/* Info */}
              <div className="md:w-3/5 lg:w-2/3 p-6 md:p-10">
                <span className={`inline-block text-xs font-semibold px-3 py-1 rounded-full bg-gradient-to-r ${gradient} text-white mb-4`}>
                  {artist.category_label}
                </span>

                <h1 className="text-3xl md:text-4xl font-bold text-navy-900 mb-5">
                  {artist.name}
                </h1>

                <div className="w-12 h-0.5 bg-gold-400 mb-6" />

                <p className="text-gray-600 whitespace-pre-line leading-relaxed text-base mb-8">
                  {artist.description}
                </p>

                <Link
                  to="/inquiry"
                  className="inline-flex items-center gap-2 px-7 py-3 bg-navy-900 text-white font-medium rounded-xl hover:bg-navy-800 transition-colors shadow-lg shadow-navy-900/20"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  섭외 문의하기
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Gallery */}
      {artist.gallery_images.length > 0 && (
        <section className="max-w-6xl mx-auto px-4 py-12 md:py-16">
          <div className="flex items-center gap-3 mb-8">
            <h2 className="text-xl font-bold text-navy-900">갤러리</h2>
            <div className="flex-1 h-px bg-gray-200" />
          </div>

          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {artist.gallery_images.map((url, i) => (
              <div key={i} className="group relative rounded-xl overflow-hidden aspect-square">
                <img
                  src={url}
                  alt={`${artist.name} 갤러리 ${i + 1}`}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-navy-950/0 group-hover:bg-navy-950/10 transition-colors duration-300" />
              </div>
            ))}
          </div>
        </section>
      )}

      {/* CTA */}
      <section className="bg-gray-50">
        <div className="max-w-6xl mx-auto px-4 py-14 text-center">
          <h2 className="text-2xl font-bold text-navy-900 mb-3">
            {artist.name} 섭외에 관심이 있으신가요?
          </h2>
          <p className="text-gray-500 mb-8">
            행사 일정, 장소, 예산 등을 알려주시면 빠르게 안내해 드립니다.
          </p>
          <Link
            to="/inquiry"
            className="inline-block px-8 py-3 bg-navy-900 text-white font-medium rounded-xl hover:bg-navy-800 transition-colors"
          >
            문의하기
          </Link>
        </div>
      </section>
    </div>
  )
}
