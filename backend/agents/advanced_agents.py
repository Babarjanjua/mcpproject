from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import LLMChain
from langchain.graphs import StateGraph, END
from langchain.schema import BaseMessage
from typing import List, Dict, Any, Optional
import os
import json
from datetime import datetime

class AdvancedCourseAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.setup_prompts()
    
    def setup_prompts(self):
        """Setup prompt templates for course recommendations"""
        self.course_recommendation_prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(
                """You are an expert educational advisor specializing in online learning and MOOC platforms. 
                Your goal is to recommend the best courses based on user preferences, learning goals, and background.
                
                Consider factors like:
                - User's current skill level
                - Learning goals and career objectives
                - Preferred learning style
                - Time availability
                - Language preferences
                - Course quality and ratings
                
                Provide personalized, actionable recommendations with explanations."""
            ),
            HumanMessagePromptTemplate.from_template(
                """User Profile:
                - Interests: {interests}
                - Current Level: {current_level}
                - Learning Goal: {learning_goal}
                - Time Available: {time_available}
                - Preferred Language: {language}
                
                Available Courses: {available_courses}
                
                Please recommend the top 5 courses that would be most suitable for this user. 
                For each recommendation, explain why it's a good fit and what the user can expect to learn."""
            )
        ])
    
    async def recommend_courses(self, user_profile: Dict[str, Any], available_courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate intelligent course recommendations using OpenAI"""
        try:
            # Prepare the prompt
            messages = self.course_recommendation_prompt.format_messages(
                interests=user_profile.get("interests", []),
                current_level=user_profile.get("current_level", "beginner"),
                learning_goal=user_profile.get("learning_goal", "skill_enhancement"),
                time_available=user_profile.get("time_available", "5-10 hours/week"),
                language=user_profile.get("preferred_language", "en"),
                available_courses=json.dumps(available_courses, indent=2)
            )
            
            # Get recommendation from OpenAI
            response = await self.llm.ainvoke(messages)
            
            # Parse the response and match with available courses
            recommended_courses = self.parse_recommendations(response.content, available_courses)
            
            return recommended_courses
            
        except Exception as e:
            print(f"Error in course recommendation: {e}")
            return available_courses[:5]  # Fallback to first 5 courses
    
    def parse_recommendations(self, llm_response: str, available_courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse LLM response and match with available courses"""
        try:
            # Simple parsing - in production, you'd want more sophisticated parsing
            recommended_courses = []
            
            # Extract course titles from LLM response and match with available courses
            for course in available_courses:
                if course["title"].lower() in llm_response.lower():
                    course["recommendation_reason"] = "AI-recommended based on your profile"
                    recommended_courses.append(course)
            
            # If no matches found, return top courses by rating
            if not recommended_courses:
                recommended_courses = sorted(available_courses, key=lambda x: x.get("rating", 0), reverse=True)[:5]
                for course in recommended_courses:
                    course["recommendation_reason"] = "Top-rated course in your area of interest"
            
            return recommended_courses
            
        except Exception as e:
            print(f"Error parsing recommendations: {e}")
            return available_courses[:5]

class AdvancedLearningPathAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.8,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.setup_learning_path_graph()
    
    def setup_learning_path_graph(self):
        """Setup LangGraph for learning path generation"""
        # Define the state
        class LearningPathState:
            def __init__(self):
                self.user_profile = {}
                self.selected_courses = []
                self.learning_path = []
                self.current_step = 0
                self.completion_estimate = ""
        
        # Create the graph
        workflow = StateGraph(LearningPathState)
        
        # Add nodes
        workflow.add_node("analyze_profile", self.analyze_user_profile)
        workflow.add_node("select_courses", self.select_optimal_courses)
        workflow.add_node("create_path", self.create_learning_path)
        workflow.add_node("estimate_completion", self.estimate_completion_time)
        
        # Add edges
        workflow.add_edge("analyze_profile", "select_courses")
        workflow.add_edge("select_courses", "create_path")
        workflow.add_edge("create_path", "estimate_completion")
        workflow.add_edge("estimate_completion", END)
        
        self.graph = workflow.compile()
    
    async def analyze_user_profile(self, state):
        """Analyze user profile and learning preferences"""
        prompt = f"""
        Analyze this user profile and extract key learning preferences:
        
        User Profile: {state.user_profile}
        
        Provide insights on:
        1. Learning style preferences
        2. Optimal study schedule
        3. Preferred difficulty progression
        4. Key learning objectives
        """
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        state.analysis = response.content
        return state
    
    async def select_optimal_courses(self, state):
        """Select optimal courses based on analysis"""
        prompt = f"""
        Based on the user analysis: {state.analysis}
        
        Available courses: {state.selected_courses}
        
        Select and order the best courses for this user's learning path.
        Consider prerequisites, difficulty progression, and learning objectives.
        """
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        state.ordered_courses = self.parse_course_selection(response.content, state.selected_courses)
        return state
    
    async def create_learning_path(self, state):
        """Create detailed learning path with milestones"""
        prompt = f"""
        Create a detailed learning path for these courses: {state.ordered_courses}
        
        For each course, provide:
        1. Learning objectives
        2. Estimated time commitment
        3. Prerequisites
        4. Success criteria
        5. Recommended study schedule
        """
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        state.learning_path = self.parse_learning_path(response.content)
        return state
    
    async def estimate_completion_time(self, state):
        """Estimate completion time based on user profile and path"""
        prompt = f"""
        Estimate completion time for this learning path: {state.learning_path}
        
        User profile: {state.user_profile}
        Analysis: {state.analysis}
        
        Provide realistic time estimates and milestones.
        """
        
        response = await self.llm.ainvoke([HumanMessage(content=prompt)])
        state.completion_estimate = response.content
        return state
    
    def parse_course_selection(self, llm_response: str, courses: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Parse course selection from LLM response"""
        # Implementation would parse the LLM response and return ordered courses
        return courses
    
    def parse_learning_path(self, llm_response: str) -> List[Dict[str, Any]]:
        """Parse learning path from LLM response"""
        # Implementation would parse the LLM response and return structured path
        return [
            {
                "step": 1,
                "title": "Foundation Course",
                "description": "Build fundamental knowledge",
                "duration": "4 weeks",
                "objectives": ["Understand basics", "Complete exercises"],
                "prerequisites": []
            }
        ]
    
    async def generate_learning_path(self, user_profile: Dict[str, Any], courses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive learning path using LangGraph"""
        try:
            # Initialize state
            initial_state = {
                "user_profile": user_profile,
                "selected_courses": courses,
                "learning_path": [],
                "current_step": 0,
                "completion_estimate": ""
            }
            
            # Run the graph
            result = await self.graph.ainvoke(initial_state)
            
            return {
                "learning_path": result.learning_path,
                "completion_estimate": result.completion_estimate,
                "analysis": result.analysis,
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error generating learning path: {e}")
            return {"learning_path": [], "error": str(e)}

class AdvancedQuizAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.5,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    
    async def generate_quiz(self, course_content: str, module_id: str, difficulty: str = "medium") -> Dict[str, Any]:
        """Generate intelligent quiz questions based on course content"""
        try:
            prompt = f"""
            Generate a quiz for the following course content:
            
            Content: {course_content}
            Module: {module_id}
            Difficulty: {difficulty}
            
            Create 5 multiple-choice questions with:
            1. Clear, unambiguous questions
            2. 4 answer options (A, B, C, D)
            3. One correct answer
            4. Explanations for correct answers
            5. Difficulty appropriate for {difficulty} level
            
            Format the response as JSON with this structure:
            {{
                "questions": [
                    {{
                        "question": "Question text",
                        "options": ["A", "B", "C", "D"],
                        "correct_answer": "A",
                        "explanation": "Why this is correct"
                    }}
                ]
            }}
            """
            
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            
            # Parse JSON response
            try:
                quiz_data = json.loads(response.content)
                return {
                    "module_id": module_id,
                    "difficulty": difficulty,
                    "questions": quiz_data.get("questions", []),
                    "total_questions": len(quiz_data.get("questions", [])),
                    "generated_at": datetime.now().isoformat()
                }
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return self.create_fallback_quiz(module_id, difficulty)
                
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return self.create_fallback_quiz(module_id, difficulty)
    
    def create_fallback_quiz(self, module_id: str, difficulty: str) -> Dict[str, Any]:
        """Create a fallback quiz if AI generation fails"""
        return {
            "module_id": module_id,
            "difficulty": difficulty,
            "questions": [
                {
                    "question": "What is the main topic of this module?",
                    "options": ["Programming", "Mathematics", "Science", "Literature"],
                    "correct_answer": "Programming",
                    "explanation": "This module focuses on programming concepts."
                }
            ],
            "total_questions": 1,
            "generated_at": datetime.now().isoformat()
        }
    
    async def grade_quiz(self, quiz_answers: Dict[str, str], correct_answers: Dict[str, str]) -> Dict[str, Any]:
        """Grade quiz answers and provide feedback"""
        try:
            score = 0
            total_questions = len(correct_answers)
            feedback = []
            
            for question_id, user_answer in quiz_answers.items():
                if question_id in correct_answers:
                    if user_answer == correct_answers[question_id]:
                        score += 1
                        feedback.append(f"Question {question_id}: Correct! ✅")
                    else:
                        feedback.append(f"Question {question_id}: Incorrect. The correct answer was {correct_answers[question_id]} ❌")
            
            percentage = (score / total_questions) * 100 if total_questions > 0 else 0
            
            # Generate personalized feedback using AI
            feedback_prompt = f"""
            The student scored {percentage}% on this quiz ({score}/{total_questions} correct).
            
            Generate encouraging, constructive feedback that:
            1. Acknowledges their performance
            2. Suggests areas for improvement
            3. Provides motivation to continue learning
            4. Offers specific study tips
            """
            
            ai_feedback = await self.llm.ainvoke([HumanMessage(content=feedback_prompt)])
            
            return {
                "score": score,
                "total_questions": total_questions,
                "percentage": percentage,
                "feedback": feedback,
                "ai_feedback": ai_feedback.content,
                "graded_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error grading quiz: {e}")
            return {"error": "Failed to grade quiz"} 