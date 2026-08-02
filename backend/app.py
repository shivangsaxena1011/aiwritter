import asyncio
import uuid
import os
import traceback
import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any

from backend.agents.content_writer import ContentWriter
from backend.agents.diagram_agent import DiagramAgent
from backend.agents.docx_exporter import DocxExporter

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

base_dir = os.path.dirname(os.path.dirname(__file__))
frontend_dir = os.path.join(base_dir, "frontend")
os.makedirs(frontend_dir, exist_ok=True)

output_dir = os.path.join(base_dir, "output")
os.makedirs(output_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

tasks: Dict[str, Dict[str, Any]] = {}
task_queues: Dict[str, asyncio.Queue] = {}

class GenerateRequest(BaseModel):
    title: str
    api_key: str
    toc: dict
    generate_images: bool = False

class ParseSyllabusRequest(BaseModel):
    text: str
    api_key: str

@app.post("/api/parse-syllabus")
async def parse_syllabus_ai(req: ParseSyllabusRequest):
    try:
        from google import genai
        from google.genai import types
        
        client = genai.Client(api_key=req.api_key)
        prompt = f"""Analyze this textbook outline/syllabus and extract a structured Table of Contents in JSON format.
INPUT TEXT:
{req.text}

RETURN ONLY A VALID JSON OBJECT matching this EXACT structure (no markdown, no code fences):
{{
  "title": "Extracted or inferred book title",
  "units": [
    {{
      "name": "Unit/Chapter 1 Title",
      "topics": [
        {{
          "name": "Topic 1.1 Title",
          "subtopics": ["Subtopic 1.1.1 Title", "Subtopic 1.1.2 Title"]
        }}
      ]
    }}
  ]
}}
"""
        response = await asyncio.to_thread(
            client.models.generate_content,
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.2,
                response_mime_type="application/json"
            )
        )
        data = json.loads(response.text)
        return data
    except Exception as e:
        return {"error": f"AI Parsing failed: {str(e)}"}

@app.get("/", response_class=HTMLResponse)
async def get_index():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        with open(index_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>AI Book Writer</h1><p>Ensure frontend is built and located at /frontend.</p>"

@app.post("/api/generate")
async def generate_book(req: GenerateRequest):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "status": "running",
        "progress": 0,
        "logs": [],
        "error": None,
        "download_file": None
    }
    task_queues[task_id] = asyncio.Queue()
    
    asyncio.create_task(run_pipeline(task_id, req.title, req.api_key, req.toc, req.generate_images))
    return {"task_id": task_id}

@app.get("/api/stream/{task_id}")
async def stream_logs(task_id: str, request: Request):
    if task_id not in tasks:
        return {"error": "Task not found"}
        
    async def event_generator():
        task = tasks[task_id]
        
        # Check task status BEFORE starting stream
        if task["status"] in ["complete", "error"]:
            event_data = {'type': task['status'], 'message': 'Task finished', 'progress': task['progress']}
            if task.get("download_file"):
                event_data["download_file"] = task["download_file"]
            yield f"data: {json.dumps(event_data)}\n\n"
            return

        q = task_queues.get(task_id)
        if not q:
            return

        while True:
            if await request.is_disconnected():
                break
            try:
                event = await asyncio.wait_for(q.get(), timeout=15.0)
                yield f"data: {event}\n\n"
                
                event_data = json.loads(event)
                if event_data.get("type") in ["complete", "error"]:
                    break
            except asyncio.TimeoutError:
                # Keepalive comments every 15 seconds to prevent timeout
                yield ": keepalive\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.get("/api/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(output_dir, filename)
    if os.path.exists(file_path):
        return FileResponse(
            path=file_path, 
            filename=filename, 
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    return {"error": "File not found"}

async def run_pipeline(task_id: str, title: str, api_key: str, toc: dict, generate_images: bool):
    task = tasks[task_id]
    q = task_queues[task_id]
    
    async def send_event(type_: str, message: str, progress: float = None):
        if progress is not None:
            task["progress"] = progress
        task["logs"].append(message)
        event_data = {"type": type_, "message": message, "progress": task["progress"]}
        # Include download_file in complete events
        if type_ == "complete" and task.get("download_file"):
            event_data["download_file"] = task["download_file"]
        event_json = json.dumps(event_data)
        await q.put(event_json)

    try:
        await send_event("log", f"Starting generation for book: {title}", 0)
        
        writer = ContentWriter(api_key)
        diagrammer = DiagramAgent(api_key)
        exporter = DocxExporter()
        
        # Calculate total steps
        total_steps = 1 # Export step
        for unit in toc.get("units", []):
            total_steps += 1 # Unit intro
            for topic in unit.get("topics", []):
                total_steps += len(topic.get("subtopics", []))
                
        current_step = 0
        content_sections = []
        
        for unit in toc.get("units", []):
            unit_name = unit.get("name", "Unknown Unit")
            topics_list = [t.get("name", "Unknown Topic") for t in unit.get("topics", [])]
            
            await send_event("log", f"✍️ Writing Introduction for Unit: {unit_name}", (current_step / total_steps) * 100)
            try:
                intro_content = await asyncio.to_thread(writer.generate_unit_introduction, title, unit_name, topics_list)
                content_sections.append({
                    "unit": unit_name,
                    "is_intro": True,
                    "content": intro_content,
                    "image_path": None,
                    "image_prompt": None
                })
            except Exception as e:
                await send_event("error", f"Failed to generate intro for {unit_name}: {str(e)}")
            current_step += 1
            
            for topic in unit.get("topics", []):
                topic_name = topic.get("name", "Unknown Topic")
                is_first_in_topic = True
                
                for subtopic in topic.get("subtopics", []):
                    await send_event("log", f"✍️ Writing: {unit_name} > {topic_name} > {subtopic}", (current_step / total_steps) * 100)
                    try:
                        prev_context = content_sections[-1]["content"][-1000:] if content_sections else ""
                        subtopic_content = await asyncio.to_thread(
                            writer.generate_subtopic_content, title, unit_name, topic_name, subtopic, prev_context
                        )
                        
                        img_path = None
                        img_prompt = None
                        
                        if generate_images:
                            await send_event("log", f"🎨 Generating diagram for: {subtopic}")
                            out_img = os.path.join(output_dir, f"img_{uuid.uuid4().hex[:8]}.png")
                            diag_res = await asyncio.to_thread(
                                diagrammer.generate_diagram, topic_name, subtopic, out_img
                            )
                            if diag_res.get("success"):
                                img_path = diag_res["path"]
                            else:
                                img_prompt = diag_res.get("prompt")
                                
                        content_sections.append({
                            "unit": unit_name,
                            "topic": topic_name,
                            "subtopic": subtopic,
                            "is_first_in_topic": is_first_in_topic,
                            "content": subtopic_content,
                            "image_path": img_path,
                            "image_prompt": img_prompt
                        })
                        is_first_in_topic = False
                    except Exception as e:
                        await send_event("error", f"Error in {subtopic}: {str(e)}")
                        
                    current_step += 1

        await send_event("log", "📚 Compiling final DOCX...", (current_step / total_steps) * 100)
        
        safe_title = title.replace(' ', '_').replace('/', '_')
        output_filename = f"{safe_title}_{uuid.uuid4().hex[:6]}.docx"
        output_filepath = os.path.join(output_dir, output_filename)
        
        await asyncio.to_thread(exporter.export, title, toc, content_sections, [], output_filepath)
        
        task["status"] = "complete"
        task["download_file"] = output_filename
        await send_event("complete", "Generation completed successfully!", 100)
        
    except Exception as e:
        err_msg = str(e)
        task["status"] = "error"
        task["error"] = err_msg
        traceback.print_exc()
        await send_event("error", f"Pipeline failed: {err_msg}", task.get("progress", 0))
