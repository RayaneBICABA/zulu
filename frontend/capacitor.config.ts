import { CapacitorConfig } from '@capacitor/cli'

const devUrl = process.env.CAP_SERVER_URL

const config: CapacitorConfig = {
  appId: 'com.zawani.app',
  appName: 'ZAWANI',
  webDir: 'dist',
  server: devUrl
    ? { url: devUrl, cleartext: true, androidScheme: 'http' }
    : { androidScheme: 'https' },
  plugins: {
    CapacitorHttp: {
      enabled: true,
    },
  },
}

export default config
