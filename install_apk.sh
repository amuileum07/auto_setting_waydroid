#!/usr/bin/env bash
# Waydroid APK 설치 헬퍼 스크립트

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APK_PATH="${1:-${SCRIPT_DIR}/AuroraStore.apk}"

if [ ! -f "$APK_PATH" ]; then
    echo "파일을 찾을 수 없습니다: $APK_PATH"
    exit 1
fi

if [ -S "${XDG_RUNTIME_DIR:-/run/user/$(id -u)}/wayland-waydroid" ]; then
    SOCKET="wayland-waydroid"
else
    SOCKET="$(find "${XDG_RUNTIME_DIR:-/run/user/$(id -u)}" -maxdepth 1 -name "wayland-*" -type s 2>/dev/null | head -n1 | xargs -n1 basename 2>/dev/null || echo "wayland-0")"
fi
export WAYLAND_DISPLAY="$SOCKET"

echo "Waydroid 세션 확인 중..."
if [ "$(waydroid status 2>/dev/null | grep -i 'Session:' | awk '{print $2}')" = "STOPPED" ]; then
    echo "❌ Waydroid 세션이 실행 중이지 않습니다."
    echo "먼저 ./run_waydroid.sh 를 실행하여 안드로이드 창을 띄워주세요."
    exit 1
fi

echo "APK 설치 진행 중: $APK_PATH"
waydroid app install "$APK_PATH"
