from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Create FastAPI app
app = FastAPI(
    title="Multilingual Learning Path Generator API",
    description="AI-powered learning path generation",
    version="1.0.0",
    debug=DEBUG
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Multilingual Learning Path Generator API",
        "version": "1.0.0",
        "environment": ENVIRONMENT,
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "database": "connected",
        "mcp_client": "available"
    }

# Mock API endpoints
@app.get("/courses")
async def get_courses(query: str = "", language: str = "en", difficulty: str = "beginner"):
    """Get courses (mock implementation)"""
    return {
        "courses": [
            {
                "id": "course-1",
                "title": f"Sample Course for '{query}'",
                "description": "This is a sample course description",
                "language": language,
                "difficulty": difficulty,
                "provider": "SampleProvider",
                "duration": "8 weeks",
                "rating": 4.5
            }
        ]
    }

@app.post("/learning-path")
async def generate_learning_path(data: dict):
    """Generate learning path (mock implementation)"""
    return {
        "learning_path": [
            {
                "title": "Step 1: Foundation",
                "description": "Learn the basics",
                "duration": "2 weeks"
            },
            {
                "title": "Step 2: Core Concepts", 
                "description": "Master core concepts",
                "duration": "4 weeks"
            }
        ]
    }

@app.post("/progress")
async def update_progress(data: dict):
    """Update progress (mock implementation)"""
    return {"status": "success", "message": "Progress updated"}

@app.post("/quiz")
async def generate_quiz(data: dict):
    """Generate quiz (mock implementation)"""
    return {
        "quiz": {
            "questions": [
                {
                    "question": "Sample question?",
                    "options": ["A", "B", "C", "D"],
                    "correct": "A"
                }
            ]
        }
    }

@app.post("/sync")
async def sync_with_classroom(data: dict):
    """Sync with Google Classroom (mock implementation)"""
    return {"status": "success", "message": "Synced with Google Classroom"}

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": "Something went wrong"}
    ) 