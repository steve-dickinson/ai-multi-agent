import streamlit as st
import asyncio
import os
import sys

# Ensure src is in path for imports
sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.orchestration.graph import app as graph_app
from govuk_content_agents.orchestration.graph import app as graph_app
from govuk_content_agents.config import settings
from govuk_content_agents.orchestration.graph import app as graph_app
from govuk_content_agents.config import settings
from govuk_content_agents.utils.web import fetch_content_from_url, fetch_content_from_govuk_api

st.set_page_config(
    page_title="GOV.UK Content AI",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 GOV.UK Content AI")
st.markdown("### Multi-Agent Content Publishing System")

# Sidebar
with st.sidebar:
    st.info("Uses OpenAI GPT-4o-mini & LangGraph")
    if not settings.OPENAI_API_KEY:
        st.error("⚠️ OPENAI_API_KEY missing!")
    
    st.markdown("---")
    st.markdown("**Agents Active:**")
    st.markdown("- 📝 Content Reviewer")
    st.markdown("- 🎨 Style Compliance")
    st.markdown("- 🔍 Consistency Check")
    st.markdown("- ✨ Improvement Agent")
    st.markdown("- ⚖️ Quality Judge")

# Main Interface
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Draft Content")
    
    input_type = st.radio("Input Source", ["Text", "URL", "GOV.UK API"], horizontal=True)
    
    content_input = ""
    
    if input_type == "Text":
        content_input = st.text_area(
            "Enter content to review:",
            height=400,
            placeholder="Subject: Tax Returns\n\nIt is imperative that you facilitate..."
        )
    elif input_type == "URL":
        url_input = st.text_input("Enter URL to fetch:", placeholder="https://www.gov.uk/...")
        if url_input:
             if st.button("Fetch Content"):
                with st.spinner("Fetching content..."):
                    try:
                        fetched = fetch_content_from_url(url_input)
                        st.session_state["fetched_content"] = fetched
                        st.success("Content fetched!")
                    except Exception as e:
                        st.error(f"Failed to fetch content: {e}")
        
        if "fetched_content" in st.session_state and st.session_state.get("last_source") == "URL":
            content_input = st.text_area("Preview Fetched Content:", value=st.session_state["fetched_content"], height=300)
            
    else: # GOV.UK API
        api_input = st.text_input("Enter GOV.UK Path or URL:", placeholder="/vat-rates")
        if api_input:
             if st.button("Fetch from API"):
                with st.spinner("Calling Content API..."):
                    try:
                        fetched = fetch_content_from_govuk_api(api_input)
                        st.session_state["fetched_content"] = fetched
                        st.session_state["last_source"] = "API" # Track source
                        st.success("Content fetched via API!")
                    except Exception as e:
                        st.error(f"Failed to fetch: {e}")
        
        if "fetched_content" in st.session_state and st.session_state.get("last_source") == "API":
             content_input = st.text_area("Preview API Content:", value=st.session_state["fetched_content"], height=300)

    # Clean up state issues if switching tabs (simple approach)
    # If we switch to URL/API, we rely on fetched_content. 
    # But if we go back to Text, we want text area. 
    # Just be mindful.
    
    if input_type == "URL": 
        st.session_state["last_source"] = "URL"

    if st.button("🚀 Start Review Process", type="primary"):
        if not content_input:
            st.warning("Please enter or fetch some content first.")
        else:
            with st.spinner("Agents are working..."):
                # Run the graph
                # We need to run async code in Streamlit
                initial_state = {
                    "input_content": content_input,
                    "current_content": content_input,
                    "feedback": [],
                    "iteration": 0,
                    "max_iterations": 3,
                    "metadata": {}
                }
                
                # Run sync wrapper for async
                try:
                    result = asyncio.run(graph_app.ainvoke(initial_state))
                    st.session_state["last_result"] = result
                    st.success("Analysis Complete!")
                except Exception as e:
                    st.error(f"Error executing workflow: {e}")

with col2:
    st.subheader("Analysis Results")
    
    if "last_result" in st.session_state:
        result = st.session_state["last_result"]
        
        final_decision = result.get("final_decision")
        final_score = result.get("final_score")
        
        # Score Card
        score_color = "green" if final_decision == "pass" else "red"
        st.markdown(f"""
        <div style="padding: 20px; border-radius: 10px; background-color: rgba(255,255,255,0.1); border: 1px solid {score_color}">
            <h2 style="color: {score_color}; margin:0;">Verdict: {final_decision.upper()}</h2>
            <h3 style="margin:0;">Score: {final_score}/100</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 Improved Content")
        st.text_area("Final Output", value=result.get("current_content"), height=300)
        
        st.markdown("### 🔬 Agent Feedback")
        # Ensure feedback is a list
        feedbacks = result.get("feedback", [])
        # Sometimes feedback accumulates, let's show unique agents or latest pass?
        # For simplicity, just list all
        for f in feedbacks:
            with st.expander(f"{f.agent_name} (Score: {f.score})"):
                st.write(f"**Summary:** {f.summary}")
                if f.issues:
                    st.write("**Issues:**")
                    for issue in f.issues:
                        st.markdown(f"- {issue['description']} ({issue['severity']})")

    else:
        st.info("Submit content to see analysis results here.")
