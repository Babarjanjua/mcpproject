from fastapi import APIRouter
from backend.agents.progress_agent import ProgressAgent

router = APIRouter()
progress_agent = ProgressAgent()

@router.post("/progress")
def update_progress(user_id: str, course_id: str, module_id: str, completion: float):
    # Use the agent to track progress (mock for now)
    result = progress_agent.track_progress(user_id, course_id, module_id, completion)
    return result 