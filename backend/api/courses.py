from fastapi import APIRouter
from backend.agents.course_agent import CourseAgent

router = APIRouter()
course_agent = CourseAgent()

@router.get("/courses")
async def list_courses(query: str = "", language: str = "en", difficulty: str = "beginner"):
    # Use the agent to get courses (now with MCP integration)
    courses = await course_agent.recommend_courses(user_profile=None, query=query, language=language, difficulty=difficulty)
    return {"courses": courses}

@router.get("/courses/{course_id}")
async def get_course_details(course_id: str):
    # Get detailed information about a specific course
    course_details = await course_agent.get_course_details(course_id)
    return course_details 