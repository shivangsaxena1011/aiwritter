import os
import uvicorn

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"

    print("=" * 60)
    print("  AI Book Writer v3.0 — Production Server Starting...")
    print(f"  Target URL: http://{host}:{port}")
    print("  API Docs:   http://{host}:{port}/docs")
    print("=" * 60)

    uvicorn.run("backend.app.main:app", host=host, port=port, reload=debug)
