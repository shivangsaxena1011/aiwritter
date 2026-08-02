@echo off
title AI Book Writer Launcher
echo ============================================================
echo Starting AI Book Writer server...
echo ============================================================
cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo Creating Python virtual environment...
    python -m venv venv
    call .\venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .\venv\Scripts\activate.bat
)

echo Opening web browser to http://127.0.0.1:8000...
start "" "http://127.0.0.1:8000"

python run.py
pause
