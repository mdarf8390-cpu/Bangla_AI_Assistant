@echo off
REM ============================================================
REM Bangla AI Assistant - PyInstaller Build Script
REM এই স্ক্রিপ্ট একটি standalone .exe ফাইল তৈরি করে
REM ============================================================

echo.
echo ============================================================
echo Bangla AI Assistant - Building Executable
echo ============================================================
echo.

REM Python আছে কিনা চেক করুন
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python installed নেই!
    pause
    exit /b 1
)

REM PyInstaller আছে কিনা চেক করুন
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ⚠️  PyInstaller found নেই। Installing...
    pip install pyinstaller
)

echo.
echo 🔨 Building executable...
echo.

REM PyInstaller দিয়ে exe তৈরি করুন
pyinstaller --clean --onefile build_app.spec

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    echo এই সমস্যাগুলি চেক করুন:
    echo 1. সমস্ত dependencies install আছে?
    echo 2. main.py ফাইল বিদ্যমান?
    echo 3. সমস্ত asset ফাইল আছে?
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ Build successful!
echo ============================================================
echo.
echo 📦 Output location: dist/Bangla_AI_Assistant.exe
echo.
echo 🎉 এখন আপনি এই exe ফাইলটি চালাতে পারেন!
echo.
pause
