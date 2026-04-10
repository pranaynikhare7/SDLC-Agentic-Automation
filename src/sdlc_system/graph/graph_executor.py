from src.sdlc_system.state.state_file import SDLCState
from src.sdlc_system.cache.redis_cache import flush_redis_cache, save_state_to_redis, get_state_from_redis
import uuid


class GraphExecutor:
    def __init__(self, graph):
        self.graph = graph

    def get_thread(self, task_id):
        return {"configurable": {"thread_id": task_id}}
    
    ## ------- Start the Workflow ------- ##
    def start_workflow(self, project_name: str):
        
        graph = self.graph
        
        flush_redis_cache()
        
        # Generate a unique task id
        task_id = f"sdlc-session-{uuid.uuid4().hex[:8]}"
        
        thread = self.get_thread(task_id)
        
        state = None
        for event in graph.stream({"project_name": project_name},thread, stream_mode="values"):
           state = event
        
        current_state = graph.get_state(thread)
        save_state_to_redis(task_id, current_state)
        
        return {"task_id" : task_id, "state": state}
    
    ## ------- User Story Generation ------- ##
    def generate_stories(self, task_id:str, requirements: list[str]):
        saved_state = get_state_from_redis(task_id)
        if saved_state:
            saved_state['requirements'] = requirements
            saved_state['next_node'] = "review_user_stories"
        
        return self.update_and_resume_graph(saved_state,task_id,"get_user_requirements")


    
        
    ## -------- Helper Method to handle the graph resume state ------- ##
    def update_and_resume_graph(self, saved_state,task_id, as_node):
        graph = self.graph
        thread = self.get_thread(task_id)
        
        graph.update_state(thread, saved_state, as_node=as_node)
        
         # Resume the graph
        state = None
        for event in graph.stream(None, thread, stream_mode="values"):
            state = event
        
        # saving the state before asking the product owner for review
        current_state = graph.get_state(thread)
        save_state_to_redis(task_id, current_state)
        
        return {"task_id" : task_id, "state": state}


    def get_updated_state(self, task_id):
        saved_state = get_state_from_redis(task_id)
        return {"task_id" : task_id, "state": saved_state}
    
    ## ------- Generic Review Flow for all the feedback stages  ------- ##
    def graph_review_flow(self, task_id, status, feedback, review_type):
        saved_state = get_state_from_redis(task_id)
        
        if saved_state:
            if review_type == "review_user_stories":
                saved_state['user_stories_review_status'] = status
                saved_state['user_stories_feedback'] = feedback
                node_name = "review_user_stories"
                saved_state['next_node'] = "review_user_stories" if status == "feedback" else "review_design_documents" 

            elif review_type == "review_design_documents":
                saved_state['design_documents_review_status'] = status
                saved_state['design_documents_feedback'] = feedback
                node_name = "review_design_documents"
                saved_state['next_node'] = "review_design_documents" if status == "feedback" else "review_code"   

            elif review_type == "review_code":
                saved_state['code_review_status'] = status
                saved_state['code_review_feedback'] = feedback
                node_name = "code_review"
                saved_state['next_node'] = "review_code" if status == "feedback" else "review_security_recommendations"
                
            elif review_type == "review_security_recommendations":
                saved_state['security_review_status'] = status
                saved_state['security_review_comments'] = feedback
                node_name = "security_review"   
                saved_state['next_node'] = "review_security_recommendations" if status == "feedback" else "review_test_cases"

            elif review_type == "review_test_cases":
                saved_state['test_case_review_status'] = status
                saved_state['test_case_review_feedback'] = feedback
                node_name = "review_test_cases" 
                saved_state['next_node'] = "review_test_cases" if status == "feedback" else "review_qa_testing"
                 
            elif review_type == "review_qa_testing":
                saved_state['qa_testing_status'] = status
                saved_state['qa_testing_feedback'] = feedback
                node_name = "qa_review"  
                saved_state['next_node'] = "review_qa_testing" if status == "feedback" else "END"


            else:
                raise ValueError(f"Unsupported review type: {review_type}")
            

        return self.update_and_resume_graph(saved_state,task_id,node_name)