import { BrowserRouter, Routes, Route, useLocation, Outlet } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { ROUTES } from './constants/routes'
import { AuthProvider } from './features/auth/context/AuthProvider'
import ProtectedRoute from './features/auth/components/ProtectedRoute'
import MobileOnly from './components/layout/MobileOnly'
import ErrorBoundary from './components/ErrorBoundary'
import SplashScreen from './pages/SplashScreen'
import NotFoundPage from './pages/NotFoundPage'
import LoginPage from './features/auth/pages/LoginPage'
import RegisterPage from './features/auth/pages/RegisterPage'
import ForgotPasswordPage from './features/auth/pages/ForgotPasswordPage'
import ArtisanDashboardPage from './pages/ArtisanDashboardPage'
import ClientHomePage from './pages/ClientHomePage'
import FavorisPage from './pages/FavorisPage'
import ClientProfilePage from './pages/ClientProfilePage'
import CommerceDetailPage from './pages/CommerceDetailPage'
import CommerceCreatePage from './pages/CommerceCreatePage'
import ClientLayout from './components/layout/ClientLayout'
import ResetPasswordPage from './features/auth/pages/ResetPasswordPage'
import LandingPage from './pages/LandingPage'

const MobileLayout = () => (
  <MobileOnly>
    <Outlet />
  </MobileOnly>
)

const AnimatedRoutes = () => {
  const location = useLocation()

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<LandingPage />} />

        <Route element={<MobileLayout />}>
          <Route path={ROUTES.splash}  element={<SplashScreen />} />
          <Route path={ROUTES.login}         element={<LoginPage />} />
          <Route path={ROUTES.register}      element={<RegisterPage />} />
          <Route path={ROUTES.forgotPassword} element={<ForgotPasswordPage />} />
          <Route path={ROUTES.resetPassword} element={<ResetPasswordPage />} />

          <Route element={<ProtectedRoute><ClientLayout /></ProtectedRoute>}>
            <Route path={ROUTES.home}           element={<ClientHomePage />} />
            <Route path={ROUTES.favoris}         element={<FavorisPage />} />
            <Route path={ROUTES.profile}         element={<ClientProfilePage />} />
            <Route path={ROUTES.commerceCreate}  element={<CommerceCreatePage />} />
            <Route path={ROUTES.dashboard}       element={<ArtisanDashboardPage />} />
          </Route>

          <Route path={ROUTES.commerceDetail} element={
            <ProtectedRoute>
              <CommerceDetailPage />
            </ProtectedRoute>
          } />
          <Route path={ROUTES.notFound}      element={<NotFoundPage />} />
        </Route>
      </Routes>
    </AnimatePresence>
  )
}

const App = () => (
  <BrowserRouter>
    <ErrorBoundary>
      <AuthProvider>
        <AnimatedRoutes />
      </AuthProvider>
    </ErrorBoundary>
  </BrowserRouter>
)

export default App
