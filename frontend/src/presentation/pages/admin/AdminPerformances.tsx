import { useState } from 'react'
import { usePerformances, useCreatePerformance, useDeletePerformance } from '../../../application/hooks/usePerformances'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import ErrorMessage from '../../components/common/ErrorMessage'
import type { FormEvent } from 'react'

export default function AdminPerformances() {
  const [page, setPage] = useState(0)
  const limit = 20
  const { data, isLoading, error, refetch } = usePerformances({ skip: page * limit, limit })
  const createMutation = useCreatePerformance()
  const deleteMutation = useDeletePerformance()

  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ title: '', description: '', event_date: '', venue: '', is_featured: false })

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage message="공연 목록을 불러올 수 없습니다." onRetry={refetch} />

  const performances = data?.performances ?? []
  const total = data?.total ?? 0
  const totalPages = Math.ceil(total / limit)

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault()
    await createMutation.mutateAsync(form)
    setForm({ title: '', description: '', event_date: '', venue: '', is_featured: false })
    setShowForm(false)
  }

  const handleDelete = (id: string, title: string) => {
    if (confirm(`"${title}" 공연을 삭제하시겠습니까?`)) {
      deleteMutation.mutate(id)
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">공연 관리</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-blue-600 text-white text-sm rounded-lg hover:bg-blue-700"
        >
          {showForm ? '취소' : '+ 공연 추가'}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleCreate} className="bg-white rounded-lg shadow-sm p-6 mb-6 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">제목 *</label>
              <input
                required
                value={form.title}
                onChange={(e) => setForm({ ...form, title: e.target.value })}
                className="w-full border rounded-lg px-3 py-2 text-sm"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">장소 *</label>
              <input
                required
                value={form.venue}
                onChange={(e) => setForm({ ...form, venue: e.target.value })}
                className="w-full border rounded-lg px-3 py-2 text-sm"
              />
            </div>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">날짜 *</label>
              <input
                required
                type="date"
                value={form.event_date}
                onChange={(e) => setForm({ ...form, event_date: e.target.value })}
                className="w-full border rounded-lg px-3 py-2 text-sm"
              />
            </div>
            <div className="flex items-end pb-2">
              <label className="flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={form.is_featured}
                  onChange={(e) => setForm({ ...form, is_featured: e.target.checked })}
                />
                주요공연
              </label>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">설명 *</label>
            <textarea
              required
              rows={3}
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              className="w-full border rounded-lg px-3 py-2 text-sm resize-none"
            />
          </div>
          <button
            type="submit"
            disabled={createMutation.isPending}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {createMutation.isPending ? '저장 중...' : '저장'}
          </button>
        </form>
      )}

      <div className="bg-white rounded-lg shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-50 text-gray-500 text-left">
              <tr>
                <th className="px-4 py-3">제목</th>
                <th className="px-4 py-3">장소</th>
                <th className="px-4 py-3">일시</th>
                <th className="px-4 py-3">주요</th>
                <th className="px-4 py-3">관리</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {performances.map((perf) => (
                <tr key={perf.id} className="hover:bg-gray-50">
                  <td className="px-4 py-3 font-medium">{perf.title}</td>
                  <td className="px-4 py-3">{perf.venue}</td>
                  <td className="px-4 py-3">{perf.event_date}</td>
                  <td className="px-4 py-3">
                    {perf.is_featured && <span className="text-xs bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded">주요</span>}
                  </td>
                  <td className="px-4 py-3">
                    <button
                      onClick={() => handleDelete(perf.id, perf.title)}
                      className="text-red-600 hover:underline"
                    >
                      삭제
                    </button>
                  </td>
                </tr>
              ))}
              {performances.length === 0 && (
                <tr><td colSpan={5} className="px-4 py-10 text-center text-gray-400">등록된 공연이 없습니다.</td></tr>
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
