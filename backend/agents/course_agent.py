# Course Recommendation/Search Agent (LangGraph/LangChain)
from backend.services.mooc_mcp_client import MOOCMCPClient
from backend.services.real_apis import RealAPIService
from backend.agents.advanced_agents import AdvancedCourseAgent
import asyncio

class CourseAgent:
    def __init__(self):
        self.mooc_client = MOOCMCPClient()
        self.real_api_service = RealAPIService()
        self.advanced_agent = AdvancedCourseAgent()

    async def recommend_courses(self, user_profile, query, language, difficulty):
        """Recommend courses using advanced AI and real APIs"""
        try:
            # Get courses from multiple sources
            all_courses = []
            
            # Get courses from MCP client (fallback)
            mcp_courses = await self.mooc_client.search_courses(query, language, difficulty)
            all_courses.extend(mcp_courses)
            
            # Get courses from real APIs
            real_courses = await self.get_real_courses(query, language, difficulty)
            all_courses.extend(real_courses)
            
            # Use advanced AI agent to recommend courses
            if user_profile and all_courses:
                recommended_courses = await self.advanced_agent.recommend_courses(user_profile, all_courses)
                return recommended_courses
            
            # Return all courses if no user profile or AI recommendation fails
            return all_courses[:10]
            
        except Exception as e:
            print(f"Error in CourseAgent: {e}")
            return []
    
    async def get_real_courses(self, query, language, difficulty):
        """Get courses from real APIs"""
        try:
            all_courses = []
            
            # Get courses from edX
            edx_courses = await self.real_api_service.search_edx_courses(query, language)
            all_courses.extend(edx_courses)
            
            # Get courses from MIT OCW
            mit_courses = await self.real_api_service.search_mit_ocw_courses(query)
            all_courses.extend(mit_courses)
            
            # Get courses from OpenStax
            openstax_courses = await self.real_api_service.search_openstax_courses(query)
            all_courses.extend(openstax_courses)
            
            # Filter by difficulty
            if difficulty != "all":
                all_courses = [course for course in all_courses if course.get("difficulty", "").lower() == difficulty.lower()]
            
            return all_courses
            
        except Exception as e:
            print(f"Error getting real courses: {e}")
            return []
    
    async def get_course_details(self, course_id):
        """Get detailed information about a specific course"""
        try:
            # Try to get from MCP client first
            course_details = await self.mooc_client.get_course_details(course_id)
            if course_details:
                return course_details
            
            # Fallback to mock data
            return {
                "id": course_id,
                "title": f"Course {course_id}",
                "description": "Course details not available",
                "modules": [],
                "duration": "Unknown",
                "difficulty": "Unknown"
            }
        except Exception as e:
            print(f"Error getting course details: {e}")
            return {}
    
    async def get_trending_courses(self):
        """Get trending courses across platforms"""
        try:
            # This would integrate with the trending courses tool from MCP server
            trending_courses = [
                {
                    "id": "trending-1",
                    "title": "Python for Data Science",
                    "description": "Learn Python programming for data analysis",
                    "language": "en",
                    "difficulty": "beginner",
                    "provider": "edX",
                    "duration": "8 weeks",
                    "rating": 4.8,
                    "trending": True
                },
                {
                    "id": "trending-2",
                    "title": "Machine Learning Fundamentals",
                    "description": "Introduction to machine learning concepts",
                    "language": "en",
                    "difficulty": "intermediate",
                    "provider": "MIT OCW",
                    "duration": "12 weeks",
                    "rating": 4.7,
                    "trending": True
                }
            ]
            return trending_courses
        except Exception as e:
            print(f"Error getting trending courses: {e}")
            return [] 