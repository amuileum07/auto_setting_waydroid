#!/usr/bin/env bash
# ==============================================================================
# Waydroid Universal Runner (X11 & Wayland)
# Loads config from ~/.config/waydroid_settings.json or CLI arguments
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_PATH="${HOME}/.config/waydroid_settings.json"

# Default Dimensions (Tablet Portrait)
WIDTH=800
HEIGHT=1200
FULLSCREEN=false
SHARE_DOWNLOADS=true

# Read JSON config if available
if [ -f "$CONFIG_PATH" ]; then
    CFG_MODE=$(python3 -c "import json; d=json.load(open('$CONFIG_PATH')); print(d.get('mode', ''))" 2>/dev/null || true)
    CFG_WIDTH=$(python3 -c "import json; d=json.load(open('$CONFIG_PATH')); print(d.get('width', 800))" 2>/dev/null || true)
    CFG_HEIGHT=$(python3 -c "import json; d=json.load(open('$CONFIG_PATH')); print(d.get('height', 1200))" 2>/dev/null || true)
    CFG_SHARE=$(python3 -c "import json; d=json.load(open('$CONFIG_PATH')); print(d.get('share_downloads', True))" 2>/dev/null || true)
    
    [ -n "$CFG_WIDTH" ] && [ "$CFG_WIDTH" -gt 0 ] && WIDTH="$CFG_WIDTH"
    [ -n "$CFG_HEIGHT" ] && [ "$CFG_HEIGHT" -gt 0 ] && HEIGHT="$CFG_HEIGHT"
    [ "$CFG_MODE" = "fullscreen" ] && FULLSCREEN=true
    [ "$CFG_SHARE" = "False" ] && SHARE_DOWNLOADS=false
    CFG_FOLDER=$(python3 -c "import json, os; d=json.load(open('$CONFIG_PATH')); print(os.path.expanduser(d.get('shared_folder_path', '~/Downloads')))" 2>/dev/null || echo "${HOME}/Downloads")
fi

# Apply Host -> Android Folder Sharing if enabled
SHARED_SOURCE="${CFG_FOLDER:-${HOME}/Downloads}"
ANDROID_DL="${HOME}/.local/share/waydroid/data/media/0/Download"

if [ "$SHARE_DOWNLOADS" = "true" ] && [ -d "$SHARED_SOURCE" ]; then
    mkdir -p "$ANDROID_DL"
    if ! mountpoint -q "$ANDROID_DL" 2>/dev/null; then
        sudo mount --bind "$SHARED_SOURCE" "$ANDROID_DL" 2>/dev/null || true
    fi
fi

# Override with CLI arguments if passed
while [[ $# -gt 0 ]]; do
    case "$1" in
        --phone)
            WIDTH=600; HEIGHT=1024; FULLSCREEN=false; shift ;;
        --tablet|--tablet-p)
            WIDTH=800; HEIGHT=1200; FULLSCREEN=false; shift ;;
        --tablet-l)
            WIDTH=1200; HEIGHT=800; FULLSCREEN=false; shift ;;
        --fullscreen|-f)
            FULLSCREEN=true; shift ;;
        --width|-w)
            WIDTH="$2"; shift 2 ;;
        --height|-h)
            HEIGHT="$2"; shift 2 ;;
        *)
            shift ;;
    esac
done

# Apply Waydroid screen properties
if [ "$FULLSCREEN" = "false" ]; then
    waydroid prop set persist.waydroid.width "$WIDTH" 2>/dev/null || true
    waydroid prop set persist.waydroid.height "$HEIGHT" 2>/dev/null || true
fi

# 1. Wayland 환경
if [ "$XDG_SESSION_TYPE" = "wayland" ]; then
    echo "[Info] Wayland 세션 감지됨. 직접 실행합니다."
    waydroid session start &
    sleep 2
    waydroid show-full-ui
    exit 0
fi

# 2. X11 환경 (Weston 중첩 실행)
echo "[Info] X11 세션 감지됨. Weston 컴포지터를 실행합니다 (해상도: ${WIDTH}x${HEIGHT})."
if ! command -v weston &> /dev/null; then
    echo "❌ Weston이 설치되어 있지 않습니다. 'sudo apt install -y weston' 을 실행하세요."
    exit 1
fi

# 기존 세션 정리
waydroid session stop 2>/dev/null || true

# Weston 실행
if [ "$FULLSCREEN" = "true" ]; then
    weston --fullscreen --shell=kiosk-shell.so 2>/dev/null || weston --fullscreen &
else
    weston --width="$WIDTH" --height="$HEIGHT" --shell=kiosk-shell.so 2>/dev/null || weston --width="$WIDTH" --height="$HEIGHT" &
fi
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

# 종료 시 세션 정리
wait $WESTON_PID 2>/dev/null || true
waydroid session stop 2>/dev/null || true
