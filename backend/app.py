import os
import uuid
import logging
import asyncio
import json
from typing import Dict, Any, List
from fastapi import FastAPI, BackgroundTasks, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse, Response

# Import Agents & Managers
from backend.agents.toc_planner import TOCPlanner
from backend.agents.content_writer import ContentWriter
from backend.agents.review_agent import ReviewAgent
from backend.agents.diagram_agent import DiagramAgent
from backend.agents.formatter import FormatterAgent
from backend.agents.docx_exporter import DOCXExporter
from backend.agents.book_context_manager import BookContextManager
from backend.agents.chapter_depth_controller import ChapterDepthController
from backend.agents.project_manager import ProjectManager

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Textbook Publishing Orchestrator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks_db: Dict[str, Dict[str, Any]] = {}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IS_VERCEL = bool(os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"))

if IS_VERCEL:
    PROJECTS_DIR = "/tmp/projects"
else:
    PROJECTS_DIR = os.path.join(BASE_DIR, "projects")

os.makedirs(PROJECTS_DIR, exist_ok=True)

if os.path.exists(PROJECTS_DIR):
    try:
        app.mount("/projects", StaticFiles(directory=PROJECTS_DIR), name="projects")
    except Exception as e:
        logger.warning(f"Static mounting notice: {e}")

project_manager = ProjectManager(PROJECTS_DIR)

class BookGenerationTask:
    def __init__(self, slug: str, toc_data: dict, openai_key: str, gemini_key: str):
        self.task_id = slug
        self.slug = slug
        self.toc_data = toc_data
        self.openai_key = openai_key
        self.gemini_key = gemini_key
        
        self.project_path = os.path.join(PROJECTS_DIR, slug)
        self.chapters_dir = os.path.join(self.project_path, "chapters")
        self.images_dir = os.path.join(self.project_path, "images")
        self.tables_dir = os.path.join(self.project_path, "tables")
        self.metadata_dir = os.path.join(self.project_path, "metadata")
        self.exports_dir = os.path.join(self.project_path, "exports")
        
        os.makedirs(self.chapters_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.tables_dir, exist_ok=True)
        os.makedirs(self.metadata_dir, exist_ok=True)
        os.makedirs(self.exports_dir, exist_ok=True)
        
        self.context_path = os.path.join(self.metadata_dir, "book_context.json")
        self.context_manager = BookContextManager(self.context_path)
        
        self.writer = ContentWriter(openai_key=openai_key, gemini_key=gemini_key)
        self.reviewer = ReviewAgent(openai_key=openai_key, gemini_key=gemini_key)
        self.depth_controller = ChapterDepthController()
        self.diagram_agent = DiagramAgent(api_key=gemini_key)
        self.formatter = FormatterAgent()
        self.exporter = DOCXExporter()

        tasks_db[slug] = {
            "status": "QUEUED",
            "progress": 0,
            "logs": [],
            "docx_url": "",
            "pdf_url": "",
            "readme_url": "",
            "completed": False
        }

    def log(self, message: str):
        logger.info(f"[{self.slug}] {message}")
        tasks_db[self.slug]["logs"].append(message)

    def set_progress(self, percent: int, status: str = None):
        tasks_db[self.slug]["progress"] = percent
        if status:
            tasks_db[self.slug]["status"] = status
            
        state_mapping = {
            "QUEUED": "draft",
            "INITIALIZING": "draft",
            "GENERATING_CONTENT": "draft",
            "REVIEWING_CONTENT": "generated",
            "GENERATING_DIAGRAMS": "reviewed",
            "AUDITING_CONSISTENCY": "reviewed",
            "COMPILING_DOCX": "reviewed",
            "FINALIZING": "reviewed",
            "COMPLETED": "exported",
            "FAILED": "draft"
        }
        
        updates = {"progress": percent}
        if status in state_mapping:
            updates["state"] = state_mapping[status]
            
        try:
            project_manager.update_project(self.slug, updates)
        except Exception as e:
            logger.error(f"Error updating project status: {e}")

    async def run_pipeline(self):
        try:
            self.set_progress(5, "INITIALIZING")
            self.log("Initializing textbook publishing pipeline...")
            
            chapters = self.toc_data.get("chapters", [])
            total_chapters = len(chapters)
            
            if total_chapters == 0:
                raise Exception("Table of Contents does not contain any chapters.")

            self.log("Bootstrapping book context registry...")
            self.context_manager.initialize_book(
                self.toc_data.get("title", "Academic Textbook"),
                self.toc_data.get("about_book", ""),
                self.toc_data
            )

            raw_chapters = {}
            reviewed_chapters = {}
            formatted_chapters = {}
            
            # PHASE 1: CONTENT WRITING
            self.set_progress(10, "GENERATING_CONTENT")
            self.log(f"--- AGENT 2 (Content Writer) STARTING ---")
            self.log(f"Writing first draft content for {total_chapters} chapters...")
            
            for index, ch in enumerate(chapters):
                ch_num = ch.get("chapter_number", index + 1)
                ch_title = ch.get("title", f"Chapter {ch_num}")
                ch_objectives = ch.get("objectives", [])
                subtopics = ch.get("subtopics", [])
                ch_key = str(ch_num)
                
                self.log(f"Writing Chapter {ch_num}: {ch_title}...")
                ch_context = self.context_manager.get_chapter_context(ch_num)
                
                self.log(f"Writing Chapter {ch_num} Introduction...")
                ch_intro = self.writer.generate_chapter_intro(ch_title, ch_num, ch_objectives, book_context=ch_context)
                ch_full_text = ch_intro + "\n\n"
                
                for sub_idx, sub in enumerate(subtopics):
                    sub_title = sub.get("title", "")
                    self.log(f"Writing Subtopic: {sub_title}...")
                    sub_content = self.writer.generate_subtopic_content(ch_title, ch_num, sub, book_context=ch_context)
                    ch_full_text += sub_content + "\n\n"
                
                self.log(f"Writing Chapter {ch_num} Summary & Questions...")
                ch_summary = self.writer.generate_chapter_summary(ch_title, ch_num)
                ch_full_text += ch_summary
                
                raw_chapters[ch_key] = ch_full_text
                current_percent = 10 + int((index + 1) / total_chapters * 30)
                self.set_progress(current_percent, "GENERATING_CONTENT")
                await asyncio.sleep(0.1)

            # PHASE 2: REVIEW
            self.set_progress(40, "REVIEWING_CONTENT")
            self.log(f"--- AGENT: Review Agent STARTING ---")
            review_reports = {}
            
            for index, ch in enumerate(chapters):
                ch_num = ch.get("chapter_number", index + 1)
                ch_title = ch.get("title", f"Chapter {ch_num}")
                ch_key = str(ch_num)
                
                self.log(f"Auditing Chapter {ch_num}: {ch_title}...")
                depth_report = self.depth_controller.analyze_chapter(raw_chapters[ch_key])
                depth_instructions = self.depth_controller.get_adjustment_instructions(depth_report)
                ch_context = self.context_manager.get_chapter_context(ch_num)
                
                loop = asyncio.get_event_loop()
                review_result = await loop.run_in_executor(
                    None,
                    self.reviewer.review_and_rewrite_chapter,
                    ch_num,
                    ch_title,
                    raw_chapters[ch_key],
                    ch_context,
                    depth_instructions
                )
                
                q_score = review_result.get("quality_score", 100)
                issues = review_result.get("issues_detected", [])
                rewritten_text = review_result.get("rewritten_content", raw_chapters[ch_key])
                ch_summary = review_result.get("chapter_summary", f"This chapter covers {ch_title}.")
                new_terminology = review_result.get("new_terminology", {})
                
                self.log(f"Chapter {ch_num} Quality Score: {q_score}/100")
                self.context_manager.register_chapter_results(ch_num, ch_summary, new_terminology)
                
                review_reports[ch_key] = {
                    "chapter_number": ch_num,
                    "title": ch_title,
                    "quality_score": q_score,
                    "issues_resolved": issues
                }
                
                reviewed_chapters[ch_key] = rewritten_text
                current_percent = 40 + int((index + 1) / total_chapters * 20)
                self.set_progress(current_percent, "REVIEWING_CONTENT")
                await asyncio.sleep(0.1)
                
            report_path = os.path.join(self.metadata_dir, "review_report.json")
            with open(report_path, "w", encoding="utf-8") as rf:
                json.dump(review_reports, rf, indent=2)

            # PHASE 3: DIAGRAMS
            self.set_progress(60, "GENERATING_DIAGRAMS")
            self.log(f"--- AGENT 3 (Diagram Agent) STARTING ---")
            fig_count = 1
            for index, ch in enumerate(chapters):
                ch_num = ch.get("chapter_number", index + 1)
                subtopics = ch.get("subtopics", [])
                
                for sub in subtopics:
                    if sub.get("needs_diagram", False):
                        diagram_topic = sub.get("diagram_topic", sub.get("title", ""))
                        self.log(f"Generating diagram figure {ch_num}.{fig_count}: {diagram_topic}...")
                        
                        img_filename = f"fig_{ch_num}_{fig_count}.png"
                        img_path = os.path.join(self.images_dir, img_filename)
                        
                        loop = asyncio.get_event_loop()
                        await loop.run_in_executor(
                            None, 
                            self.diagram_agent.generate_diagram, 
                            diagram_topic, 
                            img_path
                        )
                        fig_count += 1
                        
                current_percent = 60 + int((index + 1) / total_chapters * 15)
                self.set_progress(current_percent, "GENERATING_DIAGRAMS")
                await asyncio.sleep(0.1)

            # PHASE 4: FORMATTING
            self.set_progress(75, "AUDITING_CONSISTENCY")
            self.log(f"--- AGENT 4 (Formatter Agent) STARTING ---")
            
            for index, ch in enumerate(chapters):
                ch_num = ch.get("chapter_number", index + 1)
                ch_key = str(ch_num)
                formatted_text = self.formatter.format_content(reviewed_chapters[ch_key])
                
                ch_filename = f"chapter_{ch_num}.md"
                ch_path = os.path.join(self.chapters_dir, ch_filename)
                with open(ch_path, "w", encoding="utf-8") as f:
                    f.write(formatted_text)
                    
                formatted_chapters[ch_key] = formatted_text
                current_percent = 75 + int((index + 1) / total_chapters * 5)
                self.set_progress(current_percent, "AUDITING_CONSISTENCY")

            # PHASE 5: EXPORT
            self.set_progress(85, "COMPILING_DOCX")
            self.log(f"--- AGENT 5 (DOCX Export Agent) STARTING ---")
            
            meta = project_manager.get_project(self.slug)
            version = meta.get("version", "1.0.0")
            docx_filename = f"textbook_v{version}.docx"
            docx_path = os.path.join(self.exports_dir, docx_filename)
            template_path = os.path.join(BASE_DIR, "templates", "master_book_template.docx")
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                self.exporter.export_textbook,
                self.toc_data,
                formatted_chapters,
                self.images_dir,
                docx_path,
                template_path
            )
            
            self.log("Textbook exported to DOCX successfully.")
            self.set_progress(95, "FINALIZING")

            docx_url = f"/api/projects/{self.slug}/export/docx"
            tasks_db[self.slug]["docx_url"] = docx_url
            
            pdf_filename = f"textbook_v{version}.pdf"
            pdf_path = os.path.join(self.exports_dir, pdf_filename)
            pdf_url = ""
            if os.path.exists(pdf_path):
                pdf_url = f"/projects/{self.slug}/exports/{pdf_filename}"
                tasks_db[self.slug]["pdf_url"] = pdf_url

            project_manager.add_export(
                slug=self.slug,
                filename=docx_filename,
                docx_url=docx_url,
                pdf_url=pdf_url
            )

            self.set_progress(100, "COMPLETED")
            tasks_db[self.slug]["completed"] = True
            self.log("Textbook generation complete!")

        except Exception as e:
            logger.exception("Error during textbook generation")
            self.log(f"CRITICAL ERROR: {str(e)}")
            self.set_progress(100, "FAILED")

# ENDPOINTS

@app.get("/api/projects")
def list_projects():
    return project_manager.list_projects()

@app.get("/api/projects/{slug}")
def get_project(slug: str):
    try:
        return project_manager.get_project(slug)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Project not found")

@app.get("/api/projects/{slug}/export/docx")
def download_docx(slug: str):
    """Direct HTTP attachment download for DOCX export (supports Vercel serverless)."""
    try:
        project = project_manager.get_project(slug)
        exports_dir = os.path.join(PROJECTS_DIR, slug, "exports")
        if os.path.exists(exports_dir):
            files = [f for f in os.listdir(exports_dir) if f.endswith(".docx")]
            if files:
                latest_file = sorted(files)[-1]
                file_path = os.path.join(exports_dir, latest_file)
                return FileResponse(file_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", filename=latest_file)
        raise HTTPException(status_code=404, detail="Export not found")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/api/plan-toc")
def plan_toc(
    syllabus: str = Body(..., embed=True),
    target_chapters: int = Body(5, embed=True),
    openai_key: str = Body("", embed=True),
    gemini_key: str = Body("", embed=True)
):
    if not syllabus:
        raise HTTPException(status_code=400, detail="Syllabus text is required")
    planner = TOCPlanner(openai_key=openai_key, gemini_key=gemini_key)
    return planner.plan_toc(syllabus, target_chapters)

@app.post("/api/generate-textbook")
def generate_textbook(
    background_tasks: BackgroundTasks,
    toc_data: dict = Body(...),
    openai_key: str = Body(""),
    gemini_key: str = Body(""),
    slug: str = Body(None),
    syllabus: str = Body("")
):
    if slug:
        try:
            project_manager.get_project(slug)
            if toc_data.get("title"):
                project_manager.update_project(slug, {"book_name": toc_data["title"], "toc_data": toc_data})
        except FileNotFoundError:
            raise HTTPException(status_code=404, detail="Project not found")
    else:
        book_title = toc_data.get("title", "Academic Textbook")
        project = project_manager.create_project(book_title, syllabus, toc_data)
        slug = project["slug"]
    
    if slug in tasks_db and tasks_db[slug]["status"] not in ["COMPLETED", "FAILED"]:
        return {"task_id": slug, "status": tasks_db[slug]["status"]}
        
    task = BookGenerationTask(slug, toc_data, openai_key, gemini_key)
    background_tasks.add_task(task.run_pipeline)
    
    return {"task_id": slug, "status": "QUEUED"}

@app.get("/api/task-status/{task_id}")
def get_task_status(task_id: str):
    if task_id in tasks_db:
        return tasks_db[task_id]
        
    try:
        project = project_manager.get_project(task_id)
        docx_url = f"/api/projects/{task_id}/export/docx"
        status = "COMPLETED" if project.get("state") == "exported" else "QUEUED"
        
        tasks_db[task_id] = {
            "status": status,
            "progress": project.get("progress", 0),
            "logs": [f"[System] Loaded project status. State: {project.get('state')}"],
            "docx_url": docx_url,
            "pdf_url": "",
            "readme_url": "",
            "completed": (project.get("state") == "exported")
        }
        return tasks_db[task_id]
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Task not found")

@app.get("/api/stream-progress/{task_id}")
def stream_progress(task_id: str):
    if task_id not in tasks_db:
        try:
            get_task_status(task_id)
        except HTTPException:
            raise HTTPException(status_code=404, detail="Task not found")

    async def event_generator():
        last_log_index = 0
        while True:
            task = tasks_db.get(task_id)
            if not task:
                break
                
            current_logs = task["logs"]
            new_logs = current_logs[last_log_index:]
            last_log_index = len(current_logs)
            
            for log_line in new_logs:
                yield f"data: {{\"type\": \"log\", \"message\": {json.dumps(log_line)}}}\n\n"

            yield f"data: {{\"type\": \"progress\", \"percent\": {task['progress']}, \"status\": \"{task['status']}\"}}\n\n"
            
            if task["completed"] or task["status"] in ["COMPLETED", "FAILED"]:
                yield f"data: {{\"type\": \"completion\", \"completed\": true, \"status\": \"{task['status']}\", \"docx_url\": \"{task['docx_url']}\", \"pdf_url\": \"{task['pdf_url']}\", \"readme_url\": \"{task['readme_url']}\"}}\n\n"
                break
                
            await asyncio.sleep(0.5)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
