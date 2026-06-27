// Petits composants partagés des écrans d'authentification (Login / Register).

export const AuthAlert = ({ children }) => (
  <div className="mb-4 p-3 rounded-lg bg-errorLight text-error text-sm">{children}</div>
)

export const AuthDivider = () => (
  <div className="flex items-center gap-3 my-5">
    <span className="flex-1 h-px bg-gray-200" />
    <span className="text-xs text-gray-400">OU</span>
    <span className="flex-1 h-px bg-gray-200" />
  </div>
)

export const AuthGoogleButton = ({ onClick }) => (
  <button
    type="button"
    onClick={onClick}
    className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-full border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors"
  >
    <svg className="w-4 h-4" viewBox="0 0 48 48" aria-hidden="true">
      <path fill="#FFC107" d="M43.6 20.5h-1.9V20H24v8h11.3c-1.6 4.7-6.1 8-11.3 8a12 12 0 1 1 0-24c3 0 5.8 1.1 7.9 3l5.7-5.7A20 20 0 1 0 24 44a20 20 0 0 0 19.6-23.5z" />
      <path fill="#FF3D00" d="M6.3 14.7l6.6 4.8A12 12 0 0 1 24 12c3 0 5.8 1.1 7.9 3l5.7-5.7A20 20 0 0 0 6.3 14.7z" />
      <path fill="#4CAF50" d="M24 44c5.2 0 9.9-2 13.4-5.2l-6.2-5.2A12 12 0 0 1 12.7 28l-6.6 5.1A20 20 0 0 0 24 44z" />
      <path fill="#1976D2" d="M43.6 20.5H24v8h11.3a12 12 0 0 1-4.1 5.6l6.2 5.2C41 36.5 44 31 44 24c0-1.2-.1-2.4-.4-3.5z" />
    </svg>
    Continuer avec Google
  </button>
)

export const AuthSuccess = ({ icon, children }) => (
  <div className="text-center">
    {icon && (
      <div className="w-14 h-14 rounded-full bg-successLight flex items-center justify-center mx-auto mb-4">
        {icon}
      </div>
    )}
    {children}
  </div>
)
