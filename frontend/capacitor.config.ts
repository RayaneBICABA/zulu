import { CapacitorConfig } from '@capacitor/cli'

const config: CapacitorConfig = {
  appId: 'com.zulustarter.app',
  appName: 'Zulu Starter',
  webDir: 'dist',
  server: {
    androidScheme: 'https',
  },
}

export default config
