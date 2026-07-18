#!/bin/bash

# ============================================================
# Bangla AI Assistant - Character-Only EXE Builder (Linux/Mac)
# শুধুমাত্র Floating Character Executable তৈরি করে
# ============================================================

echo ""
echo "============================================================"
echo "Building Character-Only Executable"
echo "============================================================"
echo ""

# Python3 আছে কিনা চেক করুন
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 installed নেই!"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python Version: $PYTHON_VERSION"
echo ""

# PyInstaller আছে কিনা চেক করুন
if ! python3 -m pip show pyinstaller &> /dev/null; then
    echo "⚠️ PyInstaller found নেই। Installing..."
    python3 -m pip install pyinstaller
fi

echo ""
echo "🔨 Building Character-Only Executable..."
echo ""

# PyInstaller দিয়ে executable তৈরি করুন
python3 -m PyInstaller --clean --onefile character_launcher.spec

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Build failed!"
    echo "এই সমস্যাগুলি চেক করুন:"
    echo "1. সমস্ত dependencies install আছে?"
    echo "2. launcher_exe.py এবং character_launcher.py আছে?"
    exit 1
fi

echo ""
echo "============================================================"
echo "✅ Build successful!"
echo "============================================================"
echo ""
echo "📦 Output: dist/Bangla_AI_Assistant_Character"
echo ""
echo "🎉 Character-only executable প্রস্তুত!"
echo "এটি standalone চালবে কোন dependencies ছাড়াই।"
echo ""
