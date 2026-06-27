const fs = require('fs')
const path = require('path')

const rootDir = path.resolve(__dirname, '..')

const targets = [
  path.join(rootDir, 'node_modules', '@capacitor', 'android', 'capacitor', 'build.gradle'),
  path.join(rootDir, 'node_modules', '@capacitor', 'cli', 'dist', 'android', 'update.js'),
  path.join(rootDir, 'android', 'app', 'capacitor.build.gradle'),
  path.join(rootDir, 'android', 'capacitor-cordova-android-plugins', 'build.gradle'),
]

for (const filePath of targets) {
  if (!fs.existsSync(filePath)) continue

  const source = fs.readFileSync(filePath, 'utf8')
  const updated = source
    .replace(/JavaVersion\.VERSION_21/g, 'JavaVersion.VERSION_17')
    .replace(/sourceCompatibility JavaVersion\.VERSION_21/g, 'sourceCompatibility JavaVersion.VERSION_17')
    .replace(/targetCompatibility JavaVersion\.VERSION_21/g, 'targetCompatibility JavaVersion.VERSION_17')

  if (updated !== source) {
    fs.writeFileSync(filePath, updated)
    console.log(`Patched ${path.relative(rootDir, filePath)}`)
  }
}