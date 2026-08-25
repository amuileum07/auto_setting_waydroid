#!/usr/bin/env bash
# ==============================================================================
# Waydroid & Android Environment All-in-One Setup Script
# Works on Linux Mint / Ubuntu / Debian (x86_64)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo " 🚀 Waydroid & Android eBook 환경 자동 설치를 시작합니다"
echo "=========================================================="

# 1. 필수 시스템 패키지 설치
echo ""
echo "📦 [1/7] 필수 패키지, GUI 라이브러리 및 Weston 설치 중..."
sudo apt update
sudo apt install -y curl ca-certificates lxc weston python3 python3-venv python3-tk git iptables

# 2. Waydroid 공식 저장소 추가 및 설치
echo ""
echo "📦 [2/7] Waydroid 설치 확인 및 진행 중..."
if ! command -v waydroid &> /dev/null; then
    curl -s https://repo.waydro.id | sudo bash
    sudo apt update
    sudo apt install -y waydroid
else
    echo "  -> Waydroid가 이미 설치되어 있습니다."
fi

# 3. 네트워크 및 UFW 방화벽 자동 설정
echo ""
echo "🌐 [3/7] 네트워크 포워딩 및 방화벽(UFW) 자동 구성 중..."
if [ -f /etc/default/ufw ]; then
    sudo sed -i 's/DEFAULT_FORWARD_POLICY="DROP"/DEFAULT_FORWARD_POLICY="ACCEPT"/g' /etc/default/ufw
fi
sudo ufw route allow in on waydroid0 2>/dev/null || true
sudo ufw route allow out on waydroid0 2>/dev/null || true
sudo ufw allow in on waydroid0 2>/dev/null || true
sudo ufw allow out on waydroid0 2>/dev/null || true
sudo ufw reload 2>/dev/null || true
sudo iptables -P FORWARD ACCEPT 2>/dev/null || true
sudo sysctl -w net.ipv4.ip_forward=1 > /dev/null

# 4. Waydroid 이미지 초기화 및 컨테이너 시작
echo ""
echo "⚙️ [4/7] Waydroid 이미지 초기화 및 서비스 시작 중..."
if [ ! -d "/var/lib/waydroid/images" ] || [ ! -f "/var/lib/waydroid/images/system.img" ]; then
    echo "  -> Waydroid 순정 이미지(VANILLA) 다운로드 및 초기화 중 (시간이 다소 소요될 수 있습니다)..."
    sudo waydroid init -s VANILLA
else
    echo "  -> 이미 초기화된 Waydroid 이미지가 존재합니다."
fi

sudo systemctl enable --now waydroid-container

# 5. DNS 및 가상 WiFi 속성 등록
echo ""
echo "🔧 [5/7] Fake Wi-Fi 및 Google DNS 설정 중..."
waydroid prop set persist.waydroid.fake_wifi "*" 2>/dev/null || true
waydroid prop set persist.waydroid.dns 8.8.8.8 2>/dev/null || true
waydroid prop set persist.waydroid.dns2 1.1.1.1 2>/dev/null || true

# 6. ARM 번역 레이어 (libndk / libhoudini) + Widevine DRM 자동 설치
echo ""
echo "🧠 [6/7] CPU 아키텍처에 맞는 ARM Translation 레이어 설치 중..."
if [ ! -d "${SCRIPT_DIR}/waydroid_script" ]; then
    git clone https://github.com/casualsnek/waydroid_script "${SCRIPT_DIR}/waydroid_script"
fi

if [ ! -d "${SCRIPT_DIR}/waydroid_script/venv" ]; then
    python3 -m venv "${SCRIPT_DIR}/waydroid_script/venv"
fi

"${SCRIPT_DIR}/waydroid_script/venv/bin/pip" install -q -r "${SCRIPT_DIR}/waydroid_script/requirements.txt"

# CPU 판별 (AMD: libndk, Intel: libhoudini or libndk)
CPU_VENDOR="$(grep -m1 "vendor_id" /proc/cpuinfo | awk '{print $3}')"
if [[ "$CPU_VENDOR" =~ "AuthenticAMD" ]]; then
    echo "  -> AMD CPU 감지됨: libndk 및 widevine 설치"
    sudo "${SCRIPT_DIR}/waydroid_script/venv/bin/python3" "${SCRIPT_DIR}/waydroid_script/main.py" install libndk widevine
else
    echo "  -> Intel/기타 CPU 감지됨: libhoudini 및 widevine 설치"
    sudo "${SCRIPT_DIR}/waydroid_script/venv/bin/python3" "${SCRIPT_DIR}/waydroid_script/main.py" install libhoudini widevine || \
    sudo "${SCRIPT_DIR}/waydroid_script/venv/bin/python3" "${SCRIPT_DIR}/waydroid_script/main.py" install libndk widevine
fi

# 7. Aurora Store 최신 APK 다운로드 및 바로가기 생성
echo ""
echo "🎨 [7/7] Aurora Store 다운로드 및 바탕화면 바로가기 등록 중..."
if [ ! -f "${SCRIPT_DIR}/AuroraStore.apk" ]; then
    curl -sL "https://auroraoss.com/downloads/AuroraStore/Release/preload/AuroraStore-preload-4.7.5.apk" -o "${SCRIPT_DIR}/AuroraStore.apk" || true
fi

chmod +x "${SCRIPT_DIR}/create_desktop_shortcut.sh"
chmod +x "${SCRIPT_DIR}/run_waydroid.sh"
chmod +x "${SCRIPT_DIR}/install_apk.sh"
chmod +x "${SCRIPT_DIR}/waydroid_gui.py"
chmod +x "${SCRIPT_DIR}/uninstall.sh"
"${SCRIPT_DIR}/create_desktop_shortcut.sh"

echo ""
echo "=========================================================="
echo " 🎉 모든 설치 및 최적화가 완료되었습니다!"
echo "=========================================================="
echo "1. [Waydroid Settings Manager] 바로가기로 해상도 및 키보드를 간편하게 설정할 수 있습니다."
echo "2. [Waydroid (Android)] 바로가기로 안드로이드 환경을 바로 실행할 수 있습니다."
echo "3. Aurora Store에서 원하는 앱 및 Gboard를 설치하시면 됩니다."
echo "=========================================================="
