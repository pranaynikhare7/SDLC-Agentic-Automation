from langchain_core.messages import SystemMessage
from src.sdlc_system.state.state_file import  SDLCState, UserStoryList

class ProjectRequirementNode:
    """
    Graph Node for the project requirements    
    """
    
    def __init__(self, model):
        self.llm = model
      
    
    def get_user_requirements(self, state: SDLCState):
        """
            Gets the requirements from the user
        """
        pass
    

    def generate_user_stories(self, state: SDLCState):

        project_name = state["project_name"]
        requirements = state["requirements"]
        feedback = state.get("user_stories_feedback", "")

        # Clean, descriptive prompt with NO formatting instructions
        prompt = f"""
        Act as a senior Agile Analyst. Your goal is to convert requirements into structured User Story objects.

        Project: {project_name}
        Input Requirements: {requirements}
        Additional Feedback: {feedback}

        Task: Create one detailed User Story for every requirement provided. 
        Ensure the 'id' field follows the pattern 'US-001', 'US-002', etc.
        """

        # Force the model to focus ONLY on the tool call
        llm_with_structured = self.llm.with_structured_output(UserStoryList)
        response = llm_with_structured.invoke(prompt)
    
        return {"user_stories": response}


    

    # def generate_user_stories(self, state: SDLCState):
    #     """
    #     Auto-generate highly detailed and accurate user stories for each requirement.
    #     """
    #     project_name = state["project_name"]
    #     requirements = state["requirements"]
    #     feedback_reason = state.get("user_stories_feedback", None)

    #     prompt = f"""
    #     You are a senior software analyst specializing in Agile SDLC and user story generation. 
    #     Your task is to generate **a separate and detailed user story for EACH requirement** from the project details below.

    #     ---
    #     **Project Name:** "{project_name}"

    #     **Requirements:** "{requirements}

    #     ---
    #     **Instructions for User Story Generation:**
    #     - Create **one user story per requirement**.
    #     - Assign a **unique identifier** (e.g., US-001, US-002, etc.).
    #     - Provide a **clear and concise title** summarizing the user story.
    #     - Write a **detailed description** using the "As a [user role], I want [goal] so that [benefit]" format.
    #     - Assign a **priority level** (1 = Critical, 2 = High, 3 = Medium, 4 = Low).
    #     - Define **acceptance criteria** with bullet points to ensure testability.
    #     - Use **domain-specific terminology** for clarity.
        
    #     {f"Additionally, consider the following feedback while refining the user stories: {feedback_reason}" if feedback_reason else ""}



    #     Ensure that the user stories are **specific, testable, and aligned with Agile principles**.
    #     """

    #     llm_with_structured = self.llm.with_structured_output(UserStoryList)
    #     response = llm_with_structured.invoke(prompt)
    #     # state["user_stories"] = response
    #     return {"user_stories": response}
    
    def review_user_stories(self, state: SDLCState):
        return state
    
    def revise_user_stories(self, state: SDLCState):
        pass
    
    def review_user_stories_router(self, state: SDLCState):
        return state.get("user_stories_review_status", "approved")  # default to "approved" if not present