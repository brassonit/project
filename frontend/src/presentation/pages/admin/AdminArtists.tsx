import { useState } from 'react'
import { Link } from 'react-router-dom'
import { useAdminArtists, useDeleteArtist } from '../../../application/hooks/useArtists'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import ErrorMessage from '../../components/common/ErrorMessage'

export default function AdminArtists() {
  const [page, setPage] = useState(0)
  const limit = 20
  const { data, isLoading, error, refetch } = useAdminArtists({ skip: page * limit, limit })
  const deleteMutation = useDeleteArtist()

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage message="아티스트 목록을 불러올 수 없습니다." onRetry={refetch} />

  const artists = data?.artists ?? []
  const total = data?.total ?? 0
  const totalPages = Math.ceil(total / limit)

  const handleDelete = (id: string, name: string) => {
    if (confirm(`"${name}" 아티스트를 삭제하시겠습니까?`)) {
      deleteMutation.mutate(id)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">아티스트 관리</h1>
        <Link
          to="/admin/artists/new"
          className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
        >
          + 아티스트 추가
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-500 text-left">
              <tr>
                <th className="px-4 py-3">이름</th>
                <th className="px-4 py-3">카테고리</th>
                <th className="px-4 py-3">상태</th>
                <th className="px-4 py-3">등록일</th>
                <th className="px-4 py-3">관리</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {artists.map((artist) => (
                <tr key={artist.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium">{artist.name}</td>
                  <td className="px-4 py-3">{artist.category_label}</td>
                  <td className="px-4 py-3">
                    <span className={`px-2 py-0.5 rounded text-xs ${
                      artist.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
                    }`}>
                      {artist.is_active ? '활성' : '비활성'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-gray-500">{artist.created_at.split('T')[0]}</td>
                  <td className="px-4 py-3">
                    <div className="flex gap-2">
                      <Link
                        to={`/admin/artists/${artist.id}/edit`}
                        className="text-blue-600 hover:underline"
                      >
                        수정
                      </Link>
                      <button
                        onClick={() => handleDelete(artist.id, artist.name)}
                        className="text-red-600 hover:underline"
                      >
                        삭제
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {artists.length === 0 && (
                <tr><td colSpan={5} className="px-4 py-10 text-center text-gray-400">등록된 아티스트가 없습니다.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      {totalPages > 1 && (
        <div className="flex justify-center gap-2 mt-6">
          {Array.from({ length: totalPages }, (_, i) => (
            <button
              key={i}
              onClick={() => setPage(i)}
              className={`px-3 py-1 rounded text-sm ${
                page === i ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'
              }`}
            >
              {i + 1}
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
