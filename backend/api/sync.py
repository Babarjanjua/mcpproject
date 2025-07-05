from fastapi import APIRouter
from backend.agents.classroom_agent import ClassroomAgent

router = APIRouter()
classroom_agent = ClassroomAgent()

@router.post("/sync")
def sync_with_classroom(user_id: str, course_id: str, progress_data: dict = {}):
    # Use the agent to sync with Google Classroom (mock for now)
    result = classroom_agent.sync_with_classroom(user_id, course_id, progress_data)
    return result 