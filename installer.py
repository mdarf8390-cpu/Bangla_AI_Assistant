"""
Bangla AI Assistant - Complete Installer/Uninstaller with Ollama & Qwen
সম্পূর্ণ installation এবং uninstallation ম্যানেজমেন্ট
Ollama এবং Qwen models সহ
Author: daddypopaa
"""

import os
import sys
import subprocess
import json
import shutil
import platform
import time
from pathlib import Path
from datetime import datetime

class BanglaAIInstaller:
    """সম্পূর্ণ Installer এবং Uninstaller with Ollama & Qwen"""
    
    def __init__(self):
        self.app_name = "Bangla AI Assistant"
        self.version = "1.0.0"
        self.config_file = "installer_config.json"
        self.install_log_file = "install.log"
        
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
        
        self.ollama_models = [
            'qwen:7b',
            'qwen:14b'
        ]
        
        self.config = self.load_config()
        self.log_messages = []
    
    def log(self, message):
        """লগ মেসেজ রেকর্ড করুন"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.log_messages.append(log_entry)
        print(message)
    
    def save_logs(self):
        """লগ ফাইল সেভ করুন"""
        try:
            with open(self.install_log_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(self.log_messages))
        except Exception as e:
            print(f"⚠️ Could not save logs: {e}")
    
    def load_config(self):
        """ইনস্টলেশন কনফিগারেশন লোড করুন"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        
        return {
            'installed': False,
            'installation_date': None,
            'installed_packages': [],
            'installed_models': [],
            'install_path': os.getcwd(),
            'version': self.version,
            'os': platform.system()
        }
    
    def save_config(self):
        """কনফিগারেশন সেভ করুন"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            self.log(f"⚠️ Could not save config: {e}")
    
    def check_python_version(self):
        """Python version চেক করুন"""
        if sys.version_info < (3, 7):
            self.log("❌ Python 3.7 বা তার উপরের সংস্করণ প্রয়োজন!")
            return False
        
        self.log(f"✅ Python {sys.version.split()[0]} - OK")
        return True
    
    def upgrade_pip(self):
        """pip আপগ্রেড করুন"""
        self.log("🔧 pip আপগ্রেড করছি...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.log("✅ pip আপগ্রেড করা হয়েছে")
            return True
        except Exception as e:
            self.log(f"⚠️ pip আপগ্রেড ব্যর্থ: {e}")
            return False
    
    def check_package(self, package):
        """প্যাকেজ installed আছে কিনা চেক করুন"""
        try:
            __import__(package.replace('-', '_'))
            return True
        except ImportError:
            return False
    
    def install_package(self, package):
        """একটি প্যাকেজ ইনস্টল করুন"""
        try:
            self.log(f"  📥 {package} ইনস্টল করছি...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package, "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.log(f"  ✅ {package} সফলভাবে ইনস্টল হয়েছে")
            return True
        except Exception as e:
            self.log(f"  ❌ {package} ইনস্টল ব্যর্থ: {e}")
            return False
    
    def uninstall_package(self, package):
        """একটি প্যাকেজ আনইনস্টল করুন"""
        try:
            self.log(f"  🗑️  {package} আনইনস্টল করছি...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "uninstall", package, "-y", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.log(f"  ✅ {package} আনইনস্টল করা হয়েছে")
            return True
        except Exception as e:
            self.log(f"  ⚠️ {package} আনইনস্টল ব্যর্থ: {e}")
            return False
    
    def check_ollama_installed(self):
        """Ollama installed আছে কিনা চেক করুন"""
        try:
            if sys.platform == 'win32':
                result = subprocess.run(['where', 'ollama'], capture_output=True)
            else:
                result = subprocess.run(['which', 'ollama'], capture_output=True)
            return result.returncode == 0
        except:
            return False
    
    def install_ollama(self):
        """Ollama ডাউনলোড এবং ইনস্টল করুন"""
        self.log("\n🤖 Ollama সেটআপ করছি...")
        
        if self.check_ollama_installed():
            self.log("✅ Ollama ইতিমধ্যে ইনস্টল করা আছে")
            return True
        
        self.log("⚠️ Ollama manually ডাউনলোড করুন:")
        self.log("📥 Download: https://ollama.ai/download")
        self.log("📌 বা চালান: pip install ollama")
        
        # Try pip install
        try:
            self.log("📥 pip থেকে ollama install করছি...")
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "ollama", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            self.log("✅ Ollama pip package install হয়েছে")
            return True
        except Exception as e:
            self.log(f"⚠️ Ollama pip install ব্যর্থ: {e}")
            return False
    
    def pull_ollama_model(self, model_name):
        """Ollama model ডাউনলোড করুন"""
        try:
            self.log(f"\n  🔽 {model_name} ডাউনলোড করছি...")
            self.log(f"  ⏳ এটি সময় নিবে (মডেল সাইজ: {model_name}:7b = ~4GB, 14b = ~8GB)")
            
            # ollama pull command চালান
            process = subprocess.Popen(
                ['ollama', 'pull', model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Output দেখান
            for line in process.stdout:
                if line.strip():
                    self.log(f"    {line.strip()}")
            
            process.wait()
            
            if process.returncode == 0:
                self.log(f"  ✅ {model_name} ডাউনলোড সম্পন্ন")
                return True
            else:
                self.log(f"  ❌ {model_name} ডাউনলোড ব্যর্থ")
                return False
        
        except FileNotFoundError:
            self.log(f"  ❌ ollama command খুঁজে পাওয়া যায়নি")
            self.log(f"  💡 পরে ম্যানুয়ালি চালান: ollama pull {model_name}")
            return False
        
        except Exception as e:
            self.log(f"  ❌ {model_name} pull error: {e}")
            return False
    
    def download_ollama_models(self):
        """সব Ollama মডেল ডাউনলোড করুন"""
        self.log("\n📦 Qwen মডেল ডাউনলোড করছি...")
        self.log("=" * 60)
        
        downloaded = []
        failed = []
        
        for i, model in enumerate(self.ollama_models, 1):
            self.log(f"\n[{i}/{len(self.ollama_models)}] {model}")
            
            if self.pull_ollama_model(model):
                downloaded.append(model)
            else:
                failed.append(model)
        
        self.config['installed_models'] = downloaded
        self.save_config()
        
        return len(failed) == 0
    
    def install_all(self):
        """সব প্যাকেজ এবং মডেল ইনস্টল করুন"""
        print("\n" + "=" * 60)
        print(f"🎨 {self.app_name} - INSTALLATION WITH OLLAMA & QWEN")
        print("=" * 60 + "\n")
        
        self.log(f"🚀 Installation শুরু হচ্ছে...")
        self.log(f"📍 Installation Path: {os.getcwd()}")
        
        # Step 1: Python version check
        if not self.check_python_version():
            self.log("❌ Installation বাতিল করা হয়েছে")
            self.save_logs()
            return False
        
        # Step 2: Upgrade pip
        self.upgrade_pip()
        
        # Step 3: Install packages
        self.log(f"\n📦 {len(self.requirements)}টি প্যাকেজ ইনস্টল করছি...\n")
        
        installed_count = 0
        failed_packages = []
        
        for i, package in enumerate(self.requirements, 1):
            progress = f"[{i}/{len(self.requirements)}]"
            print(f"{progress}", end=" ")
            
            if self.check_package(package):
                self.log(f"{progress} ✅ {package} - ইতিমধ্যে installed")
                installed_count += 1
            else:
                if self.install_package(package):
                    installed_count += 1
                else:
                    failed_packages.append(package)
        
        # Step 4: Install Ollama
        self.install_ollama()
        
        # Step 5: Download Ollama models
        self.log("\n" + "=" * 60)
        self.log("🤖 Ollama & Qwen সেটআপ")
        self.log("=" * 60)
        
        models_ok = self.download_ollama_models()
        
        # Step 6: Summary
        print("\n" + "=" * 60)
        self.log(f"\n✅ Installation সম্পন্ন!")
        self.log(f"📊 ইনস্টল করা প্যাকেজ: {installed_count}/{len(self.requirements)}")
        self.log(f"🤖 ইনস্টল করা মডেল: {len(self.config['installed_models'])}/{len(self.ollama_models)}")
        
        if failed_packages:
            self.log(f"⚠️ ব্যর্থ প্যাকেজ: {', '.join(failed_packages)}")
        
        # Update config
        self.config['installed'] = True
        self.config['installation_date'] = datetime.now().isoformat()
        self.config['installed_packages'] = self.requirements
        self.save_config()
        
        self.log(f"\n📝 Log সেভ করা হয়েছে: {self.install_log_file}")
        self.save_logs()
        
        print("=" * 60)
        
        self.log("\n💡 পরবর্তী ধাপ:")
        self.log("  python character_launcher.py   # Character চালান")
        self.log("  python main.py                 # Full app চালান")
        
        return len(failed_packages) == 0
    
    def uninstall_all(self):
        """সব প্যাকেজ আনইনস্টল করুন"""
        print("\n" + "=" * 60)
        print(f"🗑️  {self.app_name} - UNINSTALLATION")
        print("=" * 60 + "\n")
        
        self.log(f"🚀 Uninstallation শুরু হচ্ছে...")
        
        # Confirmation
        print("⚠️  সতর্কতা: এই অপারেশন সব ইনস্টল করা প্যাকেজ আনইনস্টল করবে!")
        response = input("আপনি কি নিশ্চিত? (yes/no): ").strip().lower()
        
        if response != "yes":
            self.log("❌ Uninstallation বাতিল করা হয়েছে")
            return False
        
        self.log(f"\n🗑️  {len(self.requirements)}টি প্যাকেজ আনইনস্টল করছি...\n")
        
        uninstalled_count = 0
        
        for i, package in enumerate(self.requirements, 1):
            progress = f"[{i}/{len(self.requirements)}]"
            print(f"{progress}", end=" ")
            
            if self.check_package(package):
                if self.uninstall_package(package):
                    uninstalled_count += 1
            else:
                self.log(f"{progress} ⏭️  {package} - ইতিমধ্যে আনইনস্টল করা আছে")
        
        # Clean up config files
        print("\n")
        self.log("\n🧹 কনফিগারেশন ফাইল পরিষ্কার করছি...")
        
        cleanup_files = [
            self.config_file,
            self.install_log_file,
            'launcher_config.json',
            '.env'
        ]
        
        for file in cleanup_files:
            if os.path.exists(file):
                try:
                    os.remove(file)
                    self.log(f"  ✅ {file} ডিলিট করা হয়েছে")
                except Exception as e:
                    self.log(f"  ⚠️ {file} ডিলিট ব্যর্থ: {e}")
        
        # Summary
        print("=" * 60)
        self.log(f"\n✅ Uninstallation সম্পন্ন!")
        self.log(f"📊 আনইনস্টল করা: {uninstalled_count}/{len(self.requirements)}")
        self.log(f"\n📝 Log সেভ করা হয়েছে: {self.install_log_file}")
        
        self.save_logs()
        print("=" * 60)
        return True
    
    def show_status(self):
        """Installation status দেখান"""
        print("\n" + "=" * 60)
        print(f"📊 {self.app_name} - STATUS")
        print("=" * 60 + "\n")
        
        self.log(f"📦 Application: {self.app_name}")
        self.log(f"📌 Version: {self.version}")
        self.log(f"🖥️  OS: {platform.system()}")
        self.log(f"🐍 Python: {sys.version.split()[0]}")
        
        if self.config.get('installed'):
            self.log(f"\n✅ Installation Status: INSTALLED")
            self.log(f"📅 Installation Date: {self.config.get('installation_date', 'Unknown')}")
            self.log(f"📁 Install Path: {self.config.get('install_path', 'Unknown')}")
            self.log(f"📦 Installed Packages: {len(self.config.get('installed_packages', []))}")
            self.log(f"🤖 Installed Models: {len(self.config.get('installed_models', []))}")
            
            if self.config.get('installed_models'):
                self.log(f"\n🤖 Models:")
                for model in self.config.get('installed_models', []):
                    self.log(f"   ✅ {model}")
        else:
            self.log(f"\n❌ Installation Status: NOT INSTALLED")
        
        print("\n" + "=" * 60)
    
    def main_menu(self):
        """Main মেনু দেখান"""
        while True:
            print("\n" + "=" * 60)
            print(f"🎨 {self.app_name} - Installer v{self.version}")
            print("WITH OLLAMA & QWEN MODELS")
            print("=" * 60)
            print("\n📋 অপশন নির্বাচন করুন:\n")
            print("  1️⃣  Install - সব ডিপেন্ডেন্সি + Ollama + Qwen models")
            print("  2️⃣  Uninstall - সব কিছু আনইনস্টল করুন")
            print("  3️⃣  Status - ইনস্টলেশন স্ট্যাটাস দেখুন")
            print("  4️⃣  Exit - প্রোগ্রাম বন্ধ করুন")
            print("\n" + "=" * 60)
            
            choice = input("\nআপনার পছন্দ (1-4): ").strip()
            
            if choice == "1":
                if self.install_all():
                    print("\n✅ Installation সফল!")
                else:
                    print("\n⚠️ Installation কিছু ত্রুটি নিয়ে সম্পন্ন হয়েছে")
            
            elif choice == "2":
                if self.uninstall_all():
                    print("\n✅ Uninstallation সফল!")
                else:
                    print("\n❌ Uninstallation বাতিল করা হয়েছে")
            
            elif choice == "3":
                self.show_status()
            
            elif choice == "4":
                print("\n👋 ধন্যবাদ! বিদায়...")
                break
            
            else:
                print("\n❌ অবৈধ পছন্দ। আবার চেষ্টা করুন।")
            
            input("\nপ্রবেশ করতে কোন কী চাপুন...")


def main():
    """Main entry point"""
    try:
        installer = BanglaAIInstaller()
        installer.main_menu()
    except KeyboardInterrupt:
        print("\n\n⚠️ প্রোগ্রাম ব্যবহারকারী দ্বারা বন্ধ করা হয়েছে")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("প্রবেশ করতে কোন কী চাপুন...")


if __name__ == "__main__":
    main()
