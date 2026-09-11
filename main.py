from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.config import settings
from app.core.database import check_db_connection
from app.models.schemas import HealthResponse
from app.api.router import api_v1_router

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=settings.APP_NAME,
    description="Enterprise Intelligent Data & Document Assistant API",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static Files & Templates Mounting
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Mount MkDocs site if built
site_dir = BASE_DIR / "site"
if site_dir.exists():
    app.mount("/site", StaticFiles(directory=str(site_dir), html=True), name="mkdocs-site")


# Root Web Portal
@app.get("/", response_class=HTMLResponse, tags=["Web Portal"])
def render_home(request: Request):
    """Renders the DataMind AI glassmorphic web dashboard."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
        }
    )


# Telemetry Health Endpoint
@app.get("/api/health", response_model=HealthResponse, tags=["Telemetry"])
def health_check():
    """Returns real-time service health, version, and database connectivity."""
    db_ok = check_db_connection()
    return HealthResponse(
        status="healthy" if db_ok else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database_connected=db_ok,
    )


# Include API v1 Router
app.include_router(api_v1_router)