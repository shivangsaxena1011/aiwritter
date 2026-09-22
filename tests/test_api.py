import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_health_endpoint(client):
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "ai_mode" in data

def test_estimate_endpoint(client):
    payload = {
        "title": "Quantum Information",
        "writing_depth": "Standard",
        "generate_images": True,
        "toc": {
            "units": [
                {
                    "name": "Unit 1: Foundations",
                    "topics": [
                        {
                            "name": "Qubits and Gates",
                            "subtopics": ["Hadamard Gate", "Phase Gate"]
                        }
                    ]
                }
            ]
        }
    }
    res = client.post("/api/v1/books/estimate", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["total_units"] == 1
    assert data["total_subtopics"] == 2
    assert data["estimated_words"] > 0
    assert data["estimated_pages"] > 0

def test_create_and_fetch_book(client):
    payload = {
        "title": "Autonomous Systems Engineering",
        "subtitle": "Robotics and Control",
        "author": "Prof. Robotics",
        "academic_level": "Graduate",
        "writing_depth": "Detailed",
        "toc": {
            "units": [
                {
                    "name": "Unit 1: Kinematics",
                    "topics": [
                        {
                            "name": "Forward Kinematics",
                            "subtopics": ["DH Parameters", "Transformation Matrices"]
                        }
                    ]
                }
            ]
        }
    }
    res = client.post("/api/v1/books", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert "id" in data
    book_id = data["id"]

    # Fetch book
    fetch_res = client.get(f"/api/v1/books/{book_id}")
    assert fetch_res.status_code == 200
    book_data = fetch_res.json()
    assert book_data["title"] == "Autonomous Systems Engineering"
    assert len(book_data["units"]) == 1
    assert len(book_data["units"][0]["topics"]) == 1

def test_job_dispatch_and_cancel(client):
    # 1. Create book
    book_res = client.post("/api/v1/books", json={
        "title": "Parallel Computing",
        "toc": {
            "units": [{
                "name": "Unit 1: Concurrency",
                "topics": [{
                    "name": "Threads and Processes",
                    "subtopics": ["Race Conditions"]
                }]
            }]
        }
    })
    book_id = book_res.json()["id"]

    # 2. Create Job
    job_res = client.post("/api/v1/jobs", json={"book_id": book_id})
    assert job_res.status_code == 201
    job_data = job_res.json()
    job_id = job_data["id"]
    assert job_data["status"] in ["QUEUED", "PLANNING", "GENERATING"]

    # 3. Check Job
    get_res = client.get(f"/api/v1/jobs/{job_id}")
    assert get_res.status_code == 200
    assert get_res.json()["book_id"] == book_id

    # 4. Cancel Job
    cancel_res = client.post(f"/api/v1/jobs/{job_id}/cancel")
    assert cancel_res.status_code in [200, 400]  # If already completed or cancelled

def test_legacy_compat_endpoints(client):
    # Legacy /api/parse-syllabus
    parse_res = client.post("/api/parse-syllabus", json={
        "text": "1. *Chapter 1: Intro*\n- Background\n2. *Chapter 2: Methods*\n- Tools"
    })
    assert parse_res.status_code == 200
    parse_data = parse_res.json()
    assert "units" in parse_data
