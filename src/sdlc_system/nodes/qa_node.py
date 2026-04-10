from src.sdlc_system.state.state_file import SDLCState, UserStoryList

class QANode:
    """
    Graph Node for the QA
    
    """
    
    def __init__(self, model):
        self.llm = model
    
    
    ## ---- QA Testing ----- ##
    def qa_testing(self, state: SDLCState):
        """
            Performs QA testing based on the generated code and test cases
        """

        # Get the generated code and test cases from the state
        code_generated = state.get('code_generated', '')
        test_cases = state.get('test_cases', '')

        # Create a prompt for the LLM to simulate running the test cases
        prompt = f"""
            You are a QA testing expert. Based on the following Python code and test cases, simulate running the test cases and provide feedback:
            
            ### Code:
            ```
            {code_generated}
            ```

            ### Test Cases:
            ```
            {test_cases}
            ```

            Focus on:
            1. Identifying which test cases pass and which fail.
            2. Providing detailed feedback for any failed test cases, including the reason for failure.
            3. Suggesting improvements to the code or test cases if necessary.

            Provide the results in the following format:
            - Test Case ID: [ID]
            Status: [Pass/Fail]
            Feedback: [Detailed feedback if failed]
        """

        # Invoke the LLM to simulate QA testing
        response = self.llm.invoke(prompt)
        qa_testing_comments = response.content

        state["qa_testing_comments"]= qa_testing_comments
        return state
    
    def qa_review(self, state: SDLCState):
        pass

    def review_qa_router(self, state: SDLCState):
        """
            Evaluates QA is required or not.
        """
        return state.get("qa_testing_status", "approved")  # default to "approved" if not present
    
    