import { useDashboard } from '../../../application/hooks/useAdmin'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import ErrorMessage from '../../components/common/ErrorMessage'

export default function AdminDashboard() {
  const { data, isLoading, error, refetch } = useDashboard()

  if (isLoading) return <LoadingSpinner />
  if (error || !data) return <ErrorMessage message="대시보드를 불러올 수 없습니다." onRetry={refetch} />

  const cards = [
    { title: '아티스트', items: [
      { label: '전체', value: data.artists.total },
      { label: '활성', value: data.artists.active, color: 'text-green-600' },
      { label: '비활성', value: data.artists.inactive, color: 'text-gray-400' },
    ]},
    { title: '공연', items: [
      { label: '전체', value: data.performances.total },
      { label: '주요공연', value: data.performances.featured, color: 'text-yellow-600' },
    ]},
    { title: '문의', items: [
      { label: '전체', value: data.inquiries.total },
      { label: '대기 중', value: data.inquiries.pending, color: 'text-orange-600' },
      { label: '답변 완료', value: data.inquiries.replied, color: 'text-green-600' },
      { label: '종료', value: data.inquiries.closed, color: 'text-gray-400' },
    ]},
  ]

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">대시보드</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards.map((card) => (
          <div key={card.title} className="bg-white rounded-lg shadow-sm p-6">
            <h2 className="text-lg font-semibold mb-4">{card.title}</h2>
            <div className="space-y-2">
              {card.items.map((item) => (
                <div key={item.label} className="flex justify-between">
                  <span className="text-sm text-gray-500">{item.label}</span>
                  <span className={`font-semibold ${item.color || 'text-gray-900'}`}>{item.value}</span>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
