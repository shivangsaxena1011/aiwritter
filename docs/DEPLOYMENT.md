# AI Book Writer v3.0 — Deployment & Operations Guide

## 1. Deployment Topology Modes

```
+---------------------------------------------------------------------------------+
|                               MODE A: LOCAL STANDALONE                          |
|  Single process containing FastAPI Web Server, In-Process Worker, SQLite & Disk |
+---------------------------------------------------------------------------------+

+---------------------------------------------------------------------------------+
|                               MODE B: CLOUD DISTRIBUTED                         |
|  [Vercel Edge CDN] ---> [Render / Railway Web API & Persistent Worker Service]  |
|                                       |                  |                      |
|                                       v                  v                      |
|                             [Managed PostgreSQL]    [Redis Queue]               |
|                                       |                                         |
|                                       v                                         |
|                             [S3 / R2 Object Store]                              |
+---------------------------------------------------------------------------------+
```

---

## 2. Mode A: Local Deployment (Zero External Infrastructure)

### Option 1: Native Python
1. Clone the repository:
   ```bash
   git clone https://github.com/shivangsaxena1011/aiwritter.git
   cd aiwritter
   ```
2. Run using startup scripts:
   - **Windows:** Double-click `Double-Click-To-Run.bat`.
   - **Linux / macOS:** Run `./run.sh`.
3. Open your browser at `http://127.0.0.1:8000`.

### Option 2: Docker Compose
```bash
docker-compose up -d --build
```
Check container logs:
```bash
docker-compose logs -f app
```

---

## 3. Mode B: Cloud Production Deployment

### 1. Database Setup (PostgreSQL)
Create a managed PostgreSQL database (e.g. Supabase, Neon, or AWS RDS). Copy the connection URI:
```
DATABASE_URL="postgresql+psycopg2://user:password@host:5432/aiwriter?sslmode=require"
```

### 2. Backend & Worker Deployment (Render / Railway)
1. In your cloud dashboard, create a **Web Service** or **Docker Service** pointing to this repository.
2. Select Docker runtime or Python 3.11 with start command:
   ```bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
   ```
3. Set environment variables:
   ```env
   APP_ENV=production
   DATABASE_URL=postgresql+psycopg2://...
   GEMINI_API_KEY=AIzaSy...
   TEXT_MODEL=gemini-2.5-flash
   IMAGE_MODEL=imagen-3.0-generate-002
   STORAGE_TYPE=s3 (or local with persistent disk)
   ```
4. Configure persistent disk:
   Mount a 10 GB persistent disk at `/app/output` if using local storage.
5. Health Check path: `/api/v1/health`.

### 3. Frontend Deployment (Vercel)
The included `vercel.json` deploys the frontend directly to Vercel's global CDN:
1. Import repository on Vercel.
2. Ensure Root Directory is set to `./`.
3. Vercel automatically deploys static assets and handles routing.

---

## 4. Operational Checklist & Verification

- [ ] Confirm `/api/v1/health` returns HTTP 200 with `"status": "healthy"`.
- [ ] Confirm database connects and creates required tables.
- [ ] Ensure Gemini API key has quota enabled for `gemini-2.5-flash` and `imagen-3.0-generate-002`.
- [ ] Verify CORS origins match your domain.
