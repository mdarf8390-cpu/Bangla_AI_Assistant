"""
Ayesha-Pipraa Desktop Application
Main Application with 3D Character, Control Panel, and Full Features
Author: Arafat (Pipraa)
"""

import customtkinter as ctk
import threading
import asyncio
import time
import os
import logging
import json
from datetime import datetime
from edge_tts import Communicate
import psutil

# প্রয়োজনীয় মডিউলসমূহ
try:
    from ai.reasoning_engine import reasoning_engine
    from automation.action_executor import action_executor
    from core.memory_manager import memory
except ImportError as e:
    logging.warning(f"Could not import core modules: {e}")

# Avatar modules
try:
    from ui.floating_avatar import FloatingCharacterWindow, Emotion
    FLOATING_AVATAR_AVAILABLE = True
except ImportError:
    FLOATING_AVATAR_AVAILABLE = False
    logging.warning("Floating avatar module not available")

# Character Memory
try:
    from ai.character_memory import get_memory, Emotion as CharacterEmotion
    CHARACTER_MEMORY_AVAILABLE = True
except ImportError:
    CHARACTER_MEMORY_AVAILABLE = False
    logging.warning("Character memory module not available")

# Feature Request System
try:
    from ai.feature_requests import get_feature_system
    FEATURE_SYSTEM_AVAILABLE = True
except ImportError:
    FEATURE_SYSTEM_AVAILABLE = False
    logging.warning("Feature request system not available")

# লগিং কনফিগারেশন
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ayesha_app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MediaDetector:
    """মিডিয়া প্লেয়ার এবং সাউন্ড ডিটেক্ট করার ক্লাস"""
    
    def __init__(self):
        self.is_playing = False
        self.current_media = None
        self.media_players = [
            'vlc.exe', 'wmplayer.exe', 'chrome.exe', 'firefox.exe',
            'spotify.exe', 'mpv.exe', 'mpc-hc.exe', 'potplayer.exe',
            'mpc-be.exe', 'foobar2000.exe', 'winamp.exe', 'davplayer.exe'
        ]
    
    def check_audio_output(self):
        """Windows এ অডিও আউটপুট ডিটেক্ট করা"""
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    if proc.info['name'].lower() in self.media_players:
                        return True
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return False
        except Exception as e:
            logger.error(f"Audio detection error: {str(e)}")
            return False
    
    def get_current_media_info(self):
        """বর্তমান মিডিয়া ইনফরমেশন পান"""
        try:
            for proc in psutil.process_iter(['name']):
                try:
                    process_name = proc.info['name'].lower()
                    if process_name in self.media_players:
                        return {
                            'player': process_name.replace('.exe', '').upper(),
                            'status': 'Playing',
                            'pid': proc.pid
                        }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            return None
        except Exception as e:
            logger.error(f"Media info error: {str(e)}")
            return None


class SettingsManager:
    """অ্যাপ্লিকেশন সেটিংস ম্যানেজ করা"""
    
    def __init__(self):
        self.settings_file = "ayesha_settings.json"
        self.default_settings = {
            "character_name": "Ayesha",
            "character_size": 200,
            "character_opacity": 0.8,
            "auto_start": False,
            "voice_enabled": True,
            "theme": "dark",
            "language": "bengali",
            "media_detection": True,
            "character_position": "bottom-right"
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """সেটিংস ফাইল লোড করা"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
        
        return self.default_settings.copy()
    
    def save_settings(self):
        """সেটিংস ফাইল সেভ করা"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            logger.info("Settings saved successfully")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        """সেটিং ভ্যালু পান"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """সেটিং ভ্যালু সেট করুন"""
        self.settings[key] = value
        self.save_settings()


class ControlPanelWindow:
    """কন্ট্রোল প্যানেল - সব সেটিংস এক জায়গায়"""
    
    def __init__(self, settings_manager, parent_app):
        self.settings = settings_manager
        self.parent_app = parent_app
        self.window = None
    
    def create_window(self):
        """কন্ট্রোল প্যানেল উইন্ডো তৈরি করা"""
        self.window = ctk.CTkToplevel()
        self.window.title("⚙️ Ayesha Control Panel")
        self.window.geometry("500x700")
        self.window.resizable(False, False)
        
        # ========== Character Settings ==========
        char_frame = ctk.CTkFrame(self.window)
        char_frame.pack(padx=15, pady=15, fill="both", expand=False)
        
        char_label = ctk.CTkLabel(
            char_frame,
            text="👤 Character Settings",
            font=("Arial", 14, "bold")
        )
        char_label.pack(pady=10)
        
        # Character Name
        ctk.CTkLabel(char_frame, text="Character Name:").pack(anchor="w", padx=10, pady=5)
        char_name_entry = ctk.CTkEntry(
            char_frame,
            placeholder_text="Enter character name"
        )
        char_name_entry.insert(0, self.settings.get("character_name"))
        char_name_entry.pack(fill="x", padx=10, pady=5)
        
        # Character Size
        ctk.CTkLabel(char_frame, text="Character Size:").pack(anchor="w", padx=10, pady=5)
        size_slider = ctk.CTkSlider(
            char_frame,
            from_=100,
            to=400,
            number_of_steps=30
        )
        size_slider.set(self.settings.get("character_size", 200))
        size_slider.pack(fill="x", padx=10, pady=5)
        size_label = ctk.CTkLabel(char_frame, text="200px")
        size_label.pack(anchor="w", padx=10)
        
        def update_size_label(value):
            size_label.configure(text=f"{int(value)}px")
        
        size_slider.configure(command=update_size_label)
        
        # Character Opacity
        ctk.CTkLabel(char_frame, text="Character Opacity:").pack(anchor="w", padx=10, pady=5)
        opacity_slider = ctk.CTkSlider(
            char_frame,
            from_=0.1,
            to=1.0,
            number_of_steps=9
        )
        opacity_slider.set(self.settings.get("character_opacity", 0.8))
        opacity_slider.pack(fill="x", padx=10, pady=5)
        opacity_label = ctk.CTkLabel(char_frame, text="80%")
        opacity_label.pack(anchor="w", padx=10)
        
        def update_opacity_label(value):
            opacity_label.configure(text=f"{int(value*100)}%")
        
        opacity_slider.configure(command=update_opacity_label)
        
        # ========== Feature Settings ==========
        feature_frame = ctk.CTkFrame(self.window)
        feature_frame.pack(padx=15, pady=15, fill="both", expand=False)
        
        feature_label = ctk.CTkLabel(
            feature_frame,
            text="🔧 Feature Settings",
            font=("Arial", 14, "bold")
        )
        feature_label.pack(pady=10)
        
        # Voice Toggle
        voice_var = ctk.BooleanVar(value=self.settings.get("voice_enabled", True))
        voice_check = ctk.CTkCheckBox(
            feature_frame,
            text="🔊 Enable Voice Output",
            variable=voice_var
        )
        voice_check.pack(anchor="w", padx=10, pady=5)
        
        # Media Detection Toggle
        media_var = ctk.BooleanVar(value=self.settings.get("media_detection", True))
        media_check = ctk.CTkCheckBox(
            feature_frame,
            text="🎵 Enable Media Detection",
            variable=media_var
        )
        media_check.pack(anchor="w", padx=10, pady=5)
        
        # Auto Start Toggle
        autostart_var = ctk.BooleanVar(value=self.settings.get("auto_start", False))
        autostart_check = ctk.CTkCheckBox(
            feature_frame,
            text="🚀 Auto Start on Boot",
            variable=autostart_var
        )
        autostart_check.pack(anchor="w", padx=10, pady=5)
        
        # ========== Theme Settings ==========
        theme_frame = ctk.CTkFrame(self.window)
        theme_frame.pack(padx=15, pady=15, fill="both", expand=False)
        
        theme_label = ctk.CTkLabel(
            theme_frame,
            text="🎨 Appearance",
            font=("Arial", 14, "bold")
        )
        theme_label.pack(pady=10)
        
        ctk.CTkLabel(theme_frame, text="Theme:").pack(anchor="w", padx=10, pady=5)
        theme_options = ["dark", "light"]
        theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=theme_options,
            command=lambda x: None
        )
        theme_menu.set(self.settings.get("theme", "dark"))
        theme_menu.pack(fill="x", padx=10, pady=5)
        
        # ========== Button Section ==========
        button_frame = ctk.CTkFrame(self.window)
        button_frame.pack(padx=15, pady=15, fill="x")
        
        def save_all_settings():
            self.settings.set("character_name", char_name_entry.get())
            self.settings.set("character_size", int(size_slider.get()))
            self.settings.set("character_opacity", opacity_slider.get())
            self.settings.set("voice_enabled", voice_var.get())
            self.settings.set("media_detection", media_var.get())
            self.settings.set("auto_start", autostart_var.get())
            self.settings.set("theme", theme_menu.get())
            
            # Success message
            logger.info("All settings saved!")
            ctk.CTkMessagebox.show_info("Success", "Settings saved successfully!")
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Settings",
            command=save_all_settings,
            fg_color="green"
        )
        save_btn.pack(fill="x", pady=5)
        
        reset_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Reset to Default",
            command=lambda: self.reset_to_default(),
            fg_color="orange"
        )
        reset_btn.pack(fill="x", pady=5)
        
        close_btn = ctk.CTkButton(
            button_frame,
            text="❌ Close",
            command=self.window.destroy,
            fg_color="red"
        )
        close_btn.pack(fill="x", pady=5)
    
    def reset_to_default(self):
        """ডিফল্ট সেটিংস এ ফিরে যান"""
        self.settings.settings = self.settings.default_settings.copy()
        self.settings.save_settings()
        ctk.CTkMessagebox.show_info("Reset", "Settings reset to default!")
        self.window.destroy()
    
    def show(self):
        """কন্ট্রোল প্যানেল দেখান"""
        self.create_window()


class AyeshaDesktopApp:
    """Ayesha-Pipraa ডেস্কটপ অ্যাপ্লিকেশন"""
    
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("🎨 Ayesha-Pipraa | Desktop Control Center")
        self.app.geometry("900x600")
        
        # Settings Manager
        self.settings = SettingsManager()
        
        # Media Detector
        self.media_detector = MediaDetector()
        self.media_was_playing = False
        
        # Character Memory
        self.char_memory = None
        if CHARACTER_MEMORY_AVAILABLE:
            try:
                self.char_memory = get_memory()
                logger.info("Character memory initialized")
            except Exception as e:
                logger.error(f"Failed to initialize character memory: {str(e)}")
        
        # Feature System
        self.feature_system = None
        if FEATURE_SYSTEM_AVAILABLE:
            try:
                self.feature_system = get_feature_system()
                logger.info("Feature request system initialized")
            except Exception as e:
                logger.error(f"Failed to initialize feature system: {str(e)}")
        
        # Floating Avatar
        self.avatar_window = None
        if FLOATING_AVATAR_AVAILABLE:
            try:
                self.avatar_window = FloatingCharacterWindow()
                logger.info("Floating avatar initialized")
                avatar_thread = threading.Thread(target=self.avatar_window.show, daemon=True)
                avatar_thread.start()
            except Exception as e:
                logger.error(f"Failed to initialize floating avatar: {str(e)}")
                self.avatar_window = None
        
        # UI Setup
        self.setup_ui()
        
        # Start Monitors
        threading.Thread(target=self._media_monitor, daemon=True).start()
        threading.Thread(target=self._info_update_loop, daemon=True).start()
    
    def setup_ui(self):
        """UI সেটআপ করা"""
        # ========== Header ==========
        header_frame = ctk.CTkFrame(self.app, fg_color=("#1a1a1a", "#ffffff"))
        header_frame.pack(fill="x", padx=0, pady=0)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="🎨 Ayesha-Pipraa Control Center",
            font=("Arial", 20, "bold"),
            text_color=("white", "black")
        )
        header_label.pack(pady=15)
        
        info_label = ctk.CTkLabel(
            header_frame,
            text="Arafat's AI Assistant | Desktop Edition",
            font=("Arial", 12),
            text_color=("gray", "darkgray")
        )
        info_label.pack(pady=5)
        
        # ========== Main Content ==========
        main_frame = ctk.CTkFrame(self.app)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left Panel - Status & Info
        left_panel = ctk.CTkFrame(main_frame)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        status_title = ctk.CTkLabel(
            left_panel,
            text="📊 Status & Information",
            font=("Arial", 14, "bold")
        )
        status_title.pack(pady=10)
        
        # Character Status
        self.char_status_label = ctk.CTkLabel(
            left_panel,
            text="👤 Character: Ayesha",
            font=("Arial", 12),
            text_color="green"
        )
        self.char_status_label.pack(anchor="w", pady=5)
        
        # Media Status
        self.media_status_label = ctk.CTkLabel(
            left_panel,
            text="🔇 No Media Playing",
            font=("Arial", 12),
            text_color="gray"
        )
        self.media_status_label.pack(anchor="w", pady=5)
        
        # User Status
        self.user_status_label = ctk.CTkLabel(
            left_panel,
            text="👤 Active User: None",
            font=("Arial", 12),
            text_color="orange"
        )
        self.user_status_label.pack(anchor="w", pady=5)
        
        # System Info
        system_frame = ctk.CTkFrame(left_panel)
        system_frame.pack(fill="x", pady=15)
        
        system_info = ctk.CTkLabel(
            system_frame,
            text=f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n🖥️ OS: Windows\n📦 Status: Running",
            font=("Arial", 10),
            text_color="gray",
            justify="left"
        )
        system_info.pack(anchor="w")
        
        # Right Panel - Controls
        right_panel = ctk.CTkFrame(main_frame)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        control_title = ctk.CTkLabel(
            right_panel,
            text="🎮 Quick Controls",
            font=("Arial", 14, "bold")
        )
        control_title.pack(pady=10)
        
        # Control Buttons
        settings_btn = ctk.CTkButton(
            right_panel,
            text="⚙️  Open Settings",
            font=("Arial", 12),
            height=40,
            command=self.open_settings,
            fg_color="blue"
        )
        settings_btn.pack(fill="x", pady=8)
        
        hide_char_btn = ctk.CTkButton(
            right_panel,
            text="👻 Hide Character",
            font=("Arial", 12),
            height=40,
            command=self.hide_character,
            fg_color="purple"
        )
        hide_char_btn.pack(fill="x", pady=8)
        
        show_char_btn = ctk.CTkButton(
            right_panel,
            text="👤 Show Character",
            font=("Arial", 12),
            height=40,
            command=self.show_character,
            fg_color="green"
        )
        show_char_btn.pack(fill="x", pady=8)
        
        chat_btn = ctk.CTkButton(
            right_panel,
            text="💬 Open Chat",
            font=("Arial", 12),
            height=40,
            command=self.open_chat,
            fg_color="orange"
        )
        chat_btn.pack(fill="x", pady=8)
        
        media_btn = ctk.CTkButton(
            right_panel,
            text="🎵 Media Status",
            font=("Arial", 12),
            height=40,
            command=self.check_media_status,
            fg_color="cyan"
        )
        media_btn.pack(fill="x", pady=8)
        
        exit_btn = ctk.CTkButton(
            right_panel,
            text="❌ Exit",
            font=("Arial", 12),
            height=40,
            command=self.exit_app,
            fg_color="red"
        )
        exit_btn.pack(fill="x", pady=8)
    
    def open_settings(self):
        """সেটিংস খুলুন"""
        panel = ControlPanelWindow(self.settings, self)
        panel.show()
    
    def hide_character(self):
        """চরিত্র লুকান"""
        if self.avatar_window:
            try:
                self.avatar_window.hide()
                logger.info("Character hidden")
            except Exception as e:
                logger.error(f"Error hiding character: {e}")
    
    def show_character(self):
        """চরিত্র দেখান"""
        if self.avatar_window:
            try:
                self.avatar_window.show()
                logger.info("Character shown")
            except Exception as e:
                logger.error(f"Error showing character: {e}")
    
    def open_chat(self):
        """চ্যাট উইন্ডো খুলুন"""
        logger.info("Chat window opened")
        ctk.CTkMessagebox.show_info("Chat", "Chat window will open soon!")
    
    def check_media_status(self):
        """মিডিয়া স্ট্যাটাস চেক করুন"""
        media_info = self.media_detector.get_current_media_info()
        if media_info:
            msg = f"🎵 {media_info['player']} is currently playing"
        else:
            msg = "🔇 No media is currently playing"
        
        ctk.CTkMessagebox.show_info("Media Status", msg)
    
    def exit_app(self):
        """অ্যাপ বন্ধ করুন"""
        if ctk.CTkMessagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.cleanup()
            self.app.destroy()
    
    def cleanup(self):
        """রিসোর্স পরিষ্কার করুন"""
        if self.avatar_window:
            try:
                self.avatar_window._on_closing()
            except Exception as e:
                logger.error(f"Error closing avatar: {e}")
    
    def _media_monitor(self):
        """মিডিয়া মনিটর করা"""
        while True:
            try:
                media_playing = self.media_detector.check_audio_output()
                if media_playing and not self.media_was_playing:
                    media_info = self.media_detector.get_current_media_info()
                    if media_info:
                        self.media_status_label.configure(
                            text=f"🎵 {media_info['player']} Playing",
                            text_color="orange"
                        )
                    self.media_was_playing = True
                elif not media_playing and self.media_was_playing:
                    self.media_status_label.configure(
                        text="🔇 No Media Playing",
                        text_color="gray"
                    )
                    self.media_was_playing = False
                
                time.sleep(2)
            except Exception as e:
                logger.error(f"Media monitor error: {e}")
                time.sleep(5)
    
    def _info_update_loop(self):
        """তথ্য আপডেট করা"""
        while True:
            try:
                if self.char_memory and self.char_memory.is_active:
                    user = self.char_memory.active_user
                    self.user_status_label.configure(
                        text=f"👤 Active User: {user}",
                        text_color="green"
                    )
                else:
                    self.user_status_label.configure(
                        text="👤 Active User: None",
                        text_color="orange"
                    )
                
                time.sleep(1)
            except Exception as e:
                logger.error(f"Info update error: {e}")
    
    def run(self):
        """অ্যাপ চালান"""
        try:
            self.app.protocol("WM_DELETE_WINDOW", self.exit_app)
            self.app.mainloop()
        except Exception as e:
            logger.error(f"Application error: {e}")


if __name__ == "__main__":
    try:
        app = AyeshaDesktopApp()
        app.run()
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        print(f"Error: {e}")
