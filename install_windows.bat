@echo off
REM SnapStudio Installation Script for Windows
REM This script installs SnapStudio and all dependencies on Windows

echo 🎯 SnapStudio Installation Script for Windows
echo =============================================

REM Check if Python 3 is installed
echo [INFO] Checking Python 3 installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python 3 is not installed. Please install Python 3.8+ first.
    echo [INFO] Download Python 3 from: https://www.python.org/downloads/
    echo [INFO] Make sure to check "Add Python to PATH" during installation.
    pause
    exit /b 1
)

REM Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [SUCCESS] Python %PYTHON_VERSION% found

REM Check if pip is installed
echo [INFO] Checking pip installation...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed. Please install pip first.
    echo [INFO] pip usually comes with Python 3.4+. Try reinstalling Python.
    pause
    exit /b 1
)

REM Create virtual environment
echo [INFO] Creating virtual environment...
if exist venv (
    echo [WARNING] Virtual environment already exists. Removing old one...
    rmdir /s /q venv
)

python -m venv venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment created

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)
echo [SUCCESS] Virtual environment activated

REM Upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [ERROR] Failed to upgrade pip.
    pause
    exit /b 1
)
echo [SUCCESS] pip upgraded

REM Install dependencies
echo [INFO] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo [SUCCESS] Dependencies installed

REM Create necessary directories
echo [INFO] Creating necessary directories...
if not exist data mkdir data
if not exist logs mkdir logs
if not exist backups mkdir backups
if not exist exports mkdir exports
if not exist uploads mkdir uploads
if not exist temp mkdir temp
echo [SUCCESS] Directories created

REM Set up configuration file
echo [INFO] Setting up configuration...
if not exist config.yaml (
    if exist config.example.yaml (
        copy config.example.yaml config.yaml
        echo [SUCCESS] Configuration file created from example
    ) else (
        echo [WARNING] No config.example.yaml found. You'll need to create config.yaml manually.
    )
) else (
    echo [SUCCESS] Configuration file already exists
)

REM Test installation
echo [INFO] Testing installation...
python -c "import flask, sqlalchemy, yaml; print('All imports successful')"
if %errorlevel% neq 0 (
    echo [ERROR] Installation test failed.
    pause
    exit /b 1
)
echo [SUCCESS] Installation test passed

echo.
echo 🎉 SnapStudio Installation Complete!
echo ======================================
echo.
echo To start the web application:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run the web app: python web_app.py
echo 3. Open your browser to: http://localhost:5001
echo 4. Login with: admin / admin123
echo.
echo To start the CLI application:
echo 1. Activate the virtual environment: venv\Scripts\activate.bat
echo 2. Run: python main.py --help
echo.
echo For support, contact: snapappdevelopment@gmail.com
echo.
echo [SUCCESS] Installation completed successfully!
pause
