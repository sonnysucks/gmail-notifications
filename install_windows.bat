@echo off
REM SnapStudio Installation Script for Windows
REM This script installs Podman and sets up SnapStudio

echo 🎯 SnapStudio Installation Script for Windows
echo ==============================================

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running as administrator
) else (
    echo [ERROR] Please run this script as administrator
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

REM Check for Chocolatey
echo [INFO] Checking Chocolatey installation...
choco --version >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] Chocolatey found
) else (
    echo [INFO] Installing Chocolatey...
    powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    echo [SUCCESS] Chocolatey installed
)

REM Install Podman
echo [INFO] Installing Podman...
choco install podman -y
echo [SUCCESS] Podman installed

REM Check for Git
echo [INFO] Checking Git installation...
git --version >nul 2>&1
if %errorLevel% == 0 (
    echo [SUCCESS] Git found
) else (
    echo [INFO] Installing Git...
    choco install git -y
    echo [SUCCESS] Git installed
)

REM Clone repository if not already present
if not exist ".git" (
    echo [INFO] Cloning SnapStudio repository...
    git clone https://github.com/sonnysucks/gmail-notifications.git .
    echo [SUCCESS] Repository cloned
) else (
    echo [SUCCESS] Repository already present
)

REM Make scripts executable (Windows doesn't need chmod, but we'll ensure they're accessible)
echo [INFO] Setting up scripts...

REM Build and run
echo [INFO] Building SnapStudio container...
podman build -t snapstudio:latest .

echo [INFO] Starting SnapStudio container...
podman run -d --name snapstudio-app -p 5001:5001 -v snapstudio_data:/app/data -v snapstudio_logs:/app/logs -v snapstudio_backups:/app/backups -v snapstudio_exports:/app/exports -v snapstudio_uploads:/app/uploads --restart unless-stopped snapstudio:latest

echo.
echo 🎉 SnapStudio Installation Complete!
echo ======================================
echo.
echo Access the web interface at: http://localhost:5001
echo Default login: admin / admin123
echo.
echo Container management:
echo   View logs:    podman logs -f snapstudio-app
echo   Stop:         podman stop snapstudio-app
echo   Start:        podman start snapstudio-app
echo   Remove:       podman rm -f snapstudio-app
echo.
echo For support, contact: snapappdevelopment@gmail.com
echo.
echo [SUCCESS] Installation completed successfully!
pause