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
        for event in graph.stream({"project_name": project_name}, thread, stream_mode="values"):
           state = event
        
        current_state = graph.get_state(thread)
        save_state_to_redis(task_id, current_state)
        
        return {"task_id" : task_id, "state": state}
    
    ## ------- User Story Generation ------- ##
    def generate_stories(self, task_id:str, requirements: list[str]):
        # LangGraph prefers state diffs/updates rather than replacing the whole state object.
        update_payload = {
            "requirements": requirements,
            "next_node": "human_po_review"  # Updated to our new HITL naming convention!
        }
        
        # Inject just the updates as if the intake_agent generated them
        return self.update_and_resume_graph(update_payload, task_id, "intake_agent")

    
    ## -------- Helper Method to handle the graph resume state ------- ##
    def update_and_resume_graph(self, saved_state, task_id, as_node):
        graph = self.graph
        thread = self.get_thread(task_id)
        
        # Inject state at the exact node location
        graph.update_state(thread, saved_state, as_node=as_node)
        
        # Resume the graph
        state = None
        for event in graph.stream(None, thread, stream_mode="values"):
            state = event
        
        # saving the state before asking for the next review
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
                node_name = "human_po_review"
                saved_state['next_node'] = "human_po_review" if status == "feedback" else "human_design_review" 

            elif review_type == "review_design_documents":
                saved_state['design_documents_review_status'] = status
                saved_state['design_documents_feedback'] = feedback
                node_name = "human_design_review"
                saved_state['next_node'] = "human_design_review" if status == "feedback" else "human_code_review"   

            elif review_type == "review_code":
                saved_state['code_review_status'] = status
                saved_state['code_review_feedback'] = feedback
                node_name = "human_code_review"
                saved_state['next_node'] = "human_code_review" if status == "feedback" else "human_security_review"

            elif review_type == "review_security_recommendations":
                saved_state['security_review_status'] = status
                saved_state['security_review_comments'] = feedback
                node_name = "human_security_review"   
                # ✅ FIX: Feedback goes back to developer, so UI must move to Code Review
                saved_state['next_node'] = "human_code_review" if status == "feedback" else "human_test_review"

            elif review_type == "review_test_cases":
                saved_state['test_case_review_status'] = status
                saved_state['test_case_review_feedback'] = feedback
                node_name = "human_test_review" 
                saved_state['next_node'] = "human_test_review" if status == "feedback" else "human_final_qa_review"

            elif review_type == "review_qa_testing":
                saved_state['qa_testing_status'] = status
                saved_state['qa_testing_feedback'] = feedback
                node_name = "human_final_qa_review"  
                # ✅ FIX: Feedback goes back to developer, so UI must move to Code Review
                saved_state['next_node'] = "human_code_review" if status == "feedback" else "END"

            else:
                raise ValueError(f"Unsupported review type: {review_type}")

        return self.update_and_resume_graph(saved_state, task_id, node_name)


