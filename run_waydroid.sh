#!/usr/bin/env bash
# Waydroid 범용 실행 런처 (X11 & Wayland 지원)

# 1. Wayland 환경인지 X11 환경인지 감지
if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    echo "[Info] Wayland 세션 감지됨. 직접 실행합니다."
    waydroid session start &
    sleep 2
    waydroid show-full-ui
    exit 0
fi

# 2. X11 환경인 경우 Weston 실행
echo "[Info] X11 세션 감지됨. Weston(중첩 Wayland) 컴포지터를 실행합니다."
if ! command -v weston &> /dev/null; then
    notify-send "Waydroid 오류" "Weston이 설치되어 있지 않습니다. sudo apt install weston 을 실행하세요." 2>/dev/null || true
    echo "❌ Weston이 설치되어 있지 않습니다: sudo apt install -y weston"
    exit 1
fi

# 기존 세션 정리
waydroid session stop 2>/dev/null || true

# Weston 실행 (창 크기 800x1280 태블릿 비율)
weston --width=800 --height=1200 --shell=kiosk-shell.so 2>/dev/null || weston --width=800 --height=1200 &
WESTON_PID=$!

# Wayland 소켓 생성 대기
sleep 2

# 소켓 탐색
export WAYLAND_DISPLAY="$(ls -t "${XDG_RUNTIME_DIR:-/run/user/$(id -u)}"/wayland-* 2>/dev/null | head -n1 | xargs -n1 basename 2>/dev/null || echo "wayland-1")"
echo "[Info] 연결 소켓: ${WAYLAND_DISPLAY}"

# Waydroid 세션 및 UI 구동
waydroid session start &
sleep 2
waydroid show-full-ui &

# Weston 창이 닫히면 Waydroid 세션도 함께 깔끔히 종료
wait $WESTON_PID 2>/dev/null || true
waydroid session stop 2>/dev/null || true
