@echo off
REM ============================================================
REM Bangla AI Assistant - Character-Only EXE Builder
REM শুধুমাত্র Floating Character EXE তৈরি করে
REM ============================================================

echo.
echo ============================================================
echo Building Character-Only Executable
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
    echo ⚠️ PyInstaller found নেই। Installing...
    pip install pyinstaller
)

echo.
echo 🔨 Building Character-Only EXE...
echo.

REM PyInstaller দিয়ে exe তৈরি করুন
pyinstaller --clean --onefile character_launcher.spec

if errorlevel 1 (
    echo.
    echo ❌ Build failed!
    echo এই সমস্যাগুলি চেক করুন:
    echo 1. সমস্ত dependencies install আছে?
    echo 2. launcher_exe.py এবং character_launcher.py আছে?
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ Build successful!
echo ============================================================
echo.
echo 📦 Output: dist/Bangla_AI_Assistant_Character.exe
echo.
echo 🎉 Character-only executable প্রস্তুত!
echo এটি standalone চালবে কোন dependencies ছাড়াই।
echo.
pause
