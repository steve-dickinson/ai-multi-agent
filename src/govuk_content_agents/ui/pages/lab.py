import streamlit as st
import asyncio
import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.agents.persona import PersonaAgent
from govuk_content_agents.data.personas import PERSONAS

st.set_page_config(page_title="Persona Lab", page_icon="🧪", layout="wide")

st.title("🧪 The Persona Lab")
st.markdown("### Simulate User Experiences")

# Sidebar
with st.sidebar:
    st.info("Test your content against different user archetypes.")

# Initialize Agent
if "simulator" not in st.session_state:
    st.session_state["simulator"] = PersonaAgent()

# 1. Select Persona
st.subheader("1. Select Test Subject")
persona_keys = list(PERSONAS.keys())
selected_key = st.selectbox(
    "Choose a persona:",
    persona_keys,
    format_func=lambda x: PERSONAS[x]["name"]
)

persona = PERSONAS[selected_key]
st.info(f"**Role**: {persona['role']}\n\n**Stress**: {persona['stress_level']} | **Reading Ability**: {persona['reading_ability']}")

from govuk_content_agents.ui.components import render_content_input

# 2. Content Input
st.subheader("2. Load Content")
content_to_test = render_content_input(key_prefix="lab", label="Test Material")

# Fallback: if no input, try to use main session fetched content
if not content_to_test:
    if "fetched_content" in st.session_state:
        # We can't auto-fill the component easily without passing default, 
        # but the component handles its own state. 
        # We can just check session state if component returns empty.
        pass
    elif "last_result" in st.session_state:
         # Optional: show a message that recent results are available but user chose not to input text
         st.info("Tip: You can paste content from the main review here.")

# 3. specific questions (optional)
# Maybe later.

# 4. Run Simulation
if st.button("🔬 Run Simulation", type="primary"):
    if not content_to_test:
        st.warning("Please provide content to test.")
    else:
        with st.spinner(f"Simulating {persona['name']}'s experience..."):
            try:
                # Configure agent
                st.session_state["simulator"].set_persona(selected_key)
                
                # Run sync
                result = asyncio.run(
                   st.session_state["simulator"].execute(content_to_test)
                )
                st.session_state["simulation_result"] = result
                st.success("Simulation Complete!")
            except Exception as e:
                st.error(f"Simulation failed: {e}")

# 5. Results
if "simulation_result" in st.session_state:
    st.markdown("---")
    res = st.session_state["simulation_result"]
    
    # Score
    score = res.score
    color = "green" if score > 70 else "orange" if score > 40 else "red"
    
    st.markdown(f"""
    <div style="padding: 15px; border-left: 5px solid {color}; background-color: rgba(255,255,255,0.05);">
        <h3>Ease of Use Score: {score}/100</h3>
        <p><i>"{res.summary}"</i></p>
    </div>
    """, unsafe_allow_html=True)
    
    if res.issues:
        st.subheader("Pain Points")
        for issue in res.issues:
            # It should be a dict now due to agent normalization, but we code defensively
            if isinstance(issue, dict):
                desc = issue.get("description", "Unknown issue")
                sev = issue.get("severity", "Medium")
                
                # Color code severity
                sev_color = "red" if sev.lower() == "high" else "orange" if sev.lower() == "medium" else "blue"
                
                st.markdown(f"**<span style='color:{sev_color}'>{sev}</span>**: {desc}", unsafe_allow_html=True)
            else:
                 st.write(f"- {issue}")
