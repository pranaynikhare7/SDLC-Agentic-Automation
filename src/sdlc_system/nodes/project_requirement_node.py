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
        Act as a senior software analyst specialized in SDLC. 
        Your goal is to convert requirements into structured User Story objects.

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

    
    def review_user_stories(self, state: SDLCState):
        return state
    
    def revise_user_stories(self, state: SDLCState):
        pass
    
    def review_user_stories_router(self, state: SDLCState):
        return state.get("user_stories_review_status", "approved")  # default to "approved" if not present