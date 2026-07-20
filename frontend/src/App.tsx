import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './infrastructure/auth/AuthContext'
import AdminLayout from './presentation/layouts/AdminLayout'
import AdminDashboard from './presentation/pages/admin/AdminDashboard'
import AdminArtists from './presentation/pages/admin/AdminArtists'
import AdminArtistForm from './presentation/pages/admin/AdminArtistForm'
import AdminPerformances from './presentation/pages/admin/AdminPerformances'
import AdminInquiries from './presentation/pages/admin/AdminInquiries'
// 브라소닛 신규 디자인 (design_handoff_brassonit)
import { BrassProvider } from './brassonit/store'
import BrassLayout from './brassonit/Layout'
import HomePage from './brassonit/pages/HomePage'
import ShowsPage from './brassonit/pages/ShowsPage'
import ShowDetailPage from './brassonit/pages/ShowDetailPage'
import CategoryPage from './brassonit/pages/CategoryPage'
import SearchPage from './brassonit/pages/SearchPage'
import ArtistPage from './brassonit/pages/ArtistPage'
import { LoginPage, SignupPage } from './brassonit/pages/AuthPages'
import VerifyEmailPage from './brassonit/pages/VerifyEmailPage'
import CartPage from './brassonit/pages/CartPage'
import QuoteFormPage from './brassonit/pages/QuoteFormPage'
import QuotesPage from './brassonit/pages/QuotesPage'
import WishlistPage from './brassonit/pages/WishlistPage'
import ProfilePage from './brassonit/pages/ProfilePage'
import { AboutPage, TermsPage, PrivacyPage } from './brassonit/pages/DocsPages'

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
          <BrassProvider>
            <Routes>
              {/* Public — 브라소닛 디자인 */}
              <Route element={<BrassLayout />}>
                <Route path="/" element={<HomePage />} />
                <Route path="/shows" element={<ShowsPage />} />
                <Route path="/shows/:idx" element={<ShowDetailPage />} />
                <Route path="/category/:cat" element={<CategoryPage />} />
                <Route path="/category/:cat/:sub" element={<CategoryPage />} />
                <Route path="/search" element={<SearchPage />} />
                <Route path="/artist/:id" element={<ArtistPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/signup" element={<SignupPage />} />
                <Route path="/verify-email" element={<VerifyEmailPage />} />
                <Route path="/cart" element={<CartPage />} />
                <Route path="/quote" element={<QuoteFormPage />} />
                <Route path="/quotes" element={<QuotesPage />} />
                <Route path="/wishlist" element={<WishlistPage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/about" element={<AboutPage />} />
                <Route path="/terms" element={<TermsPage />} />
                <Route path="/privacy" element={<PrivacyPage />} />
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
          </BrassProvider>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  )
}

export default App
