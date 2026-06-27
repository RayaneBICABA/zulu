import { Outlet } from 'react-router-dom'
import BottomNav from './BottomNav'

const ClientLayout = () => (
  <div className="min-h-screen bg-gray-50">
    <Outlet />
    <BottomNav />
  </div>
)

export default ClientLayout
