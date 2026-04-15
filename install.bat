@echo off
setlocal EnableDelayedExpansion
title Piyuai Installer

echo.
echo  ██████╗ ██╗██╗   ██╗██╗   ██╗ █████╗ ██╗
echo  ██╔══██╗██║╚██╗ ██╔╝██║   ██║██╔══██╗██║
echo  ██████╔╝██║ ╚████╔╝ ██║   ██║███████║██║
echo  ██╔═══╝ ██║  ╚██╔╝  ██║   ██║██╔══██║██║
echo  ██║     ██║   ██║   ╚██████╔╝██║  ██║██║
echo  ╚═╝     ╚═╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚═╝
echo.
echo  AI Coding Assistant - Powered by NVIDIA NIM
echo  Installing for Windows...
echo.

:: ── Check if Python is already installed ──────────────────────────────────
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo [✓] Python found. Using existing installation.
    goto :install_deps
)

:: ── No Python — download and install it silently ──────────────────────────
echo [~] Python not found. Downloading Python 3.11...
echo.

set PYTHON_URL=https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe
set PYTHON_INSTALLER=%TEMP%\python-installer.exe

curl -L --progress-bar "%PYTHON_URL%" -o "%PYTHON_INSTALLER%"
if %errorlevel% neq 0 (
    echo [✗] Failed to download Python. Check your internet connection.
    pause & exit /b 1
)

echo [~] Installing Python silently...
"%PYTHON_INSTALLER%" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1
if %errorlevel% neq 0 (
    echo [✗] Python installation failed.
    pause & exit /b 1
)

:: Refresh PATH so python is found
call refreshenv >nul 2>&1
set "PATH=%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts;%PATH%"

echo [✓] Python installed successfully.
echo.

:install_deps
:: ── Create install directory ───────────────────────────────────────────────
set INSTALL_DIR=%USERPROFILE%\piyuai
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

echo [~] Downloading Piyuai...

:: Download piyuai.py
curl -L --progress-bar "https://raw.githubusercontent.com/YOUR_USERNAME/piyuai/main/piyuai.py" -o "%INSTALL_DIR%\piyuai.py"
if %errorlevel% neq 0 (
    echo [✗] Failed to download piyuai.py
    echo     Make sure you have internet access.
    pause & exit /b 1
)

echo [✓] Downloaded piyuai.py

:: ── Install Python dependencies ───────────────────────────────────────────
echo [~] Installing dependencies...
python -m pip install --upgrade pip -q
python -m pip install openai rich prompt_toolkit --no-cache-dir -q
if %errorlevel% neq 0 (
    echo [✗] Failed to install dependencies.
    pause & exit /b 1
)
echo [✓] Dependencies installed.

:: ── Create launcher script ────────────────────────────────────────────────
echo @echo off > "%INSTALL_DIR%\piyuai.cmd"
echo python "%INSTALL_DIR%\piyuai.py" %%* >> "%INSTALL_DIR%\piyuai.cmd"

:: ── Add to PATH (user-level) ──────────────────────────────────────────────
for /f "tokens=2*" %%a in ('reg query "HKCU\Environment" /v PATH 2^>nul') do set "USERPATH=%%b"
echo %USERPATH% | find /i "%INSTALL_DIR%" >nul 2>&1
if %errorlevel% neq 0 (
    setx PATH "%USERPATH%;%INSTALL_DIR%" >nul
    echo [✓] Added Piyuai to PATH.
)

echo.
echo  ╔══════════════════════════════════════════════╗
echo  ║   Piyuai installed successfully!             ║
echo  ║                                              ║
echo  ║   Open a NEW terminal and run:               ║
echo  ║     piyuai                                   ║
echo  ║                                              ║
echo  ║   Get your free NVIDIA NIM API key at:       ║
echo  ║     https://build.nvidia.com                 ║
echo  ╚══════════════════════════════════════════════╝
echo.
pause
