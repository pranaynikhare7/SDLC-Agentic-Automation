import streamlit as st
import os
from langchain_groq import ChatGroq
from src.sdlc_system.graph.build_graph import GraphBuilder
from src.sdlc_system.graph.graph_executor import GraphExecutor
from src.sdlc_system.cache.redis_cache import get_state_from_redis

# --- Page Config ---
st.set_page_config(page_title="AI SDLC Designer", layout="wide")

# --- Initialize Backend ---
@st.cache_resource
def get_executor():
    # Initialize your LLM here
    llm = ChatGroq(model='openai/gpt-oss-20b')
    builder = GraphBuilder(llm)
    graph = builder.setup_graph()
    return GraphExecutor(graph)

executor = get_executor()

# --- Helper: Sync UI State with Redis ---
def sync_state(task_id):
    """Fetch the latest state from Redis and update UI session state."""
    latest_state = get_state_from_redis(task_id)
    if latest_state:
        st.session_state.current_state = latest_state
        st.session_state.task_id = task_id

# --- App Logic ---
st.title("🛡️ Redis-Backed SDLC Agent")

# Sidebar for Session Recovery
with st.sidebar:
    st.header("Session Management")
    recovery_id = st.text_input("Resume Task ID")
    if st.button("Resume Session") and recovery_id:
        sync_state(recovery_id)
    
    if st.session_state.get("task_id"):
        st.success(f"Active Session: `{st.session_state.task_id}`")
        if st.button("Clear / New Project"):
            st.session_state.clear()
            st.rerun()

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
elif not st.session_state.current_state.get("user_stories"):
    st.subheader(f"Project: {st.session_state.current_state['project_name']}")
    req_input = st.text_area("Enter Requirements (one per line)", height=150)
    
    if st.button("Generate Stories"):
        requirements = [r.strip() for r in req_input.split("\n") if r.strip()]
        with st.spinner("AI is drafting user stories..."):
            response = executor.generate_stories(st.session_state.task_id, requirements)
            st.session_state.current_state = response["state"]
            st.rerun()

# Stage 3: Review & Approval Loop
else:
    st.subheader("📋 Review Generated User Stories")
    stories_data = st.session_state.current_state["user_stories"]
    
    # Handle both Pydantic objects or dicts coming back from Redis
    stories = stories_data.user_stories if hasattr(stories_data, 'user_stories') else stories_data['user_stories']

    for story in stories:
        with st.expander(f"**{story['id'] if isinstance(story, dict) else story.id}**: {story['title'] if isinstance(story, dict) else story.title}"):
            st.write(story['description'] if isinstance(story, dict) else story.description)
            st.caption(f"Priority: {story['priority'] if isinstance(story, dict) else story.priority}")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Approve", use_container_width=True):
            response = executor.graph_review_flow(st.session_state.task_id, "approved", "", "review_user_stories")
            st.session_state.current_state = response["state"]
            st.success("Workflow finished and saved to Redis!")
            st.balloons()

    with col2:
        with st.popover("🔄 Revision Required"):
            feedback = st.text_area("What needs improvement?")
            if st.button("Submit Feedback"):
                response = executor.graph_review_flow(st.session_state.task_id, "feedback", feedback, "review_user_stories")
                st.session_state.current_state = response["state"]
                st.rerun()