from src.sdlc_system.state.state_file import SDLCState, UserStoryList

class CodingNode:
    """
    Graph Node for the Coding
    
    """
    
    def __init__(self, model):
        self.llm = model
    
    ## ---- Code Generation ----- ##
    def generate_code(self, state: SDLCState):
        """
            Generates the code for the given SDLC state as multiple Python files.
        """
        
        requirements = state.get('requirements', '')
        user_stories = state.get('user_stories', '')
        code_feedback = state.get('code_review_feedback', '') if 'code_generated' in state else ""
        security_feedback = state.get('security_recommendations', '') if 'security_recommendations' in state else ""
        
        prompt = f"""
        Generate a complete Python project organized as multiple code files. 
        Based on the following SDLC state, generate only the Python code files with their complete implementations. 
        Do NOT include any explanations, requirements text, or design document details in the output—only code files with proper names and code content.

        SDLC State:
        ---------------
        Project Name: {state['project_name']}

        Requirements:
        {requirements}

        User Stories:
        {user_stories}

        Functional Design Document:
        {state['design_documents']['functional']}

        Technical Design Document:
        {state['design_documents']['technical']}

        {"Note: Incorporate the following code review feedback: " + code_feedback if code_feedback else ""}
        {"Note: Apply the following security recommendations: " + security_feedback if security_feedback else ""}

        Instructions:
        - Structure the output as multiple code files (for example,  "main.py", "module1.py", etc.), each separated clearly.
        - Each file should contain only the code necessary for a modular, fully-functional project based on the input state.
        - Do not output any additional text, explanations, or commentary outside the code files.
        - Ensure the code follows Python best practices, is syntactically correct, and is ready for development.
        """
        response = self.llm.invoke(prompt)
        code_review_comments = self.get_code_review_comments(code=response.content)
        return {
                'code_generated': response.content, 
                'code_review_comments': code_review_comments
            }
    
    ## This code review comments will be used while generating test cases
    def get_code_review_comments(self, code: str):
        """
        Generate code review comments for the provided code
        """
        
        # Create a prompt for the LLM to review the code
        prompt = f"""
            You are a coding expert. Please review the following code and provide detailed feedback:
            ```
            {code}
            ```
            Focus on:
            1. Code quality and best practices
            2. Potential bugs or edge cases
            3. Performance considerations
            4. Security concerns
            
            End your review with an explicit APPROVED or NEEDS_FEEDBACK status.
        """
        
        # Get the review from the LLM
        response = self.llm.invoke(prompt)
        review_comments = response.content
        return review_comments
    
    def code_review(self, state: SDLCState):
        return state
    
    
    def code_review_router(self, state: SDLCState):
        """
            Evaluates Code review is required or not.
        """
        return state.get("code_review_status", "approved")  # default to "approved" if not present
    
    