import logging
import os
from typing import Any, Dict, Optional
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from scholarly import search_scholarly_literature
from analyzer import analyze_research_project
from sample_data import SAMPLE_PROJECTS
from export_service import generate_markdown_report

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("researchecho")

# Simple .env loader without external dependencies
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SEMANTIC_SCHOLAR_API_KEY = os.getenv("SEMANTIC_SCHOLAR_API_KEY")

app = FastAPI(
    title="ResearchEcho API",
    description="Evidence-First AI Research Assistant & Literature Gap Engine",
    version="1.0.0"
)

# Enable CORS for local dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalysisRequest(BaseModel):
    title: str = Field(..., min_length=4, max_length=300, description="Project title")
    abstract: str = Field(..., min_length=20, max_length=5000, description="Project abstract or idea description")
    domain: str = Field(default="Computer Science", description="Target academic research domain")

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3)
    domain: Optional[str] = "General"
    limit: Optional[int] = 6

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "ResearchEcho Backend",
        "scholarly_provider": "OpenAlex Works API (Active, Free Tier)",
        "gemini_configured": bool(GEMINI_API_KEY),
        "semantic_scholar_configured": bool(SEMANTIC_SCHOLAR_API_KEY)
    }

@app.get("/api/presets")
def get_presets():
    """Return pre-configured sample projects for quick hackathon demonstrations."""
    return {"presets": SAMPLE_PROJECTS}

@app.post("/api/search")
def search_papers(payload: SearchRequest):
    """Retrieve authentic scholarly literature without fabricating citations."""
    papers = search_scholarly_literature(
        query=payload.query,
        domain=payload.domain,
        semantic_scholar_key=SEMANTIC_SCHOLAR_API_KEY,
        limit=payload.limit or 6
    )
    return {
        "query": payload.query,
        "count": len(papers),
        "papers": papers
    }

@app.post("/api/analyze")
def analyze_idea(payload: AnalysisRequest):
    """
    Main research analysis pipeline:
    1. Retrieve real research papers via scholarly API
    2. Extract comparative dimensions
    3. Synthesize evidence-backed research gaps with exact quotations
    4. Verify claims against source texts
    5. Generate uncertainty and coverage metrics
    """
    clean_title = payload.title.strip()
    clean_abstract = payload.abstract.strip()

    if len(clean_title) < 4:
        raise HTTPException(status_code=400, detail="Title must be at least 4 characters.")
    if len(clean_abstract) < 20:
        raise HTTPException(status_code=400, detail="Abstract or description must be at least 20 characters.")

    # Formulate scholarly search query
    search_query = f"{clean_title}"

    logger.info(f"Initiating research analysis for: '{clean_title}' in domain '{payload.domain}'")
    papers = search_scholarly_literature(
        query=search_query,
        domain=payload.domain,
        semantic_scholar_key=SEMANTIC_SCHOLAR_API_KEY,
        limit=6
    )

    if not papers:
        # Retry with simpler keywords
        words = [w for w in clean_title.split() if len(w) > 3][:4]
        fallback_query = " ".join(words)
        papers = search_scholarly_literature(
            query=fallback_query,
            domain=payload.domain,
            semantic_scholar_key=SEMANTIC_SCHOLAR_API_KEY,
            limit=6
        )

    analysis_result = analyze_research_project(
        title=clean_title,
        abstract=clean_abstract,
        domain=payload.domain,
        papers=papers,
        gemini_api_key=GEMINI_API_KEY
    )

    return analysis_result

@app.post("/api/export/markdown")
def export_markdown(payload: Dict[str, Any]):
    """Generate downloadable Markdown research report."""
    md_content = generate_markdown_report(payload)
    return Response(
        content=md_content,
        media_type="text/markdown",
        headers={"Content-Disposition": "attachment; filename=researchecho-report.md"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
