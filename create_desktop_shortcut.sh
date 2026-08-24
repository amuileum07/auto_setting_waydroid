#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER_PATH="${SCRIPT_DIR}/run_waydroid.sh"
DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || echo "${HOME}/Desktop")"
[ ! -d "$DESKTOP_DIR" ] && [ -d "${HOME}/바탕화면" ] && DESKTOP_DIR="${HOME}/바탕화면"

# 1. 런처 스크립트 실행 권한 확인
chmod +x "$RUNNER_PATH"

# 2. .desktop 내용 생성
DESKTOP_CONTENT="[Desktop Entry]
Name=Waydroid (Android)
Comment=Launch Waydroid Android Environment
Exec=${RUNNER_PATH}
Icon=waydroid
Terminal=false
Type=Application
Categories=Utility;Application;
StartupNotify=true"

# 3. 애플리케이션 메뉴(~/.local/share/applications/)에 등록
mkdir -p "${HOME}/.local/share/applications"
echo "$DESKTOP_CONTENT" > "${HOME}/.local/share/applications/waydroid-weston.desktop"
chmod +x "${HOME}/.local/share/applications/waydroid-weston.desktop"

# 4. 바탕화면에 바로가기 아이콘 생성
if [ -d "$DESKTOP_DIR" ]; then
    SHORTCUT_PATH="${DESKTOP_DIR}/Waydroid.desktop"
    echo "$DESKTOP_CONTENT" > "$SHORTCUT_PATH"
    chmod +x "$SHORTCUT_PATH"
    # Linux Mint / GNOME / Cinnamon 신뢰 플래그 설정 (gio 명령어가 있을 경우)
    if command -v gio &> /dev/null; then
        gio set "$SHORTCUT_PATH" metadata::trusted true 2>/dev/null || true
    fi
    echo "✅ 바탕화면 바로가기 생성 완료: ${SHORTCUT_PATH}"
fi

echo "✅ 시작 메뉴 바로가기 생성 완료: ${HOME}/.local/share/applications/waydroid-weston.desktop"
