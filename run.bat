@echo off
setlocal
cd /d "%~dp0"

echo ===================================================
echo       Starting AI Fitness Planner Web App
echo ===================================================
echo.

:: 1. Check or create virtual environment
if not exist "venv\Scripts\activate.bat" (
    echo [1/4] Virtual environment not found. Creating 'venv'...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Python is not installed or not in PATH!
        pause
        exit /b 1
    )
)

:: 2. Activate virtual environment
echo [2/4] Activating virtual environment...
call venv\Scripts\activate.bat

:: 3. Ensure Django is installed
python -c "import django" >nul 2>&1
if %errorlevel% neq 0 (
    echo [3/4] Installing required packages...
    pip install django
) else (
    echo [3/4] Dependencies verified.
)

:: 4. Run database migrations
echo [4/4] Checking database migrations...
python manage.py migrate --noinput

echo.
echo ===================================================
echo   App is starting at: http://127.0.0.1:8000/
echo   Opening browser automatically...
echo   (Press Ctrl+C in this window to stop the server)
echo ===================================================
echo.

:: Automatically open browser after 2 seconds in the background
start "" cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:8000/"

:: Start Django server
python manage.py runserver 127.0.0.1:8000

pause
