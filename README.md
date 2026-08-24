# Waydroid Auto Setup Suite 🚀

**English** | [한국어 (Korean)](README_KR.md)

An all-in-one automated setup suite for running **Waydroid** (Android container) seamlessly on **Linux Mint (Cinnamon / X11)** and **Ubuntu / Debian** systems.

This suite automatically configures **X11 Weston nested compositor**, **ARM Translation (libndk / libhoudini)**, **UFW firewall & network forwarding fixes**, **Aurora Store**, and **Desktop shortcut launchers**.

---

## ⚡ Quick Start (1-Line Setup on a Fresh Machine)

Open a terminal on your target machine and run:

```bash
git clone https://github.com/amuileum07/auto_setting_waydroid.git
cd auto_setting_waydroid
./install.sh
```

---

## 📂 Repository Contents

| File | Description |
| :--- | :--- |
| **`install.sh`** | Master one-click installer for Waydroid, ARM translation, network fixes, and desktop shortcuts |
| **`run_waydroid.sh`** | Universal launcher supporting both X11 (via Weston) and native Wayland sessions |
| **`create_desktop_shortcut.sh`** | Generates desktop and application menu shortcut icons |
| **`install_apk.sh`** | Helper script to easily sideload APK files into Waydroid |
| **`diagnose_and_fix_network.sh`** | Standalone script to resolve UFW firewall blocking, IP forwarding, and DNS issues |

---

## 📖 How to Use

### 1. Launching Android
* Double-click the **`Waydroid (Android)`** icon on your Desktop or launch it from the Application Menu.
* Alternatively, run `./run_waydroid.sh` in your terminal.

### 2. Installing Android Apps (Aurora Store)
1. In the Waydroid window, swipe up from the bottom to open the App Drawer.
2. Launch **Aurora Store**, choose **Anonymous Login**, and search for your desired Android apps (e.g., eBook readers, messengers, utilities).

### 3. Setting Up Multilingual Keyboard (e.g., Gboard)
1. Install **Gboard** from Aurora Store.
2. Navigate to Android **Settings → System → Languages & input → On-screen keyboard** and enable Gboard with your preferred languages.
3. For physical laptop keyboards, toggle languages using **`Shift + Space`**.

---

## 🔧 Automated Features & Optimizations
* **Seamless X11 Support**: Automatically spawns and integrates a Weston Wayland window when running under standard X11 desktop environments (such as Linux Mint Cinnamon).
* **Firewall & Routing Fixes**: Automatically configures `/etc/default/ufw` packet forwarding (`ACCEPT`), routes `waydroid0` virtual bridge traffic, and sets Google DNS (`8.8.8.8`) / Cloudflare DNS (`1.1.1.1`).
* **Hardware-Aware ARM Translation**: Automatically detects CPU vendor (AMD Ryzen → `libndk`, Intel → `libhoudini`) and installs Widevine DRM L3 support.
* **Clean Session Lifecycle**: Automatically cleans up and stops background Waydroid container sessions when closing the Weston display window.
