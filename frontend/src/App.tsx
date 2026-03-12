import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './infrastructure/auth/AuthContext'
import MainLayout from './presentation/layouts/MainLayout'
import AdminLayout from './presentation/layouts/AdminLayout'
import HomePage from './presentation/pages/home/HomePage'
import PerformanceListPage from './presentation/pages/performances/PerformanceListPage'
import PerformanceDetailPage from './presentation/pages/performances/PerformanceDetailPage'
import BookingCategoryPage from './presentation/pages/booking/BookingCategoryPage'
import ArtistDetailPage from './presentation/pages/booking/ArtistDetailPage'
import InquiryPage from './presentation/pages/inquiry/InquiryPage'
import LoginPage from './presentation/pages/auth/LoginPage'
import RegisterPage from './presentation/pages/auth/RegisterPage'
import VerifyEmailPage from './presentation/pages/auth/VerifyEmailPage'
import AdminDashboard from './presentation/pages/admin/AdminDashboard'
import AdminArtists from './presentation/pages/admin/AdminArtists'
import AdminArtistForm from './presentation/pages/admin/AdminArtistForm'
import AdminPerformances from './presentation/pages/admin/AdminPerformances'
import AdminInquiries from './presentation/pages/admin/AdminInquiries'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: 1, staleTime: 30_000 },
  },
})

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            {/* Public */}
            <Route element={<MainLayout />}>
              <Route path="/" element={<HomePage />} />
              <Route path="/performances" element={<PerformanceListPage />} />
              <Route path="/performances/:id" element={<PerformanceDetailPage />} />
              <Route path="/booking/:categoryPath" element={<BookingCategoryPage />} />
              <Route path="/booking/artist/:id" element={<ArtistDetailPage />} />
              <Route path="/inquiry" element={<InquiryPage />} />
              <Route path="/login" element={<LoginPage />} />
              <Route path="/register" element={<RegisterPage />} />
              <Route path="/verify-email" element={<VerifyEmailPage />} />
            </Route>

            {/* Admin (Protected) */}
            <Route element={<AdminLayout />}>
              <Route path="/admin" element={<AdminDashboard />} />
              <Route path="/admin/artists" element={<AdminArtists />} />
              <Route path="/admin/artists/new" element={<AdminArtistForm />} />
              <Route path="/admin/artists/:id/edit" element={<AdminArtistForm />} />
              <Route path="/admin/performances" element={<AdminPerformances />} />
              <Route path="/admin/inquiries" element={<AdminInquiries />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
