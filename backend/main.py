from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.courses import router as courses_router
from backend.api.learning_path import router as learning_path_router
from backend.api.progress import router as progress_router
from backend.api.quiz import router as quiz_router
from backend.api.sync import router as sync_router
from backend.db.database import create_tables
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Multilingual Learning Path Generator",
    description="An AI-powered learning platform with MCP integration",
    version="1.0.0"
)

# Add CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(courses_router)
app.include_router(learning_path_router)
app.include_router(progress_router)
app.include_router(quiz_router)
app.include_router(sync_router)

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    create_tables()

@app.get("/")
def read_root():
    return {
        "message": "Backend is running!",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"} 