# -*- mode: python ; coding: utf-8 -*-
"""
Bangla AI Assistant - Character-Only PyInstaller Config
শুধুমাত্র Floating Character EXE তৈরি করে
সব dependencies সহ standalone executable
"""

import sys
import os
from PyInstaller.utils.hooks import get_module_collection_mode

block_cipher = None

a = Analysis(
    ['launcher_exe.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        # Character modules
        ('ui', 'ui'),
        ('ai', 'ai'),
        ('core', 'core'),
        ('automation', 'automation'),
    ],
    hiddenimports=[
        # GUI
        'customtkinter',
        'tkinter',
        'tkinter.messagebox',
        'tkinter.ttk',
        
        # Audio/Voice
        'pyttsx3',
        'pyttsx3.drivers',
        'pyttsx3.drivers.sapi5',
        'SpeechRecognition',
        'pyaudio',
        'edge_tts',
        'asyncio',
        
        # Vision
        'cv2',
        'PIL',
        'PIL.Image',
        
        # System
        'pyautogui',
        'keyboard',
        'mouse',
        'psutil',
        'platform',
        'subprocess',
        'threading',
        
        # Data
        'rapidfuzz',
        'requests',
        
        # Core
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
        
        # Ollama
        'ollama',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[
        'matplotlib',
        'scipy',
        'pytest',
        'setuptools',
        'pip',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove unnecessary files
for excluded in ['tests', 'test', 'docs', '__pycache__', '.git', '.pytest_cache']:
    a.datas = [(x, y) for x, y in a.datas if excluded not in x]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Bangla_AI_Assistant_Character',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
