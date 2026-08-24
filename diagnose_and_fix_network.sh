#!/usr/bin/env bash
set -e

echo "=== [1/5] UFW 포워딩 정책 수정 (DROP -> ACCEPT) ==="
# UFW 기본 포워딩 정책을 ACCEPT로 변경하여 컨테이너 패킷 통과 허용
if [ -f /etc/default/ufw ]; then
    sudo sed -i 's/DEFAULT_FORWARD_POLICY="DROP"/DEFAULT_FORWARD_POLICY="ACCEPT"/g' /etc/default/ufw
fi

echo "=== [2/5] UFW 및 iptables 방화벽 규칙 적용 ==="
sudo ufw route allow in on waydroid0 || true
sudo ufw route allow out on waydroid0 || true
sudo ufw allow in on waydroid0 || true
sudo ufw allow out on waydroid0 || true
sudo ufw reload
sudo iptables -P FORWARD ACCEPT

echo "=== [3/5] 커널 IP 포워딩 활성화 ==="
sudo sysctl -w net.ipv4.ip_forward=1

echo "=== [4/5] Waydroid 네트워크 브리지 및 컨테이너 재시작 ==="
sudo /usr/lib/waydroid/data/scripts/waydroid-net.sh restart || sudo /usr/lib/waydroid/data/scripts/waydroid-net.sh start
sudo systemctl restart waydroid-container

echo "=== [5/5] Waydroid DNS 및 가상 WiFi 설정 ==="
waydroid prop set persist.waydroid.fake_wifi "*"
waydroid prop set persist.waydroid.dns 8.8.8.8
waydroid prop set persist.waydroid.dns2 1.1.1.1

echo "--------------------------------------------------"
echo "✅ 네트워크 및 방화벽 설정 완료!"
echo "이제 './run_waydroid.sh' 로 Waydroid를 다시 실행해 보세요."
