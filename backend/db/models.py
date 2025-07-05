from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    preferred_language = Column(String, default="en")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="user")
    progress_records = relationship("ProgressRecord", back_populates="user")
    learning_paths = relationship("LearningPath", back_populates="user")

class Course(Base):
    __tablename__ = "courses"
    
    id = Column(String, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    provider = Column(String)
    language = Column(String, default="en")
    difficulty = Column(String, default="beginner")
    duration = Column(String)
    rating = Column(Float, default=0.0)
    metadata = Column(JSON)  # Store additional course data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    enrollments = relationship("Enrollment", back_populates="course")
    progress_records = relationship("ProgressRecord", back_populates="course")

class Enrollment(Base):
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")  # active, completed, dropped
    completion_percentage = Column(Float, default=0.0)
    
    # Relationships
    user = relationship("User", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")

class ProgressRecord(Base):
    __tablename__ = "progress_records"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    module_id = Column(String, nullable=False)
    completion_percentage = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="progress_records")
    course = relationship("Course", back_populates="progress_records")

class LearningPath(Base):
    __tablename__ = "learning_paths"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    path_data = Column(JSON)  # Store the learning path structure
    status = Column(String, default="active")  # active, completed, paused
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="learning_paths")

class Quiz(Base):
    __tablename__ = "quizzes"
    
    id = Column(Integer, primary_key=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False)
    module_id = Column(String, nullable=False)
    title = Column(String, nullable=False)
    questions = Column(JSON)  # Store quiz questions and answers
    created_at = Column(DateTime, default=datetime.utcnow)

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"), nullable=False)
    score = Column(Float, nullable=False)
    answers = Column(JSON)  # Store user's answers
    completed_at = Column(DateTime, default=datetime.utcnow) 