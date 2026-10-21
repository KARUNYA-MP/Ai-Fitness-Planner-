# Run Script for PowerShell
$ErrorActionPreference = "Stop"
Set-Location -Path $PSScriptRoot

Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "      Starting AI Fitness Planner Web App          " -ForegroundColor Cyan
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Virtual environment check
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "[1/4] Creating virtual environment 'venv'..." -ForegroundColor Yellow
    python -m venv venv
}

# 2. Activate virtual environment
Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"

# 3. Check Django
try {
    python -c "import django" 2>$null
} catch {
    Write-Host "[3/4] Installing Django..." -ForegroundColor Yellow
    pip install django
}

# 4. Migrate database
Write-Host "[4/4] Applying database migrations..." -ForegroundColor Green
python manage.py migrate --noinput

Write-Host ""
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host "  App is starting at: http://127.0.0.1:8000/       " -ForegroundColor Green
Write-Host "  (Press Ctrl+C to stop the server)                " -ForegroundColor Yellow
Write-Host "===================================================" -ForegroundColor Cyan
Write-Host ""

# Open browser
Start-Process "http://127.0.0.1:8000/"

# Start server
python manage.py runserver 127.0.0.1:8000
