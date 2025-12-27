import streamlit as st
import asyncio
import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.agents.template import TemplateAgent
from govuk_content_agents.templates.govuk_patterns import GOVUK_TEMPLATES

st.set_page_config(page_title="Create Content", page_icon="🏗️", layout="wide")

st.title("🏗️ Content Architect")
st.markdown("### Generate GOV.UK content from templates")

# Initialize Agent
if "architect" not in st.session_state:
    st.session_state["architect"] = TemplateAgent()

# 1. Select Template
st.subheader("1. Choose a Pattern")
template_keys = list(GOVUK_TEMPLATES.keys())
selected_key = st.selectbox(
    "Select a content type:",
    template_keys,
    format_func=lambda x: GOVUK_TEMPLATES[x]["name"]
)

template = GOVUK_TEMPLATES[selected_key]
st.info(f"**{template['name']}**: {template['description']}")
with st.expander("View Structure"):
    st.code(template["structure"], language="markdown")

# 2. Enter Brief
st.subheader("2. Your Brief")
user_brief = st.text_area(
    "Describe the content you need:",
    height=150,
    placeholder="e.g., I need a guide for fishermen on how to apply for a rod license. It costs £30 and takes 2 days."
)

# 3. Generate
if st.button("✨ Generate Draft", type="primary"):
    if not user_brief:
        st.warning("Please enter a brief first.")
    else:
        with st.spinner("The Architect is building your draft..."):
            try:
                # Run async agent
                draft = asyncio.run(
                    st.session_state["architect"].generate_draft(selected_key, user_brief)
                )
                st.session_state["generated_draft"] = draft
                st.success("Draft Generated!")
            except Exception as e:
                st.error(f"Error generating draft: {e}")

# 4. Result & Actions
if "generated_draft" in st.session_state:
    st.markdown("---")
    st.subheader("3. Review Generated Draft")
    
    draft_content = st.text_area("Generated Content", value=st.session_state["generated_draft"], height=500)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 Copy to Clipboard"):
            st.write("Content copied! (Simulated)")
            # Streamlit doesn't natively support clipboard copy easily without components, 
            # but users can just copy the text area.
            
    with col2:
        if st.button("🚀 Send to Review Agent"):
            # Set this as the "fetched/input" content for the main app
            # We need to switch page or just tell user to go there?
            # Storing in session state allows the main app to pick it up if we code it right.
            st.session_state["fetched_content"] = draft_content
            st.session_state["last_source"] = "Architect"
            
            st.success("Sent to Review Pipeline! Go to the **Main Dashboard** (ui/app.py) to run the analysis.")
            st.info("Note: You need to navigate back to the main app page manually via the sidebar if running locally.")
