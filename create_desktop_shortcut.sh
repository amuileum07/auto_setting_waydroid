#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER_PATH="${SCRIPT_DIR}/run_waydroid.sh"
GUI_PATH="${SCRIPT_DIR}/waydroid_gui.py"
DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || echo "${HOME}/Desktop")"
[ ! -d "$DESKTOP_DIR" ] && [ -d "${HOME}/바탕화면" ] && DESKTOP_DIR="${HOME}/바탕화면"

# 1. 실행 권한 부여
chmod +x "$RUNNER_PATH" "$GUI_PATH"

mkdir -p "${HOME}/.local/share/applications"

# 2. Waydroid 메인 실행 바로가기
MAIN_DESKTOP="[Desktop Entry]
Name=Waydroid (Android)
Comment=Launch Waydroid Android Environment
Exec=${RUNNER_PATH}
Icon=waydroid
Terminal=false
Type=Application
Categories=Utility;Application;
StartupNotify=true"

echo "$MAIN_DESKTOP" > "${HOME}/.local/share/applications/waydroid-weston.desktop"
chmod +x "${HOME}/.local/share/applications/waydroid-weston.desktop"

# 3. Waydroid 설정 매니저(GUI) 바로가기
SETTINGS_DESKTOP="[Desktop Entry]
Name=Waydroid Settings Manager
Comment=Configure Waydroid Resolution, Keyboard, and Network
Exec=python3 ${GUI_PATH}
Icon=preferences-system
Terminal=false
Type=Application
Categories=Settings;Utility;
StartupNotify=true"

echo "$SETTINGS_DESKTOP" > "${HOME}/.local/share/applications/waydroid-settings.desktop"
chmod +x "${HOME}/.local/share/applications/waydroid-settings.desktop"

# 4. 바탕화면에 바로가기 생성
if [ -d "$DESKTOP_DIR" ]; then
    echo "$MAIN_DESKTOP" > "${DESKTOP_DIR}/Waydroid.desktop"
    echo "$SETTINGS_DESKTOP" > "${DESKTOP_DIR}/Waydroid-Settings.desktop"
    chmod +x "${DESKTOP_DIR}/Waydroid.desktop" "${DESKTOP_DIR}/Waydroid-Settings.desktop"
    
    if command -v gio &> /dev/null; then
        gio set "${DESKTOP_DIR}/Waydroid.desktop" metadata::trusted true 2>/dev/null || true
        gio set "${DESKTOP_DIR}/Waydroid-Settings.desktop" metadata::trusted true 2>/dev/null || true
    fi
    echo "✅ 바탕화면 바로가기 생성 완료: ${DESKTOP_DIR}"
fi

echo "✅ 시작 메뉴 바로가기 등록 완료"
