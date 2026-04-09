import streamlit as st
from langchain_groq import ChatGroq
from src.sdlc_system.graph.build_graph import GraphBuilder
from src.sdlc_system.graph.graph_executor import GraphExecutor
from src.sdlc_system.cache.redis_cache import get_state_from_redis

# --- Page Config ---
st.set_page_config(page_title="AI SDLC Designer", layout="wide")

# --- Initialize Backend ---
@st.cache_resource
def get_executor():
    llm = ChatGroq(model='openai/gpt-oss-20b')
    builder = GraphBuilder(llm)
    graph = builder.setup_graph()
    return GraphExecutor(graph)

executor = get_executor()

# --- Helper: Sync UI State ---
def sync_state(task_id):
    latest_state = get_state_from_redis(task_id)
    if latest_state:
        st.session_state.current_state = latest_state
        st.session_state.task_id = task_id

# --- App Logic ---
st.title("🛡️ Redis-Backed SDLC Agent")

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

# Stage 1: New Project Initialization
if "task_id" not in st.session_state:
    st.subheader("Start a New Software Project")
    p_name = st.text_input("Project Name", value="Smart Home IoT Dashboard")
    if st.button("Initialize Workflow"):
        response = executor.start_workflow(p_name)
        st.session_state.task_id = response["task_id"]
        st.session_state.current_state = response["state"]
        st.rerun()

# Stage 2: Requirement Gathering
elif not state.get("user_stories"):
    st.subheader(f"Project: {state['project_name']}")
    req_input = st.text_area("Enter Requirements (one per line)", height=150)
    if st.button("Generate Stories"):
        requirements = [r.strip() for r in req_input.split("\n") if r.strip()]
        with st.spinner("AI is drafting user stories..."):
            response = executor.generate_stories(st.session_state.task_id, requirements)
            st.session_state.current_state = response["state"]
            st.rerun()

# Stage 3: Review User Stories
elif not state.get("design_documents"):
    st.subheader("📋 Phase 1: Review User Stories")
    stories_data = state["user_stories"]
    stories = stories_data.user_stories if hasattr(stories_data, 'user_stories') else stories_data['user_stories']
    
    # for story in stories:
    #     story_dict = story.model_dump() if hasattr(story, "model_dump") else story

    #     with st.expander(f"**{story_dict.get('id', 'US')}**: {story_dict.get('title', 'Title')}"):
    #         st.write(story_dict.get('description', ''))
    #         st.caption(f"Priority: {story_dict.get('priority', '3')}")

    for story in stories:
        with st.expander(f"**{story['id'] if isinstance(story, dict) else story.id}**: {story['title'] if isinstance(story, dict) else story.title}"):
            st.write(story['description'] if isinstance(story, dict) else story.description)
            st.caption(f"Priority: {story['priority'] if isinstance(story, dict) else story.priority}")

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Approve Stories", use_container_width=True):
            response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_user_stories")
            st.session_state.current_state = response["state"]
            st.rerun()
    with c2:
        with st.popover("🔄 Revise Stories"):
            feedback = st.text_area("What should change in stories?")
            if st.button("Submit Story Feedback"):
                response = executor.graph_review_flow(st.session_state.task_id, "feedback", feedback, "review_user_stories")
                st.session_state.current_state = response["state"]
                st.rerun()

# Stage 4: Review Design Documents
elif not state.get("code_generated"):
    st.subheader("🏗️ Phase 2: Design Documents")
    design = state["design_documents"]
    t1, t2 = st.tabs(["📄 Functional Design", "💻 Technical Design"])

    design_dict = design.model_dump() if hasattr(design, "model_dump") else design

    with t1: 
        st.markdown(design_dict.get('functional', ''))

    with t2: 
        st.markdown(f"```markdown\n{design_dict.get('technical', '')}\n```")


    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Approve Design", use_container_width=True):
            response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_design_documents")
            st.session_state.current_state = response["state"]
            st.rerun()
    with c2:
        with st.popover("🔄 Revise Design"):
            fback = st.text_area("What should change in design?")
            if st.button("Submit Design Feedback"):
                response = executor.graph_review_flow(st.session_state.task_id, "feedback", fback, "review_design_documents")
                st.session_state.current_state = response["state"]
                st.rerun()

# Stage 5: Code Review
elif not state.get("security_recommendations"):
    st.subheader("💻 Phase 3: Code Review")
    
    col_code, col_review = st.columns([2, 1])
    with col_code:
        st.markdown("**Generated Code**")
        st.code(state.get("code_generated", ""), language="python")
    
    with col_review:
        st.markdown("**AI Peer Review Comments**")
        st.info(state.get("code_review_comments", "No comments available."))

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Approve Code", use_container_width=True):
            response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_code")
            st.session_state.current_state = response["state"]
            st.rerun()
    with c2:
        with st.popover("🔄 Request Code Fix"):
            fback = st.text_area("Specify changes/fixes needed:")
            if st.button("Submit Code Feedback"):
                response = executor.graph_review_flow(st.session_state.task_id, "feedback", fback, "review_code")
                st.session_state.current_state = response["state"]
                st.rerun()

# Stage 6: Security Review
else:
    st.subheader("🔒 Phase 4: Security Review")
    
    t1, t2 = st.tabs(["🛡️ Security Recommendations", "📝 Auditor Comments"])
    with t1:
        st.warning("Critical Security Recommendations")
        st.markdown(state.get("security_recommendations", "Scanning..."))
    with t2:
        st.markdown(state.get("security_review_comments", "N/A"))

    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Final Approval", use_container_width=True):
            response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_security_recommendations")
            st.session_state.current_state = response["state"]
            st.success("Software Securely Designed & Built!")
            st.balloons()
    with c2:
        with st.popover("🚨 Security Feedback"):
            fback = st.text_area("Describe security vulnerabilities to fix:")
            if st.button("Send Back to Coding"):
                response = executor.graph_review_flow(st.session_state.task_id, "feedback", fback, "review_security_recommendations")
                st.session_state.current_state = response["state"]
                st.rerun()