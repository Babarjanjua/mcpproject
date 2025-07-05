import streamlit as st
import requests
import json
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
import os

# Page configuration
st.set_page_config(
    page_title="Multilingual Learning Path Generator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .course-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #28a745;
    }
    .progress-bar {
        background-color: #e9ecef;
        border-radius: 0.25rem;
        height: 1.5rem;
        overflow: hidden;
    }
    .progress-fill {
        background-color: #28a745;
        height: 100%;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Backend API configuration - use environment variable or default
BACKEND_URL = os.getenv("BACKEND_URL", "https://mcpproject-jqjf81o5m-babars-projects-8d452f16.vercel.app")

def call_backend_api(endpoint, method="GET", data=None):
    """Helper function to call backend API with better error handling"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        # Add timeout and headers for production
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "LearningPathGenerator/1.0"
        }
        
        if method == "GET":
            response = requests.get(url, params=data, headers=headers, timeout=30)
        else:
            response = requests.post(url, json=data, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            st.error(f"API endpoint not found: {endpoint}")
            return None
        elif response.status_code == 500:
            st.error("Backend server error. Please try again later.")
            return None
        else:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.Timeout:
        st.error("Request timeout. Please check your connection and try again.")
        return None
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to backend at {BACKEND_URL}. Please check if the backend is running.")
        return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 Multilingual Learning Path Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your AI-powered learning companion</p>', unsafe_allow_html=True)
    
    # Show backend status
    if st.sidebar.checkbox("🔧 Show Debug Info"):
        st.sidebar.info(f"Backend URL: {BACKEND_URL}")
        
        # Test backend connection
        if st.sidebar.button("Test Backend Connection"):
            with st.spinner("Testing connection..."):
                result = call_backend_api("/")
                if result:
                    st.sidebar.success("✅ Backend connected!")
                else:
                    st.sidebar.error("❌ Backend connection failed")
    
    # Sidebar
    with st.sidebar:
        st.header("🎯 Navigation")
        page = st.selectbox(
            "Choose a page:",
            ["🏠 Dashboard", "📚 Course Search", "🛤️ Learning Paths", "📊 Progress Tracking", "❓ Quizzes", "🔄 Sync"]
        )
        
        st.header("🌍 Language Settings")
        language = st.selectbox(
            "Select Language:",
            ["English", "Spanish", "French", "German", "Chinese", "Japanese", "Korean", "Arabic", "Hindi", "Portuguese"]
        )
        
        st.header("👤 User Profile")
        user_id = st.text_input("User ID:", value="user_123")
        
        if st.button("🔄 Refresh Data"):
            st.rerun()
    
    # Main content based on selected page
    if page == "🏠 Dashboard":
        show_dashboard(user_id, language)
    elif page == "📚 Course Search":
        show_course_search(language)
    elif page == "🛤️ Learning Paths":
        show_learning_paths(user_id, language)
    elif page == "📊 Progress Tracking":
        show_progress_tracking(user_id)
    elif page == "❓ Quizzes":
        show_quizzes(user_id)
    elif page == "🔄 Sync":
        show_sync(user_id)

def show_dashboard(user_id, language):
    """Dashboard page with overview and metrics"""
    st.header("📊 Learning Dashboard")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📚 Courses Enrolled</h3>
            <h2>5</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h3>✅ Completed</h3>
            <h2>3</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h3>⏱️ Study Time</h3>
            <h2>45.5h</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h3>🔥 Streak</h3>
            <h2>12 days</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Weekly Progress")
        # Sample data for progress chart
        weeks = ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6", "Week 7"]
        progress = [10, 15, 20, 25, 30, 35, 40]
        
        fig = px.line(x=weeks, y=progress, title="Learning Progress Over Time")
        fig.update_layout(xaxis_title="Week", yaxis_title="Progress (%)")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Daily Study Time")
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        study_time = [2.5, 3.0, 2.0, 4.0, 3.5, 2.5, 3.0]
        
        fig = px.bar(x=days, y=study_time, title="Daily Study Hours")
        fig.update_layout(xaxis_title="Day", yaxis_title="Hours")
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.subheader("🕒 Recent Activity")
    activities = [
        {"time": "2 hours ago", "action": "Completed Module 3 of Python Basics", "course": "Python Programming"},
        {"time": "1 day ago", "action": "Took Quiz 2", "course": "Data Science Fundamentals"},
        {"time": "2 days ago", "action": "Started new course", "course": "Machine Learning"},
        {"time": "3 days ago", "action": "Synced progress with Google Classroom", "course": "Web Development"}
    ]
    
    for activity in activities:
        st.markdown(f"""
        <div style="padding: 1rem; background-color: #f8f9fa; border-radius: 0.5rem; margin-bottom: 0.5rem;">
            <strong>{activity['action']}</strong><br>
            <small style="color: #666;">{activity['time']} • {activity['course']}</small>
        </div>
        """, unsafe_allow_html=True)

def show_course_search(language):
    """Course search page"""
    st.header("📚 Course Search")
    
    # Search filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search courses:", placeholder="e.g., Python, Machine Learning")
    
    with col2:
        difficulty = st.selectbox("📊 Difficulty:", ["Beginner", "Intermediate", "Advanced"])
    
    with col3:
        category = st.selectbox("📂 Category:", ["All", "Programming", "Data Science", "Mathematics", "Business", "Arts"])
    
    # Search button
    if st.button("🔍 Search Courses", type="primary"):
        with st.spinner("Searching for courses..."):
            # Call backend API
            courses_data = call_backend_api("/courses", "GET", {
                "query": search_query,
                "language": language.lower(),
                "difficulty": difficulty.lower()
            })
            
            if courses_data and "courses" in courses_data:
                display_courses(courses_data["courses"])
            else:
                st.warning("No courses found. Try different search terms.")
    
    # Show sample courses if no search
    if not search_query:
        st.subheader("🎯 Popular Courses")
        sample_courses = [
            {
                "id": "course-1",
                "title": "Python Programming for Beginners",
                "description": "Learn Python from scratch with hands-on projects",
                "language": "English",
                "difficulty": "Beginner",
                "provider": "MockProvider",
                "duration": "8 weeks",
                "rating": 4.5
            },
            {
                "id": "course-2",
                "title": "Advanced Machine Learning",
                "description": "Master machine learning algorithms and techniques",
                "language": "English", 
                "difficulty": "Advanced",
                "provider": "MockProvider",
                "duration": "12 weeks",
                "rating": 4.8
            }
        ]
        display_courses(sample_courses)

def display_courses(courses):
    """Display courses in a grid layout"""
    for course in courses:
        st.markdown(f"""
        <div class="course-card">
            <h3>{course.get('title', 'Untitled Course')}</h3>
            <p>{course.get('description', 'No description available')}</p>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <span style="background-color: #e3f2fd; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.8rem;">
                        {course.get('difficulty', 'Unknown')}
                    </span>
                    <span style="background-color: #f3e5f5; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.8rem; margin-left: 0.5rem;">
                        {course.get('duration', 'Unknown')}
                    </span>
                </div>
                <div>
                    <span style="color: #ff9800;">{'⭐' * int(course.get('rating', 0))}</span>
                    <span style="color: #666; font-size: 0.9rem;">({course.get('rating', 0)})</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button(f"📖 View Details", key=f"view_{course['id']}"):
                show_course_details(course['id'])
        with col2:
            if st.button(f"➕ Enroll", key=f"enroll_{course['id']}"):
                st.success(f"Enrolled in {course['title']}!")

def show_course_details(course_id):
    """Show detailed course information"""
    st.subheader("📖 Course Details")
    
    # Call backend API for course details
    course_details = call_backend_api(f"/courses/{course_id}", "GET")
    
    if course_details:
        st.json(course_details)
    else:
        st.info("Course details not available")

def show_learning_paths(user_id, language):
    """Learning paths page"""
    st.header("🛤️ Learning Paths")
    
    st.subheader("🎯 Generate Personalized Learning Path")
    
    # User preferences
    col1, col2 = st.columns(2)
    
    with col1:
        interests = st.multiselect(
            "🎨 Areas of Interest:",
            ["Programming", "Data Science", "Mathematics", "Business", "Arts", "Languages", "Science"]
        )
        
        time_available = st.selectbox(
            "⏰ Time Available:",
            ["1-2 hours/week", "3-5 hours/week", "5-10 hours/week", "10+ hours/week"]
        )
    
    with col2:
        learning_style = st.selectbox(
            "🧠 Learning Style:",
            ["Visual", "Auditory", "Reading/Writing", "Kinesthetic"]
        )
        
        goal = st.selectbox(
            "🎯 Learning Goal:",
            ["Career Change", "Skill Enhancement", "Personal Interest", "Academic Credit"]
        )
    
    if st.button("🚀 Generate Learning Path", type="primary"):
        with st.spinner("Generating your personalized learning path..."):
            # Call backend API
            user_profile = {
                "interests": interests,
                "time_available": time_available,
                "learning_style": learning_style,
                "goal": goal
            }
            
            path_data = call_backend_api("/learning-path", "POST", {
                "user_profile": user_profile,
                "courses": []
            })
            
            if path_data and "learning_path" in path_data:
                display_learning_path(path_data["learning_path"])
            else:
                st.warning("Could not generate learning path. Please try again.")

def display_learning_path(learning_path):
    """Display the generated learning path"""
    st.subheader("📋 Your Personalized Learning Path")
    
    if not learning_path:
        st.info("No learning path generated yet. Please try generating one.")
        return
    
    # Display path as a timeline
    for i, step in enumerate(learning_path, 1):
        st.markdown(f"""
        <div style="border-left: 3px solid #1f77b4; padding-left: 1rem; margin: 1rem 0;">
            <h4>Step {i}: {step.get('title', 'Learning Step')}</h4>
            <p>{step.get('description', 'No description')}</p>
            <small style="color: #666;">Duration: {step.get('duration', 'Unknown')}</small>
        </div>
        """, unsafe_allow_html=True)

def show_progress_tracking(user_id):
    """Progress tracking page"""
    st.header("📊 Progress Tracking")
    
    # Current courses progress
    st.subheader("📚 Current Courses")
    
    courses_progress = [
        {"course": "Python Programming", "progress": 75, "modules": 8, "completed": 6},
        {"course": "Data Science Fundamentals", "progress": 45, "modules": 10, "completed": 4},
        {"course": "Machine Learning", "progress": 20, "modules": 12, "completed": 2}
    ]
    
    for course in courses_progress:
        st.markdown(f"""
        <div style="background-color: white; padding: 1.5rem; border-radius: 0.5rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1); margin-bottom: 1rem;">
            <h4>{course['course']}</h4>
            <div class="progress-bar">
                <div class="progress-fill" style="width: {course['progress']}%;"></div>
            </div>
            <p style="margin-top: 0.5rem;">
                <strong>{course['progress']}%</strong> complete • 
                {course['completed']}/{course['modules']} modules finished
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Update progress
    st.subheader("📝 Update Progress")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_course = st.selectbox("Course:", [c["course"] for c in courses_progress])
    
    with col2:
        module_id = st.text_input("Module ID:", value="module_1")
    
    with col3:
        completion = st.slider("Completion %:", 0, 100, 50)
    
    if st.button("💾 Update Progress"):
        with st.spinner("Updating progress..."):
            # Call backend API
            result = call_backend_api("/progress", "POST", {
                "user_id": user_id,
                "course_id": selected_course,
                "module_id": module_id,
                "completion": completion
            })
            
            if result:
                st.success("Progress updated successfully!")
            else:
                st.error("Failed to update progress")

def show_quizzes(user_id):
    """Quizzes page"""
    st.header("❓ Quizzes")
    
    st.subheader("🎯 Generate Quiz")
    
    col1, col2 = st.columns(2)
    
    with col1:
        course_id = st.text_input("Course ID:", value="course_1")
    
    with col2:
        module_id = st.text_input("Module ID:", value="module_1")
    
    if st.button("🎲 Generate Quiz", type="primary"):
        with st.spinner("Generating quiz..."):
            # Call backend API
            quiz_data = call_backend_api("/quiz", "POST", {
                "course_id": course_id,
                "module_id": module_id
            })
            
            if quiz_data and "quiz" in quiz_data:
                display_quiz(quiz_data["quiz"])
            else:
                st.warning("Could not generate quiz. Please try again.")

def display_quiz(quiz):
    """Display the generated quiz"""
    st.subheader("📝 Quiz")
    
    if not quiz:
        st.info("No quiz available.")
        return
    
    # Sample quiz display
    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem;">
        <h4>Sample Quiz Question</h4>
        <p>What is the primary purpose of Python's 'if __name__ == "__main__":' statement?</p>
        
        <div style="margin: 1rem 0;">
            <input type="radio" id="a" name="answer">
            <label for="a">To define a function</label>
        </div>
        
        <div style="margin: 1rem 0;">
            <input type="radio" id="b" name="answer">
            <label for="b">To check if the script is run directly</label>
        </div>
        
        <div style="margin: 1rem 0;">
            <input type="radio" id="c" name="answer">
            <label for="c">To import modules</label>
        </div>
        
        <div style="margin: 1rem 0;">
            <input type="radio" id="d" name="answer">
            <label for="d">To create a class</label>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("✅ Submit Answer"):
        st.success("Answer submitted! Correct answer: B")

def show_sync(user_id):
    """Sync with Google Classroom page"""
    st.header("🔄 Google Classroom Sync")
    
    st.subheader("📚 Sync Learning Progress")
    
    # Sync options
    col1, col2 = st.columns(2)
    
    with col1:
        sync_courses = st.checkbox("Sync course enrollments")
        sync_progress = st.checkbox("Sync learning progress")
        sync_assignments = st.checkbox("Sync assignments")
    
    with col2:
        auto_sync = st.checkbox("Enable automatic sync")
        sync_frequency = st.selectbox("Sync frequency:", ["Daily", "Weekly", "Monthly"])
    
    if st.button("🔄 Sync Now", type="primary"):
        with st.spinner("Syncing with Google Classroom..."):
            # Call backend API
            sync_data = {
                "user_id": user_id,
                "course_id": "sample_course",
                "progress_data": {
                    "sync_courses": sync_courses,
                    "sync_progress": sync_progress,
                    "sync_assignments": sync_assignments
                }
            }
            
            result = call_backend_api("/sync", "POST", sync_data)
            
            if result:
                st.success("Successfully synced with Google Classroom!")
            else:
                st.error("Failed to sync with Google Classroom")
    
    # Sync status
    st.subheader("📊 Sync Status")
    
    sync_status = [
        {"item": "Course Enrollments", "status": "✅ Synced", "last_sync": "2 hours ago"},
        {"item": "Learning Progress", "status": "✅ Synced", "last_sync": "1 hour ago"},
        {"item": "Assignments", "status": "⏳ Pending", "last_sync": "Never"},
        {"item": "Grades", "status": "❌ Failed", "last_sync": "3 days ago"}
    ]
    
    for item in sync_status:
        st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem; background-color: #f8f9fa; border-radius: 0.25rem; margin-bottom: 0.5rem;">
            <span><strong>{item['item']}</strong></span>
            <span>{item['status']}</span>
            <span style="color: #666; font-size: 0.9rem;">{item['last_sync']}</span>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 