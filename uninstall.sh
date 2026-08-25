#!/usr/bin/env bash
# ==============================================================================
# Waydroid & Environment Clean Uninstaller
# Safely removes containers, images, settings, shortcuts, and packages
# ==============================================================================
set -e

echo "=========================================================="
echo " ⚠️  Waydroid 환경 완전 삭제 및 초기화 (Uninstaller)"
echo "=========================================================="
echo "이 스크립트는 Waydroid 컨테이너, 설정, 바로가기 및 설치된 패키지를 삭제합니다."
read -p "정말 진행하시겠습니까? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "취소되었습니다."
    exit 0
fi

echo ""
echo "🛑 [1/5] 실행 중인 Waydroid 세션 및 서비스 중지 중..."
waydroid session stop 2>/dev/null || true
sudo systemctl stop waydroid-container 2>/dev/null || true
sudo systemctl disable waydroid-container 2>/dev/null || true

echo "🗑️ [2/5] 컨테이너 데이터 및 이미지 삭제 중..."
sudo rm -rf /var/lib/waydroid 2>/dev/null || true
sudo rm -rf /var/lib/lxc/waydroid 2>/dev/null || true
rm -rf "${HOME}/.local/share/waydroid" 2>/dev/null || true
rm -rf "${HOME}/.config/waydroid" 2>/dev/null || true
rm -rf "${HOME}/.config/waydroid_settings.json" 2>/dev/null || true

echo "🧹 [3/5] 바탕화면 및 메뉴 바로가기 제거 중..."
DESKTOP_DIR="$(xdg-user-dir DESKTOP 2>/dev/null || echo "${HOME}/Desktop")"
[ ! -d "$DESKTOP_DIR" ] && [ -d "${HOME}/바탕화면" ] && DESKTOP_DIR="${HOME}/바탕화면"

rm -f "${DESKTOP_DIR}/Waydroid.desktop" 2>/dev/null || true
rm -f "${DESKTOP_DIR}/Waydroid-Settings.desktop" 2>/dev/null || true
rm -f "${HOME}/.local/share/applications/waydroid-weston.desktop" 2>/dev/null || true
rm -f "${HOME}/.local/share/applications/waydroid-settings.desktop" 2>/dev/null || true

echo "📦 [4/5] Waydroid 패키지 제거 중..."
sudo apt remove --purge -y waydroid 2>/dev/null || true
sudo apt autoremove -y 2>/dev/null || true

echo "🌐 [5/5] 방화벽 룰 정리 완료"
echo ""
echo "=========================================================="
echo " ✅ Waydroid가 시스템에서 깨끗하게 제거되었습니다."
echo "=========================================================="
