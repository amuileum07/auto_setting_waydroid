# Waydroid Auto Setup Suite 🚀

**English** | [한국어 (Korean)](README_KR.md)

An all-in-one automated setup and management suite for running **Waydroid** (Android container) seamlessly on **Linux Mint (Cinnamon / X11)** and **Ubuntu / Debian** systems.

Includes a **multi-language Python GUI Settings Manager** (supporting 8 languages), automated **ARM Translation (libndk / libhoudini)**, **UFW firewall/network fixes**, **Aurora Store**, **host-container file sharing**, and **desktop launchers**.

---

## ✨ Key Features

* 🖥️ **GUI Settings Manager (`waydroid_gui.py`)**:
  * **8 Languages supported**: English (Default), 한국어 (Korean), 日本語 (Japanese), 中文 (Chinese), Español (Spanish), Deutsch (German), Français (French), Italiano (Italian).
  * **Window Size & Mode Presets**: Phone (600×1024), Tablet Portrait (800×1200), Tablet Landscape (1200×800), Fullscreen, and Custom Resolutions.
  * **One-Click Gboard & Input Helper**: Quick IME enabling and physical keyboard `Shift + Space` language switching guide.
  * **Host File Sharing**: Shared `~/Downloads` folder with Android (`/sdcard/Download`).
  * **Network Diagnostic & Maintenance**: One-click UFW and DNS resolver.
* ⚡ **Zero-Config Installer (`install.sh`)**: Automates package installation, Waydroid initialization, ARM translation for both AMD & Intel CPUs, and desktop shortcuts.
* 🧹 **Clean Uninstaller (`uninstall.sh`)**: Completely and cleanly roll back containers, images, shortcuts, and network configurations.

---

## ⚡ Quick Start (1-Line Setup on Fresh Laptop)

Open a terminal on your machine and run:

```bash
git clone https://github.com/amuileum07/auto_setting_waydroid.git
cd auto_setting_waydroid
./install.sh
```

---

## 📂 Repository Contents

| File | Description |
| :--- | :--- |
| **`install.sh`** | Master one-click installer for Waydroid, ARM translation, network fixes, and GUI shortcuts |
| **`waydroid_gui.py`** | Multi-language graphical settings manager and session controller |
| **`run_waydroid.sh`** | Universal launcher supporting both X11 (via Weston) and native Wayland sessions |
| **`create_desktop_shortcut.sh`** | Generates desktop and application menu shortcut icons |
| **`install_apk.sh`** | Helper script to easily sideload APK files into Waydroid |
| **`diagnose_and_fix_network.sh`** | Standalone script to resolve UFW firewall blocking, IP forwarding, and DNS issues |
| **`uninstall.sh`** | Clean uninstaller to purge containers, configurations, and shortcuts |
| **`LICENSE`** | MIT License |

---

## 📖 How to Use

### 1. Launching GUI Settings Manager
* Double-click **`Waydroid Settings Manager`** on your Desktop or launch `python3 waydroid_gui.py`.
* Select your preferred window size (Phone, Tablet, or Fullscreen) and launch Waydroid directly.

### 2. Installing Android Apps (Aurora Store)
1. In the Waydroid window, swipe up from the bottom to open the App Drawer.
2. Launch **Aurora Store**, choose **Anonymous Login**, and search for your desired Android apps.

### 3. Multilingual Typing (Gboard)
1. Install **Gboard** from Aurora Store.
2. Click **"Set Gboard as Default Keyboard"** in the Settings GUI Manager (or navigate to Android **Settings → System → Languages & input**).
3. On physical laptop keyboards, toggle input languages using **`Shift + Space`**.

---

## 🗑️ Uninstallation

To completely remove Waydroid and its configuration from your machine:

```bash
./uninstall.sh
```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
