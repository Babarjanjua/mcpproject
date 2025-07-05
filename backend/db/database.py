from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Database URL - use SQLite for development, can be changed to PostgreSQL for production
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./learning_path_generator.db")

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """Initialize database tables"""
    try:
        # Import models to ensure they're registered
        from .models import User, Course, Enrollment, Progress, LearningPath, Quiz, QuizAttempt
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)

def drop_tables():
    """Drop all database tables"""
    Base.metadata.drop_all(bind=engine) 