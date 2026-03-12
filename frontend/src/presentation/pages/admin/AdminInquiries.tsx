import { useState } from 'react'
import { useAdminInquiries, useReplyInquiry, useDeleteInquiry } from '../../../application/hooks/useInquiries'
import { INQUIRY_STATUS_LABELS, type InquiryStatus, type Inquiry } from '../../../domain/models/types'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import ErrorMessage from '../../components/common/ErrorMessage'

export default function AdminInquiries() {
  const [page, setPage] = useState(0)
  const [statusFilter, setStatusFilter] = useState<string>('')
  const limit = 20
  const { data, isLoading, error, refetch } = useAdminInquiries({
    skip: page * limit,
    limit,
    status: statusFilter || undefined,
  })
  const replyMutation = useReplyInquiry()
  const deleteMutation = useDeleteInquiry()

  const [replyTarget, setReplyTarget] = useState<Inquiry | null>(null)
  const [replyText, setReplyText] = useState('')

  if (isLoading) return <LoadingSpinner />
  if (error) return <ErrorMessage message="문의 목록을 불러올 수 없습니다." onRetry={refetch} />

  const inquiries = data?.inquiries ?? []
  const total = data?.total ?? 0
  const totalPages = Math.ceil(total / limit)

  const handleReply = async () => {
    if (!replyTarget || !replyText.trim()) return
    await replyMutation.mutateAsync({ id: replyTarget.id, reply: replyText })
    setReplyTarget(null)
    setReplyText('')
  }

  const handleDelete = (id: string) => {
    if (confirm('이 문의를 삭제하시겠습니까?')) {
      deleteMutation.mutate(id)
    }
  }

  const statusBadge = (status: InquiryStatus) => {
    const colors: Record<InquiryStatus, string> = {
      pending: 'bg-orange-100 text-orange-700',
      replied: 'bg-green-100 text-green-700',
      closed: 'bg-gray-100 text-gray-500',
    }
    return (
      <span className={`px-2 py-0.5 rounded text-xs ${colors[status]}`}>
        {INQUIRY_STATUS_LABELS[status]}
      </span>
    )
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">문의 관리</h1>

      {/* Status Filter */}
      <div className="flex gap-2 mb-4">
        {['', 'pending', 'replied', 'closed'].map((s) => (
          <button
            key={s}
            onClick={() => { setStatusFilter(s); setPage(0) }}
            className={`px-3 py-1.5 text-sm rounded ${
              statusFilter === s ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-100'
            }`}
          >
            {s ? INQUIRY_STATUS_LABELS[s as InquiryStatus] : '전체'}
          </button>
        ))}
      </div>

      <div className="space-y-4">
        {inquiries.map((inquiry) => (
          <div key={inquiry.id} className="bg-white rounded-lg shadow-sm p-5">
            <div className="flex items-start justify-between mb-3">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  {statusBadge(inquiry.status as InquiryStatus)}
                  <span className="font-semibold">{inquiry.subject}</span>
                </div>
                <p className="text-sm text-gray-500">
                  {inquiry.name} ({inquiry.email}) &middot; {inquiry.created_at.split('T')[0]}
                </p>
              </div>
              <button
                onClick={() => handleDelete(inquiry.id)}
                className="text-sm text-red-500 hover:underline"
              >
                삭제
              </button>
            </div>

            <p className="text-sm text-gray-700 whitespace-pre-line mb-3">{inquiry.message}</p>

            {inquiry.admin_reply && (
              <div className="bg-blue-50 rounded p-3 text-sm">
                <p className="text-xs text-blue-600 font-medium mb-1">관리자 답변</p>
                <p className="text-gray-700 whitespace-pre-line">{inquiry.admin_reply}</p>
              </div>
            )}

            {inquiry.status === 'pending' && (
              <div className="mt-3">
                {replyTarget?.id === inquiry.id ? (
                  <div className="space-y-2">
                    <textarea
                      rows={3}
                      value={replyText}
                      onChange={(e) => setReplyText(e.target.value)}
                      placeholder="답변을 입력하세요"
                      className="w-full border rounded-lg px-3 py-2 text-sm resize-none"
                    />
                    <div className="flex gap-2">
                      <button
                        onClick={handleReply}
                        disabled={replyMutation.isPending}
                        className="px-4 py-1.5 bg-blue-600 text-white text-sm rounded hover:bg-blue-700 disabled:opacity-50"
                      >
                        {replyMutation.isPending ? '전송 중...' : '답변 전송'}
                      </button>
                      <button
                        onClick={() => { setReplyTarget(null); setReplyText('') }}
                        className="px-4 py-1.5 border text-sm rounded text-gray-600"
                      >
                        취소
                      </button>
                    </div>
                  </div>
                ) : (
                  <button
                    onClick={() => setReplyTarget(inquiry)}
                    className="text-sm text-blue-600 hover:underline"
                  >
                    답변하기
                  </button>
                )}
              </div>
            )}
          </div>
        ))}

        {inquiries.length === 0 && (
          <p className="text-gray-400 text-center py-10">문의가 없습니다.</p>
        )}
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
