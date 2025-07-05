from fastapi import APIRouter
from backend.agents.learning_path_agent import LearningPathAgent

router = APIRouter()
learning_path_agent = LearningPathAgent()

@router.post("/learning-path")
def generate_learning_path(user_profile: dict = {}, courses: list = []):
    # Use the agent to generate a learning path (mock for now)
    path = learning_path_agent.generate_learning_path(user_profile, courses)
    return {"learning_path": path} 