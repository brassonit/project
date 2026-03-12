import { useState, type FormEvent } from 'react'
import { useNavigate, useParams } from 'react-router-dom'
import { useArtist, useCreateArtist, useUpdateArtist } from '../../../application/hooks/useArtists'
import { useUploadImage } from '../../../application/hooks/useAdmin'
import { ARTIST_CATEGORY_LABELS, type ArtistCategory } from '../../../domain/models/types'
import LoadingSpinner from '../../components/common/LoadingSpinner'

const CATEGORIES = Object.entries(ARTIST_CATEGORY_LABELS) as [ArtistCategory, string][]

export default function AdminArtistForm() {
  const { id } = useParams<{ id: string }>()
  const isEdit = !!id
  const { data: existing, isLoading } = useArtist(id ?? '')

  if (isEdit && isLoading) return <LoadingSpinner />

  return <ArtistFormInner id={id} isEdit={isEdit} existing={existing ?? undefined} />
}

interface FormInnerProps {
  id?: string
  isEdit: boolean
  existing?: {
    name: string
    category: string
    description: string
    profile_image_url: string | null
    gallery_images: string[]
    is_active: boolean
  }
}

function ArtistFormInner({ id, isEdit, existing }: FormInnerProps) {
  const navigate = useNavigate()
  const createMutation = useCreateArtist()
  const updateMutation = useUpdateArtist()
  const uploadMutation = useUploadImage()

  const [form, setForm] = useState({
    name: existing?.name ?? '',
    category: existing?.category ?? 'singer',
    description: existing?.description ?? '',
    profile_image_url: existing?.profile_image_url ?? '',
    gallery_images: existing?.gallery_images ?? [],
    is_active: existing?.is_active ?? true,
  })
  const [error, setError] = useState('')

  const handleImageUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    try {
      const result = await uploadMutation.mutateAsync(file)
      setForm({ ...form, profile_image_url: result.url })
    } catch {
      setError('이미지 업로드에 실패했습니다.')
    }
  }

  const handleGalleryUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return
    try {
      const result = await uploadMutation.mutateAsync(file)
      setForm({ ...form, gallery_images: [...form.gallery_images, result.url] })
    } catch {
      setError('이미지 업로드에 실패했습니다.')
    }
  }

  const removeGalleryImage = (index: number) => {
    setForm({ ...form, gallery_images: form.gallery_images.filter((_, i) => i !== index) })
  }

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      const body = {
        name: form.name,
        category: form.category,
        description: form.description,
        profile_image_url: form.profile_image_url || undefined,
        gallery_images: form.gallery_images,
      }
      if (isEdit && id) {
        await updateMutation.mutateAsync({ id, ...body, is_active: form.is_active })
      } else {
        await createMutation.mutateAsync(body)
      }
      navigate('/admin/artists')
    } catch {
      setError('저장에 실패했습니다.')
    }
  }

  const isPending = createMutation.isPending || updateMutation.isPending

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold mb-6">{isEdit ? '아티스트 수정' : '아티스트 추가'}</h1>

      <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-sm p-6 space-y-5">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">이름 *</label>
          <input
            required
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">카테고리 *</label>
          <select
            value={form.category}
            onChange={(e) => setForm({ ...form, category: e.target.value })}
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            {CATEGORIES.map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">설명 *</label>
          <textarea
            required
            rows={4}
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            className="w-full border rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">프로필 이미지</label>
          <input type="file" accept="image/*" onChange={handleImageUpload} className="text-sm" />
          {form.profile_image_url && (
            <img src={form.profile_image_url} alt="프로필" className="mt-2 w-32 h-32 object-cover rounded-lg" />
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">갤러리 이미지</label>
          <input type="file" accept="image/*" onChange={handleGalleryUpload} className="text-sm" />
          {form.gallery_images.length > 0 && (
            <div className="flex gap-2 mt-2 flex-wrap">
              {form.gallery_images.map((url, i) => (
                <div key={i} className="relative">
                  <img src={url} alt={`갤러리 ${i + 1}`} className="w-24 h-24 object-cover rounded" />
                  <button
                    type="button"
                    onClick={() => removeGalleryImage(i)}
                    className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white rounded-full text-xs"
                  >
                    X
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        {isEdit && (
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              id="is_active"
              checked={form.is_active}
              onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
            />
            <label htmlFor="is_active" className="text-sm">활성 상태</label>
          </div>
        )}

        {error && <p className="text-red-600 text-sm">{error}</p>}

        <div className="flex gap-3">
          <button
            type="submit"
            disabled={isPending}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {isPending ? '저장 중...' : '저장'}
          </button>
          <button
            type="button"
            onClick={() => navigate('/admin/artists')}
            className="px-6 py-2 border rounded-lg text-gray-700 hover:bg-gray-50"
          >
            취소
          </button>
        </div>
      </form>
    </div>
  )
}
