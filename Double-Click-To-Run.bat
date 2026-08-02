@echo off
title AI Book Writer
echo ============================================================
echo   AI Book Writer — Starting...
echo ============================================================
cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
    call .\venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .\venv\Scripts\activate.bat
)

echo Opening browser...
start "" "http://127.0.0.1:8000"
python run.py
pause
