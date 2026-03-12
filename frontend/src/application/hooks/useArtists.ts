import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import apiClient from '../../infrastructure/api/client'
import type { Artist, ArtistListResponse, ArtistCategory } from '../../domain/models/types'

interface ListParams {
  skip?: number
  limit?: number
  category?: ArtistCategory
  search?: string
}

export function useArtists(params: ListParams = {}) {
  return useQuery({
    queryKey: ['artists', params],
    queryFn: async () => {
      const { data } = await apiClient.get<ArtistListResponse>('/artists', { params })
      return data
    },
  })
}

export function useArtist(id: string) {
  return useQuery({
    queryKey: ['artist', id],
    queryFn: async () => {
      const { data } = await apiClient.get<Artist>(`/artists/${id}`)
      return data
    },
    enabled: !!id,
  })
}

export function useCreateArtist() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: { name: string; category: string; description: string; profile_image_url?: string; gallery_images?: string[] }) =>
      apiClient.post<Artist>('/artists', body).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['artists'] }),
  })
}

export function useUpdateArtist() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, ...body }: { id: string; name?: string; category?: string; description?: string; profile_image_url?: string; gallery_images?: string[]; is_active?: boolean }) =>
      apiClient.put<Artist>(`/artists/${id}`, body).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['artists'] })
      qc.invalidateQueries({ queryKey: ['artist'] })
    },
  })
}

export function useDeleteArtist() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => apiClient.delete(`/artists/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['artists'] }),
  })
}

export function useAdminArtists(params: { skip?: number; limit?: number } = {}) {
  return useQuery({
    queryKey: ['admin-artists', params],
    queryFn: async () => {
      const { data } = await apiClient.get<ArtistListResponse>('/admin/artists', { params })
      return data
    },
  })
}
