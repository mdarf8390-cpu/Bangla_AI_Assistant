"""
Bangla AI Assistant - Smart Launcher with Auto-Installer
EXE খুলবে → Dependencies auto-install → Floating Character শুরু হবে
Author: Arafat (daddypopaa)
"""

import os
import sys
import subprocess
import json
import threading
import time
from pathlib import Path

class DependencyInstaller:
    """সব dependencies auto-install করার ক্লাস"""
    
    def __init__(self):
        self.requirements = [
            'customtkinter',
            'ollama',
            'pyttsx3',
            'SpeechRecognition',
            'pyaudio',
            'opencv-python',
            'pillow',
            'pygame',
            'pyautogui',
            'keyboard',
            'mouse',
            'psutil',
            'python-dotenv',
            'rapidfuzz',
            'edge-tts',
            'requests'
        ]
        self.installed = set()
        self.failed = set()
    
    def check_package(self, package):
        """প্যাকেজ installed আছে কিনা চেক করুন"""
        try:
            __import__(package.replace('-', '_'))
            return True
        except ImportError:
            return False
    
    def install_requirements(self, progress_callback=None):
        """সব requirements install করুন"""
        print("🔧 Dependencies ইনস্টল করছি...")
        
        # Upgrade pip first
        print("📦 pip আপগ্রেড করছি...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"])
        except:
            pass
        
        for i, package in enumerate(self.requirements):
            if self.check_package(package):
                self.installed.add(package)
                status = f"✅ {package} - ইতিমধ্যে installed"
            else:
                print(f"📥 {package} ইনস্টল করছি...")
                try:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package, "-q"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )
                    self.installed.add(package)
                    status = f"✅ {package} - ইনস্টল হয়েছে"
                except Exception as e:
                    self.failed.add(package)
                    status = f"⚠️ {package} - ইনস্টল ব্যর্থ"
            
            print(status)
            progress = int((i + 1) / len(self.requirements) * 100)
            
            if progress_callback:
                progress_callback(progress, status)
        
        return len(self.failed) == 0
    
    def get_status(self):
        """ইনস্টলেশন স্ট্যাটাস পান"""
        return {
            'installed': len(self.installed),
            'failed': len(self.failed),
            'total': len(self.requirements),
            'success': len(self.failed) == 0
        }


class SmartLauncher:
    """স্মার্ট লঞ্চার - Auto-install এবং Character শুরু করে"""
    
    def __init__(self):
        self.config_file = "launcher_config.json"
        self.config = self.load_config()
        self.installer = DependencyInstaller()
        self.app_running = False
    
    def load_config(self):
        """কনফিগারেশন লোড করুন"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'first_run': True,
            'installation_done': False,
            'character_enabled': True,
            'auto_start': True
        }
    
    def save_config(self):
        """কনফিগারেশন সেভ করুন"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=4)
        except:
            pass
    
    def check_dependencies(self):
        """সব dependencies check করুন"""
        print("🔍 Dependencies চেক করছি...")
        all_ok = True
        
        for package in self.installer.requirements:
            if not self.installer.check_package(package):
                print(f"❌ {package} - Missing")
                all_ok = False
            else:
                print(f"✅ {package} - OK")
        
        return all_ok
    
    def auto_install_if_needed(self):
        """প্রয়োজন হলে dependencies install করুন"""
        if not self.check_dependencies():
            print("\n⚠️ কিছু packages missing আছে। Auto-installing...")
            print("=" * 60)
            
            success = self.installer.install_requirements()
            
            print("=" * 60)
            if success:
                print("✅ সব dependencies সফলভাবে ইনস্টল হয়েছে!")
                self.config['installation_done'] = True
                self.save_config()
            else:
                print("❌ কিছু packages ইনস্টল ব্যর্থ হয়েছে")
                print("ম্যানুয়ালি ইনস্টল করুন: pip install -r requirements.txt")
                return False
        
        return True
    
    def launch_character_only(self):
        """শুধু Floating Character লঞ্চ করুন"""
        print("\n🎨 Floating Character লঞ্চ করছি...")
        
        try:
            # Floating character script চালান
            from character_launcher import start_floating_character
            start_floating_character()
        except ImportError:
            print("⚠️ Character module found নেই। main.py চালাচ্ছি...")
            try:
                subprocess.Popen([sys.executable, "main.py"])
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def launch_app(self):
        """সম্পূর্ণ অ্যাপ্লিকেশন লঞ্চ করুন"""
        print("🚀 Application লঞ্চ করছি...")
        
        try:
            if os.path.exists("main.py"):
                subprocess.Popen([sys.executable, "main.py"])
            elif os.path.exists("ayesha_pipraa_app.py"):
                subprocess.Popen([sys.executable, "ayesha_pipraa_app.py"])
            else:
                print("❌ main.py বা ayesha_pipraa_app.py খুঁজে পাওয়া যায়নি")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def run(self):
        """লঞ্চার শুরু করুন"""
        print("=" * 60)
        print("🎨 Bangla AI Assistant - Smart Launcher")
        print("=" * 60)
        print()
        
        # Step 1: Auto-install dependencies
        if not self.auto_install_if_needed():
            print("❌ Installation failed. Please install manually.")
            return False
        
        print()
        print("✅ All systems ready!")
        print()
        
        # Step 2: Launch character
        if self.config.get('auto_start', True):
            self.launch_character_only()
        
        self.app_running = True
        return True


def main():
    """Main entry point"""
    try:
        launcher = SmartLauncher()
        launcher.run()
        
        # Keep running
        while launcher.app_running:
            time.sleep(1)
    
    except Exception as e:
        print(f"❌ Launcher Error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
