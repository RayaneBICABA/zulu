import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { ROUTES } from './constants/routes'
import { AuthProvider } from './features/auth/context/AuthProvider'
import ProtectedRoute from './features/auth/components/ProtectedRoute'
import MobileOnly from './components/layout/MobileOnly'
import SplashScreen from './pages/SplashScreen'
import NotFoundPage from './pages/NotFoundPage'
import LoginPage from './features/auth/pages/LoginPage'
import RegisterPage from './features/auth/pages/RegisterPage'
import ForgotPasswordPage from './features/auth/pages/ForgotPasswordPage'
import ResetPasswordPage from './features/auth/pages/ResetPasswordPage'
import VerifyEmailPage from './features/auth/pages/VerifyEmailPage'
import GoogleCallbackPage from './features/auth/pages/GoogleCallbackPage'
import DashboardPage from './pages/DashboardPage'
import ClientHomePage from './pages/ClientHomePage'
import FavorisPage from './pages/FavorisPage'
import ClientProfilePage from './pages/ClientProfilePage'
import ClientLayout from './components/layout/ClientLayout'

const App = () => (
  <BrowserRouter>
    <AuthProvider>
      <MobileOnly>
        <AnimatePresence mode="wait">
          <Routes>
            <Route path={ROUTES.landing} element={<HomePage />} />
            <Route path={ROUTES.splash}  element={<SplashScreen />} />
            <Route path={ROUTES.login}         element={<LoginPage />} />
            <Route path={ROUTES.register}      element={<RegisterPage />} />
            <Route path={ROUTES.forgotPassword} element={<ForgotPasswordPage />} />
            <Route path={ROUTES.resetPassword}  element={<ResetPasswordPage />} />
            <Route path={ROUTES.verifyEmail}    element={<VerifyEmailPage />} />
            <Route path={ROUTES.googleCallback} element={<GoogleCallbackPage />} />

            <Route element={<ProtectedRoute><ClientLayout /></ProtectedRoute>}>
              <Route path={ROUTES.home}    element={<ClientHomePage />} />
              <Route path={ROUTES.favoris}  element={<FavorisPage />} />
              <Route path={ROUTES.profile}  element={<ClientProfilePage />} />
            </Route>

            <Route path={ROUTES.dashboard}     element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            } />
            <Route path={ROUTES.notFound}      element={<NotFoundPage />} />
          </Routes>
        </AnimatePresence>
      </MobileOnly>
    </AuthProvider>
  </BrowserRouter>
)

export default App
