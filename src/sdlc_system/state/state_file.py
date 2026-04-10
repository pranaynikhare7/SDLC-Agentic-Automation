from pydantic import BaseModel, Field
from typing import TypedDict, Any, Dict, Literal, Optional
import json


class UserStories(BaseModel):
    id: str = Field(...,description="The unique identifier of the user story")
    title: str = Field(...,description="The title of the user story")
    description: str = Field(...,description="The description of the user story")
    priority: int = Field(...,description="The priority of the user story")
    acceptance_criteria: str = Field(...,description="The acceptance criteria of the user story")

class UserStoryList(BaseModel):
    user_stories: list[UserStories]


class DesignDocument(BaseModel):
    functional: str = Field(..., description="Holds the functional design Document")
    technical: str = Field(..., description="Holds the technical design Document")


class SDLCState(TypedDict):
    """
    Represents the structure of the state used in the SDLC graph
    """    
    next_node: str 
    project_name: str
    requirements: list[str]

    # phase 1: Generating User stories 
    user_stories: UserStoryList
    user_stories_feedback: str
    user_stories_review_status: str

    # Phase 2: Design Documents
    design_documents: DesignDocument
    design_documents_feedback: str
    design_documents_review_status: str
    
    # Phase 3: Code Generation and Review
    code_generated: str
    code_review_comments: str
    code_review_feedback: str
    code_review_status: str

    # Phase 4: Security Review
    security_recommendations: str
    security_review_comments: str
    security_review_status: str

    # Phase 5: Test Cases
    test_cases: str
    test_case_review_status: str
    test_case_review_feedback: str

    # Phase 6: QA
    qa_testing_comments: str
    qa_testing_status: str
    qa_testing_feedback: str

    artifacts: dict[str, str]

    