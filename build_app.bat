@echo off
REM Ayesha-Pipraa Desktop App Build Script
REM Builds the Windows .exe executable

echo.
echo ========================================
echo  Ayesha-Pipraa Desktop App Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

echo [1/4] Installing required packages...
pip install customtkinter psutil edge-tts pyinstaller -q

echo.
echo [2/4] Cleaning old build files...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "__pycache__" rmdir /s /q "__pycache__"

echo.
echo [3/4] Building executable...
pyinstaller build_app.spec

echo.
echo [4/4] Build complete!
echo.
echo ========================================
echo  Build Successful!
echo ========================================
echo.
echo Your executable is ready at:
echo   dist\Ayesha-Pipraa.exe
echo.
echo To install:
echo   1. Copy dist\Ayesha-Pipraa.exe to your desired location
echo   2. Create a shortcut on Desktop
echo   3. Run Ayesha-Pipraa.exe
echo.
pause
