import streamlit as st
import os
import sys

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.utils.analytics import analyze_tone, generate_diff_html

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Visual Analytics")
st.markdown("### Tone Heatmap & Semantic Diff")

tab1, tab2 = st.tabs(["Tone Heatmap", "Diff Tool"])

with tab1:
    st.subheader("Tone Heatmap")
    st.info("Highlights: **Passive Voice (Red)**, **Complex Words (Blue)**, **Long Sentences (Yellow)**")
    
    # Pre-fill content
    default_text = ""
    if "fetched_content" in st.session_state:
        default_text = st.session_state["fetched_content"]
    
    heatmap_input = st.text_area("Content to Analyse:", value=default_text, height=200)
    
    if st.button("🔥 Generate Heatmap", type="primary"):
        if heatmap_input:
            html = analyze_tone(heatmap_input)
            st.markdown(f"""
            <div style="padding: 20px; border: 1px solid #ccc; border-radius: 5px; background-color: white; color: black; line-height: 1.6;">
                {html}
            </div>
            """, unsafe_allow_html=True)
            
            # Counter metrics
            # We could count spans for a summary
            pass

with tab2:
    st.subheader("Diff Tool")
    st.markdown("Compare Original Draft vs AI Rewritten version.")
    
    col1, col2 = st.columns(2)
    with col1:
        original = st.text_area("Original Text", height=200, placeholder="Old version...")
    with col2:
        new_version = st.text_area("New Version", height=200, placeholder="New version...")
        
    if st.button("↔️ Compare Versions"):
        if original and new_version:
            diff_html = generate_diff_html(original, new_version)
            st.markdown(diff_html, unsafe_allow_html=True)
            
        elif "fetched_content" in st.session_state and "last_result" in st.session_state:
            # Auto-fill if user didn't provide input but state exists
            st.info("Auto-comparing session content.")
            orig = st.session_state["fetched_content"]
            new = st.session_state["last_result"].get("content", "") or st.session_state["last_result"].get("rewritten_content", "") or st.session_state["last_result"].get("current_content", "")
            
            diff_html = generate_diff_html(orig, new)
            st.components.v1.html(diff_html, height=600, scrolling=True)
        else:
            st.warning("Please enter text or run a review first.")
