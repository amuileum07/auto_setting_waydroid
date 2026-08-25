#!/usr/bin/env python3
"""
Waydroid Settings Manager (GUI)
Multi-language support (EN, KO, JA, ZH, ES, DE, FR, IT)
Configures resolution, keyboard/Gboard, shared folders, network fixes, and session control.
"""

import os
import sys
import json
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.expanduser("~/.config/waydroid_settings.json")

# Default Configuration
DEFAULT_CONFIG = {
    "language": "en",
    "mode": "tablet_portrait",
    "width": 800,
    "height": 1200,
    "dpi": 280,
    "share_downloads": True,
    "custom_width": 1080,
    "custom_height": 1920,
}

# Translations Dictionary (Order: EN, KO, JA, ZH, ES, DE, FR, IT)
TRANSLATIONS = {
    "en": {
        "title": "Waydroid Settings Manager",
        "lang_label": "🌐 Language:",
        "tab_display": "Display & Window",
        "tab_input": "Keyboard & Input",
        "tab_storage": "Storage & Sharing",
        "tab_network": "Network & Tools",
        "window_presets": "Window Size Presets:",
        "preset_phone": "📱 Phone (600 x 1024)",
        "preset_tablet_p": "📖 Tablet Portrait (800 x 1200)",
        "preset_tablet_l": "💻 Tablet Landscape (1200 x 800)",
        "preset_fullscreen": "🖥️ Fullscreen",
        "preset_custom": "⚙️ Custom Resolution",
        "width_label": "Width (px):",
        "height_label": "Height (px):",
        "dpi_label": "DPI Density:",
        "gboard_section": "Gboard (Google Keyboard) Settings:",
        "gboard_desc": "Gboard supports multilingual typing and physical keyboard switching.",
        "btn_enable_gboard": "Set Gboard as Default Keyboard",
        "btn_open_ime_settings": "Open Android Keyboard Settings",
        "shortcut_tip": "💡 Tip: Use Shift + Space or Hangul key to toggle languages on physical keyboard.",
        "storage_section": "Host File Sharing:",
        "share_downloads_label": "Share ~/Downloads folder with Android (/sdcard/Download)",
        "btn_open_downloads": "Open Downloads Folder",
        "network_section": "Network & Maintenance:",
        "btn_fix_network": "🛡️ Fix UFW Firewall & Network",
        "btn_install_apk": "📦 Install APK File...",
        "btn_stop_session": "⏹ Stop Waydroid",
        "btn_launch": "🚀 Launch Waydroid",
        "status_running": "Status: Running",
        "status_stopped": "Status: Stopped",
        "msg_saved": "Settings saved successfully!",
        "msg_apk_success": "APK installed successfully!",
        "msg_apk_fail": "Failed to install APK.",
        "msg_gboard_done": "Gboard enabled as default keyboard.",
        "msg_net_fixed": "Network configuration script executed.",
    },
    "ko": {
        "title": "Waydroid 환경설정 매니저",
        "lang_label": "🌐 언어 설정:",
        "tab_display": "디스플레이 및 창",
        "tab_input": "키보드 및 입력",
        "tab_storage": "저장공간 및 공유",
        "tab_network": "네트워크 및 도구",
        "window_presets": "창 크기 프리셋:",
        "preset_phone": "📱 스마트폰 모드 (600 x 1024)",
        "preset_tablet_p": "📖 태블릿 세로 모드 (800 x 1200)",
        "preset_tablet_l": "💻 태블릿 가로 모드 (1200 x 800)",
        "preset_fullscreen": "🖥️ 전체화면",
        "preset_custom": "⚙️ 사용자 지정 해상도",
        "width_label": "너비 (가로 px):",
        "height_label": "높이 (세로 px):",
        "dpi_label": "DPI 배율:",
        "gboard_section": "Gboard (구글 키보드) 설정:",
        "gboard_desc": "Gboard를 통해 한글/다국어 입력 및 노트북 키보드 한/영 전환을 지원합니다.",
        "btn_enable_gboard": "Gboard를 기본 키보드로 활성화",
        "btn_open_ime_settings": "안드로이드 언어/키보드 설정 열기",
        "shortcut_tip": "💡 팁: 노트북 물리 키보드로 입력 시 [Shift + Space] 또는 [한/영] 키로 전환됩니다.",
        "storage_section": "파일 공유 설정:",
        "share_downloads_label": "리눅스 ~/Downloads 폴더를 안드로이드와 자동 공유",
        "btn_open_downloads": "다운로드 폴더 열기",
        "network_section": "네트워크 및 유지관리:",
        "btn_fix_network": "🛡️ 방화벽(UFW) 및 인터넷 차단 해결",
        "btn_install_apk": "📦 APK 파일 직접 설치...",
        "btn_stop_session": "⏹ Waydroid 종료",
        "btn_launch": "🚀 Waydroid 실행하기",
        "status_running": "상태: 실행 중",
        "status_stopped": "상태: 꺼짐",
        "msg_saved": "설정이 저장되었습니다!",
        "msg_apk_success": "APK가 성공적으로 설치되었습니다!",
        "msg_apk_fail": "APK 설치에 실패했습니다.",
        "msg_gboard_done": "Gboard가 기본 키보드로 설정되었습니다.",
        "msg_net_fixed": "네트워크 복구 스크립트를 실행했습니다.",
    },
    "ja": {
        "title": "Waydroid 設定マネージャー",
        "lang_label": "🌐 言語:",
        "tab_display": "ディスプレイとウィンドウ",
        "tab_input": "キーボードと入力",
        "tab_storage": "ストレージと共有",
        "tab_network": "ネットワークとツール",
        "window_presets": "ウィンドウサイズ プリセット:",
        "preset_phone": "📱 スマホ (600 x 1024)",
        "preset_tablet_p": "📖 タブレット 縦 (800 x 1200)",
        "preset_tablet_l": "💻 タブレット 横 (1200 x 800)",
        "preset_fullscreen": "🖥️ 全画面表示",
        "preset_custom": "⚙️ カスタム解像度",
        "width_label": "幅 (px):",
        "height_label": "高さ (px):",
        "dpi_label": "DPI 密度:",
        "gboard_section": "Gboard (Google キーボード) 設定:",
        "gboard_desc": "Gboardで日本語入力と物理キーボード切り替えをサポートします。",
        "btn_enable_gboard": "Gboardをデフォルトに設定",
        "btn_open_ime_settings": "Androidキーボード設定を開く",
        "shortcut_tip": "💡 ヒント: 物理キーボードで Shift + Space を押して言語を切り替えます。",
        "storage_section": "ホストファイル共有:",
        "share_downloads_label": "~/Downloads フォルダを共有 (/sdcard/Download)",
        "btn_open_downloads": "ダウンロードフォルダを開く",
        "network_section": "ネットワークとメンテナンス:",
        "btn_fix_network": "🛡️ UFWファイアウォール & ネット修復",
        "btn_install_apk": "📦 APKファイルをインストール...",
        "btn_stop_session": "⏹ Waydroid 停止",
        "btn_launch": "🚀 Waydroid 起動",
        "status_running": "ステータス: 実行中",
        "status_stopped": "ステータス: 停止中",
        "msg_saved": "設定が保存されました！",
        "msg_apk_success": "APKが正常にインストールされました！",
        "msg_apk_fail": "APKのインストールに失敗しました。",
        "msg_gboard_done": "Gboardがデフォルトキーボードに設定されました。",
        "msg_net_fixed": "ネットワーク設定スクリプトを実行しました。",
    },
    "zh": {
        "title": "Waydroid 设置管理器",
        "lang_label": "🌐 语言:",
        "tab_display": "显示与窗口",
        "tab_input": "键盘与输入",
        "tab_storage": "存储与共享",
        "tab_network": "网络与工具",
        "window_presets": "窗口尺寸预设:",
        "preset_phone": "📱 手机 (600 x 1024)",
        "preset_tablet_p": "📖 平板竖屏 (800 x 1200)",
        "preset_tablet_l": "💻 平板横屏 (1200 x 800)",
        "preset_fullscreen": "🖥️ 全屏模式",
        "preset_custom": "⚙️ 自定义分辨率",
        "width_label": "宽度 (px):",
        "height_label": "高度 (px):",
        "dpi_label": "DPI 密度:",
        "gboard_section": "Gboard (谷歌输入法) 设置:",
        "gboard_desc": "Gboard支持多语言输入和实体键盘切换。",
        "btn_enable_gboard": "将Gboard设为默认输入法",
        "btn_open_ime_settings": "打开Android输入法设置",
        "shortcut_tip": "💡 提示: 在实体键盘上按 Shift + Space 切换输入语言。",
        "storage_section": "文件共享设置:",
        "share_downloads_label": "共享 ~/Downloads 文件夹 (/sdcard/Download)",
        "btn_open_downloads": "打开下载文件夹",
        "network_section": "网络与维护:",
        "btn_fix_network": "🛡️ 修复UFW防火墙与网络",
        "btn_install_apk": "📦 安装APK文件...",
        "btn_stop_session": "⏹ 停止 Waydroid",
        "btn_launch": "🚀 启动 Waydroid",
        "status_running": "状态: 运行中",
        "status_stopped": "状态: 已停止",
        "msg_saved": "设置已成功保存！",
        "msg_apk_success": "APK 安装成功！",
        "msg_apk_fail": "APK 安装失败。",
        "msg_gboard_done": "已将 Gboard 设置为默认输入法。",
        "msg_net_fixed": "网络修复脚本已执行。",
    },
    "es": {
        "title": "Administrador de Waydroid",
        "lang_label": "🌐 Idioma:",
        "tab_display": "Pantalla y Ventana",
        "tab_input": "Teclado y Entrada",
        "tab_storage": "Almacenamiento",
        "tab_network": "Red y Herramientas",
        "window_presets": "Tamaño de Ventana:",
        "preset_phone": "📱 Móvil (600 x 1024)",
        "preset_tablet_p": "📖 Tableta Vertical (800 x 1200)",
        "preset_tablet_l": "💻 Tableta Horizontal (1200 x 800)",
        "preset_fullscreen": "🖥️ Pantalla Completa",
        "preset_custom": "⚙️ Personalizado",
        "width_label": "Ancho (px):",
        "height_label": "Alto (px):",
        "dpi_label": "Densidad DPI:",
        "gboard_section": "Configuración de Gboard:",
        "gboard_desc": "Gboard admite escritura multilingüe y teclado físico.",
        "btn_enable_gboard": "Establecer Gboard por Defecto",
        "btn_open_ime_settings": "Abrir Ajustes de Teclado Android",
        "shortcut_tip": "💡 Consejo: Usa Shift + Space para cambiar de idioma en teclado físico.",
        "storage_section": "Archivos Compartidos:",
        "share_downloads_label": "Compartir carpeta ~/Downloads (/sdcard/Download)",
        "btn_open_downloads": "Abrir Descargas",
        "network_section": "Red y Mantenimiento:",
        "btn_fix_network": "🛡️ Reparar Cortafuegos UFW",
        "btn_install_apk": "📦 Instalar archivo APK...",
        "btn_stop_session": "⏹ Detener Waydroid",
        "btn_launch": "🚀 Iniciar Waydroid",
        "status_running": "Estado: En ejecución",
        "status_stopped": "Estado: Detenido",
        "msg_saved": "¡Ajustes guardados!",
        "msg_apk_success": "¡APK instalado con éxito!",
        "msg_apk_fail": "Error al instalar APK.",
        "msg_gboard_done": "Gboard configurado como teclado predeterminado.",
        "msg_net_fixed": "Script de red ejecutado.",
    },
    "de": {
        "title": "Waydroid Einstellungen",
        "lang_label": "🌐 Sprache:",
        "tab_display": "Anzeige & Fenster",
        "tab_input": "Tastatur & Eingabe",
        "tab_storage": "Speicher & Freigabe",
        "tab_network": "Netzwerk & Tools",
        "window_presets": "Fenstergrößen-Voreinstellungen:",
        "preset_phone": "📱 Smartphone (600 x 1024)",
        "preset_tablet_p": "📖 Tablet Hochformat (800 x 1200)",
        "preset_tablet_l": "💻 Tablet Querformat (1200 x 800)",
        "preset_fullscreen": "🖥️ Vollbild",
        "preset_custom": "⚙️ Benutzerdefiniert",
        "width_label": "Breite (px):",
        "height_label": "Höhe (px):",
        "dpi_label": "DPI-Dichte:",
        "gboard_section": "Gboard (Google-Tastatur) Einstellungen:",
        "gboard_desc": "Gboard unterstützt mehrsprachige Eingabe und Tastaturwechsel.",
        "btn_enable_gboard": "Gboard als Standard festlegen",
        "btn_open_ime_settings": "Android-Tastatureinstellungen öffnen",
        "shortcut_tip": "💡 Tipp: Mit Umschalt + Leertaste zwischen Sprachen wechseln.",
        "storage_section": "Dateifreigabe:",
        "share_downloads_label": "~/Downloads mit Android teilen (/sdcard/Download)",
        "btn_open_downloads": "Downloads öffnen",
        "network_section": "Netzwerk & Wartung:",
        "btn_fix_network": "🛡️ UFW-Firewall & Netzwerk reparieren",
        "btn_install_apk": "📦 APK-Datei installieren...",
        "btn_stop_session": "⏹ Waydroid stoppen",
        "btn_launch": "🚀 Waydroid starten",
        "status_running": "Status: Läuft",
        "status_stopped": "Status: Gestoppt",
        "msg_saved": "Einstellungen erfolgreich gespeichert!",
        "msg_apk_success": "APK erfolgreich installiert!",
        "msg_apk_fail": "Installation der APK fehlgeschlagen.",
        "msg_gboard_done": "Gboard als Standardtastatur aktiviert.",
        "msg_net_fixed": "Netzwerk-Skript ausgeführt.",
    },
    "fr": {
        "title": "Gestionnaire Waydroid",
        "lang_label": "🌐 Langue:",
        "tab_display": "Affichage & Fenêtre",
        "tab_input": "Clavier & Saisie",
        "tab_storage": "Stockage & Partage",
        "tab_network": "Réseau & Outils",
        "window_presets": "Préréglages de Taille:",
        "preset_phone": "📱 Téléphone (600 x 1024)",
        "preset_tablet_p": "📖 Tablette Portrait (800 x 1200)",
        "preset_tablet_l": "💻 Tablette Paysage (1200 x 800)",
        "preset_fullscreen": "🖥️ Plein écran",
        "preset_custom": "⚙️ Personnalisé",
        "width_label": "Largeur (px):",
        "height_label": "Hauteur (px):",
        "dpi_label": "Densité DPI:",
        "gboard_section": "Paramètres Gboard:",
        "gboard_desc": "Gboard prend en charge la saisie multilingue et le clavier physique.",
        "btn_enable_gboard": "Définir Gboard par défaut",
        "btn_open_ime_settings": "Ouvrir paramètres clavier Android",
        "shortcut_tip": "💡 Astuce: Utilisez Shift + Espace pour changer de langue.",
        "storage_section": "Partage de fichiers:",
        "share_downloads_label": "Partager ~/Downloads (/sdcard/Download)",
        "btn_open_downloads": "Ouvrir Téléchargements",
        "network_section": "Réseau & Maintenance:",
        "btn_fix_network": "🛡️ Réparer pare-feu UFW",
        "btn_install_apk": "📦 Installer un fichier APK...",
        "btn_stop_session": "⏹ Arrêter Waydroid",
        "btn_launch": "🚀 Lancer Waydroid",
        "status_running": "Statut: En cours",
        "status_stopped": "Statut: Arrêté",
        "msg_saved": "Paramètres enregistrés !",
        "msg_apk_success": "APK installée avec succès !",
        "msg_apk_fail": "Échec de l'installation de l'APK.",
        "msg_gboard_done": "Gboard configuré comme clavier par défaut.",
        "msg_net_fixed": "Script réseau exécuté.",
    },
    "it": {
        "title": "Gestore Impostazioni Waydroid",
        "lang_label": "🌐 Lingua:",
        "tab_display": "Schermo e Finestra",
        "tab_input": "Tastiera e Input",
        "tab_storage": "Archiviazione",
        "tab_network": "Rete e Strumenti",
        "window_presets": "Dimensioni Finestra:",
        "preset_phone": "📱 Telefono (600 x 1024)",
        "preset_tablet_p": "📖 Tablet Verticale (800 x 1200)",
        "preset_tablet_l": "💻 Tablet Orizzontale (1200 x 800)",
        "preset_fullscreen": "🖥️ Schermo Intero",
        "preset_custom": "⚙️ Personalizzato",
        "width_label": "Larghezza (px):",
        "height_label": "Altezza (px):",
        "dpi_label": "Densità DPI:",
        "gboard_section": "Impostazioni Gboard:",
        "gboard_desc": "Gboard supporta la digitazione multilingue e la tastiera fisica.",
        "btn_enable_gboard": "Imposta Gboard come Predefinito",
        "btn_open_ime_settings": "Apri Impostazioni Tastiera Android",
        "shortcut_tip": "💡 Suggerimento: Usa Shift + Spazio per cambiare lingua sulla tastiera fisica.",
        "storage_section": "Condivisione File:",
        "share_downloads_label": "Condividi cartella ~/Downloads (/sdcard/Download)",
        "btn_open_downloads": "Apri Download",
        "network_section": "Rete e Manutenzione:",
        "btn_fix_network": "🛡️ Ripara Firewall UFW & Rete",
        "btn_install_apk": "📦 Installa file APK...",
        "btn_stop_session": "⏹ Ferma Waydroid",
        "btn_launch": "🚀 Avvia Waydroid",
        "status_running": "Stato: In esecuzione",
        "status_stopped": "Stato: Arrestato",
        "msg_saved": "Impostazioni salvate con successo!",
        "msg_apk_success": "APK installato con successo!",
        "msg_apk_fail": "Impossibile installare APK.",
        "msg_gboard_done": "Gboard impostata come tastiera predefinita.",
        "msg_net_fixed": "Script di rete eseguito.",
    }
}

LANGUAGE_NAMES = [
    ("en", "English"),
    ("ko", "한국어 (Korean)"),
    ("ja", "日本語 (Japanese)"),
    ("zh", "中文 (Chinese)"),
    ("es", "Español (Spanish)"),
    ("de", "Deutsch (German)"),
    ("fr", "Français (French)"),
    ("it", "Italiano (Italian)"),
]

class WaydroidManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.config_data = self.load_config()
        self.current_lang = self.config_data.get("language", "en")
        
        self.title("Waydroid Settings Manager")
        self.geometry("640x560")
        self.minsize(560, 500)
        
        # Configure styles
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.create_widgets()
        self.update_language(self.current_lang)

    def load_config(self):
        config = DEFAULT_CONFIG.copy()
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                    config.update(json.load(f))
            except Exception:
                pass
        return config

    def save_config(self):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(self.config_data, f, indent=2)

    def tr(self, key):
        return TRANSLATIONS.get(self.current_lang, TRANSLATIONS["en"]).get(key, key)

    def create_widgets(self):
        # Top Bar: Language Selector
        top_frame = ttk.Frame(self, padding=(12, 10))
        top_frame.pack(fill="x")
        
        self.lbl_lang = ttk.Label(top_frame, text=self.tr("lang_label"), font=("Arial", 10, "bold"))
        self.lbl_lang.pack(side="left", padx=(0, 8))
        
        self.combo_lang = ttk.Combobox(top_frame, state="readonly", width=22)
        self.combo_lang["values"] = [name for _, name in LANGUAGE_NAMES]
        current_idx = [code for code, _ in LANGUAGE_NAMES].index(self.current_lang) if self.current_lang in [code for code, _ in LANGUAGE_NAMES] else 0
        self.combo_lang.current(current_idx)
        self.combo_lang.bind("<<ComboboxSelected>>", self.on_language_change)
        self.combo_lang.pack(side="left")
        
        self.lbl_status = ttk.Label(top_frame, text="", font=("Arial", 9, "italic"))
        self.lbl_status.pack(side="right")
        self.check_status()

        # Notebook (Tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=(0, 10))
        
        # Tab 1: Display
        self.tab_display = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(self.tab_display, text=self.tr("tab_display"))
        self.setup_display_tab()
        
        # Tab 2: Keyboard & Input
        self.tab_input = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(self.tab_input, text=self.tr("tab_input"))
        self.setup_input_tab()
        
        # Tab 3: Storage & Sharing
        self.tab_storage = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(self.tab_storage, text=self.tr("tab_storage"))
        self.setup_storage_tab()
        
        # Tab 4: Network & Tools
        self.tab_network = ttk.Frame(self.notebook, padding=16)
        self.notebook.add(self.tab_network, text=self.tr("tab_network"))
        self.setup_network_tab()

        # Bottom Action Bar
        bottom_frame = ttk.Frame(self, padding=(12, 10))
        bottom_frame.pack(fill="x", side="bottom")
        
        self.btn_stop = ttk.Button(bottom_frame, text=self.tr("btn_stop_session"), command=self.stop_waydroid)
        self.btn_stop.pack(side="left", padx=5)
        
        self.btn_launch = ttk.Button(bottom_frame, text=self.tr("btn_launch"), command=self.launch_waydroid)
        self.btn_launch.pack(side="right", padx=5)

    def setup_display_tab(self):
        self.lbl_presets = ttk.Label(self.tab_display, text=self.tr("window_presets"), font=("Arial", 10, "bold"))
        self.lbl_presets.pack(anchor="w", pady=(0, 8))
        
        self.mode_var = tk.StringVar(value=self.config_data.get("mode", "tablet_portrait"))
        
        self.rb_phone = ttk.Radiobutton(self.tab_display, text=self.tr("preset_phone"), value="phone", variable=self.mode_var, command=self.on_mode_change)
        self.rb_phone.pack(anchor="w", pady=2)
        
        self.rb_tablet_p = ttk.Radiobutton(self.tab_display, text=self.tr("preset_tablet_p"), value="tablet_portrait", variable=self.mode_var, command=self.on_mode_change)
        self.rb_tablet_p.pack(anchor="w", pady=2)
        
        self.rb_tablet_l = ttk.Radiobutton(self.tab_display, text=self.tr("preset_tablet_l"), value="tablet_landscape", variable=self.mode_var, command=self.on_mode_change)
        self.rb_tablet_l.pack(anchor="w", pady=2)
        
        self.rb_full = ttk.Radiobutton(self.tab_display, text=self.tr("preset_fullscreen"), value="fullscreen", variable=self.mode_var, command=self.on_mode_change)
        self.rb_full.pack(anchor="w", pady=2)
        
        self.rb_custom = ttk.Radiobutton(self.tab_display, text=self.tr("preset_custom"), value="custom", variable=self.mode_var, command=self.on_mode_change)
        self.rb_custom.pack(anchor="w", pady=2)
        
        # Custom Resolution inputs
        self.custom_frame = ttk.LabelFrame(self.tab_display, text="Custom Size", padding=10)
        self.custom_frame.pack(fill="x", pady=10)
        
        self.lbl_w = ttk.Label(self.custom_frame, text=self.tr("width_label"))
        self.lbl_w.grid(row=0, column=0, padx=5, pady=4, sticky="w")
        self.ent_w = ttk.Entry(self.custom_frame, width=8)
        self.ent_w.insert(0, str(self.config_data.get("custom_width", 1080)))
        self.ent_w.grid(row=0, column=1, padx=5, pady=4)
        
        self.lbl_h = ttk.Label(self.custom_frame, text=self.tr("height_label"))
        self.lbl_h.grid(row=0, column=2, padx=5, pady=4, sticky="w")
        self.ent_h = ttk.Entry(self.custom_frame, width=8)
        self.ent_h.insert(0, str(self.config_data.get("custom_height", 1920)))
        self.ent_h.grid(row=0, column=3, padx=5, pady=4)
        
        self.lbl_dpi = ttk.Label(self.custom_frame, text=self.tr("dpi_label"))
        self.lbl_dpi.grid(row=0, column=4, padx=5, pady=4, sticky="w")
        self.ent_dpi = ttk.Entry(self.custom_frame, width=6)
        self.ent_dpi.insert(0, str(self.config_data.get("dpi", 280)))
        self.ent_dpi.grid(row=0, column=5, padx=5, pady=4)

    def setup_input_tab(self):
        self.lbl_gboard_sec = ttk.Label(self.tab_input, text=self.tr("gboard_section"), font=("Arial", 10, "bold"))
        self.lbl_gboard_sec.pack(anchor="w", pady=(0, 6))
        
        self.lbl_gboard_desc = ttk.Label(self.tab_input, text=self.tr("gboard_desc"), wraplength=560)
        self.lbl_gboard_desc.pack(anchor="w", pady=(0, 12))
        
        self.btn_gboard = ttk.Button(self.tab_input, text=self.tr("btn_enable_gboard"), command=self.enable_gboard)
        self.btn_gboard.pack(anchor="w", pady=4)
        
        self.btn_ime_settings = ttk.Button(self.tab_input, text=self.tr("btn_open_ime_settings"), command=self.open_ime_settings)
        self.btn_ime_settings.pack(anchor="w", pady=4)
        
        self.lbl_tip = ttk.Label(self.tab_input, text=self.tr("shortcut_tip"), foreground="#2b5797", wraplength=560, font=("Arial", 9, "italic"))
        self.lbl_tip.pack(anchor="w", pady=(16, 0))

    def setup_storage_tab(self):
        self.lbl_storage_sec = ttk.Label(self.tab_storage, text=self.tr("storage_section"), font=("Arial", 10, "bold"))
        self.lbl_storage_sec.pack(anchor="w", pady=(0, 6))
        
        self.share_var = tk.BooleanVar(value=self.config_data.get("share_downloads", True))
        self.cb_share = ttk.Checkbutton(self.tab_storage, text=self.tr("share_downloads_label"), variable=self.share_var, command=self.on_share_change)
        self.cb_share.pack(anchor="w", pady=8)
        
        self.btn_open_dl = ttk.Button(self.tab_storage, text=self.tr("btn_open_downloads"), command=self.open_downloads)
        self.btn_open_dl.pack(anchor="w", pady=4)

    def setup_network_tab(self):
        self.lbl_net_sec = ttk.Label(self.tab_network, text=self.tr("network_section"), font=("Arial", 10, "bold"))
        self.lbl_net_sec.pack(anchor="w", pady=(0, 8))
        
        self.btn_fix_net = ttk.Button(self.tab_network, text=self.tr("btn_fix_network"), command=self.fix_network)
        self.btn_fix_net.pack(anchor="w", pady=4)
        
        self.btn_apk = ttk.Button(self.tab_network, text=self.tr("btn_install_apk"), command=self.install_apk)
        self.btn_apk.pack(anchor="w", pady=4)

    def on_language_change(self, event=None):
        selected_idx = self.combo_lang.current()
        if selected_idx >= 0 and selected_idx < len(LANGUAGE_NAMES):
            self.current_lang = LANGUAGE_NAMES[selected_idx][0]
            self.config_data["language"] = self.current_lang
            self.save_config()
            self.update_language(self.current_lang)

    def update_language(self, lang_code):
        self.current_lang = lang_code
        self.title(self.tr("title"))
        self.lbl_lang.config(text=self.tr("lang_label"))
        
        # Update Notebook tab names
        self.notebook.tab(0, text=self.tr("tab_display"))
        self.notebook.tab(1, text=self.tr("tab_input"))
        self.notebook.tab(2, text=self.tr("tab_storage"))
        self.notebook.tab(3, text=self.tr("tab_network"))
        
        # Display tab
        self.lbl_presets.config(text=self.tr("window_presets"))
        self.rb_phone.config(text=self.tr("preset_phone"))
        self.rb_tablet_p.config(text=self.tr("preset_tablet_p"))
        self.rb_tablet_l.config(text=self.tr("preset_tablet_l"))
        self.rb_full.config(text=self.tr("preset_fullscreen"))
        self.rb_custom.config(text=self.tr("preset_custom"))
        self.lbl_w.config(text=self.tr("width_label"))
        self.lbl_h.config(text=self.tr("height_label"))
        self.lbl_dpi.config(text=self.tr("dpi_label"))
        
        # Input tab
        self.lbl_gboard_sec.config(text=self.tr("gboard_section"))
        self.lbl_gboard_desc.config(text=self.tr("gboard_desc"))
        self.btn_gboard.config(text=self.tr("btn_enable_gboard"))
        self.btn_ime_settings.config(text=self.tr("btn_open_ime_settings"))
        self.lbl_tip.config(text=self.tr("shortcut_tip"))
        
        # Storage tab
        self.lbl_storage_sec.config(text=self.tr("storage_section"))
        self.cb_share.config(text=self.tr("share_downloads_label"))
        self.btn_open_dl.config(text=self.tr("btn_open_downloads"))
        
        # Network tab
        self.lbl_net_sec.config(text=self.tr("network_section"))
        self.btn_fix_net.config(text=self.tr("btn_fix_network"))
        self.btn_apk.config(text=self.tr("btn_install_apk"))
        
        # Bottom
        self.btn_stop.config(text=self.tr("btn_stop_session"))
        self.btn_launch.config(text=self.tr("btn_launch"))
        self.check_status()

    def on_mode_change(self):
        mode = self.mode_var.get()
        self.config_data["mode"] = mode
        if mode == "phone":
            self.config_data["width"] = 600
            self.config_data["height"] = 1024
        elif mode == "tablet_portrait":
            self.config_data["width"] = 800
            self.config_data["height"] = 1200
        elif mode == "tablet_landscape":
            self.config_data["width"] = 1200
            self.config_data["height"] = 800
        elif mode == "fullscreen":
            self.config_data["width"] = 0
            self.config_data["height"] = 0
        elif mode == "custom":
            try:
                self.config_data["width"] = int(self.ent_w.get())
                self.config_data["height"] = int(self.ent_h.get())
                self.config_data["dpi"] = int(self.ent_dpi.get())
            except ValueError:
                pass
        self.save_config()

    def on_share_change(self):
        self.config_data["share_downloads"] = self.share_var.get()
        self.save_config()

    def check_status(self):
        try:
            out = subprocess.check_output(["waydroid", "status"], text=True, stderr=subprocess.DEVNULL)
            if "Session:\tRUNNING" in out or "Session: RUNNING" in out:
                self.lbl_status.config(text=self.tr("status_running"), foreground="green")
            else:
                self.lbl_status.config(text=self.tr("status_stopped"), foreground="gray")
        except Exception:
            self.lbl_status.config(text=self.tr("status_stopped"), foreground="gray")

    def enable_gboard(self):
        try:
            # Enable Gboard IME via waydroid shell
            subprocess.run([
                "waydroid", "shell", "ime", "enable",
                "com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME"
            ], check=False)
            subprocess.run([
                "waydroid", "shell", "ime", "set",
                "com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME"
            ], check=False)
            messagebox.showinfo("Waydroid", self.tr("msg_gboard_done"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_ime_settings(self):
        try:
            subprocess.Popen(["waydroid", "shell", "am", "start", "-a", "android.settings.INPUT_METHOD_SETTINGS"])
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_downloads(self):
        dl_path = os.path.expanduser("~/Downloads")
        if os.path.exists(dl_path):
            subprocess.Popen(["xdg-open", dl_path])

    def fix_network(self):
        script = os.path.join(SCRIPT_DIR, "diagnose_and_fix_network.sh")
        if os.path.exists(script):
            subprocess.Popen(["x-terminal-emulator", "-e", f"bash {script}"])
            messagebox.showinfo("Waydroid", self.tr("msg_net_fixed"))

    def install_apk(self):
        file_path = filedialog.askopenfilename(
            title="Select APK File",
            filetypes=[("Android Package", "*.apk"), ("All Files", "*.*")]
        )
        if file_path:
            installer = os.path.join(SCRIPT_DIR, "install_apk.sh")
            try:
                res = subprocess.run([installer, file_path], capture_output=True, text=True)
                if res.returncode == 0:
                    messagebox.showinfo("Waydroid", self.tr("msg_apk_success"))
                else:
                    messagebox.showerror("Waydroid", f"{self.tr('msg_apk_fail')}\n{res.stderr or res.stdout}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def stop_waydroid(self):
        subprocess.run(["waydroid", "session", "stop"], check=False)
        self.check_status()

    def launch_waydroid(self):
        self.on_mode_change()
        runner = os.path.join(SCRIPT_DIR, "run_waydroid.sh")
        subprocess.Popen([runner])
        self.after(3000, self.check_status)

if __name__ == "__main__":
    app = WaydroidManagerApp()
    app.mainloop()
