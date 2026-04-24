from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.graph import MermaidDrawMethod

from src.sdlc_system.state.state_file import SDLCState
from src.sdlc_system.nodes.project_requirement_node import ProjectRequirementNode
from src.sdlc_system.nodes.design_doc_node import DesingDocumentNode
from src.sdlc_system.nodes.coding_node import CodingNode
from src.sdlc_system.nodes.security_node import SecurityNode
from src.sdlc_system.nodes.test_cases_node import TestNode
from src.sdlc_system.nodes.qa_node import QANode
from src.sdlc_system.nodes.markdown_node import MarkdownArtifactsNode


class GraphBuilder:
    
    def __init__(self, llm):
        self.llm = llm
        self.graph_builder = StateGraph(SDLCState)
        self.memory = MemorySaver()
                
    
    def build_sdlc_graph(self):
        """
            Configure the graph by adding nodes, edges
        """
        
        self.project_requirement_node = ProjectRequirementNode(self.llm)
        self.design_doc_node = DesingDocumentNode(self.llm)
        self.coding_node = CodingNode(self.llm)
        self.security_node = SecurityNode(self.llm)    
        self.test_node = TestNode(self.llm)   
        self.qa_node = QANode(self.llm) 
        self.markdown_node = MarkdownArtifactsNode()
   
        ## Nodes
   
        self.graph_builder.add_node("intake_agent", self.project_requirement_node.get_user_requirements)
        
        # Phase 1: User Stories
        self.graph_builder.add_node("business_analyst_agent", self.project_requirement_node.generate_user_stories)
        self.graph_builder.add_node("human_po_review", self.project_requirement_node.review_user_stories)
        
        # Phase 2: Design Documents
        self.graph_builder.add_node("architect_agent", self.design_doc_node.create_design_documents)
        self.graph_builder.add_node("human_design_review", self.design_doc_node.review_design_documents)
        
        # Phase 3: Code Generate using design document
        self.graph_builder.add_node("developer_agent", self.coding_node.generate_code)
        self.graph_builder.add_node("human_code_review", self.coding_node.code_review)
     
        # Phase 4: Security Review        
        self.graph_builder.add_node("security_consultant_agent", self.security_node.security_review_recommendations)
        self.graph_builder.add_node("human_security_review", self.security_node.security_review)
       
       # Phase 5: Test Cases Generation
        self.graph_builder.add_node("sdet_agent", self.test_node.write_test_cases)
        self.graph_builder.add_node("human_test_review", self.test_node.review_test_cases)
        
        # Phase 6: QA Testing
        self.graph_builder.add_node("execution_agent", self.qa_node.qa_testing)
        self.graph_builder.add_node("human_final_qa_review", self.qa_node.qa_review)        

        # Phase 7: Download Artifacts
        self.graph_builder.add_node("artifact_compiler_agent", self.markdown_node.generate_markdown_artifacts)
        
        # ***************************** Edges *****************************

        # Phase 1: User Stories
        self.graph_builder.add_edge(START, "intake_agent")
        self.graph_builder.add_edge("intake_agent", "business_analyst_agent")
        
        # Review User stories
        self.graph_builder.add_edge("business_analyst_agent", "human_po_review") 
        
        self.graph_builder.add_conditional_edges(
            "human_po_review",
            self.project_requirement_node.review_user_stories_router,
            {
                "approved": "architect_agent",
                "feedback": "business_analyst_agent"
            }
        )
        
        
        # Phase 2: Design Documents
        self.graph_builder.add_edge("architect_agent", "human_design_review")
        self.graph_builder.add_conditional_edges(
            "human_design_review",
            self.design_doc_node.review_design_documents_router,
            {
                "approved": "developer_agent",
                "feedback": "architect_agent"
            }
        )
     

        # Phase 3: Code Generate using design document and review
        self.graph_builder.add_edge("developer_agent", "human_code_review")
        self.graph_builder.add_conditional_edges(
            "human_code_review",
            self.coding_node.code_review_router,
            {
                "approved": "security_consultant_agent",
                "feedback": "developer_agent"
            }
        )
     

        # Phase 4: Security Review 
        self.graph_builder.add_edge("security_consultant_agent", "human_security_review")
        self.graph_builder.add_conditional_edges(
            "human_security_review",
            self.security_node.security_review_router,
            {
                "approved": "sdet_agent",
                "feedback": "developer_agent"
            }
        )
     
        # Phase 5: Test Cases 
        self.graph_builder.add_edge("sdet_agent", "human_test_review")
        self.graph_builder.add_conditional_edges(
            "human_test_review",
            self.test_node.review_test_cases_router,
            {
                "approved": "execution_agent",
                "feedback": "sdet_agent"
            }
        )
     

        # Phase 6: QA Testing
        self.graph_builder.add_edge("execution_agent", "human_final_qa_review")
        self.graph_builder.add_conditional_edges(
            "human_final_qa_review",
            self.qa_node.review_qa_router,
            {
                "approved": "artifact_compiler_agent",
                "feedback": "developer_agent"
            }
        )

        # Phase 7: Download Artifacts
        self.graph_builder.add_edge("artifact_compiler_agent", END)


        
    def setup_graph(self):
        """
        Sets up the graph
        """
        self.build_sdlc_graph()
        return self.graph_builder.compile(
            interrupt_before=[
                'intake_agent',
                'human_po_review',        
                'human_design_review',    
                'human_code_review',      
                'human_security_review',  
                'human_test_review',     
                'human_final_qa_review'
            ], checkpointer=self.memory
        )
        
             
    
    
    def save_graph_image(self,graph):
        # Generate the PNG image
        img_data = graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API
            )

        # Save the image to a file
        graph_path = "workflow_graph.png"
        with open(graph_path, "wb") as f:
            f.write(img_data)