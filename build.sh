#!/bin/bash

# ============================================================
# Bangla AI Assistant - PyInstaller Build Script (Linux/Mac)
# এই স্ক্রিপ্ট একটি standalone executable ফাইল তৈরি করে
# ============================================================

echo ""
echo "============================================================"
echo "Bangla AI Assistant - Building Executable"
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
    echo "⚠️  PyInstaller found নেই। Installing..."
    python3 -m pip install pyinstaller
fi

echo ""
echo "🔨 Building executable..."
echo ""

# PyInstaller দিয়ে executable তৈরি করুন
python3 -m PyInstaller --clean --onefile build_app.spec

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Build failed!"
    echo "এই সমস্যাগুলি চেক করুন:"
    echo "1. সমস্ত dependencies install আছে?"
    echo "2. main.py ফাইল বিদ্যমান?"
    echo "3. সমস্ত asset ফাইল আছে?"
    exit 1
fi

echo ""
echo "============================================================"
echo "✅ Build successful!"
echo "============================================================"
echo ""
echo "📦 Output location: dist/Bangla_AI_Assistant"
echo ""
echo "🎉 এখন আপনি এই executable ফাইলটি চালাতে পারেন!"
echo ""
