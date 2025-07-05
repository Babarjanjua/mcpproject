from fastapi import APIRouter
from backend.agents.quiz_agent import QuizAgent

router = APIRouter()
quiz_agent = QuizAgent()

@router.post("/quiz")
def generate_quiz(course_id: str, module_id: str):
    # Use the agent to generate a quiz (mock for now)
    quiz = quiz_agent.generate_quiz(course_id, module_id)
    return {"quiz": quiz} 