import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { ROUTES } from './constants/routes'
import { AuthProvider } from './features/auth/context/AuthProvider'
import ProtectedRoute from './features/auth/components/ProtectedRoute'
import HomePage from './pages/HomePage'
import NotFoundPage from './pages/NotFoundPage'
import LoginPage from './features/auth/pages/LoginPage'
import RegisterPage from './features/auth/pages/RegisterPage'
import ForgotPasswordPage from './features/auth/pages/ForgotPasswordPage'
import ResetPasswordPage from './features/auth/pages/ResetPasswordPage'
import VerifyEmailPage from './features/auth/pages/VerifyEmailPage'
import DashboardPage from './pages/DashboardPage'
import SplashScreen from './pages/SplashScreen'
import AddBusinessPage from './pages/AddBusinessPage'
import ArtisanHomePage from './pages/ArtisanHomePage'

const App = () => (
  <BrowserRouter>
    <AuthProvider>
      <AnimatePresence mode="wait">
        <Routes>
          <Route path="/" element={<SplashScreen />} />
          <Route path={ROUTES.home} element={<HomePage />} />
          <Route path={ROUTES.login} element={<LoginPage />} />
          <Route path={ROUTES.register} element={<RegisterPage />} />
          <Route path={ROUTES.forgotPassword} element={<ForgotPasswordPage />} />
          <Route path={ROUTES.resetPassword} element={<ResetPasswordPage />} />
          <Route path={ROUTES.verifyEmail} element={<VerifyEmailPage />} />
          <Route path={ROUTES.dashboard} element={
            <ProtectedRoute>
              <DashboardPage />
            </ProtectedRoute>
          } />
          <Route path={ROUTES.addBusiness} element={
            <ProtectedRoute>
              <AddBusinessPage />
            </ProtectedRoute>
          } />
          <Route path={ROUTES.artisanHome} element={
            <ProtectedRoute>
              <ArtisanHomePage />
            </ProtectedRoute>
          } />
          <Route path={ROUTES.notFound} element={<NotFoundPage />} />
        </Routes>
      </AnimatePresence>
    </AuthProvider>
  </BrowserRouter>
)

export default App