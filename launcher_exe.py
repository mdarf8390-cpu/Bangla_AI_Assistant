"""
Bangla AI Assistant - Windows EXE Wrapper
এটি Windows এ .exe হিসাবে চলবে এবং সব dependencies auto-install করবে
PyInstaller দিয়ে এটি compile করুন: pyinstaller --onefile --windowed launcher_exe.py
"""

import os
import sys
import subprocess
import json
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.getcwd())

def ensure_dependencies():
    """সব dependencies installed আছে কিনা নিশ্চিত করুন"""
    requirements = [
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
    
    print("=" * 60)
    print("🎨 Bangla AI Assistant - Initializing")
    print("=" * 60 + "\n")
    
    missing = []
    for pkg in requirements:
        try:
            __import__(pkg.replace('-', '_'))
        except ImportError:
            missing.append(pkg)
    
    if missing:
        print(f"📦 Missing {len(missing)} packages. Installing...\n")
        
        # Upgrade pip
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "-q"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except:
            pass
        
        # Install missing packages
        for pkg in missing:
            print(f"  📥 Installing {pkg}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", pkg, "-q"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                print(f"  ✅ {pkg}")
            except Exception as e:
                print(f"  ❌ {pkg} - {e}")
        
        print()
    else:
        print("✅ All dependencies ready!\n")
    
    print("=" * 60 + "\n")


def main():
    """Main launcher"""
    try:
        # Ensure dependencies
        ensure_dependencies()
        
        # Import and run character launcher
        from character_launcher import start_floating_character
        start_floating_character()
    
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Please run: pip install -r requirements.txt")
        input("Press Enter to exit...")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")


if __name__ == "__main__":
    main()
