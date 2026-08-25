# Waydroid 자동 설정 및 관리 매니저 🚀

[English README](README.md) | **한국어**

Linux Mint (Cinnamon / X11) 및 Ubuntu / Debian 환경에서 **Waydroid**(안드로이드 컨테이너)를 원클릭으로 설치하고, **8개 국어 지원 GUI 설정 매니저**, **ARM Translation(libndk/libhoudini)**, **방화벽(UFW) 네트워크 해결**, **Aurora Store**, **다운로드 폴더 공유**, **바탕화면 바로가기 아이콘 생성**까지 완전히 자동화해 주는 올인원 패키지입니다.

---

## ✨ 주요 기능

* 🖥️ **GUI 환경설정 매니저 (`waydroid_gui.py`)**:
  * **8개 언어 즉시 전환 지원**: English (기본), 한국어, 日本語 (일본어), 中文 (중국어), Español (스페인어), Deutsch (독일어), Français (프랑스어), Italiano (이탈리아어).
  * **창 크기/해상도 원클릭 프리셋**: 스마트폰(600×1024), 태블릿 세로(800×1200), 태블릿 가로(1200×800), 전체화면, 사용자 정의 해상도.
  * **Gboard 및 한글/다국어 입력 도우미**: 기본 키보드 원클릭 활성화 및 노트북 키보드 `Shift + Space` 한/영 전환 지원.
  * **호스트 ↔ 안드로이드 파일 공유**: `~/Downloads` 폴더를 안드로이드(`/sdcard/Download`)와 자동 연동.
  * **네트워크 자동 점검 및 수정**: UFW 방화벽 차단 및 DNS 이슈 원클릭 복구.
* ⚡ **올인원 자동 설치 스크립트 (`install.sh`)**: 패키지 설치부터 AMD/Intel CPU 자동 감지 기반 ARM 번역 레이어 탑재까지 한 번에 완료.
* 🧹 **완전 삭제/복구 스크립트 (`uninstall.sh`)**: 컨테이너, 설정 파일, 바로가기 및 패키지를 시스템에서 깨끗하게 제거.

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
| **`waydroid_gui.py`** | 8개 국어 지원 그래픽 환경설정 매니저 및 실행기 |
| **`run_waydroid.sh`** | X11/Wayland 환경을 자동 감지하여 안드로이드 창을 실행하는 범용 런처 |
| **`create_desktop_shortcut.sh`** | 바탕화면 및 시작 메뉴에 바로가기 아이콘 2종(메인/설정)을 생성하는 스크립트 |
| **`install_apk.sh`** | APK 파일을 Waydroid에 쉽게 설치해 주는 헬퍼 스크립트 |
| **`diagnose_and_fix_network.sh`** | UFW 방화벽 차단 및 DNS/Fake Wi-Fi 이슈 해결 스크립트 |
| **`uninstall.sh`** | Waydroid 및 관련 설정을 시스템에서 깨끗하게 제거하는 언인스톨러 |
| **`LICENSE`** | MIT License |

---

## 📖 사용 방법

### 1. 설정 매니저(GUI) 실행
* 바탕화면의 **`Waydroid Settings Manager`** 아이콘을 더블 클릭하여 실행합니다. (또는 `python3 waydroid_gui.py`)
* 원하는 해상도(스마트폰/태블릿)를 선택하고 바로 실행할 수 있습니다.

### 2. 안드로이드 앱 설치 (Aurora Store)
1. 안드로이드 화면을 아래에서 위로 쓸어 올려 **Aurora Store** 실행
2. 익명(Anonymous) 로그인 후 원하는 앱(전자책, 메신저 등) 검색 및 설치

### 3. 한글 및 다국어 입력 (Gboard)
1. Aurora Store에서 **`Gboard`** 설치
2. 설정 매니저(GUI)에서 **"Gboard를 기본 키보드로 활성화"** 클릭 (또는 안드로이드 설정에서 지정)
3. 노트북 키보드로 타이핑 시 **`Shift + Space`** 또는 **`한/영`** 키로 언어 전환

---

## 🗑️ 완전 삭제 (Uninstall)

Waydroid 환경을 시스템에서 완전히 제거하고 복구하려면:

```bash
./uninstall.sh
```

---

## 📄 라이선스
이 프로젝트는 [MIT License](LICENSE)를 따릅니다.
