# 🎨 Ayesha-Pipraa Desktop Application

**Arafat's AI Assistant - Professional Windows Desktop Application**

এটি একটি সম্পূর্ণ standalone Windows Desktop Application যা Ayesha AI Assistant কে নিয়ে আসে আপনার PC-তে।

## ✨ Features

### 🎭 3D Floating Character (Avatar)
- **Transparent 3D Character** - স্বচ্ছ চরিত্র যা সারা screen এ ভাসে
- **Double Click to Minimize** - দ্বিবার ক্লিক করলে ছোট হয়ে যায়
- **Emotion Expressions** - বিভিন্ন ইমোশন প্রকাশ করে
- **Customizable Size & Opacity** - আকার এবং স্বচ্ছতা পরিবর্তন করুন

### ⚙️ Control Panel
- **Character Settings** - চরিত্রের নাম, আকার, স্বচ্ছতা সামঞ্জস্য করুন
- **Feature Settings** - ভয়েস, মিডিয়া ডিটেকশন, ��টো-স্টার্ট
- **Theme Settings** - Dark/Light থিম নির্বাচন করুন
- **Easy Save/Reset** - সেটিংস সংরক্ষণ বা রিসেট করুন

### 🎵 Media Detection
- **স্বয়ংক্রিয় সঙ্গ/মুভি শনাক্তকরণ** - PC-তে কোনো মিডিয়া চলছে বুঝে নেয়
- **Real-time Status** - UI-তে রিয়েল-টাইম স্ট্যাটাস দেখায়
- **Auto Pause** - AI কথা বলার সময় মিডিয়া স্বয়ংক্রিয়ভাবে পজ হয়

### 💬 Chat & Communication
- **Bangla Support** - সম্পূর্ণ বাংলা ভাষায় যোগাযোগ
- **Text-to-Speech** - Bangla voice output সহ
- **Character Memory** - ব্যবহারকারী তথ্য মনে রাখে

### 📊 Status & Monitoring
- **Live Status Dashboard** - চরিত্র, মিডিয়া, ব্যবহারকারী স্ট্যাটাস দেখুন
- **System Information** - অ্যাপ্লিকেশন তথ্য এবং অবস্থা
- **Activity Logs** - সব কার্যকলাপ লগ ফাইলে সংরক্ষিত

## 🚀 Installation

### Method 1: Automatic Setup (Recommended)
```bash
python install_app.py
```

এটি সব প্রয়োজনীয় প্যাকেজ ইনস্টল করবে এবং .exe তৈরি করবে।

### Method 2: Manual Build
```bash
# Install dependencies
pip install -r requirements_app.txt

# Build executable
pyinstaller build_app.spec

# Run from dist folder
dist/Ayesha-Pipraa.exe
```

### Method 3: Batch Script (Windows Only)
```batch
build_app.bat
```

## 📁 Project Structure

```
Ayesha-Pipraa/
├── ayesha_pipraa_app.py      # Main application
├── build_app.spec            # PyInstaller configuration
├── build_app.bat             # Windows build script
├── install_app.py            # Python installer
├── requirements_app.txt       # Dependencies
├── ayesha_settings.json       # Default settings
├── dist/                      # Output executable
│   └── Ayesha-Pipraa.exe     # Final .exe file
└── logs/                      # Application logs
```

## ⌨️ Quick Start

1. **একবার ইনস্টল করুন:**
   ```bash
   python install_app.py
   ```

2. **অ্যাপ্লিকেশন চালান:**
   ```bash
   dist/Ayesha-Pipraa.exe
   ```

3. **ডেস্কটপ শর্টকাট তৈরি করুন** (ঐচ্ছিক)

## 🎮 Control Center Guide

### Main Window
- **⚙️ Open Settings** - সেটিংস প্যানেল খুলুন
- **👻 Hide Character** - চরিত্র লুকান
- **👤 Show Character** - চরিত্র দেখান
- **💬 Open Chat** - চ্যাট উইন্ডো খুলুন
- **🎵 Media Status** - মিডিয়া স্ট্যাটাস চেক করুন
- **❌ Exit** - অ্যাপ বন্ধ করুন

### Settings Panel
- **Character Settings** - চরিত্র কাস্টমাইজ করুন
- **Feature Settings** - বৈশিষ্ট্য সক্রিয়/নিষ্ক্রিয় করুন
- **Appearance** - থিম পরিবর্তন করুন

## 🔧 Configuration

Settings স্বয়ংক্রিয়ভাবে `ayesha_settings.json` এ সংরক্ষিত হয়:

```json
{
    "character_name": "Ayesha",
    "character_size": 200,
    "character_opacity": 0.8,
    "auto_start": false,
    "voice_enabled": true,
    "theme": "dark",
    "language": "bengali",
    "media_detection": true,
    "character_position": "bottom-right"
}
```

## 📝 Logging

সব কার্যকলাপ `ayesha_app.log` ফাইলে লগ হয়:
```
logs/
└── ayesha_app.log
```

## 🛠️ Development

### Add New Features
1. `ayesha_pipraa_app.py` এ নতুন মেথড যোগ করুন
2. UI এ নতুন বাটন/উইজেট যোগ করুন
3. Settings Panel এ সেটিংস অপশন যোগ করুন
4. পুনরায় build করুন: `pyinstaller build_app.spec`

### Customize Avatar
3D Character ফাইলগুলি `ui/` ফোল্ডারে রয়েছে:
- `ui/floating_avatar.py` - Avatar logic
- অন্যান্য asset ফাইলগুলি

## ⚠️ Troubleshooting

### "Module not found" Error
```bash
pip install -r requirements_app.txt
```

### Executable won't start
- Windows Defender দ্বারা ব্লক হতে পারে - অনুমতি দিন
- সব dependencies ইনস্টল করুন

### Avatar not showing
- Graphics driver আপডেট করুন
- OpenGL support চেক করুন

## 📞 Support

**Creator:** Arafat (Pipraa)
**GitHub:** mdarf8390-cpu

## 📄 License

This project is part of Bangla_AI_Assistant
All rights reserved © 2026

---

**Enjoy using Ayesha-Pipraa! 🎨✨**
