#!/usr/bin/env bash
set -e

# Change directory to the folder containing this script
cd "$(dirname "$0")"

echo "==================================================="
echo "      Starting AI Fitness Planner Web App          "
echo "==================================================="
echo ""

# 1. Determine Python command (python3 or python)
if command -v python3 &>/dev/null; then
    PY_CMD="python3"
elif command -v python &>/dev/null; then
    PY_CMD="python"
else
    echo "Error: Python is not installed or not in PATH!"
    exit 1
fi

# 2. Check / create virtual environment
if [ ! -d "venv" ] || [ ! -f "venv/bin/activate" ]; then
    echo "[1/4] Virtual environment not found. Creating 'venv'..."
    $PY_CMD -m venv venv
fi

# 3. Activate virtual environment
echo "[2/4] Activating virtual environment..."
source venv/bin/activate

# 4. Check & install Django
if ! python -c "import django" &>/dev/null; then
    echo "[3/4] Installing Django..."
    pip install django
else
    echo "[3/4] Dependencies verified."
fi

# 5. Database migrations
echo "[4/4] Checking database migrations..."
python manage.py migrate --noinput

echo ""
echo "==================================================="
echo "  App is starting at: http://127.0.0.1:8000/       "
echo "  Opening browser automatically...                 "
echo "  (Press Ctrl+C to stop the server)                "
echo "==================================================="
echo ""

# Open browser based on OS (Linux / macOS / WSL)
if command -v xdg-open &>/dev/null; then
    (sleep 2 && xdg-open "http://127.0.0.1:8000/") &
elif command -v open &>/dev/null; then
    (sleep 2 && open "http://127.0.0.1:8000/") &
fi

# Start Django server
python manage.py runserver 127.0.0.1:8000
