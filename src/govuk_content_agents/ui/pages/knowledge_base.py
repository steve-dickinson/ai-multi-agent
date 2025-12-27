import streamlit as st
import sys
import os
from datetime import datetime

# Ensure src is in path
sys.path.append(os.path.join(os.getcwd(), "src"))

from govuk_content_agents.storage.vectors import vector_service, vector_client
from govuk_content_agents.ui.components import render_content_input

st.set_page_config(page_title="Knowledge Base", page_icon="📚", layout="wide")

st.title("📚 Knowledge Base Manager")
st.markdown("Manage the external policies used for the **Silo Breaker** consistency checks.")

# Tabs: Add New / Manage Existing
tab1, tab2 = st.tabs(["➕ Add Policy", "📂 Manage Policies"])

with tab1:
    st.subheader("Add New Policy")
    st.markdown("Index content from other departments (e.g., HMRC, DWP) to find contradictions.")
    
    # Metadata Form
    col1, col2 = st.columns(2)
    with col1:
        department = st.selectbox(
            "Department / Org",
            ["HMRC", "DWP", "Home Office", "DfE", "MoJ", "Other"]
        )
    with col2:
        topic = st.text_input("Topic / Title", placeholder="e.g. VAT Rates 2024")
        
    # Unified Content Input
    content = render_content_input(key_prefix="kb_input", label="Policy Content")
    
    if st.button("💾 Save to Knowledge Base", type="primary"):
        if not content:
            st.warning("Please provide content first.")
        elif not topic:
            st.warning("Please provide a Topic/Title.")
        else:
            with st.spinner("Embedding and Indexing..."):
                try:
                    doc_id = vector_service.upsert_policy(
                        content=content,
                        metadata={
                            "department": department,
                            "topic": topic,
                            "source": "manual_upload",
                            "added_at": datetime.utcnow().isoformat()
                        }
                    )
                    st.success(f"Policy saved successfully! ID: {doc_id}")
                except Exception as e:
                    st.error(f"Error saving policy: {e}")

with tab2:
    st.subheader("Existing Policies")
    
    # Simple search
    search_query = st.text_input("Search Policies", placeholder="Search by topic or content...")
    
    if search_query:
        # Vector search
        try:
            embedding = vector_service.embed_text(search_query)
            results = vector_client.search_similar(embedding, limit=10)
            
            for res in results:
                meta = res.get("metadata", {})
                with st.expander(f"{meta.get('department', 'Unknown')} - {meta.get('topic', 'Untitled')} (Score: {res['similarity']:.3f})"):
                    st.markdown(f"**ID:** `{res['id']}`")
                    st.markdown(f"**Added:** {meta.get('added_at', 'Unknown')}")
                    st.text_area("Content Preview", res['content'][:500] + "...", height=150, key=f"preview_{res['id']}")
                    
                    if st.button("Delete (Not Implemented)", key=f"del_{res['id']}"):
                         st.warning("Deletion not yet implemented in VectorDBClient.")
                         
        except Exception as e:
             st.error(f"Search failed: {e}")
    else:
        st.info("Enter a search term to find policies.")
