from langgraph.graph import StateGraph,START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables.graph import MermaidDrawMethod
from src.sdlc_system.nodes.project_requirement_node import ProjectRequirementNode
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
   
        ## Nodes
   
        self.graph_builder.add_node("get_user_requirements", self.project_requirement_node.get_user_requirements)
        
        self.graph_builder.add_node("generate_user_stories", self.project_requirement_node.generate_user_stories)
        self.graph_builder.add_node("review_user_stories", self.project_requirement_node.review_user_stories)
        self.graph_builder.add_node("revise_user_stories", self.project_requirement_node.revise_user_stories)
        
        
        
        ## Edges
   
        self.graph_builder.add_edge(START,"get_user_requirements")
        self.graph_builder.add_edge("get_user_requirements","generate_user_stories")
        self.graph_builder.add_edge("generate_user_stories","review_user_stories") 
        self.graph_builder.add_conditional_edges(
            "review_user_stories",
            self.project_requirement_node.review_user_stories_router,
            {
                # "approved": "create_design_documents",
                "approved": END,
                "feedback": "revise_user_stories"
            }
        )
        self.graph_builder.add_edge("revise_user_stories","generate_user_stories")
        
              
        
    def setup_graph(self):
        """
        Sets up the graph
        """
        self.build_sdlc_graph()
        return self.graph_builder.compile(
            interrupt_before=[
                'get_user_requirements',
                'review_user_stories',
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
            
        