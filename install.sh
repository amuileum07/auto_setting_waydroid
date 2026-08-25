#!/usr/bin/env bash
# ==============================================================================
# Waydroid & Android Environment All-in-One Setup Script
# Works on Linux Mint / Ubuntu / Debian (x86_64)
# ==============================================================================
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo " Starting the Waydroid environment automatic installation"
echo "=========================================================="

# 1. 필수 시스템 패키지 설치
echo ""
echo " [1/7] Installing essential packages, GUI libraries, and Weston..."
sudo apt update
sudo apt install -y curl ca-certificates lxc weston python3 python3-venv python3-tk git iptables

# 2. Waydroid 공식 저장소 추가 및 설치
echo ""
echo " [2/7] Waydroid installation verification and in progress..."
if ! command -v waydroid &> /dev/null; then
    curl -s https://repo.waydro.id | sudo bash
    sudo apt update
    sudo apt install -y waydroid
else
    echo "  -> Waydroid is already installed."
fi

# 3. 네트워크 및 UFW 방화벽 자동 설정
echo ""
echo " [3/7] Configuring Network Forwarding and Firewall (UFW) automatically..."
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
echo " [4/7] Initializing Waydroid image and starting service..."
if [ ! -d "/var/lib/waydroid/images" ] || [ ! -f "/var/lib/waydroid/images/system.img" ]; then
    echo "  -> Downloading Waydroid stock image (VANILLA) and resetting (this may take some time)..."
    sudo waydroid init -s VANILLA
else
    echo "  -> An initialized Waydroid image already exists."
fi

sudo systemctl enable --now waydroid-container

# 5. DNS 및 가상 WiFi 속성 등록
echo ""
echo " [5/7] Setting up Fake Wi-Fi and Google DNS..."
waydroid prop set persist.waydroid.fake_wifi "*" 2>/dev/null || true
waydroid prop set persist.waydroid.dns 8.8.8.8 2>/dev/null || true
waydroid prop set persist.waydroid.dns2 1.1.1.1 2>/dev/null || true

# 6. ARM 번역 레이어 (libndk / libhoudini) + Widevine DRM 자동 설치
echo ""
echo " [6/7] Installing ARM Translation layer compatible with CPU architecture..."
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
    echo "  -> AMD CPU Detected: Install libndk and widevine"
    sudo "${SCRIPT_DIR}/waydroid_script/venv/bin/python3" "${SCRIPT_DIR}/waydroid_script/main.py" install libndk widevine
else
    echo "  -> Intel/Other CPUs Detected: Install libhoudini and widevine"
    sudo "${SCRIPT_DIR}/waydroid_script/venv/bin/python3" "${SCRIPT_DIR}/waydroid_script/main.py" install libhoudini widevine || \
    sudo "${SCRIPT_DIR}/waydroid_script/venv/bin/python3" "${SCRIPT_DIR}/waydroid_script/main.py" install libndk widevine
fi

# 7. Aurora Store 최신 APK 다운로드 및 바로가기 생성
echo ""
echo " [7/7] Downloading Aurora Store and adding desktop shortcut.."
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
echo " All installation and optimization are complete!"
echo "=========================================================="
echo "1. [Waydroid Settings Manager] You can easily set the resolution and keyboard using shortcuts."
echo "2. [Waydroid (Android)] You can launch the Android environment directly via a shortcut."
echo "3. You can install the apps and Gboard you want from the Aurora Store."
echo "=========================================================="
