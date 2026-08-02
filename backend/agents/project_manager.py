import os
import re
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from backend.agents.book_context_manager import BookContextManager

logger = logging.getLogger(__name__)

def slugify(text: str) -> str:
    """Converts a string to a URL/folder-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text

class ProjectManager:
    def __init__(self, projects_dir: str):
        self.projects_dir = projects_dir
        try:
            os.makedirs(self.projects_dir, exist_ok=True)
        except Exception as e:
            logger.warning(f"Could not create projects dir {projects_dir}: {e}")

    def list_projects(self) -> List[Dict[str, Any]]:
        """Lists all projects by reading project_metadata.json from each subdirectory."""
        projects = []
        if not os.path.exists(self.projects_dir):
            return projects

        for folder_name in os.listdir(self.projects_dir):
            folder_path = os.path.join(self.projects_dir, folder_name)
            if not os.path.isdir(folder_path):
                continue
            
            metadata_path = os.path.join(folder_path, "metadata", "project_metadata.json")
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                        projects.append(meta)
                except Exception as e:
                    logger.error(f"Failed to read project metadata for {folder_name}: {e}")
        
        projects.sort(key=lambda x: x.get("updated_at", x.get("created_at", "")), reverse=True)
        return projects

    def get_project_dir(self, slug: str) -> str:
        return os.path.join(self.projects_dir, slug)

    def create_project(self, book_name: str, syllabus: str, toc_data: dict) -> Dict[str, Any]:
        """Creates directory structure and initial metadata for a new textbook project."""
        base_slug = slugify(book_name) or "untitled-textbook"
        slug = base_slug
        
        counter = 1
        while os.path.exists(self.get_project_dir(slug)):
            slug = f"{base_slug}-{counter}"
            counter += 1

        project_dir = self.get_project_dir(slug)
        
        os.makedirs(os.path.join(project_dir, "chapters"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "tables"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "metadata"), exist_ok=True)
        os.makedirs(os.path.join(project_dir, "exports"), exist_ok=True)

        now = datetime.utcnow().isoformat() + "Z"
        
        metadata = {
            "book_name": book_name,
            "slug": slug,
            "created_at": now,
            "updated_at": now,
            "state": "draft",
            "version": "1.0.0",
            "progress": 0,
            "syllabus": syllabus,
            "toc_data": toc_data,
            "export_history": []
        }
        
        metadata_path = os.path.join(project_dir, "metadata", "project_metadata.json")
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        context_path = os.path.join(project_dir, "metadata", "book_context.json")
        context_manager = BookContextManager(context_path)
        context_manager.initialize_book(book_name, toc_data.get("about_book", ""), toc_data)

        logger.info(f"Created project {book_name} with slug {slug}")
        return metadata

    def get_project(self, slug: str) -> Dict[str, Any]:
        """Loads and returns project metadata."""
        project_dir = self.get_project_dir(slug)
        metadata_path = os.path.join(project_dir, "metadata", "project_metadata.json")
        
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Project with slug {slug} not found.")
            
        with open(metadata_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def update_project(self, slug: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Updates specific fields in project metadata on disk."""
        project_dir = self.get_project_dir(slug)
        metadata_path = os.path.join(project_dir, "metadata", "project_metadata.json")
        
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Project with slug {slug} not found.")
            
        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        for k, v in updates.items():
            meta[k] = v
            
        meta["updated_at"] = datetime.utcnow().isoformat() + "Z"
        
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
            
        return meta

    def add_export(self, slug: str, filename: str, docx_url: str, pdf_url: str = "") -> Dict[str, Any]:
        """Adds an export record to history and bumps patch version."""
        project_dir = self.get_project_dir(slug)
        metadata_path = os.path.join(project_dir, "metadata", "project_metadata.json")
        
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Project with slug {slug} not found.")
            
        with open(metadata_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
            
        current_ver = meta.get("version", "1.0.0")
        now = datetime.utcnow().isoformat() + "Z"
        
        export_record = {
            "version": current_ver,
            "exported_at": now,
            "docx_url": docx_url,
            "pdf_url": pdf_url,
            "filename": filename
        }
        
        if "export_history" not in meta:
            meta["export_history"] = []
            
        meta["export_history"].append(export_record)
        meta["state"] = "exported"
        meta["progress"] = 100
        
        try:
            parts = current_ver.split(".")
            if len(parts) == 3:
                parts[2] = str(int(parts[2]) + 1)
                meta["version"] = ".".join(parts)
        except Exception:
            pass
            
        meta["updated_at"] = now
        
        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
            
        return meta
