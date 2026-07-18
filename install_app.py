#!/usr/bin/env python3
"""
Ayesha-Pipraa Desktop App Installer
Easy installation script for Windows
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path

def print_header():
    print("\n" + "="*50)
    print("  🎨 Ayesha-Pipraa Desktop App Installer")
    print("  Created by: Arafat (Pipraa)")
    print("="*50 + "\n")

def check_requirements():
    """প্রয়োজনীয় প্যাকেজ চেক করা"""
    print("✓ Checking requirements...")
    
    requirements = [
        'customtkinter',
        'psutil',
        'edge-tts',
        'pyinstaller'
    ]
    
    for package in requirements:
        try:
            __import__(package)
            print(f"  ✓ {package} is installed")
        except ImportError:
            print(f"  ✗ {package} is not installed")
            print(f"    Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package, "-q"])
            print(f"  ✓ {package} installed successfully")

def create_shortcuts():
    """ডেস্কটপ শর্টকাট তৈরি করা"""
    print("\n✓ Creating shortcuts...")
    
    try:
        import win32com.client
        shell = win32com.client.Dispatch("WScript.Shell")
        
        desktop = Path.home() / "Desktop"
        shortcut_path = desktop / "Ayesha-Pipraa.lnk"
        
        target = os.path.abspath("dist/Ayesha-Pipraa.exe")
        
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.Targetpath = target
        shortcut.WorkingDirectory = os.path.dirname(target)
        shortcut.IconLocation = target
        shortcut.save()
        
        print(f"  ✓ Desktop shortcut created")
    except ImportError:
        print("  ℹ pywin32 not available. Skipping shortcut creation.")
    except Exception as e:
        print(f"  ℹ Could not create shortcut: {e}")

def create_config():
    """ডিফল্ট কনফিগারেশন তৈরি করা"""
    print("\n✓ Creating default configuration...")
    
    config = {
        "character_name": "Ayesha",
        "character_size": 200,
        "character_opacity": 0.8,
        "auto_start": False,
        "voice_enabled": True,
        "theme": "dark",
        "language": "bengali",
        "media_detection": True,
        "character_position": "bottom-right",
        "version": "1.0.0",
        "created": "2026-07-18"
    }
    
    with open("ayesha_settings.json", "w") as f:
        json.dump(config, f, indent=4)
    
    print("  ✓ Configuration file created")

def main():
    print_header()
    
    print("📦 Installation Process Started\n")
    
    # Step 1: Check requirements
    check_requirements()
    
    # Step 2: Create config
    create_config()
    
    # Step 3: Build application
    print("\n✓ Building application...")
    print("  This may take a few minutes...\n")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "PyInstaller", "build_app.spec"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("  ✓ Application built successfully")
        else:
            print("  ✗ Build failed")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"  ✗ Error during build: {e}")
        return False
    
    # Step 4: Create shortcuts
    create_shortcuts()
    
    # Step 5: Success message
    print("\n" + "="*50)
    print("  ✅ Installation Completed Successfully!")
    print("="*50)
    print("\n📍 Your application is ready at:")
    print(f"   {os.path.abspath('dist/Ayesha-Pipraa.exe')}\n")
    print("🚀 You can now:")
    print("   1. Run: dist/Ayesha-Pipraa.exe")
    print("   2. Create shortcuts to Desktop")
    print("   3. Add to Start Menu\n")
    print("💡 Tip: Double-click the executable to start using Ayesha!\n")

if __name__ == "__main__":
    main()
