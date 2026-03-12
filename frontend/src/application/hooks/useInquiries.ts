import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import apiClient from '../../infrastructure/api/client'
import type { Inquiry, InquiryListResponse } from '../../domain/models/types'

export function useCreateInquiry() {
  return useMutation({
    mutationFn: (body: { name: string; email: string; phone?: string; subject: string; message: string }) =>
      apiClient.post<Inquiry>('/inquiries', body).then((r) => r.data),
  })
}

export function useAdminInquiries(params: { skip?: number; limit?: number; status?: string } = {}) {
  return useQuery({
    queryKey: ['admin-inquiries', params],
    queryFn: async () => {
      const { data } = await apiClient.get<InquiryListResponse>('/inquiries', { params })
      return data
    },
  })
}

export function useAdminInquiry(id: string) {
  return useQuery({
    queryKey: ['admin-inquiry', id],
    queryFn: async () => {
      const { data } = await apiClient.get<Inquiry>(`/inquiries/${id}`)
      return data
    },
    enabled: !!id,
  })
}

export function useReplyInquiry() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: ({ id, reply }: { id: string; reply: string }) =>
      apiClient.patch<Inquiry>(`/inquiries/${id}/reply`, { reply }).then((r) => r.data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['admin-inquiries'] })
      qc.invalidateQueries({ queryKey: ['admin-inquiry'] })
    },
  })
}

export function useDeleteInquiry() {
  const qc = useQueryClient()
  return useMutation({
    mutationFn: (id: string) => apiClient.delete(`/inquiries/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['admin-inquiries'] }),
  })
}
