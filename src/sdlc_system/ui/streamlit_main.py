import streamlit as st
import re
import os
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from src.sdlc_system.graph.build_graph import GraphBuilder
from src.sdlc_system.graph.graph_executor import GraphExecutor
from src.sdlc_system.cache.redis_cache import get_state_from_redis

# --- Backend Initialization (Cached) ---
# Kept outside the function so Streamlit can cache it at the module level
@st.cache_resource(show_spinner="Connecting to AI Engine...")
def get_executor(provider, model_name, api_key):
    if not api_key:
        return None
    try:
        if provider == "OpenAI":
            llm = ChatOpenAI(model=model_name, openai_api_key=api_key)
        else:
            llm = ChatGroq(model=model_name, groq_api_key=api_key)
            
        builder = GraphBuilder(llm)
        graph = builder.setup_graph()
        return GraphExecutor(graph)
    except Exception as e:
        st.error(f"Initialization Error: {e}")
        return None

def run_sdlc_app():
    # --- Page Config ---
    # Must be the first Streamlit command called
    st.set_page_config(page_title="AI SDLC Designer Pro", layout="wide", page_icon="🛡️")

    # --- Sidebar: Configuration & Session Management ---
    with st.sidebar:
        st.header("🔑 API Configuration")
        
        # 1. LLM Provider Selection
        provider = st.selectbox("Select Provider", ["OpenAI", "Groq"])
        
        # 2. Dynamic Model Selection & Key Input
        if provider == "OpenAI":
            api_key = st.text_input("OpenAI API Key", type="password", help="Enter your sk-... key")
            model_name = st.selectbox("Select Model", ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo"])
        else:
            api_key = st.text_input("Groq API Key", type="password", help="Enter your gsk-... key")
            model_name = st.selectbox("Select Model", [
                "openai/gpt-oss-20b",
                "openai/gpt-oss-120b", 
                "llama-3.3-70b-versatile", 
                "llama-3.1-8b-instant"
            ])

        st.divider()
        st.header("📂 Session Management")
        recovery_id = st.text_input("Resume Task ID")
        
        if st.button("Resume Session") and recovery_id:
            latest_state = get_state_from_redis(recovery_id)
            if latest_state:
                st.session_state.current_state = latest_state
                st.session_state.task_id = recovery_id
                st.success(f"Resumed: {recovery_id}")
            else:
                st.error("Task ID not found in cache.")

        if st.session_state.get("task_id"):
            st.divider()
            st.success(f"**Active Session:** `{st.session_state.task_id}`")
            st.info(f"**Current Node:** `{st.session_state.get('current_state', {}).get('next_node', 'Start')}`")
            if st.button("🗑️ Clear / New Project", use_container_width=True):
                st.session_state.clear()
                st.rerun()

    # Instantiate Executor
    executor = get_executor(provider, model_name, api_key)

    # --- Main UI Logic ---
    st.title("🛡️ Agentic SDLC Automation System")

    # Guardrail: Ensure keys are present before showing workflow
    if not api_key:
        st.info("👈 Please enter your API Key in the sidebar to get started.")
        st.stop()

    if not executor:
        st.error("The AI Engine could not be started. Check your API key and model selection.")
        st.stop()

    # Get current workflow state
    state = st.session_state.get("current_state", {})
    next_step = state.get("next_node")

    # --- WORKFLOW STAGES ---

    # Stage 1: New Project Initialization
    if "task_id" not in st.session_state:
        st.subheader("🚀 Start a New Software Project")
        p_name = st.text_input("Project Name", value="Simple Calculator")
        if st.button("Initialize Workflow"):
            response = executor.start_workflow(p_name)
            st.session_state.task_id = response["task_id"]
            st.session_state.current_state = response["state"]
            st.rerun()

    # Stage 2: Requirement Gathering
    elif not next_step:
        st.subheader(f"📝 Project: {state.get('project_name', 'Unknown')}")
        req_input = st.text_area("Enter Requirements (one per line)", height=150, placeholder="1. User can add two numbers\n2. User can subtract two numbers...")
        if st.button("Generate Stories"):
            requirements = [r.strip() for r in req_input.split("\n") if r.strip()]
            if not requirements:
                st.warning("Please enter at least one requirement.")
            else:
                with st.spinner("Business Analyst Agent is drafting user stories..."):
                    response = executor.generate_stories(st.session_state.task_id, requirements)
                    st.session_state.current_state = response["state"]
                    st.rerun()

    # Stage 3: Review User Stories
    elif next_step == "human_po_review":
        st.subheader("📋 Phase 1: Product Owner Review")
        stories_data = state.get("user_stories", {})
        stories = stories_data.user_stories if hasattr(stories_data, 'user_stories') else stories_data.get('user_stories', [])
        
        for story in stories:
            with st.expander(f"**{story['id'] if isinstance(story, dict) else story.id}**: {story['title'] if isinstance(story, dict) else story.title}"):
                st.write(story['description'] if isinstance(story, dict) else story.description)
                st.caption(f"Priority: {story['priority'] if isinstance(story, dict) else story.priority}")
        
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Stories", use_container_width=True):
                with st.spinner("Architect Agent is building Design Documents..."):
                    response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_user_stories")
                    st.session_state.current_state = response["state"]
                    st.rerun()
        with c2:
            with st.popover("🔄 Revise Stories"):
                fback = st.text_area("What should change in stories?")
                if st.button("Submit Story Feedback"):
                    with st.spinner("Business Analyst is revising stories..."):
                        response = executor.graph_review_flow(st.session_state.task_id, "feedback", fback, "review_user_stories")
                        st.session_state.current_state = response["state"]
                        st.rerun()

    # Stage 4: Review Design Documents
    elif next_step == "human_design_review":
        st.subheader("🏗️ Phase 2: Architecture Review")
        design = state.get("design_documents", {})
        design_dict = design.model_dump() if hasattr(design, "model_dump") else design
        
        t1, t2 = st.tabs(["📄 Functional Design", "💻 Technical Design"])
        with t1: st.markdown(design_dict.get('functional', ''))
        with t2: st.markdown(design_dict.get('technical', ''))

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Design", use_container_width=True):
                with st.spinner("Developer Agent is generating code..."):
                    response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_design_documents")
                    st.session_state.current_state = response["state"]
                    st.rerun()
        with c2:
            with st.popover("🔄 Revise Design"):
                fback = st.text_area("What should change in design?")
                if st.button("Submit Design Feedback"):
                    with st.spinner("Architect Agent is revising designs..."):
                        response = executor.graph_review_flow(st.session_state.task_id, "feedback", fback, "review_design_documents")
                        st.session_state.current_state = response["state"]
                        st.rerun()

    # Stage 5: Code Review
    elif next_step == "human_code_review":
        st.subheader("💻 Phase 3: Code Review")
        col_code, col_review = st.columns([2, 1])
        with col_code:
            st.markdown("**Generated Code**")
            st.code(state.get("code_generated", "# No code found"), language="python")
        with col_review:
            st.markdown("**AI Peer Review Comments**")
            st.info(state.get("code_review_comments", "No comments available."))

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Code", use_container_width=True):
                with st.spinner("Security Consultant Agent is running security review..."):
                    response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_code")
                    st.session_state.current_state = response["state"]
                    st.rerun()
        with c2:
            with st.popover("🔄 Request Code Fix"):
                fback = st.text_area("Specify changes/fixes needed:")
                if st.button("Submit Code Feedback"):
                    with st.spinner("Developer Agent is refactoring code..."):
                        response = executor.graph_review_flow(st.session_state.task_id, "feedback", fback, "review_code")
                        st.session_state.current_state = response["state"]
                        st.rerun()

    # Stage 6: Security Review
    elif next_step == "human_security_review":
        st.subheader("🔒 Phase 4: Security Review")
        t1, t2 = st.tabs(["🛡️ Security Recommendations", "📝 Auditor Comments"])
        with t1: st.warning(state.get("security_recommendations", "Scanning complete (No data returned)."))
        with t2: st.markdown(state.get("security_review_comments", "N/A"))

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Security", use_container_width=True):
                with st.spinner("SDET Agent is writing Test Suite..."):
                    response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_security_recommendations")
                    st.session_state.current_state = response["state"]
                    st.rerun()
        with c2:
            with st.popover("🚨 Security Feedback"):
                fback = st.text_area("Describe security vulnerabilities to fix:")
                if st.button("Send Back to Coding"):
                    with st.spinner("Developer Agent is applying patches..."):
                        response = executor.graph_review_flow(st.session_state.task_id, "feedback", fback, "review_security_recommendations")
                        st.session_state.current_state = response["state"]
                        st.rerun()

    # Stage 7: Review Test Cases
    elif next_step == "human_test_review":
        st.subheader("🧪 Phase 5: Test Plan Review")
        test_cases = state.get("test_cases", "")
        if not test_cases:
            st.error("⚠️ AI returned an empty test suite.")
        else:
            st.code(test_cases, language="python")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Test Cases", use_container_width=True):
                with st.spinner("Execution Agent is running tests..."):
                    response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_test_cases")
                    st.session_state.current_state = response["state"]
                    st.rerun()
        with c2:
            with st.popover("🔄 Revise Test Cases"):
                fback = st.text_area("What is missing in the test cases?")
                if st.button("Submit Test Feedback"):
                    with st.spinner("SDET Agent is regenerating..."):
                        response = executor.graph_review_flow(st.session_state.task_id, "feedback", fback, "review_test_cases")
                        st.session_state.current_state = response["state"]
                        st.rerun()

    # Stage 8: QA Review
    elif next_step == "human_final_qa_review":
        st.subheader("🧐 Phase 6: Final QA Review")
        
        with st.expander("📊 Detailed QA Report", expanded=True):
            qa_results = state.get("qa_testing_comments", "") 
            pass_count = len(re.findall(r"status[:\s\*]*pass", qa_results, re.IGNORECASE))
            fail_count = len(re.findall(r"status[:\s\*]*fail", qa_results, re.IGNORECASE))
            total = pass_count + fail_count

            col1, col2 = st.columns(2)
            col1.metric("Tests Passed", f"{pass_count}/{total}" if total > 0 else "0", delta=None)
            col2.metric("Tests Failed", f"{fail_count}/{total}" if total > 0 else "0", 
                        delta=f"-{fail_count}" if fail_count > 0 else None, 
                        delta_color="inverse")

            st.divider()
            if qa_results:
                st.markdown(qa_results)
            else:
                st.warning("No QA testing data found in state.")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 Final Release Approval", use_container_width=True):
                with st.spinner("Artifact Compiler Agent is packaging files..."):
                    response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_qa_testing")
                    st.session_state.current_state = response["state"]
                    st.rerun()
        with c2:
            with st.popover("🐞 Bugs Found - Reject"):
                fback = st.text_area("List bugs to be fixed in the code:")
                if st.button("Submit Bug Report"):
                    with st.spinner("Sending bugs back to developer agent..."):
                        response = executor.graph_review_flow(st.session_state.task_id, "feedback", fback, "review_qa_testing")
                        st.session_state.current_state = response["state"]
                        st.rerun()

    # Stage 9: Final Download Artifacts
    else:
        st.balloons()
        st.subheader("🎉 Project Complete: Artifacts Ready")
        st.success("Your software has passed all checks and is ready for deployment!")
        
        st.markdown("### 📥 Download Center")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.download_button("💻 Download Source Code", data=state.get("code_generated", ""), file_name="main_app.py", mime="text/x-python", use_container_width=True)
        with col2:
            design = state.get("design_documents", {})
            d_dict = design.model_dump() if hasattr(design, "model_dump") else design
            st.download_button("🏗️ Download Design Docs", data=f"# Functional\n{d_dict.get('functional','')}\n\n# Technical\n{d_dict.get('technical','')}", file_name="design.md", mime="text/markdown", use_container_width=True)
        with col3:
            st.download_button("🧪 Download Test Suite", data=state.get("test_cases", ""), file_name="tests.py", mime="text/x-python", use_container_width=True)

if __name__ == "__main__":
    # Execute the Streamlit UI flow
    run_sdlc_app()