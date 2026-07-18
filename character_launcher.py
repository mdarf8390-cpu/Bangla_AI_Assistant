"""
Bangla AI Assistant - Character Launcher
শুধুমাত্র Floating Character - Background এ সব চলবে
Features:
- Double-click to hide/show
- Voice activation
- Auto-start background AI
"""

import customtkinter as ctk
import threading
import time
import logging
from PIL import Image, ImageDraw
import io

# লগিং কনফিগারেশন
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from ui.floating_avatar import FloatingCharacterWindow, Emotion
    FLOATING_AVATAR_AVAILABLE = True
except ImportError:
    FLOATING_AVATAR_AVAILABLE = False
    logger.warning("Floating avatar module not available")

try:
    from ai.character_memory import get_memory
    CHARACTER_MEMORY_AVAILABLE = True
except ImportError:
    CHARACTER_MEMORY_AVAILABLE = False
    logger.warning("Character memory module not available")


class CharacterLauncher:
    """শুধুমাত্র Floating Character লঞ্চার"""
    
    def __init__(self):
        self.avatar_window = None
        self.is_active = True
        self.char_memory = None
        self.background_ai_running = False
        
        # Character Memory initialize
        if CHARACTER_MEMORY_AVAILABLE:
            try:
                self.char_memory = get_memory()
                logger.info("Character memory initialized")
            except Exception as e:
                logger.error(f"Failed to initialize character memory: {e}")
    
    def create_simple_avatar(self):
        """সাধারণ avatar তৈরি করুন (যদি module না থাকে)"""
        try:
            # একটি সাধারণ colored window তৈরি করুন
            root = ctk.CTkToplevel()
            root.title("🎨 Ayesha")
            root.geometry("200x200")
            root.config(bg="#2E2E2E")
            
            # Character emoji/text
            label = ctk.CTkLabel(
                root,
                text="🎨\nAyesha\nAI Assistant",
                font=("Arial", 24, "bold"),
                text_color="cyan"
            )
            label.pack(expand=True)
            
            return root
        except:
            return None
    
    def start_background_ai(self):
        """Background এ AI চালু করুন"""
        if self.background_ai_running:
            return
        
        self.background_ai_running = True
        logger.info("🚀 Background AI শুরু হয়েছে")
        
        try:
            # Background thread এ main.py চালান
            import subprocess
            import sys
            subprocess.Popen(
                [sys.executable, "main.py"],
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
        except Exception as e:
            logger.error(f"Background AI start error: {e}")
    
    def toggle_character_visibility(self):
        """Character visibility টগল করুন"""
        if self.avatar_window:
            if self.is_active:
                logger.info("👻 Character লুকাচ্ছি...")
                self.avatar_window.hide()
                self.is_active = False
            else:
                logger.info("👤 Character দেখাচ্ছি...")
                self.avatar_window.show()
                self.is_active = True
    
    def double_click_handler(self):
        """Double-click handler"""
        self.toggle_character_visibility()
    
    def launch(self):
        """Character লঞ্চ করুন"""
        logger.info("=" * 60)
        logger.info("🎨 Bangla AI Assistant - Character Launcher")
        logger.info("=" * 60)
        
        # Floating Avatar শুরু করুন
        if FLOATING_AVATAR_AVAILABLE:
            try:
                logger.info("🎨 Floating Avatar লঞ্চ করছি...")
                self.avatar_window = FloatingCharacterWindow()
                
                # Double-click listener সেট করুন
                if hasattr(self.avatar_window, 'set_double_click_callback'):
                    self.avatar_window.set_double_click_callback(self.double_click_handler)
                
                # Avatar show করুন
                avatar_thread = threading.Thread(
                    target=self.avatar_window.show,
                    daemon=True
                )
                avatar_thread.start()
                
                logger.info("✅ Avatar সফলভাবে লঞ্চ হয়েছে!")
            except Exception as e:
                logger.error(f"Avatar launch error: {e}")
                logger.info("⚠️ Simple avatar দেখাচ্ছি...")
                self.avatar_window = self.create_simple_avatar()
        else:
            logger.warning("⚠️ Floating avatar module not available")
            logger.info("📦 Simple avatar ব্যবহার করছি...")
            self.avatar_window = self.create_simple_avatar()
        
        # Background AI শুরু করুন (অপশনাল)
        logger.info("\n🔧 Background services শুরু করছি...")
        ai_thread = threading.Thread(
            target=self.start_background_ai,
            daemon=True
        )
        ai_thread.start()
        
        logger.info("\n✅ সবকিছু প্রস্তুত!")
        logger.info("💡 Hints:")
        logger.info("  • চরিত্রে double-click করুন হিডেন/দেখানোর জন্য")
        logger.info("  • 'ayesha' বা 'hey' বলুন কথা শুরু করতে")
        logger.info("  • ESC চাপুন বন্ধ করতে")
        logger.info("\n" + "=" * 60 + "\n")
        
        # Keep running
        self._monitor_loop()
    
    def _monitor_loop(self):
        """Monitor loop - character status চেক করুন"""
        try:
            while True:
                time.sleep(1)
                
                # Character memory status আপডেট করুন
                if self.char_memory and self.char_memory.is_active:
                    user = self.char_memory.active_user
                    logger.debug(f"👤 Active user: {user}")
                
        except KeyboardInterrupt:
            logger.info("\n👋 ধন্যবাদ! বিদায়...")
            self.cleanup()
    
    def cleanup(self):
        """সম্পদ পরিষ্কার করুন"""
        logger.info("🧹 পরিষ্কার করছি...")
        
        if self.avatar_window:
            try:
                if hasattr(self.avatar_window, '_on_closing'):
                    self.avatar_window._on_closing()
            except:
                pass
        
        logger.info("✅ Exit করা হয়েছে")


def start_floating_character():
    """Character লঞ্চার শুরু করুন"""
    launcher = CharacterLauncher()
    launcher.launch()


def main():
    """Main entry point"""
    try:
        start_floating_character()
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    main()
