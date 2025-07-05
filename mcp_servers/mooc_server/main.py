import requests
import aiohttp
import asyncio
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("MOOC-Server")

# Real API service
class RealMOOCService:
    def __init__(self):
        self.session = None
    
    async def get_session(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def search_edx_courses(self, query: str, language: str = "en"):
        """Search courses from edX API"""
        try:
            session = await self.get_session()
            url = "https://api.edx.org/catalog/v1/catalogs/edx/courses/"
            params = {
                "search": query,
                "language": language,
                "page_size": 10
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    courses = []
                    for course in data.get("results", []):
                        courses.append({
                            "id": course.get("key"),
                            "title": course.get("name"),
                            "description": course.get("short_description", ""),
                            "language": course.get("language", "en"),
                            "difficulty": course.get("level", "beginner"),
                            "provider": "edX",
                            "duration": f"{course.get('effort', 'Unknown')} hours/week",
                            "rating": course.get("rating", 0.0),
                            "url": course.get("marketing_url", "")
                        })
                    return courses
                else:
                    print(f"edX API error: {response.status}")
                    return []
        except Exception as e:
            print(f"Error fetching from edX: {e}")
            return []
    
    async def search_mit_ocw_courses(self, query: str):
        """Search courses from MIT OpenCourseWare"""
        try:
            session = await self.get_session()
            url = "https://ocw.mit.edu/api/v1/search/"
            params = {
                "q": query,
                "type": "course"
            }
            
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    courses = []
                    for course in data.get("results", []):
                        courses.append({
                            "id": course.get("id"),
                            "title": course.get("title"),
                            "description": course.get("description", ""),
                            "language": "en",
                            "difficulty": "intermediate",
                            "provider": "MIT OCW",
                            "duration": "Self-paced",
                            "rating": 4.5,
                            "url": course.get("url", "")
                        })
                    return courses
                else:
                    print(f"MIT OCW API error: {response.status}")
                    return []
        except Exception as e:
            print(f"Error fetching from MIT OCW: {e}")
            return []

# Initialize the service
mooc_service = RealMOOCService()

@mcp.tool()
async def search_courses(query: str, language: str = "en", difficulty: str = "beginner") -> list:
    """
    Search for courses across multiple MOOC platforms using real APIs.
    """
    print(f"Server received course search request: {query}, {language}, {difficulty}")
    
    try:
        # Search from multiple sources
        all_courses = []
        
        # Search edX
        edx_courses = await mooc_service.search_edx_courses(query, language)
        all_courses.extend(edx_courses)
        
        # Search MIT OCW
        mit_courses = await mooc_service.search_mit_ocw_courses(query)
        all_courses.extend(mit_courses)
        
        # Filter by difficulty if specified
        if difficulty != "all":
            all_courses = [course for course in all_courses if course.get("difficulty", "").lower() == difficulty.lower()]
        
        # Return top results
        return all_courses[:20]
        
    except Exception as e:
        print(f"Error in search_courses: {e}")
        # Fallback to mock data
        return [
            {
                "id": "fallback-course-1",
                "title": f"Fallback Course for '{query}'",
                "description": "This is a fallback course when API is unavailable",
                "language": language,
                "difficulty": difficulty,
                "provider": "FallbackProvider",
                "duration": "8 weeks",
                "rating": 4.0
            }
        ]

@mcp.tool()
def get_course_details(course_id: str) -> dict:
    """
    Get detailed information about a specific course.
    """
    print(f"Server received course details request: {course_id}")
    
    # For now, return mock details - in production, you'd fetch from the specific platform
    return {
        "id": course_id,
        "title": f"Detailed Course {course_id}",
        "description": "This is a comprehensive course description with detailed information about the course content, learning objectives, and prerequisites.",
        "modules": [
            {"id": "module-1", "title": "Introduction", "duration": "2 weeks", "content": "Basic concepts and setup"},
            {"id": "module-2", "title": "Core Concepts", "duration": "4 weeks", "content": "Main learning objectives"},
            {"id": "module-3", "title": "Advanced Topics", "duration": "2 weeks", "content": "Advanced concepts and applications"}
        ],
        "duration": "8 weeks",
        "difficulty": "beginner",
        "instructor": "Dr. Sample Instructor",
        "prerequisites": ["Basic programming knowledge"],
        "certificate": True,
        "enrollment_count": 1250,
        "last_updated": "2024-01-01"
    }

@mcp.tool()
async def get_trending_courses() -> list:
    """
    Get trending courses across platforms.
    """
    print("Server received trending courses request")
    
    try:
        # Search for popular topics
        trending_topics = ["python", "machine learning", "data science", "web development"]
        trending_courses = []
        
        for topic in trending_topics:
            courses = await mooc_service.search_edx_courses(topic, "en")
            trending_courses.extend(courses[:3])  # Top 3 from each topic
        
        # Sort by rating and return top results
        trending_courses.sort(key=lambda x: x.get("rating", 0), reverse=True)
        return trending_courses[:10]
        
    except Exception as e:
        print(f"Error getting trending courses: {e}")
        return []

if __name__ == "__main__":
    print("Starting MOOC MCP Server with Real API Integration....")
    mcp.run(transport="stdio")