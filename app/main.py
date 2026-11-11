from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

# Tamam models import karna lazmi hai taake Base.metadata database tables create kar sake
import app.models


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application Lifespan:
    - Startup: Database tables automatically create karta hai agar pehle se na bane hon.
    - Shutdown: Cleanup logic handle karta hai.
    """
    print("Starting up: Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")
    yield
    print("Application shutdown complete.")


# FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="TaskPulse - Modern Task & Project Management API with Role-Based Access Control",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Middleware (Frontend aur Swagger UI access ke liye)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Central API Router mount karein (/api/v1)
app.include_router(api_router, prefix=settings.API_V1_STR)


# Root Health Check endpoint
@app.get("/", tags=["Health Check"])
def health_check():
    """Server status check karne ke liye simple endpoint"""
    return {
        "status": "online",
        "app_name": settings.PROJECT_NAME,
        "docs_url": "/docs",
        "api_v1_prefix": settings.API_V1_STR
    }
