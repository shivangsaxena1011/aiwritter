#!/usr/bin/env bash
# =============================================================================
# AI Book Writer v3.0 — Unix Startup Script
# =============================================================================
set -e

echo "============================================================"
echo "  AI Book Writer v3.0 — Starting Platform..."
echo "============================================================"

# Navigate to script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Initialize virtual environment if needed
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment in ./venv..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing production dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Ensure storage output directory exists
mkdir -p data output

# Launch application
python run.py
