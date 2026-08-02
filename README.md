# AI Book Writer - Vercel Ready Textbook Orchestrator

An agentic multi-book publishing system that generates university-grade textbooks from a syllabus with custom graphics, structured layouts, review agents, and DOCX/PDF export capabilities.

## 🚀 How to Deploy on Vercel (0 Effort)

### Method 1: Using Vercel CLI (Recommended & Fastest)

1. Open your terminal in this project folder (`C:\Users\shiva\.gemini\antigravity\scratch\ai-book-writer`).
2. Run:
   ```bash
   npx vercel
   ```
3. Follow the quick prompts in your terminal:
   - **Set up and deploy?**: `Y`
   - **Which scope?**: Select your Vercel account.
   - **Link to existing project?**: `N`
   - **What's your project's name?**: `ai-book-writer`
   - **In which directory is your code located?**: `./`
   - **Want to modify build settings?**: `N`
4. Done! Vercel will instantly build and give you a live production URL!

---

### Method 2: Deploying via GitHub & Vercel Dashboard

1. Push this folder to a new GitHub repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit for Vercel deployment"
   git remote add origin https://github.com/YOUR_USERNAME/ai-book-writer.git
   git push -u origin main
   ```
2. Go to your [Vercel Dashboard](https://vercel.com/dashboard).
3. Click **Add New...** -> **Project**.
4. Select your `ai-book-writer` GitHub repository and click **Deploy**.
5. Vercel will automatically detect `vercel.json` and deploy both the backend and frontend!

---

## 💻 Running Locally (One Click)

Double-click **`Double-Click-To-Run.bat`** in this folder!
It will automatically set up the Python environment, start the local server, and open your web browser to `http://127.0.0.1:8000`.

---

## ⚡ Key Vercel Optimizations Included

- **Vercel Serverless Function Config (`vercel.json`)**: Routes static assets to `frontend/` and API endpoints to `backend/app.py`.
- **Ephemeral `/tmp` Storage Handling**: Uses `/tmp/projects` when running in serverless environments.
- **Direct Word Download Endpoint**: `/api/projects/{slug}/export/docx` streams `.docx` files directly to the browser.
- **Gemini & OpenAI API Fallbacks**: Automatically falls back to Gemini 2.5 Flash if OpenAI API limits are reached.
