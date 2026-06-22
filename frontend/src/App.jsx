import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { AnimatePresence } from 'framer-motion'
import { ROUTES } from './constants/routes'
import HomePage from './pages/HomePage'
import NotFoundPage from './pages/NotFoundPage'

const App = () => (
  <BrowserRouter>
    <AnimatePresence mode="wait">
      <Routes>
        <Route path={ROUTES.home}     element={<HomePage />} />
        <Route path={ROUTES.notFound} element={<NotFoundPage />} />
      </Routes>
    </AnimatePresence>
  </BrowserRouter>
)

export default App
