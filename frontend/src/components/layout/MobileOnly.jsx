const MobileOnly = ({ children }) => (
  <div className="min-h-screen bg-gray-50 flex justify-center">
    <div className="w-full max-w-[430px] min-h-screen bg-white relative overflow-x-hidden md:border-x md:border-gray-200 md:shadow-xl">
      {children}
    </div>
  </div>
)

export default MobileOnly
