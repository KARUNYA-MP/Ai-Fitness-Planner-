#!/usr/bin/env python3
"""
Universal Cross-Platform Runner for AI Fitness Planner
Works on Windows, macOS, and Linux without needing any shell scripts.
Usage: python run.py
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_ROOT)

def get_venv_python():
    """Locate the Python executable in the virtual environment."""
    if sys.platform.startswith("win"):
        return os.path.join(PROJECT_ROOT, "venv", "Scripts", "python.exe")
    return os.path.join(PROJECT_ROOT, "venv", "bin", "python")

def get_venv_pip():
    """Locate the Pip executable in the virtual environment."""
    if sys.platform.startswith("win"):
        return os.path.join(PROJECT_ROOT, "venv", "Scripts", "pip.exe")
    return os.path.join(PROJECT_ROOT, "venv", "bin", "pip")

def main():
    print("=" * 55)
    print("       Starting AI Fitness Planner Web App")
    print("=" * 55)
    print()

    venv_python = get_venv_python()
    venv_pip = get_venv_pip()

    # 1. Create venv if not present
    if not os.path.exists(venv_python):
        print("[1/4] Virtual environment not found. Creating 'venv'...")
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    else:
        print("[1/4] Virtual environment detected.")

    # 2. Check if django is installed in venv
    try:
        subprocess.check_call(
            [venv_python, "-c", "import django"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("[2/4] Dependencies verified.")
    except subprocess.CalledProcessError:
        print("[2/4] Installing Django...")
        subprocess.check_call([venv_pip, "install", "django"])

    # 3. Apply migrations
    print("[3/4] Running database migrations...")
    subprocess.check_call([venv_python, "manage.py", "migrate", "--noinput"])

    # 4. Open browser in a background thread after a brief delay
    def open_browser():
        time.sleep(2)
        webbrowser.open("http://127.0.0.1:8000/")

    threading.Thread(target=open_browser, daemon=True).start()

    print()
    print("=" * 55)
    print("  App running at: http://127.0.0.1:8000/")
    print("  (Press Ctrl+C to stop the server)")
    print("=" * 55)
    print()

    # 5. Run Django server
    try:
        subprocess.call([venv_python, "manage.py", "runserver", "127.0.0.1:8000"])
    except KeyboardInterrupt:
        print("\nServer stopped.")

if __name__ == "__main__":
    main()
