@echo off
REM Latagan - Quick Setup Script for Windows

echo ============================================
echo Latagan - Online Thrift Store Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Error: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

REM Run migrations
echo Running database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error: Failed to run migrations
    pause
    exit /b 1
)

REM Create superuser
echo.
echo ============================================
echo Create Admin Account
echo ============================================
python manage.py createsuperuser

REM Collect static files
echo.
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the development server, run:
echo    python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000/
echo Admin panel: http://127.0.0.1:8000/admin/
echo.
pause
