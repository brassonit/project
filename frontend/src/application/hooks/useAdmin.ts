import { useQuery, useMutation } from '@tanstack/react-query'
import apiClient from '../../infrastructure/api/client'
import type { DashboardStats, ImageUploadResponse } from '../../domain/models/types'

export function useDashboard() {
  return useQuery({
    queryKey: ['admin-dashboard'],
    queryFn: async () => {
      const { data } = await apiClient.get<DashboardStats>('/admin/dashboard')
      return data
    },
  })
}

export function useUploadImage() {
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData()
      formData.append('file', file)
      const { data } = await apiClient.post<ImageUploadResponse>('/admin/upload/image', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      return data
    },
  })
}
