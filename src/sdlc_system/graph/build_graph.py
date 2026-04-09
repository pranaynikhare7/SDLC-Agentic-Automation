from langgraph.graph import StateGraph,START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.graph import MermaidDrawMethod
from src.sdlc_system.nodes.project_requirement_node import ProjectRequirementNode
from src.sdlc_system.nodes.design_doc_node import DesingDocumentNode
from src.sdlc_system.state.state_file import SDLCState

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
   
        ## Nodes
   
        self.graph_builder.add_node("get_user_requirements", self.project_requirement_node.get_user_requirements)
        
        # Phase 1: User Stories
        self.graph_builder.add_node("generate_user_stories", self.project_requirement_node.generate_user_stories)
        self.graph_builder.add_node("review_user_stories", self.project_requirement_node.review_user_stories)
        self.graph_builder.add_node("revise_user_stories", self.project_requirement_node.revise_user_stories)
        
        # Phase 2: Design Documents
        self.graph_builder.add_node("create_design_documents", self.design_doc_node.create_design_documents)
        self.graph_builder.add_node("review_design_documents", self.design_doc_node.review_design_documents)
        self.graph_builder.add_node("revise_design_documents", self.design_doc_node.revise_design_documents)
        

        
        
        ## Edges
   
        self.graph_builder.add_edge(START,"get_user_requirements")
        self.graph_builder.add_edge("get_user_requirements","generate_user_stories")
        
        
        self.graph_builder.add_edge("generate_user_stories","review_user_stories") 
        self.graph_builder.add_conditional_edges(
            "review_user_stories",
            self.project_requirement_node.review_user_stories_router,
            {
                "approved": "create_design_documents",
                "feedback": "revise_user_stories"
            }
        )
        self.graph_builder.add_edge("revise_user_stories","generate_user_stories")
        
        
        self.graph_builder.add_edge("create_design_documents","review_design_documents")
        self.graph_builder.add_conditional_edges(
            "review_design_documents",
            self.design_doc_node.review_design_documents_router,
            {
                # "approved": "generate_code",
                "approved": END,
                "feedback": "revise_design_documents"
            }
        )
        self.graph_builder.add_edge("revise_design_documents","create_design_documents")




        
    def setup_graph(self):
        """
        Sets up the graph
        """
        self.build_sdlc_graph()
        return self.graph_builder.compile(
            interrupt_before=[
                'get_user_requirements',
                'review_user_stories',
                'review_design_documents'
            ],checkpointer=self.memory
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
            
        