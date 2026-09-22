import os
import pytest
from docx import Document
from backend.app.services.document.docx_engine import DocxEngine

def test_docx_export_with_native_tables(tmp_path):
    output_docx = str(tmp_path / "output_test_book.docx")

    metadata = {
        "title": "Principles of Cloud Architecture",
        "subtitle": "Scalable, Resilient Distributed Systems",
        "author": "Dr. Alan Turing & AI Academic Press",
        "academic_level": "Graduate",
        "citation_style": "IEEE"
    }

    sections = [
        {
            "unit": "Unit 1: Cloud Paradigms",
            "topic": "Microservices vs Monoliths",
            "subtopic": "Architectural Tradeoffs",
            "content": """
### Microservices vs Monoliths: A Detailed Trade-off Matrix

When designing modern distributed applications, system architects face fundamental choices regarding deployment topology.

| Metric | Monolith Architecture | Microservice Architecture |
|---|---|---|
| Deployment Velocity | Low (coupled releases) | High (independent CI/CD) |
| Latency Overhead | Sub-microsecond (in-memory) | Milliseconds (network RPC/HTTP) |
| Operational Complexity | Low to Medium | High (distributed tracing, mesh) |
| Data Consistency | ACID (single DB transactions) | Eventual Consistency (Saga / 2PC) |

As shown above, microservices decouple team boundaries at the expense of distributed complexity.

> Note: Care must be taken to avoid distributed monolithic topologies.
            """,
            "image_path": None
        }
    ]

    engine = DocxEngine()
    result_path = engine.generate_document(
        metadata=metadata,
        sections=sections,
        output_path=output_docx
    )

    assert os.path.exists(result_path)
    assert os.path.getsize(result_path) > 1000

    # Inspect generated document
    doc = Document(result_path)
    # Check that at least one native Word table was added
    assert len(doc.tables) >= 1

    table = doc.tables[0]
    assert len(table.rows) == 5  # 1 header + 4 data rows
    assert len(table.columns) == 3
    # Check cell text
    assert "Metric" in table.rows[0].cells[0].text
    assert "Monolith Architecture" in table.rows[0].cells[1].text
