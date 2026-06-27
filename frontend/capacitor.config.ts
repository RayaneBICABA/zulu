import { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.zawani.app',
  appName: 'ZAWANI',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
    url: 'http://192.168.1.100:5173',
    cleartext: true,
  },
}

export default config
