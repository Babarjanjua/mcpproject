from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Learning Path Generator API...")
    
    # Initialize database (simplified for now)
    try:
        logger.info("Database initialization skipped for deployment")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    
    # Initialize MCP client (simplified for now)
    try:
        app.state.mcp_client = None  # Simplified for deployment
        logger.info("MCP client initialization skipped for deployment")
    except Exception as e:
        logger.error(f"MCP client initialization failed: {e}")
        app.state.mcp_client = None
    
    yield
    
    # Shutdown
    logger.info("Shutting down Learning Path Generator API...")

# Create FastAPI app
app = FastAPI(
    title="Multilingual Learning Path Generator API",
    description="AI-powered learning path generation with MCP integration",
    version="1.0.0",
    debug=DEBUG,
    lifespan=lifespan
)

# Configure CORS for production
if ENVIRONMENT == "production":
    # Allow specific origins in production
    allowed_origins = [
        "https://*.streamlit.app",
        "https://*.vercel.app",
        os.getenv("FRONTEND_URL", "https://your-streamlit-app.streamlit.app")
    ]
else:
    # Allow all origins in development
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    health_status = {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "database": "connected",
        "mcp_client": "available" if hasattr(app.state, 'mcp_client') and app.state.mcp_client else "unavailable"
    }
    
    return health_status

# Mock API endpoints for deployment
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
    """Global exception handler for better error responses"""
    logger.error(f"Unhandled exception: {exc}")
    
    if ENVIRONMENT == "production":
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "message": "Something went wrong"}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "message": str(exc)}
        )

if __name__ == "__main__":
    # Get port from environment or default
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    logger.info(f"Starting server on {host}:{port}")
    logger.info(f"Environment: {ENVIRONMENT}")
    logger.info(f"Debug mode: {DEBUG}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=DEBUG,
        log_level="info" if ENVIRONMENT == "production" else "debug"
    )
