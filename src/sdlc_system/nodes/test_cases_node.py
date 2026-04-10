from src.sdlc_system.state.state_file import SDLCState, UserStoryList

class TestNode:
    """
    Graph Node for the generating test cases
    
    """
    
    def __init__(self, model):
        self.llm = model
    
    
    ## ---- Test Cases ----- ##
    def write_test_cases(self, state: SDLCState):
        """
            Generates the test cases based on the generated code and code review comments
        """
    
        # Get the generated code and code review comments from the state
        code_generated = state.get('code_generated', '')
        code_review_comments = state.get('code_review_comments', '')

        # Create a prompt for the LLM to generate test cases
        prompt = f"""
            You are a software testing expert. Based on the following Python code and its review comments, generate comprehensive test cases:
            
            ### Code:
            ```
                {code_generated}
                ```

                ### Code Review Comments:
                {code_review_comments}

                Focus on:
                1. Covering all edge cases and boundary conditions.
                2. Ensuring functional correctness of the code.
                3. Including both positive and negative test cases.
                4. Writing test cases in Python's `unittest` framework format.

                Provide the test cases in Python code format, ready to be executed.
        """

        response = self.llm.invoke(prompt)
        state["test_cases"] = response.content

        return state
    
    def review_test_cases(self, state: SDLCState):
        return state
    
    def revise_test_cases(self, state: SDLCState):
        pass
    
    def review_test_cases_router(self, state: SDLCState):
        """
            Evaluates Test Cases review is required or not.
        """
        return state.get("test_case_review_status", "approved")  # default to "approved" if not present
    
    
    