# -*- mode: python ; coding: utf-8 -*-
"""
Advanced PyInstaller Configuration for Bangla AI Assistant Desktop App
সম্পূর্ণ স্বয়ংসম্পূর্ণ Windows .exe এক্সিকিউটেবল তৈরি করে
ইনস্টলেশনের পরে কোনো বাহ্যিক dependencies প্রয়োজন নেই
"""

import sys
import os
from PyInstaller.utils.hooks import get_module_collection_mode

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[
        # Optional: FFmpeg বা অন্যান্য binaries যোগ করুন যদি প্রয়োজন
        # ('path/to/ffmpeg.exe', '.'),
    ],
    datas=[
        # সমস্ত প্রকল্প মডিউল এবং ডিরেক্টরি অন্তর্ভুক্ত করুন
        # ('modules', 'modules'),  # আপনার মডিউল ডিরেক্টরি থাকলে
        # ('models', 'models'),    # AI মডেল ফাইলগুলি থাকলে
        # ('data', 'data'),        # ডাটা ফাইলগুলি থাকলে
        ('assets', 'assets'),      # ইমেজ, সাউন্ড এবং অন্যান্য সম্পদ
        # কনফিগারেশন ফাইলগুলি
        # ('.env', '.'),
        # ('config.json', '.'),
    ],
    hiddenimports=[
        # GUI এবং ফ্রেমওয়ার্ক
        'customtkinter',
        'tkinter',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.scrolledtext',
        'tkinter.ttk',
        
        # অডিও এবং ভয়েস প্রসেসিং
        'pyttsx3',
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'SpeechRecognition',
        'pyaudio',
        'pygame',
        'pygame.mixer',
        'edge_tts',
        'asyncio',
        
        # ভিশন এবং ক্যামেরা
        'cv2',
        'cv2.cv2',
        'PIL',
        'PIL.Image',
        'PIL.ImageDraw',
        'PIL.ImageFont',
        'PIL.ImageTk',
        
        # সিস্টেম ইন্টারঅ্যাকশন
        'pyautogui',
        'keyboard',
        'mouse',
        'psutil',
        'platform',
        'subprocess',
        'threading',
        'multiprocessing',
        
        # ডাটা প্রসেসিং এবং স্ট্রিং ম্যাচিং
        'rapidfuzz',
        'rapidfuzz.fuzz',
        
        # HTTP এবং নেটওয়ার্কিং
        'requests',
        'urllib3',
        'urllib',
        
        # কোর Python মডিউলগুলি
        'json',
        'logging',
        'sys',
        'os',
        'time',
        'datetime',
        'pathlib',
        'configparser',
        'shutil',
        'hashlib',
        'uuid',
        'secrets',
        'base64',
        'pickle',
        'csv',
        'sqlite3',
        'collections',
        'itertools',
        'functools',
        
        # সিস্টেম এবং Windows ইন্টিগ্রেশন
        'winreg',
        'ctypes',
        'ctypes.wintypes',
        
        # পরিবেশ এবং কনফিগারেশন
        'dotenv',
        'dotenv.main',
        
        # Ollama AI ইন্টিগ্রেশন
        'ollama',
        
        # Optional ML/AI imports (যদি ব্যবহার করা হয়)
        # 'numpy',
        # 'pandas',
        # 'sklearn',
        # 'torch',
        # 'transformers',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[
        # অপ্রয়োজনীয় মডিউলগুলি বাদ দিন (exe আকার কমাতে)
        'matplotlib',
        'scipy',
        'pytest',
        'setuptools',
        'pip',
        'email',
        'html.parser',
        'urllib.request',
        'distutils',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# অপ্টিমাইজেশন: অপ্রয়োজনীয় প্যাকেজগুলি সরান
for excluded in ['tests', 'test', 'docs', '__pycache__', '.git', '.pytest_cache', 'node_modules']:
    a.datas = [(x, y) for x, y in a.datas if excluded not in x]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Bangla_AI_Assistant',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # কনসোল উইন্ডো দেখাবেন না
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # আইকন থাকলে: 'assets/bangla_ai_icon.ico'
)

# Optional: macOS এর জন্য bundle তৈরি করুন (যদি প্রয়োজন)
app = BUNDLE(
    exe,
    name='Bangla_AI_Assistant.app',
    icon=None,
    bundle_identifier='com.bangla.ai.assistant',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapable': 'True',
    },
)
