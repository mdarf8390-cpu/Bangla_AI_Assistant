# 🚀 Ayesha-Pipraa Desktop App - Quick Start Guide

## ⚡ 5-Minute Quick Start

### Step 1: Prerequisites
- **Windows 7/8/10/11**
- **Python 3.8+** (Download from https://www.python.org)
- **Internet connection** (for first-time setup)

### Step 2: Installation

#### Option A: Automatic Installation (Recommended)
```bash
# Download the repository
git clone https://github.com/mdarf8390-cpu/Bangla_AI_Assistant.git
cd Bangla_AI_Assistant

# Run installer
python install_app.py
```

The installer will:
- ✓ Install all dependencies
- ✓ Build the executable
- ✓ Create desktop shortcut
- ✓ Create configuration files

#### Option B: Manual Build
```bash
# Install dependencies
pip install -r requirements_app.txt

# Build executable
pyinstaller build_app.spec

# Run from dist folder
dist/Ayesha-Pipraa.exe
```

#### Option C: Batch Script (Windows Only)
```bash
# Double-click build_app.bat
# Or run in Command Prompt:
build_app.bat
```

### Step 3: Launch Application
```bash
# Method 1: Direct execution
dist/Ayesha-Pipraa.exe

# Method 2: From desktop shortcut (if created)
Click "Ayesha-Pipraa" shortcut

# Method 3: From Python
python ayesha_pipraa_app.py
```

---

## 🎮 Using the Application

### Main Control Center

#### 📊 Status Panel (Left Side)
- **Character Status** - Shows current character state
- **Media Status** - Real-time media detection
- **User Status** - Active user information
- **System Info** - App version and status

#### 🎮 Quick Controls (Right Side)
- **⚙️ Open Settings** - Configure character and features
- **👻 Hide Character** - Minimize 3D avatar
- **👤 Show Character** - Display 3D avatar
- **💬 Open Chat** - Start conversation
- **🎵 Media Status** - Check playing media
- **❌ Exit** - Close application

### Settings Panel

#### 👤 Character Settings
- **Character Name** - Change avatar name
- **Character Size** - Adjust avatar size (100-400px)
- **Opacity** - Set transparency level (10%-100%)

#### 🔧 Feature Settings
- **🔊 Voice Output** - Enable/disable TTS
- **🎵 Media Detection** - Auto-detect songs/movies
- **🚀 Auto Start** - Launch on boot

#### 🎨 Appearance
- **Theme** - Dark/Light mode
- **Language** - Select interface language

---

## 📁 File Structure

```
Bangla_AI_Assistant/
├── ayesha_pipraa_app.py          # Main application
├── build_app.spec                # PyInstaller config
├── build_app.bat                 # Windows build script
├── install_app.py                # Python installer
├── requirements_app.txt          # Dependencies
├── ayesha_settings.json          # Default settings
├── AYESHA_APP_README.md          # Full documentation
├── QUICKSTART.md                 # This file
├── dist/
│   └── Ayesha-Pipraa.exe        # Final executable
└── logs/
    └── ayesha_app.log            # Application logs
```

---

## 🎯 Common Tasks

### ✅ Change Character Settings
1. Click **⚙️ Open Settings**
2. Go to **👤 Character Settings** tab
3. Adjust name, size, opacity
4. Click **💾 Save Settings**

### ✅ Hide/Show Character
1. Click **👻 Hide Character** to minimize avatar
2. Click **👤 Show Character** to display it again
3. **Double-click character** to toggle

### ✅ Check Media Status
1. Click **🎵 Media Status**
2. See current playing media information
3. Application auto-pauses media when speaking

### ✅ Reset to Default Settings
1. Open **⚙️ Settings**
2. Click **🔄 Reset to Default**
3. Confirm reset
4. App restarts with default settings

---

## 🔍 Troubleshooting

### Issue: "Module not found" Error
**Solution:**
```bash
pip install -r requirements_app.txt
```

### Issue: Executable won't start
**Solution:**
- Windows Defender may block it - click "Allow"
- Check if Python 3.8+ is installed
- Run as Administrator

### Issue: Character not showing
**Solution:**
- Update graphics drivers
- Check OpenGL support on your PC
- Verify GPU is properly connected

### Issue: Voice not working
**Solution:**
- Check internet connection
- Ensure speakers are enabled
- Check volume levels
- Restart application

### Issue: Settings not saving
**Solution:**
- Check if app has write permissions
- Ensure ayesha_settings.json is writable
- Run as Administrator

---

## 📝 Logs and Debugging

Application logs are saved to: **ayesha_app.log**

View logs:
```bash
# In PowerShell
Get-Content ayesha_app.log -Tail 50

# In Command Prompt
type ayesha_app.log | more
```

---

## 🎵 Media Detection Features

### Supported Players
- VLC Media Player
- Windows Media Player
- Chrome / Firefox
- Spotify
- MPV
- Potplayer
- Foobar2000
- Winamp
- And more...

### How It Works
1. App monitors system processes
2. Detects when media starts playing
3. Shows **🎵 Media Playing** status
4. Auto-pauses media when AI speaks
5. Resumes after AI finishes

---

## ⚙️ System Requirements

### Minimum
- Windows 7 or later
- Python 3.8+
- 2GB RAM
- 500MB Disk space
- Graphics card with OpenGL support

### Recommended
- Windows 10/11
- Python 3.10+
- 4GB+ RAM
- 1GB Disk space
- Modern GPU

---

## 🆘 Getting Help

### Common Resources
1. **README** - `AYESHA_APP_README.md`
2. **Logs** - Check `ayesha_app.log`
3. **GitHub Issues** - Report bugs
4. **GitHub Discussions** - Ask questions

### Contact
- **Creator:** Arafat (Pipraa)
- **GitHub:** mdarf8390-cpu
- **Project:** Bangla_AI_Assistant

---

## 🎨 Customization

### Change Default Settings
Edit `ayesha_settings.json`:
```json
{
    "character_name": "Your Name",
    "character_size": 250,
    "character_opacity": 0.9,
    "theme": "light"
}
```

### Add Custom Features
Edit `ayesha_pipraa_app.py` and add methods to control panel

---

## 📦 Uninstall

### Method 1: Delete Folder
```bash
# Simply delete the application folder
rmdir /s "C:\Path\To\Ayesha-Pipraa"
```

### Method 2: Remove Shortcut
- Right-click desktop shortcut
- Click **Delete**

### Method 3: Clean Registry (Advanced)
- Press `Win + R`
- Type `regedit`
- Search for "Ayesha" and delete entries

---

## 🚀 Next Steps

1. ✅ Install the application
2. ✅ Launch and explore settings
3. ✅ Customize character appearance
4. ✅ Enable/disable features
5. ✅ Start using Ayesha AI!

---

**Enjoy using Ayesha-Pipraa! 🎨✨**

For more help, see `AYESHA_APP_README.md`
