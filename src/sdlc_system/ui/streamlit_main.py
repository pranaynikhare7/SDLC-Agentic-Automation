import streamlit as st
import re
import io
import zipfile
from langchain_openai import ChatOpenAI

from src.sdlc_system.graph.build_graph import GraphBuilder
from src.sdlc_system.graph.graph_executor import GraphExecutor
from src.sdlc_system.cache.redis_cache import get_state_from_redis

# --- Initialize Backend ---
# We keep this outside the main function so Streamlit caches it globally
@st.cache_resource
def get_executor():
    llm = ChatOpenAI(model='gpt-4o-mini')
    builder = GraphBuilder(llm)
    graph = builder.setup_graph()
    return GraphExecutor(graph)


# --- Utility Functions ---
def package_code_to_zip(raw_llm_output):
    """
    Parses a string containing multiple Markdown code blocks, extracts the code,
    guesses the filenames, and returns a binary ZIP file in memory.
    """
    files_to_zip = {}
    
    # Safely construct the regex pattern without using literal triple-backticks
    # This prevents markdown parsers from prematurely cutting off the code!
    fence = '`' * 3
    pattern = fence + r'(?:python)?\n(.*?)' + fence
    
    blocks = re.finditer(pattern, raw_llm_output, re.DOTALL | re.IGNORECASE)
    
    match_found = False
    for i, block in enumerate(blocks):
        match_found = True
        content = block.group(1).strip()
        
        first_line = content.split('\n')[0].strip()
        if first_line.startswith('#') and ('.py' in first_line or '.' in first_line):
            filename = first_line.replace('#', '').strip()
        else:
            filename = f"module_{i+1}.py"
            
        files_to_zip[filename] = content
        
    if not match_found:
        files_to_zip['generated_app.py'] = raw_llm_output

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for file_name, file_content in files_to_zip.items():
            zip_file.writestr(file_name, file_content)
            
    return zip_buffer.getvalue()


# --- Main Application Function ---
def run_sdlc_app():
    """
    The main entry point for the Streamlit UI.
    Call this function from your root app.py file.
    """
    # st.set_page_config MUST be the first Streamlit command called
    st.set_page_config(page_title="AI SDLC Designer", layout="wide")
    
    executor = get_executor()

    # --- Nested UI Helpers ---
    # Nesting these here gives them access to the local `executor` instance
    def sync_state(task_id):
        latest_state = get_state_from_redis(task_id)
        if latest_state:
            st.session_state.current_state = latest_state
            st.session_state.task_id = task_id
            st.sidebar.success("Session restored!")
            st.rerun()
        else:
            st.sidebar.error("Invalid Task ID or session expired.")

    def execute_node_transition(task_id, status, feedback, node_name, loading_msg):
        try:
            with st.spinner(loading_msg):
                response = executor.graph_review_flow(task_id, status, feedback, node_name)
                st.session_state.current_state = response["state"]
                st.rerun()
        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}")

    # --- App Logic & UI Rendering ---
    st.title("🛡️ SDLC Automation System")

    # Sidebar for Session Recovery & Status
    with st.sidebar:
        st.header("Session Management")
        recovery_id = st.text_input("Resume Task ID")
        if st.button("Resume Session") and recovery_id:
            sync_state(recovery_id)
        
        if st.session_state.get("task_id"):
            st.success(f"Active Session: `{st.session_state.task_id}`")
            st.info(f"Current Node: `{st.session_state.current_state.get('next_node', 'Start')}`")
            if st.button("Clear / New Project"):
                st.session_state.clear()
                st.rerun()

    # --- WORKFLOW ROUTING ---
    state = st.session_state.get("current_state", {})
    next_step = state.get("next_node")

    # Stage 1: New Project Initialization
    if "task_id" not in st.session_state:
        st.subheader("Start a New Software Project")
        p_name = st.text_input("Project Name", value="Smart Home IoT Dashboard")
        if st.button("Initialize Workflow"):
            try:
                response = executor.start_workflow(p_name)
                st.session_state.task_id = response["task_id"]
                st.session_state.current_state = response["state"]
                st.rerun()
            except Exception as e:
                st.error(f"Failed to initialize workflow: {str(e)}")

    # Stage 2: Requirement Gathering
    elif not next_step:
        st.subheader(f"Project: {state.get('project_name', 'Unknown')}")
        req_input = st.text_area("Enter Requirements (one per line)", height=150)
        if st.button("Generate Stories"):
            requirements = [r.strip() for r in req_input.split("\n") if r.strip()]
            try:
                with st.spinner("AI is drafting user stories..."):
                    response = executor.generate_stories(st.session_state.task_id, requirements)
                    st.session_state.current_state = response["state"]
                    st.rerun()
            except Exception as e:
                st.error(f"Failed to generate stories: {str(e)}")

    # Stage 3: Review User Stories
    elif next_step == "review_user_stories":
        st.subheader("📋 Phase 1: Review User Stories")
        stories_data = state.get("user_stories", {})
        stories = stories_data.user_stories if hasattr(stories_data, 'user_stories') else stories_data.get('user_stories', [])
        
        for story in stories:
            sid = story['id'] if isinstance(story, dict) else story.id
            title = story['title'] if isinstance(story, dict) else story.title
            desc = story['description'] if isinstance(story, dict) else story.description
            prio = story['priority'] if isinstance(story, dict) else story.priority
            
            with st.expander(f"**{sid}**: {title}"):
                st.write(desc)
                st.caption(f"Priority: {prio}")
        
        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Stories", use_container_width=True):
                execute_node_transition(st.session_state.task_id, "approved", "", "review_user_stories", "Architecting Design Documents...")
        with c2:
            with st.popover("🔄 Revise Stories"):
                fback = st.text_area("What should change in stories?")
                if st.button("Submit Story Feedback"):
                    execute_node_transition(st.session_state.task_id, "feedback", fback, "review_user_stories", "Revising stories...")

    # Stage 4: Review Design Documents
    elif next_step == "review_design_documents":
        st.subheader("🏗️ Phase 2: Design Documents")
        design = state.get("design_documents", {})
        design_dict = design.model_dump() if hasattr(design, "model_dump") else design
        
        t1, t2 = st.tabs(["📄 Functional Design", "💻 Technical Design"])
        with t1: st.markdown(design_dict.get('functional', ''))
        with t2: st.markdown(f"```markdown\n{design_dict.get('technical', '')}\n```")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Design", use_container_width=True):
                execute_node_transition(st.session_state.task_id, "approved", "", "review_design_documents", "Generating application code...")
        with c2:
            with st.popover("🔄 Revise Design"):
                fback = st.text_area("What should change in design?")
                if st.button("Submit Design Feedback"):
                    execute_node_transition(st.session_state.task_id, "feedback", fback, "review_design_documents", "Revising design...")

    # Stage 5: Code Review
    elif next_step == "review_code":
        st.subheader("💻 Phase 3: Code Review")
        col_code, col_review = st.columns([2, 1])
        with col_code:
            st.markdown("**Generated Code**")
            st.code(state.get("code_generated", "# Code generation failed"), language="python")
        with col_review:
            st.markdown("**AI Peer Review Comments**")
            st.info(state.get("code_review_comments", "No comments available."))

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Code", use_container_width=True):
                execute_node_transition(st.session_state.task_id, "approved", "", "review_code", "Running security review...")
        with c2:
            with st.popover("🔄 Request Code Fix"):
                fback = st.text_area("Specify changes/fixes needed:")
                if st.button("Submit Code Feedback"):
                    execute_node_transition(st.session_state.task_id, "feedback", fback, "review_code", "Refactoring code...")

    # Stage 6: Security Review
    elif next_step == "review_security_recommendations":
        st.subheader("🔒 Phase 4: Security Review")
        t1, t2 = st.tabs(["🛡️ Security Recommendations", "📝 Auditor Comments"])
        with t1: st.warning(state.get("security_recommendations", "No data returned."))
        with t2: st.markdown(state.get("security_review_comments", "N/A"))

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Security", use_container_width=True):
                execute_node_transition(st.session_state.task_id, "approved", "", "review_security_recommendations", "Writing Test Suite...")
        with c2:
            with st.popover("🚨 Security Feedback"):
                fback = st.text_area("Describe security vulnerabilities to fix:")
                if st.button("Send Back to Coding"):
                    execute_node_transition(st.session_state.task_id, "feedback", fback, "review_security_recommendations", "Applying security patches...")

    # Stage 7: Review Test Cases
    elif next_step == "review_test_cases":
        st.subheader("🧪 Phase 5: Test Case Review")
        test_cases = state.get("test_cases", "")
        if not test_cases:
            st.error("⚠️ AI returned an empty test suite. Please request a revision.")
        else:
            st.code(test_cases, language="python")

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Approve Test Cases", use_container_width=True):
                execute_node_transition(st.session_state.task_id, "approved", "", "review_test_cases", "Executing QA Tests...")
        with c2:
            with st.popover("🔄 Revise Test Cases"):
                fback = st.text_area("What is missing in the test cases?")
                if st.button("Submit Test Feedback"):
                    execute_node_transition(st.session_state.task_id, "feedback", fback, "review_test_cases", "Regenerating test cases...")

    # Stage 8: QA Review
    elif next_step == "review_qa_testing":
        st.subheader("🧐 Phase 6: QA Review & Bug Report")
        st.error(state.get("qa_testing_comments", "Testing data missing..."))

        st.divider()
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🚀 Final Release Approval", use_container_width=True):
                execute_node_transition(st.session_state.task_id, "approved", "", "review_qa_testing", "Packaging artifacts...")
        with c2:
            with st.popover("🐞 Bugs Found - Reject"):
                fback = st.text_area("List bugs to be fixed in the code:")
                if st.button("Submit Bug Report"):
                    execute_node_transition(st.session_state.task_id, "feedback", fback, "review_qa_testing", "Sending bugs back to engineering...")

    # Stage 9: Final Download Artifacts
    else:
        st.balloons()
        st.subheader("🎉 Project Complete: Artifacts Ready")
        st.success("Your software has passed all checks and is ready for deployment!")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            raw_code = state.get("code_generated", "")
            zip_data = package_code_to_zip(raw_code)
            
            st.download_button(
                label="📦 Download Project Code (.zip)", 
                data=zip_data, 
                file_name=f"{state.get('project_name', 'project').replace(' ', '_')}_code.zip", 
                mime="application/zip", 
                use_container_width=True
            )
            
        with col2:
            design = state.get("design_documents", {})
            d_dict = design.model_dump() if hasattr(design, "model_dump") else design
            markdown_content = f"# Functional Design\n{d_dict.get('functional','')}\n\n# Technical Design\n{d_dict.get('technical','')}"
            
            st.download_button(
                label="🏗️ Download Design Docs", 
                data=markdown_content, 
                file_name="architecture_docs.md", 
                mime="text/markdown", 
                use_container_width=True
            )
            
        with col3:
            st.download_button(
                label="🧪 Download Test Suite", 
                data=state.get("test_cases", ""), 
                file_name="test_suite.py", 
                mime="text/x-python", 
                use_container_width=True
            )