# Bangla AI Assistant - Build Configuration Guide

## 🚀 PyInstaller Build Configuration

এই ডকুমেন্টেশন `build_app.spec` ফাইলের advanced configuration ব্যাখ্যা করে।

---

## 📋 প্রয়োজনীয় প্রিরিকুইজিট

```bash
# PyInstaller ইনস্টল করুন
pip install pyinstaller

# সমস্ত dependencies ইনস্টল করুন
pip install -r requirements.txt
```

---

## 🔨 Build Process

### অপশন ১: স্বয়ংক্রিয় বিল্ড স্ক্রিপ্ট

#### Windows:
```bash
build.bat
```

#### Linux/Mac:
```bash
chmod +x build.sh
./build.sh
```

### অপশন ২: ম্যানুয়াল বিল্ডিং

```bash
# উপায় ১: আমাদের spec ফাইল ব্যবহার করে
pyinstaller --clean --onefile build_app.spec

# উপায় ২: সরাসরি Python ফাইল থেকে
pyinstaller --onefile --windowed main.py
```

---

## 📦 Build আউটপুট

বিল্ড সম্পন্ন হলে আপনি পাবেন:

```
project/
├── build/              # তৈরি ফাইলগুলি (আপনার প্রয়োজন নেই)
├── dist/
│   └── Bangla_AI_Assistant.exe  # ✅ চূড়ান্ত executable
├── build_app.spec      # PyInstaller specification
└── ...
```

---

## ⚙️ Configuration বিস্তারিত

### 1. **Entry Point - main.py**
```python
a = Analysis(
    ['main.py'],
```
- আপনার প্রকল্পের মূল Python স্ক্রিপ্ট ফাইল
- এটি অবশ্যই আপনার প্রকল্পের entry point হতে হবে

### 2. **datas** - ডাটা ফাইল এবং সম্পদ

```python
datas=[
    ('assets', 'assets'),      # ইমেজ, সাউন্ড এবং অন্যান্য সম্পদ
    # ('models', 'models'),    # AI মডেলগুলি (যদি থাকে)
    # ('data', 'data'),        # ডাটা ফাইলগুলি (যদি থাকে)
]
```

**মডিউল যোগ করতে:**
- আপনার প্রয়োজনীয় ডিরেক্টরি এখানে যোগ করুন
- ফরম্যাট: `('source_dir', 'dest_dir')`

### 3. **hiddenimports** - লুকানো ইমপোর্ট

এতে অন্তর্ভুক্ত:
- **GUI:** customtkinter, tkinter সমস্ত মডিউল
- **অডিও:** pyttsx3, SpeechRecognition, pyaudio, pygame, edge_tts
- **ভিশন:** cv2, PIL সমস্ত উপমডিউল
- **সিস্টেম:** pyautogui, keyboard, mouse, psutil, platform
- **ডাটা:** rapidfuzz, requests, urllib
- **কোর:** json, logging, threading, subprocess, datetime, এবং আরও অনেক কিছু

**কেন এটি প্রয়োজন?**
- PyInstaller স্বয়ংক্রিয়ভাবে সমস্ত imports সনাক্ত করতে পারে না
- গতিশীল imports (যেমন `__import__()`) মিস হতে পারে

### 4. **excludedimports** - বর্জিত মডিউলগুলি

```python
excludedimports=[
    'matplotlib',  # অপ্রয়োজনীয় (আকার কমায়)
    'scipy',       # অপ্রয়োজনীয়
    'pytest',      # শুধুমাত্র development
]
```

**এক্সিকিউটেবল আকার কমাতে অপ্রয়োজনীয় প্যাকেজ বাদ দিন**

### 5. **EXE Configuration**

```python
exe = EXE(
    name='Bangla_AI_Assistant',  # এক্সিকিউটেবল নাম
    console=False,               # কোনো কনসোল উইন্ডো নেই
    icon=None,                   # আইকন ফাইল (ঐচ্ছিক)
    upx=True,                    # UPX সংকুচিত করা
)
```

---

## 🎨 কাস্টমাইজেশন

### আইকন যোগ করুন

```python
icon='assets/bangla_ai_icon.ico',  # 256x256 পিক্সেল সুপারিশ করা হয়
```

### কনসোল চালু করুন (Debugging এর জন্য)

```python
console=True,  # কনসোল উইন্ডো দেখাবে
```

### UPX সংকোচন নিষ্ক্রিয় করুন

```python
upx=False,  # আকার অপ্টিমাইজেশন বন্ধ করুন
```

---

## ⚠️ সাধারণ সমস্যা এবং সমাধান

### সমস্যা ১: মডিউল 'xyz' নেই

**কারণ:** হিডেন ইমপোর্ট মিসিং
**সমাধান:** 
```python
hiddenimports=[
    'xyz',  # আপনার মিসিং মডিউল যোগ করুন
]
```

### সমস্যা ২: অ্যাসেট ফাইল খুঁজে পাওয়া যায় না

**কারণ:** datas তালিকায় যোগ করা হয়নি
**সমাধান:**
```python
datas=[
    ('your_assets_folder', 'your_assets_folder'),
]
```

### সমস্যা ৩: বিল্ড খুব বড়

**সমাধান:**
1. অপ্রয়োজনীয় প্যাকেজ excludedimports এ যোগ করুন
2. `--onefile` এর পরিবর্তে `--onedir` ব্যবহার করুন
3. UPX সংকোচন চালু রাখুন

### সমস্যা ৪: Runtime এ ModuleNotFoundError

**কারণ:** ডাইনামিক imports সনাক্ত হয়নি
**সমাধান:** স্পষ্টভাবে hiddenimports এ যোগ করুন

---

## 🚀 উন্নত বিল্ডিং অপশন

### একক ফাইল exe (সুপারিশ করা হয়):
```bash
pyinstaller --onefile build_app.spec
```

### একাধিক ফাইল (দ্রুত লঞ্চ):
```bash
pyinstaller --onedir build_app.spec
```

### সাইলেন্ট মোড (কোনো আউটপুট নেই):
```bash
pyinstaller --windowed build_app.spec
```

### কাস্টম আউটপুট পাথ:
```bash
pyinstaller --distpath ./custom_output build_app.spec
```

### Cleaning পূর্ববর্তী বিল্ড:
```bash
pyinstaller --clean build_app.spec
```

---

## 📊 বিল্ড অপ্টিমাইজেশন টিপস

1. **আকার কমান:**
   - অপ্রয়োজনীয় প্যাকেজ বাদ দিন
   - UPX সংকোচন চালু করুন
   - বড় ডাটা ফাইলগুলি বাহ্যিক রাখুন

2. **পারফরম্যান্স উন্নত করুন:**
   - `--onedir` ব্যবহার করে দ্রুত লঞ্চ করুন
   - অপ্রয়োজনীয় hooks মুছুন
   - মডিউল কালেকশন অপ্টিমাইজ করুন

3. **নির্ভরযোগ্যতা বাড়ান:**
   - সমস্ত dependencies hiddenimports এ যোগ করুন
   - বিভিন্ন Windows সংস্করণে পরীক্ষা করুন
   - Runtime অনুমতি পরীক্ষা করুন

---

## 🧪 বিল্ড পরীক্ষা

```bash
# তৈরি exe চালান
dist/Bangla_AI_Assistant.exe

# বা Linux/Mac এ:
./dist/Bangla_AI_Assistant
```

---

## 📝 কমান্ড রেফারেন্স

| কমান্ড | বিবরণ |
|--------|--------|
| `--onefile` | একক .exe ফাইল তৈরি করুন |
| `--onedir` | ডিরেক্টরি এবং ফাইল তৈরি করুন |
| `--windowed` | কনসোল উইন্ডো ছাড়াই |
| `--console` | কনসোল উইন্ডো দেখান |
| `--icon=icon.ico` | আইকন সেট করুন |
| `--clean` | ক্যাশ পরিষ্কার করুন |
| `--add-data src:dest` | ডাটা যোগ করুন |
| `--hidden-import=xyz` | হিডেন ইমপোর্ট যোগ করুন |

---

## 🆘 সাহায্য

- [PyInstaller Official Documentation](https://pyinstaller.org/)
- GitHub Issues এ সমস্যা রিপোর্ট করুন
- Build Log দেখুন বিস্তারিত ত্রুটি জানতে

---

## 📌 চেকলিস্ট - Build করার আগে

- [ ] সমস্ত dependencies install করেছেন? (`pip install -r requirements.txt`)
- [ ] main.py ফাইল বিদ্যমান এবং কাজ করছে?
- [ ] সমস্ত asset ফাইল সঠিক পাথে আছে?
- [ ] build_app.spec ফাইল সঠিকভাবে কনফিগার করা?
- [ ] PyInstaller ইনস্টল করেছেন? (`pip install pyinstaller`)

---

**Happy Building! 🎉**
