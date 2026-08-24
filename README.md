# Waydroid Linux Mint / Ubuntu Auto Setup 🚀

Linux Mint (Cinnamon / X11) 및 Ubuntu 환경에서 **Waydroid**를 원클릭으로 설치하고, **ARM Translation(libndk/libhoudini)**, **방화벽(UFW) 네트워크 해결**, **Aurora Store 및 바탕화면 바로가기 아이콘 생성**까지 완전히 자동화해 주는 패키지입니다.

---

## ⚡ 빠른 시작 (새로운 노트북에서 1줄 설치)

새 노트북에서 터미널을 열고 아래 명령어를 붙여넣기만 하면 전체 설정이 완료됩니다:

```bash
git clone https://github.com/amuileum07/auto_setting_waydroid.git
cd auto_setting_waydroid
./install.sh
```

---

## 📂 파일 구성

| 파일 | 설명 |
| :--- | :--- |
| **`install.sh`** | 전체 환경(Waydroid, 방화벽, ARM 변환, 스토어, 바로가기) 원클릭 자동 설치 스크립트 |
| **`run_waydroid.sh`** | X11/Wayland 환경을 자동 감지하여 안드로이드 창을 실행하는 범용 런처 |
| **`create_desktop_shortcut.sh`** | 바탕화면 및 시작 메뉴에 원클릭 실행 아이콘을 생성하는 스크립트 |
| **`install_apk.sh`** | APK 파일을 Waydroid에 쉽게 설치해 주는 헬퍼 스크립트 |
| **`diagnose_and_fix_network.sh`** | UFW 방화벽 차단 및 DNS/Fake Wi-Fi 이슈 해결 스크립트 |

---

## 📖 사용 방법

### 1. 안드로이드 실행
* **바탕화면의 `Waydroid (Android)` 아이콘**을 더블 클릭하여 실행합니다.
* 또는 터미널에서 `./run_waydroid.sh` 실행

### 2. 안드로이드 앱 설치 (Aurora Store)
1. 안드로이드 화면을 아래에서 위로 쓸어 올려 **Aurora Store** 실행
2. 익명(Anonymous) 로그인 후 원하는 앱(전자책, 메신저 등) 검색 및 설치

### 3. 한글 키보드(Gboard) 설정
1. Aurora Store에서 **`Gboard`** 설치
2. 안드로이드 **설정(Settings) → 시스템(System) → 언어 및 입력(Languages & input)** 에서 Gboard 활성화 및 한국어 추가
3. 노트북 키보드로 타이핑 시 **`Shift + Space`** 로 한/영 전환

---

## 🔧 주요 자동 최적화 내용
* **X11 Weston 통합**: Linux Mint Cinnamon 등 X11 세션에서도 문제없이 중첩 Wayland 창으로 Waydroid 구동.
* **UFW 방화벽 / IP Forwarding 자동 허용**: Waydroid 컨테이너의 가상 네트워크(`waydroid0`) 인터넷 연결 차단 문제 해결.
* **CPU 감지 및 최적 ARM 변환 레이어 자동 탑재**: AMD Ryzen(`libndk`), Intel(`libhoudini`) 자동 분기 설치로 ARM 전용 앱 구동 보장.
* **창 닫기 시 깔끔한 세션 정리**: Weston 창 종료 시 백그라운드 세션 자동 종료.
