.PHONY: build sync apk apk-debug apk-release install clean icons live-reload

APP_NAME    := ZAWANI
APK_DIR     := frontend/android/app/build/outputs/apk
BUILD_TYPE  ?= debug
JAVA_HOME   := /usr/lib/jvm/jdk-25
export JAVA_HOME

# ─── Frontend ───────────────────────────────────────────────
build:
	cd frontend && npm run build

# ─── Capacitor sync ─────────────────────────────────────────
sync: build
	cd frontend && npx cap sync android

# ─── Android icons from logo.png ────────────────────────────
icons:
	@echo "Generating Android icons from frontend/public/logo.png ..."
	@SRC="frontend/public/logo.png" && \
	RES="frontend/android/app/src/main/res" && \
	convert "$$SRC" -resize 48x48    "$$RES/mipmap-mdpi/ic_launcher.png" && \
	convert "$$SRC" -resize 72x72    "$$RES/mipmap-hdpi/ic_launcher.png" && \
	convert "$$SRC" -resize 96x96    "$$RES/mipmap-xhdpi/ic_launcher.png" && \
	convert "$$SRC" -resize 144x144  "$$RES/mipmap-xxhdpi/ic_launcher.png" && \
	convert "$$SRC" -resize 192x192  "$$RES/mipmap-xxxhdpi/ic_launcher.png" && \
	convert "$$SRC" -resize 48x48    -gravity center -extent 48x48   -alpha set -virtual-pixel transparent -channel A -evaluate set 100% +channel -size 48x48   xc:none -fill white -draw "circle 24,24 24,0"   -compose DstIn -composite "$$RES/mipmap-mdpi/ic_launcher_round.png" && \
	convert "$$SRC" -resize 72x72    -gravity center -extent 72x72   -alpha set -virtual-pixel transparent -channel A -evaluate set 100% +channel -size 72x72   xc:none -fill white -draw "circle 36,36 36,0"   -compose DstIn -composite "$$RES/mipmap-hdpi/ic_launcher_round.png" && \
	convert "$$SRC" -resize 96x96    -gravity center -extent 96x96   -alpha set -virtual-pixel transparent -channel A -evaluate set 100% +channel -size 96x96   xc:none -fill white -draw "circle 48,48 48,0"   -compose DstIn -composite "$$RES/mipmap-xhdpi/ic_launcher_round.png" && \
	convert "$$SRC" -resize 144x144  -gravity center -extent 144x144 -alpha set -virtual-pixel transparent -channel A -evaluate set 100% +channel -size 144x144 xc:none -fill white -draw "circle 72,72 72,0"   -compose DstIn -composite "$$RES/mipmap-xxhdpi/ic_launcher_round.png" && \
	convert "$$SRC" -resize 192x192  -gravity center -extent 192x192 -alpha set -virtual-pixel transparent -channel A -evaluate set 100% +channel -size 192x192 xc:none -fill white -draw "circle 96,96 96,0"   -compose DstIn -composite "$$RES/mipmap-xxxhdpi/ic_launcher_round.png" && \
	convert "$$SRC" -resize 108x108  -gravity center -extent 108x108  "$$RES/mipmap-mdpi/ic_launcher_foreground.png" && \
	convert "$$SRC" -resize 162x162  -gravity center -extent 162x162  "$$RES/mipmap-hdpi/ic_launcher_foreground.png" && \
	convert "$$SRC" -resize 216x216  -gravity center -extent 216x216  "$$RES/mipmap-xhdpi/ic_launcher_foreground.png" && \
	convert "$$SRC" -resize 324x324  -gravity center -extent 324x324  "$$RES/mipmap-xxhdpi/ic_launcher_foreground.png" && \
	convert "$$SRC" -resize 432x432  -gravity center -extent 432x432  "$$RES/mipmap-xxxhdpi/ic_launcher_foreground.png" && \
	echo "Icons generated for all densities."

# ─── Build APK ──────────────────────────────────────────────
apk: sync
	cd frontend/android && JAVA_HOME=$(JAVA_HOME) ./gradlew --no-daemon assemble$(BUILD_TYPE)
	@echo ""
	@echo "APK: $(APK_DIR)/$(BUILD_TYPE)/app-$(BUILD_TYPE).apk"

apk-debug: sync
	cd frontend/android && JAVA_HOME=$(JAVA_HOME) ./gradlew --no-daemon assembleDebug
	@echo ""
	@echo "APK: $(APK_DIR)/debug/app-debug.apk"

apk-release: sync
	cd frontend/android && JAVA_HOME=$(JAVA_HOME) ./gradlew --no-daemon assembleRelease
	@echo ""
	@echo "APK: $(APK_DIR)/release/app-release-unsigned.apk"

# ─── Install on device ─────────────────────────────────────
install: apk-debug
	adb install -r $(APK_DIR)/debug/app-debug.apk
	@echo "$(APP_NAME) installed on device."

# ─── Live Reload (no rebuild needed) ───────────────────────
# 1. Lance le serveur Vite:  cd frontend && npm run dev:network
# 2. Lance l'app sur le device:  make live-reload
# 3. Modifie le code → hot reload instantané sur l'appareil
live-reload:
	cd frontend && npx cap run android --livereload --external

# ─── Clean ──────────────────────────────────────────────────
clean:
	cd frontend && rm -rf dist
	cd frontend/android && JAVA_HOME=$(JAVA_HOME) ./gradlew --no-daemon clean
	@echo "Clean complete."
