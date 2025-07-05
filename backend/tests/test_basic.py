import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert response.json()["message"] == "Backend is running!"

def test_courses_endpoint():
    """Test the courses endpoint"""
    response = client.get("/courses")
    assert response.status_code == 200
    assert "courses" in response.json()

def test_courses_with_params():
    """Test the courses endpoint with query parameters"""
    response = client.get("/courses?query=python&language=en&difficulty=beginner")
    assert response.status_code == 200
    assert "courses" in response.json()

def test_course_details_endpoint():
    """Test the course details endpoint"""
    response = client.get("/courses/test-course-id")
    assert response.status_code == 200

def test_learning_path_endpoint():
    """Test the learning path endpoint"""
    data = {
        "user_profile": {"interests": ["programming"]},
        "courses": []
    }
    response = client.post("/learning-path", json=data)
    assert response.status_code == 200
    assert "learning_path" in response.json()

def test_progress_endpoint():
    """Test the progress endpoint"""
    data = {
        "user_id": "test_user",
        "course_id": "test_course",
        "module_id": "test_module",
        "completion": 75.0
    }
    response = client.post("/progress", json=data)
    assert response.status_code == 200

def test_quiz_endpoint():
    """Test the quiz endpoint"""
    data = {
        "course_id": "test_course",
        "module_id": "test_module"
    }
    response = client.post("/quiz", json=data)
    assert response.status_code == 200
    assert "quiz" in response.json()

def test_sync_endpoint():
    """Test the sync endpoint"""
    data = {
        "user_id": "test_user",
        "course_id": "test_course",
        "progress_data": {"sync": True}
    }
    response = client.post("/sync", json=data)
    assert response.status_code == 200 