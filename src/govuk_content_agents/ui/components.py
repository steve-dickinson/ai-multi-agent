import streamlit as st
from govuk_content_agents.utils.web import fetch_content_from_url, fetch_content_from_govuk_api

def render_content_input(key_prefix: str = "main", label: str = "Input Content") -> str:
    """
    Renders a unified input section (Text, URL, API).
    Returns the content string.
    """
    
    input_type = st.radio(
        f"{label} Source", 
        ["Text", "URL", "GOV.UK API"], 
        horizontal=True,
        key=f"{key_prefix}_source"
    )
    
    content = ""
    
    if input_type == "Text":
        content = st.text_area(
            "Paste text:",
            height=200,
            key=f"{key_prefix}_text",
            placeholder="Paste your draft content here..."
        )
        
    elif input_type == "URL":
        col1, col2 = st.columns([3, 1])
        with col1:
            url_input = st.text_input("Enter URL:", placeholder="https://...", key=f"{key_prefix}_url")
        with col2:
            fetch_btn = st.button("Fetch", key=f"{key_prefix}_fetch_url")
            
        if fetch_btn and url_input:
            with st.spinner("Fetching..."):
                try:
                    fetched = fetch_content_from_url(url_input)
                    st.session_state[f"{key_prefix}_fetched"] = fetched
                    st.success("Fetched!")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        # Display preview if fetched
        if f"{key_prefix}_fetched" in st.session_state:
            content = st.text_area("Preview:", value=st.session_state[f"{key_prefix}_fetched"], height=200, key=f"{key_prefix}_preview_url")
            
    else: # API
        col1, col2 = st.columns([3, 1])
        with col1:
            api_input = st.text_input("GOV.UK Path:", placeholder="/vat-rates", key=f"{key_prefix}_api")
        with col2:
            fetch_btn = st.button("Fetch API", key=f"{key_prefix}_fetch_api")
            
        if fetch_btn and api_input:
            with st.spinner("Calling API..."):
                try:
                    fetched = fetch_content_from_govuk_api(api_input)
                    st.session_state[f"{key_prefix}_fetched"] = fetched
                    st.success("Fetched!")
                except Exception as e:
                    st.error(f"Error: {e}")
                    
        # Display preview if fetched
        if f"{key_prefix}_fetched" in st.session_state:
            content = st.text_area("Preview:", value=st.session_state[f"{key_prefix}_fetched"], height=200, key=f"{key_prefix}_preview_api")
            
    return content
