import uvicorn
import os

if __name__ == "__main__":
    print("=" * 60)
    print("Starting AI Academic Textbook Publishing Orchestrator...")
    print("Serving dashboard locally at: http://127.0.0.1:8000")
    print("=" * 60)
    uvicorn.run("backend.app:app", host="127.0.0.1", port=8000, reload=True)
