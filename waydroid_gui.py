#!/usr/bin/env python3
"""
Waydroid Settings Manager (GUI)
Clean UI with Multi-language support (EN, KO, JA, ZH, ES, DE, FR, IT)
Optimized for Linux FreeType/Noto TrueType font rendering without broken emojis.
"""

import os
import sys
import json
import subprocess
import tkinter as tk
import tkinter.font as tkfont
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
    "shared_folder_path": os.path.expanduser("~/Downloads"),
    "custom_width": 1080,
    "custom_height": 1920,
}

# Clean Translations Dictionary without broken Unicode emoji glyphs
TRANSLATIONS = {
    "en": {
        "title": "Waydroid Settings Manager",
        "lang_label": "Language:",
        "tab_display": "Display & Window",
        "tab_input": "Keyboard & Input",
        "tab_storage": "Storage & Sharing",
        "tab_network": "Network & Tools",
        "window_presets": "Window Size Presets:",
        "preset_phone": "Phone Mode (600 x 1024)",
        "preset_tablet_p": "Tablet Portrait Mode (800 x 1200)",
        "preset_tablet_l": "Tablet Landscape Mode (1200 x 800)",
        "preset_fullscreen": "Fullscreen Mode",
        "preset_custom": "Custom Resolution",
        "width_label": "Width (px):",
        "height_label": "Height (px):",
        "dpi_label": "DPI Density:",
        "gboard_section": "Gboard (Google Keyboard) Configuration:",
        "gboard_desc": "Gboard provides smooth multilingual typing and physical keyboard language switching.",
        "btn_enable_gboard": "Set Gboard as Default Keyboard",
        "btn_open_ime_settings": "Open Android Keyboard Settings",
        "shortcut_tip": "Shortcut: Press [Shift + Space] or [Hangul] key to toggle language on physical keyboard.",
        "storage_section": "Host-Android Folder Sharing:",
        "storage_desc": "Automatically share a local computer folder with Android Download storage (/sdcard/Download).",
        "share_downloads_label": "Enable Folder Sharing with Android",
        "shared_folder_label": "Local Folder to Share:",
        "btn_browse": "Browse...",
        "btn_open_downloads": "Open Selected Folder",
        "network_section": "Network Diagnostics & Maintenance:",
        "btn_fix_network": "Fix UFW Firewall & Network",
        "btn_install_apk": "Install APK File...",
        "btn_stop_session": "Stop Waydroid",
        "btn_launch": "Launch Waydroid",
        "status_running": "Status: Running",
        "status_stopped": "Status: Stopped",
        "msg_saved": "Settings saved successfully.",
        "msg_apk_success": "APK installed successfully!",
        "msg_apk_fail": "Failed to install APK.",
        "msg_gboard_done": "Gboard has been configured as the default keyboard.",
        "msg_net_fixed": "Network configuration script executed.",
    },
    "ko": {
        "title": "Waydroid 환경설정 매니저",
        "lang_label": "언어 설정:",
        "tab_display": "디스플레이 및 창",
        "tab_input": "키보드 및 입력",
        "tab_storage": "저장공간 및 공유",
        "tab_network": "네트워크 및 도구",
        "window_presets": "창 크기 프리셋:",
        "preset_phone": "스마트폰 모드 (600 x 1024)",
        "preset_tablet_p": "태블릿 세로 모드 (800 x 1200)",
        "preset_tablet_l": "태블릿 가로 모드 (1200 x 800)",
        "preset_fullscreen": "전체화면 모드",
        "preset_custom": "사용자 지정 해상도",
        "width_label": "너비 (가로 px):",
        "height_label": "높이 (세로 px):",
        "dpi_label": "DPI 배율:",
        "gboard_section": "Gboard (구글 키보드) 설정:",
        "gboard_desc": "Gboard를 통해 한글/다국어 입력 및 노트북 키보드 한/영 전환을 지원합니다.",
        "btn_enable_gboard": "Gboard를 기본 키보드로 활성화",
        "btn_open_ime_settings": "안드로이드 언어/키보드 설정 열기",
        "shortcut_tip": "단축키 안내: 노트북 물리 키보드로 입력 시 [Shift + Space] 또는 [한/영] 키로 전환됩니다.",
        "storage_section": "호스트-안드로이드 폴더 공유:",
        "storage_desc": "리눅스 PC의 폴더를 안드로이드의 Download 폴더(/sdcard/Download)와 공유합니다.",
        "share_downloads_label": "호스트-안드로이드 폴더 공유 활성화",
        "shared_folder_label": "공유할 호스트 폴더 경로:",
        "btn_browse": "폴더 찾기...",
        "btn_open_downloads": "선택된 폴더 열기",
        "network_section": "네트워크 및 유지관리:",
        "btn_fix_network": "방화벽(UFW) 및 인터넷 차단 해결",
        "btn_install_apk": "APK 파일 직접 설치...",
        "btn_stop_session": "Waydroid 종료",
        "btn_launch": "Waydroid 실행하기",
        "status_running": "상태: 실행 중",
        "status_stopped": "상태: 꺼짐",
        "msg_saved": "설정이 저장되었습니다.",
        "msg_apk_success": "APK가 성공적으로 설치되었습니다!",
        "msg_apk_fail": "APK 설치에 실패했습니다.",
        "msg_gboard_done": "Gboard가 기본 키보드로 설정되었습니다.",
        "msg_net_fixed": "네트워크 복구 스크립트를 실행했습니다.",
    },
    "ja": {
        "title": "Waydroid 設定マネージャー",
        "lang_label": "言語設定:",
        "tab_display": "ディスプレイとウィンドウ",
        "tab_input": "キーボードと入力",
        "tab_storage": "ストレージと共有",
        "tab_network": "ネットワークとツール",
        "window_presets": "ウィンドウサイズ プリセット:",
        "preset_phone": "スマホモード (600 x 1024)",
        "preset_tablet_p": "タブレット縦モード (800 x 1200)",
        "preset_tablet_l": "タブレット横モード (1200 x 800)",
        "preset_fullscreen": "全画面表示モード",
        "preset_custom": "カスタム解像度",
        "width_label": "幅 (px):",
        "height_label": "高さ (px):",
        "dpi_label": "DPI 密度:",
        "gboard_section": "Gboard (Google キーボード) 設定:",
        "gboard_desc": "Gboardで日本語入力と物理キーボード切り替えをサポートします。",
        "btn_enable_gboard": "Gboardをデフォルトに設定",
        "btn_open_ime_settings": "Androidキーボード設定を開く",
        "shortcut_tip": "ヒント: 物理キーボードで [Shift + Space] を押して言語を切り替えます。",
        "storage_section": "フォルダ共有オプション:",
        "storage_desc": "ホストPCのフォルダをAndroid (/sdcard/Download) と共有します。",
        "share_downloads_label": "ホスト ↔ Android フォルダ共有を有効化",
        "shared_folder_label": "共有するホストフォルダ:",
        "btn_browse": "参照...",
        "btn_open_downloads": "選択したフォルダを開く",
        "network_section": "ネットワークとメンテナンス:",
        "btn_fix_network": "UFWファイアウォール & ネット修復",
        "btn_install_apk": "APKファイルをインストール...",
        "btn_stop_session": "Waydroid 停止",
        "btn_launch": "Waydroid 起動",
        "status_running": "ステータス: 実行中",
        "status_stopped": "ステータス: 停止中",
        "msg_saved": "設定が保存されました。",
        "msg_apk_success": "APKが正常にインストールされました！",
        "msg_apk_fail": "APKのインストールに失敗しました。",
        "msg_gboard_done": "Gboardがデフォルトキーボードに設定されました。",
        "msg_net_fixed": "ネットワーク設定スクリプトを実行しました。",
    },
    "zh": {
        "title": "Waydroid 设置管理器",
        "lang_label": "语言设置:",
        "tab_display": "显示与窗口",
        "tab_input": "键盘与输入",
        "tab_storage": "存储与共享",
        "tab_network": "网络与工具",
        "window_presets": "窗口尺寸预设:",
        "preset_phone": "手机模式 (600 x 1024)",
        "preset_tablet_p": "平板竖屏 (800 x 1200)",
        "preset_tablet_l": "平板横屏 (1200 x 800)",
        "preset_fullscreen": "全屏模式",
        "preset_custom": "自定义分辨率",
        "width_label": "宽度 (px):",
        "height_label": "高度 (px):",
        "dpi_label": "DPI 密度:",
        "gboard_section": "Gboard (谷歌输入法) 设置:",
        "gboard_desc": "Gboard支持多语言输入和实体键盘切换。",
        "btn_enable_gboard": "将Gboard设为默认输入法",
        "btn_open_ime_settings": "打开Android输入法设置",
        "shortcut_tip": "提示: 在实体键盘上按 [Shift + Space] 切换输入语言。",
        "storage_section": "文件夹共享设置:",
        "storage_desc": "将主机电脑文件夹与 Android (/sdcard/Download) 共享。",
        "share_downloads_label": "启用主机与Android文件夹共享",
        "shared_folder_label": "共享的主机文件夹路径:",
        "btn_browse": "浏览...",
        "btn_open_downloads": "打开所选文件夹",
        "network_section": "网络与维护:",
        "btn_fix_network": "修复UFW防火墙与网络",
        "btn_install_apk": "安装APK文件...",
        "btn_stop_session": "停止 Waydroid",
        "btn_launch": "启动 Waydroid",
        "status_running": "状态: 运行中",
        "status_stopped": "状态: 已停止",
        "msg_saved": "设置已成功保存。",
        "msg_apk_success": "APK 安装成功！",
        "msg_apk_fail": "APK 安装失败。",
        "msg_gboard_done": "已将 Gboard 设置为默认输入法。",
        "msg_net_fixed": "网络修复脚本已执行。",
    },
    "es": {
        "title": "Administrador de Waydroid",
        "lang_label": "Idioma:",
        "tab_display": "Pantalla y Ventana",
        "tab_input": "Teclado y Entrada",
        "tab_storage": "Almacenamiento",
        "tab_network": "Red y Herramientas",
        "window_presets": "Tamaño de Ventana:",
        "preset_phone": "Modo Movil (600 x 1024)",
        "preset_tablet_p": "Modo Tableta Vertical (800 x 1200)",
        "preset_tablet_l": "Modo Tableta Horizontal (1200 x 800)",
        "preset_fullscreen": "Pantalla Completa",
        "preset_custom": "Resolucion Personalizada",
        "width_label": "Ancho (px):",
        "height_label": "Alto (px):",
        "dpi_label": "Densidad DPI:",
        "gboard_section": "Configuracion de Gboard:",
        "gboard_desc": "Gboard admite escritura multilingue y cambio de idioma en teclado fisico.",
        "btn_enable_gboard": "Establecer Gboard por Defecto",
        "btn_open_ime_settings": "Abrir Ajustes de Teclado Android",
        "shortcut_tip": "Consejo: Usa [Shift + Space] para cambiar de idioma en teclado fisico.",
        "storage_section": "Opciones de Compartir:",
        "storage_desc": "Comparte una carpeta del host con Android (/sdcard/Download).",
        "share_downloads_label": "Habilitar carpeta compartida Host-Android",
        "shared_folder_label": "Carpeta del host a compartir:",
        "btn_browse": "Examinar...",
        "btn_open_downloads": "Abrir Carpeta Seleccionada",
        "network_section": "Red y Mantenimiento:",
        "btn_fix_network": "Reparar Cortafuegos UFW",
        "btn_install_apk": "Instalar archivo APK...",
        "btn_stop_session": "Detener Waydroid",
        "btn_launch": "Iniciar Waydroid",
        "status_running": "Estado: En ejecucion",
        "status_stopped": "Estado: Detenido",
        "msg_saved": "Ajustes guardados correctamente.",
        "msg_apk_success": "APK instalado con exito!",
        "msg_apk_fail": "Error al instalar APK.",
        "msg_gboard_done": "Gboard configurado como teclado predeterminado.",
        "msg_net_fixed": "Script de red ejecutado.",
    },
    "de": {
        "title": "Waydroid Einstellungen",
        "lang_label": "Sprache:",
        "tab_display": "Anzeige & Fenster",
        "tab_input": "Tastatur & Eingabe",
        "tab_storage": "Speicher & Freigabe",
        "tab_network": "Netzwerk & Tools",
        "window_presets": "Fenstergroessen-Voreinstellungen:",
        "preset_phone": "Smartphone-Modus (600 x 1024)",
        "preset_tablet_p": "Tablet Hochformat (800 x 1200)",
        "preset_tablet_l": "Tablet Querformat (1200 x 800)",
        "preset_fullscreen": "Vollbildmodus",
        "preset_custom": "Benutzerdefinierte Aufloesung",
        "width_label": "Breite (px):",
        "height_label": "Hoehe (px):",
        "dpi_label": "DPI-Dichte:",
        "gboard_section": "Gboard (Google-Tastatur) Einstellungen:",
        "gboard_desc": "Gboard unterstuetzt mehrsprachige Eingabe und Tastaturwechsel.",
        "btn_enable_gboard": "Gboard als Standard festlegen",
        "btn_open_ime_settings": "Android-Tastatureinstellungen oeffnen",
        "shortcut_tip": "Tipp: Mit [Umschalt + Leertaste] zwischen Sprachen wechseln.",
        "storage_section": "Ordnerfreigabe-Optionen:",
        "storage_desc": "Host-Ordner fuer Android (/sdcard/Download) freigeben.",
        "share_downloads_label": "Host-Android Ordnerfreigabe aktivieren",
        "shared_folder_label": "Freizugebender Host-Ordner:",
        "btn_browse": "Durchsuchen...",
        "btn_open_downloads": "Ausgewaehlten Ordner oeffnen",
        "network_section": "Netzwerk & Wartung:",
        "btn_fix_network": "UFW-Firewall & Netzwerk reparieren",
        "btn_install_apk": "APK-Datei installieren...",
        "btn_stop_session": "Waydroid stoppen",
        "btn_launch": "Waydroid starten",
        "status_running": "Status: Laeuft",
        "status_stopped": "Status: Gestoppt",
        "msg_saved": "Einstellungen erfolgreich gespeichert.",
        "msg_apk_success": "APK erfolgreich installiert!",
        "msg_apk_fail": "Installation der APK fehlgeschlagen.",
        "msg_gboard_done": "Gboard als Standardtastatur aktiviert.",
        "msg_net_fixed": "Netzwerk-Skript ausgefuehrt.",
    },
    "fr": {
        "title": "Gestionnaire Waydroid",
        "lang_label": "Langue :",
        "tab_display": "Affichage & Fenetre",
        "tab_input": "Clavier & Saisie",
        "tab_storage": "Stockage & Partage",
        "tab_network": "Reseau & Outils",
        "window_presets": "Prereglages de Taille :",
        "preset_phone": "Mode Telephone (600 x 1024)",
        "preset_tablet_p": "Mode Tablette Portrait (800 x 1200)",
        "preset_tablet_l": "Mode Tablette Paysage (1200 x 800)",
        "preset_fullscreen": "Mode Plein ecran",
        "preset_custom": "Resolution Personnalisee",
        "width_label": "Largeur (px) :",
        "height_label": "Hauteur (px) :",
        "dpi_label": "Densite DPI :",
        "gboard_section": "Parametres Gboard :",
        "gboard_desc": "Gboard prend en charge la saisie multilingue et le clavier physique.",
        "btn_enable_gboard": "Definir Gboard par defaut",
        "btn_open_ime_settings": "Ouvrir parametres clavier Android",
        "shortcut_tip": "Astuce : Utilisez [Shift + Espace] pour changer de langue.",
        "storage_section": "Options de Partage de Dossier :",
        "storage_desc": "Partager un dossier hote avec Android (/sdcard/Download).",
        "share_downloads_label": "Activer le partage de dossier Hote-Android",
        "shared_folder_label": "Dossier hote a partager :",
        "btn_browse": "Parcourir...",
        "btn_open_downloads": "Ouvrir le dossier selectionne",
        "network_section": "Reseau & Maintenance :",
        "btn_fix_network": "Reparer pare-feu UFW",
        "btn_install_apk": "Installer un fichier APK...",
        "btn_stop_session": "Arreter Waydroid",
        "btn_launch": "Lancer Waydroid",
        "status_running": "Statut : En cours",
        "status_stopped": "Statut : Arrete",
        "msg_saved": "Parametres enregistres avec succes.",
        "msg_apk_success": "APK installee avec succes !",
        "msg_apk_fail": "Echec de l'installation de l'APK.",
        "msg_gboard_done": "Gboard configure comme clavier par defaut.",
        "msg_net_fixed": "Script reseau execute.",
    },
    "it": {
        "title": "Gestore Impostazioni Waydroid",
        "lang_label": "Lingua:",
        "tab_display": "Schermo e Finestra",
        "tab_input": "Tastiera e Input",
        "tab_storage": "Archiviazione",
        "tab_network": "Rete e Strumenti",
        "window_presets": "Dimensioni Finestra:",
        "preset_phone": "Modo Telefono (600 x 1024)",
        "preset_tablet_p": "Modo Tablet Verticale (800 x 1200)",
        "preset_tablet_l": "Modo Tablet Orizzontale (1200 x 800)",
        "preset_fullscreen": "Schermo Intero",
        "preset_custom": "Risoluzione Personalizzata",
        "width_label": "Larghezza (px):",
        "height_label": "Altezza (px):",
        "dpi_label": "Densita DPI:",
        "gboard_section": "Impostazioni Gboard:",
        "gboard_desc": "Gboard supporta la digitazione multilingue e la tastiera fisica.",
        "btn_enable_gboard": "Imposta Gboard come Predefinito",
        "btn_open_ime_settings": "Apri Impostazioni Tastiera Android",
        "shortcut_tip": "Suggerimento: Usa [Shift + Spazio] per cambiare lingua sulla tastiera fisica.",
        "storage_section": "Opzioni di Condivisione Cartelle:",
        "storage_desc": "Condividi una cartella host con Android (/sdcard/Download).",
        "share_downloads_label": "Abilita condivisione cartella Host-Android",
        "shared_folder_label": "Cartella host da condividere:",
        "btn_browse": "Sfoglia...",
        "btn_open_downloads": "Apri Cartella Selezionata",
        "network_section": "Rete e Manutenzione:",
        "btn_fix_network": "Ripara Firewall UFW & Rete",
        "btn_install_apk": "Installa file APK...",
        "btn_stop_session": "Ferma Waydroid",
        "btn_launch": "Avvia Waydroid",
        "status_running": "Stato: In esecuzione",
        "status_stopped": "Stato: Arrestato",
        "msg_saved": "Impostazioni salvate con successo.",
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
        self.geometry("640x580")
        self.minsize(580, 520)
        
        # Configure Fonts (Prioritize Google Noto Sans / Ubuntu TrueType fonts)
        self.configure_system_fonts()
        
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
            
        self.configure_styles()
        self.create_widgets()
        self.update_language(self.current_lang)

    def configure_system_fonts(self):
        available_fonts = tkfont.families()
        chosen_font = "DejaVu Sans"
        for candidate in ["Noto Sans CJK KR", "Noto Sans", "Ubuntu", "DejaVu Sans", "Sans"]:
            if candidate in available_fonts:
                chosen_font = candidate
                break

        self.base_font = (chosen_font, 10)
        self.bold_font = (chosen_font, 10, "bold")
        self.title_font = (chosen_font, 11, "bold")
        self.italic_font = (chosen_font, 9, "italic")

        # Configure default Tk fonts
        for name in ["TkDefaultFont", "TkTextFont", "TkMenuFont"]:
            try:
                tkfont.nametofont(name).configure(family=chosen_font, size=10)
            except Exception:
                pass
        try:
            tkfont.nametofont("TkHeadingFont").configure(family=chosen_font, size=11, weight="bold")
        except Exception:
            pass

    def configure_styles(self):
        self.style.configure(".", font=self.base_font)
        self.style.configure("TLabel", font=self.base_font)
        self.style.configure("TButton", font=self.base_font, padding=4)
        self.style.configure("TRadiobutton", font=self.base_font)
        self.style.configure("TCheckbutton", font=self.base_font)
        self.style.configure("TNotebook.Tab", font=self.base_font, padding=(10, 4))
        self.style.configure("Accent.TButton", font=self.bold_font, foreground="#ffffff", background="#1a73e8")

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
        
        self.lbl_lang = ttk.Label(top_frame, text=self.tr("lang_label"), font=self.bold_font)
        self.lbl_lang.pack(side="left", padx=(0, 8))
        
        self.combo_lang = ttk.Combobox(top_frame, state="readonly", width=22, font=self.base_font)
        self.combo_lang["values"] = [name for _, name in LANGUAGE_NAMES]
        current_idx = [code for code, _ in LANGUAGE_NAMES].index(self.current_lang) if self.current_lang in [code for code, _ in LANGUAGE_NAMES] else 0
        self.combo_lang.current(current_idx)
        self.combo_lang.bind("<<ComboboxSelected>>", self.on_language_change)
        self.combo_lang.pack(side="left")
        
        self.lbl_status = ttk.Label(top_frame, text="", font=self.italic_font)
        self.lbl_status.pack(side="right", padx=6)
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
        self.lbl_presets = ttk.Label(self.tab_display, text=self.tr("window_presets"), font=self.bold_font)
        self.lbl_presets.pack(anchor="w", pady=(0, 8))
        
        self.mode_var = tk.StringVar(value=self.config_data.get("mode", "tablet_portrait"))
        
        self.rb_phone = ttk.Radiobutton(self.tab_display, text=self.tr("preset_phone"), value="phone", variable=self.mode_var, command=self.on_mode_change)
        self.rb_phone.pack(anchor="w", pady=3)
        
        self.rb_tablet_p = ttk.Radiobutton(self.tab_display, text=self.tr("preset_tablet_p"), value="tablet_portrait", variable=self.mode_var, command=self.on_mode_change)
        self.rb_tablet_p.pack(anchor="w", pady=3)
        
        self.rb_tablet_l = ttk.Radiobutton(self.tab_display, text=self.tr("preset_tablet_l"), value="tablet_landscape", variable=self.mode_var, command=self.on_mode_change)
        self.rb_tablet_l.pack(anchor="w", pady=3)
        
        self.rb_full = ttk.Radiobutton(self.tab_display, text=self.tr("preset_fullscreen"), value="fullscreen", variable=self.mode_var, command=self.on_mode_change)
        self.rb_full.pack(anchor="w", pady=3)
        
        self.rb_custom = ttk.Radiobutton(self.tab_display, text=self.tr("preset_custom"), value="custom", variable=self.mode_var, command=self.on_mode_change)
        self.rb_custom.pack(anchor="w", pady=3)
        
        # Custom Resolution inputs
        self.custom_frame = ttk.LabelFrame(self.tab_display, text="Custom Size", padding=10)
        self.custom_frame.pack(fill="x", pady=12)
        
        self.lbl_w = ttk.Label(self.custom_frame, text=self.tr("width_label"))
        self.lbl_w.grid(row=0, column=0, padx=5, pady=4, sticky="w")
        self.ent_w = ttk.Entry(self.custom_frame, width=8, font=self.base_font)
        self.ent_w.insert(0, str(self.config_data.get("custom_width", 1080)))
        self.ent_w.grid(row=0, column=1, padx=5, pady=4)
        
        self.lbl_h = ttk.Label(self.custom_frame, text=self.tr("height_label"))
        self.lbl_h.grid(row=0, column=2, padx=5, pady=4, sticky="w")
        self.ent_h = ttk.Entry(self.custom_frame, width=8, font=self.base_font)
        self.ent_h.insert(0, str(self.config_data.get("custom_height", 1920)))
        self.ent_h.grid(row=0, column=3, padx=5, pady=4)
        
        self.lbl_dpi = ttk.Label(self.custom_frame, text=self.tr("dpi_label"))
        self.lbl_dpi.grid(row=0, column=4, padx=5, pady=4, sticky="w")
        self.ent_dpi = ttk.Entry(self.custom_frame, width=6, font=self.base_font)
        self.ent_dpi.insert(0, str(self.config_data.get("dpi", 280)))
        self.ent_dpi.grid(row=0, column=5, padx=5, pady=4)

    def setup_input_tab(self):
        self.lbl_gboard_sec = ttk.Label(self.tab_input, text=self.tr("gboard_section"), font=self.bold_font)
        self.lbl_gboard_sec.pack(anchor="w", pady=(0, 6))
        
        self.lbl_gboard_desc = ttk.Label(self.tab_input, text=self.tr("gboard_desc"), wraplength=560)
        self.lbl_gboard_desc.pack(anchor="w", pady=(0, 12))
        
        self.btn_gboard = ttk.Button(self.tab_input, text=self.tr("btn_enable_gboard"), command=self.enable_gboard)
        self.btn_gboard.pack(anchor="w", pady=4)
        
        self.btn_ime_settings = ttk.Button(self.tab_input, text=self.tr("btn_open_ime_settings"), command=self.open_ime_settings)
        self.btn_ime_settings.pack(anchor="w", pady=4)
        
        self.lbl_tip = ttk.Label(self.tab_input, text=self.tr("shortcut_tip"), foreground="#1a73e8", wraplength=560, font=self.italic_font)
        self.lbl_tip.pack(anchor="w", pady=(16, 0))

    def setup_storage_tab(self):
        self.lbl_storage_sec = ttk.Label(self.tab_storage, text=self.tr("storage_section"), font=self.bold_font)
        self.lbl_storage_sec.pack(anchor="w", pady=(0, 4))
        
        self.lbl_storage_desc = ttk.Label(self.tab_storage, text=self.tr("storage_desc"), wraplength=560)
        self.lbl_storage_desc.pack(anchor="w", pady=(0, 10))
        
        self.share_var = tk.BooleanVar(value=self.config_data.get("share_downloads", True))
        self.cb_share = ttk.Checkbutton(
            self.tab_storage,
            text=self.tr("share_downloads_label"),
            variable=self.share_var,
            command=self.on_share_toggle
        )
        self.cb_share.pack(anchor="w", pady=6)
        
        # Folder Path Selector Frame
        self.folder_frame = ttk.LabelFrame(self.tab_storage, text="Shared Folder Location", padding=10)
        self.folder_frame.pack(fill="x", pady=8)
        
        self.lbl_folder_path = ttk.Label(self.folder_frame, text=self.tr("shared_folder_label"))
        self.lbl_folder_path.pack(anchor="w", pady=(0, 4))
        
        path_row = ttk.Frame(self.folder_frame)
        path_row.pack(fill="x", pady=2)
        
        self.ent_folder = ttk.Entry(path_row, font=self.base_font)
        current_path = self.config_data.get("shared_folder_path", os.path.expanduser("~/Downloads"))
        self.ent_folder.insert(0, current_path)
        self.ent_folder.pack(side="left", fill="x", expand=True, padx=(0, 6))
        
        self.btn_browse = ttk.Button(path_row, text=self.tr("btn_browse"), command=self.browse_folder)
        self.btn_browse.pack(side="right")
        
        self.btn_open_dl = ttk.Button(self.tab_storage, text=self.tr("btn_open_downloads"), command=self.open_downloads)
        self.btn_open_dl.pack(anchor="w", pady=10)

    def setup_network_tab(self):
        self.lbl_net_sec = ttk.Label(self.tab_network, text=self.tr("network_section"), font=self.bold_font)
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
        self.lbl_storage_desc.config(text=self.tr("storage_desc"))
        self.cb_share.config(text=self.tr("share_downloads_label"))
        self.lbl_folder_path.config(text=self.tr("shared_folder_label"))
        self.btn_browse.config(text=self.tr("btn_browse"))
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

    def on_share_toggle(self):
        self.config_data["share_downloads"] = self.share_var.get()
        self.config_data["shared_folder_path"] = self.ent_folder.get().strip()
        self.save_config()

    def browse_folder(self):
        folder = filedialog.askdirectory(title="Select Folder to Share with Android")
        if folder:
            self.ent_folder.delete(0, tk.END)
            self.ent_folder.insert(0, folder)
            self.config_data["shared_folder_path"] = folder
            self.save_config()

    def check_status(self):
        try:
            out = subprocess.check_output(["waydroid", "status"], text=True, stderr=subprocess.DEVNULL)
            if "Session:\tRUNNING" in out or "Session: RUNNING" in out:
                self.lbl_status.config(text=self.tr("status_running"), foreground="#2e7d32")
            else:
                self.lbl_status.config(text=self.tr("status_stopped"), foreground="#757575")
        except Exception:
            self.lbl_status.config(text=self.tr("status_stopped"), foreground="#757575")

    def enable_gboard(self):
        try:
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
        target_path = self.ent_folder.get().strip() or os.path.expanduser("~/Downloads")
        if os.path.exists(target_path):
            subprocess.Popen(["xdg-open", target_path])

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
        self.on_share_toggle()
        runner = os.path.join(SCRIPT_DIR, "run_waydroid.sh")
        subprocess.Popen([runner])
        self.after(3000, self.check_status)

if __name__ == "__main__":
    app = WaydroidManagerApp()
    app.mainloop()
