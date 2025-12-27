import streamlit as st

st.set_page_config(page_title="Review Queue", page_icon="📋")

st.title("📋 Review Queue")

if "last_result" in st.session_state:
    result = st.session_state["last_result"]
    if result.get("final_decision") == "pass":
        st.success("This content has passed AI review and is ready for human sign-off.")
        
        st.markdown("### Content for Approval")
        st.write(result.get("current_content"))
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Approve & Publish"):
                st.balloons()
                st.success("Content published to CMS!")
        with col2:
            if st.button("❌ Reject"):
                st.error("Content rejected.")
    else:
        st.warning("The latest content did not pass AI review. Please improve it in the main dashboard.")
else:
    st.info("No content currently pending review.")
