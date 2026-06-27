import { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.zawani.app',
  appName: 'ZAWANI',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
    url: 'https://zawani-api.onrender.com',
    cleartext: true,
  },
}

export default config
