@echo off
setlocal enabledelayedexpansion

:: ImgPrompt Launcher
:: Automatically activates virtual environment and runs Streamlit app

:: Configuration
set "APP_NAME=ImgPrompt"
set "VENV_PATH=<YOUR_PATH>\ImgPrompt\.venv"
set "APP_PATH=<YOUR_PATH>\ImgPrompt\app.py"

:: Check if virtual environment exists
if not exist "%VENV_PATH%\Scripts\activate.bat" (
    echo Error: Virtual environment not found at %VENV_PATH%
    echo Please create the virtual environment first
    pause
    exit /b 1
)

:: Activate virtual environment and run app
echo Starting %APP_NAME%...
call "%VENV_PATH%\Scripts\activate.bat"
if %ERRORLEVEL% neq 0 (
    echo Error: Failed to activate virtual environment
    pause
    exit /b 1
)

:: Check if Python is in PATH
where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Python not found in PATH
    echo Please ensure Python is installed and added to PATH
    pause
    exit /b 1
)

echo Running Streamlit application...
streamlit run "%APP_PATH%"

:: Keep console open if there's an error
if %ERRORLEVEL% neq 0 pause