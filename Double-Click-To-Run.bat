@echo off
title AI Book Writer v3.0 — Academic Publishing Platform
echo ============================================================
echo   AI Book Writer v3.0 — Starting Application...
echo ============================================================
cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo Creating Python virtual environment in .\venv...
    python -m venv venv
    call .\venv\Scripts\activate.bat
    echo Installing production dependencies...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    call .\venv\Scripts\activate.bat
)

if not exist "data" mkdir "data"
if not exist "output" mkdir "output"

echo Opening browser...
start "" "http://127.0.0.1:8000"
python run.py
pause
