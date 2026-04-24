from src.sdlc_system.state.state_file import SDLCState, DesignDocument


class DesingDocumentNode:
    """
    Graph Node for the Desing Documents
    
    """
    
    def __init__(self, model):
        self.llm = model
    
    def create_design_documents(self, state: SDLCState):
        """
        Generates the Design document functional and technical
        """

        requirements = state.get('requirements', '')
        user_stories = state.get('user_stories', '')
        project_name = state.get('project_name', '')
        design_feedback = None
        
        if 'design_documents' in state:
            design_feedback = state.get('design_documents_feedback','')

        functional_documents = self.generate_functional_design(
            project_name=project_name,
            requirements=requirements,
            user_stories=user_stories,
            design_feedback=design_feedback
        )

        technical_documents = self.generate_technical_design(
            project_name=project_name,
            requirements=requirements,
            user_stories=user_stories,
            design_feedback=design_feedback
        )

        design_documents = DesignDocument(
            functional=functional_documents,
            technical = technical_documents
        )

        return {
            **state,
            "design_documents": design_documents,
            "technical_documents": technical_documents
        }
    
    def generate_functional_design(self, project_name, requirements, user_stories, design_feedback):
        """
        Helper method to generate functional design document
        """

        prompt = f"""
        You are a senior product analyst and system designer.
        Create a detailed Functional Design Document (FDD) for the project: {project_name} in Markdown format.

        Follow these instructions:
        - Use proper Markdown syntax (e.g., # for titles, ## for sections, bullet points, tables, and code blocks where needed).
        - Be specific, structured, and implementation-oriented
        - Maintain consistency across sections.

        Requirements:
        {requirements}

        User Stories:
        {user_stories}

        {f"Also consider this feedback while creating the design: {design_feedback}" if design_feedback else ""}

        The document should include:

        # Functional Design Document: {project_name}

        ## 1. Overview and Objectives
        ## 2. Scope Definition
        ## 3. Roles and Access Control
        ## 4. Functional Requirements Analysis
        ## 5. User Interface and Experience Guidelines
        ## 6. Business Workflow Processes
        ## 7. Data Model and Relationships
        ## 8. Data Validation and Business Rules
        ## 9. Reporting and Analytics Requirements
        ## 10. System Integrations and Interfaces

        Keep the formatting clean and consistent throughout.
        """

        response = self.llm.invoke(prompt)
        return response.content



    def generate_technical_design(self, project_name, requirements, user_stories, design_feedback):
            """
                Helper method to generate technical design document in Markdown format
            """
        
            prompt = f"""
                Create a detailed Technical Design Document (TDD) for {project_name} in Markdown format.
                
                Follow proper Markdown conventions:
                - Use # for main titles, ## for sections, and ### for subsections
                - Include bullet points, numbered lists, tables, and code blocks where appropriate
                - Represent diagrams in structured textual form (e.g., flow descriptions, architecture layers)
 
                Requirements:
                {requirements}
            
                User Stories:
                {user_stories}

                {f"When creating this technical design document, please incorporate the following feedback about the requirements: {design_feedback}" if design_feedback else ""}
                
                The technical design document should include the following sections, each with proper Markdown formatting:
                
                # Technical Design Document: {project_name}

                ## 1. System Architecture Overview
                ## 2. Technology Stack and Rationale
                ## 3. Data Model and Schema Design
                ## 4. API Design and Specifications
                ## 5. Security Architecture and Controls
                ## 6. Performance Optimization Strategies
                ## 7. Scalability and Reliability Approach
                ## 8. Deployment and Release Strategy
                ## 9. External Integrations and Dependencies
                ## 10. Environment Setup (Development, Testing, Production)
                
                For any code examples, use ```language-name to specify the programming language.
                For database schemas, represent tables and relationships using Markdown tables.
                Make sure to maintain proper Markdown formatting throughout the document.
            """
            response = self.llm.invoke(prompt)
            return response.content
    
    def review_design_documents(self, state: SDLCState):
        return state
    
    
    def review_design_documents_router(self, state: SDLCState):
        """
            Evaluates design review is required or not.
        """
        return state.get("design_documents_review_status", "approved")  # default to "approved" if not present
    