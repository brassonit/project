import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import apiClient from '../../infrastructure/api/client'
import type { Performance, PerformanceListResponse } from '../../domain/models/types'

export function usePerformances(params: { skip?: number; limit?: number } = {}) {
  return useQuery({
    queryKey: ['performances', params],
    queryFn: async () => {
      const { data } = await apiClient.get<PerformanceListResponse>('/performances', { params })
      return data
    },
  })
}

export function useFeaturedPerformances() {
  return useQuery({
    queryKey: ['performances', 'featured'],
    queryFn: async () => {
      const { data } = await apiClient.get<PerformanceListResponse>('/performances/featured')
      return data
    },
  })
}

export function usePerformance(id: string) {
  return useQuery({
    queryKey: ['performance', id],
    queryFn: async () => {
      const { data } = await apiClient.get<Performance>(`/performances/${id}`)
      return data
    },
    enabled: !!id,
  })
}

export function useCreatePerformance() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (body: { title: string; description: string; event_date: string; venue: string; image_url?: string; is_featured?: boolean }) =>
      apiClient.post<Performance>('/performances', body).then((r) => r.data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['performances'] }),
  })
}

export function useUpdatePerformance() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, ...body }: { id: string; title?: string; description?: string; event_date?: string; venue?: string; image_url?: string; is_featured?: boolean }) =>
      apiClient.put<Performance>(`/performances/${id}`, body).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['performances'] })
      qc.invalidateQueries({ queryKey: ['performance'] })
    },
  })
}

export function useDeletePerformance() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => apiClient.delete(`/performances/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['performances'] }),
  })
}
