import streamlit as st
import requests
import json
import sseclient
import pandas as pd
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings, Settings

# Define the API base URL Adjust this if your API is hosted elsewhere
API_BASE_URL = "http://localhost:8000" 

st.title("GraphFleet Search App")

tab1, tab2, tab3 = st.tabs(["Search", "Question Generation", "Settings"])

with tab1:
    st.header("Search")
    search_type = st.radio("Select search type:", ("Local", "Global"))
    query = st.text_input("Enter your search query:")
    streaming = st.checkbox("Enable streaming")

    if st.button("Search"):
        if query:
            endpoint = f"{API_BASE_URL}/search/{search_type.lower()}"
            if streaming:
                endpoint += "/stream"
            
            try:
                with st.spinner("Searching..."):
                    if streaming:
                        with requests.post(endpoint, json={"query": query}, stream=True) as response:
                            response.raise_for_status()
                            client = sseclient.SSEClient(response)
                            
                            stream_output = st.empty()
                            full_response = ""
                            
                            try:
                                for event in client.events():
                                    full_response += event.data
                                    stream_output.write(full_response)
                            except Exception as e:
                                st.error(f"Streaming error: {str(e)}")
                    else:
                        response = requests.post(endpoint, json={"query": query})
                        response.raise_for_status()
                        result = response.json()
                        
                        st.subheader("Response:")
                        st.write(result["response"])
                        
                        if search_type == "Global":
                            st.subheader("Report Counts:")
                            st.write(f"Total report count: {result['total_report_count']}")
                            st.write(f"Filtered report count: {result['filtered_report_count']}")
                        
                        if "context_data" in result:
                            with st.expander("View Context Data"):
                                for key, value in result["context_data"].items():
                                    st.subheader(key.capitalize())
                                    if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                                        st.dataframe(pd.DataFrame(value))
                                    else:
                                        st.write(value)
                        
                        if "reports_head" in result and result["reports_head"]:
                            st.subheader("Reports Head:")
                            st.dataframe(pd.DataFrame(result["reports_head"]))
                        else:
                            st.info("No reports data available for this search.")
                        
                        if search_type == "Global" and "reports" in result:
                            with st.expander("View All Reports"):
                                st.dataframe(pd.DataFrame(result["reports"]))
            except requests.RequestException as e:
                st.error(f"An error occurred: {str(e)}")
                if hasattr(e, 'response') and e.response is not None:
                    st.error(f"Server response: {e.response.text}")
        else:
            st.warning("Please enter a search query.")

with tab2:
    st.header("Question Generation")
    question_query = st.text_input("Enter a topic or context for question generation:")

    if st.button("Generate Questions"):
        if question_query:
            try:
                with st.spinner("Generating questions..."):
                    response = requests.post(f"{API_BASE_URL}/generate_questions", json={"query": question_query})
                    response.raise_for_status()
                    result = response.json()
                    
                    st.subheader("Generated Questions:")
                    for question in result["questions"]:
                        st.write(f"- {question}")
            except requests.RequestException as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a topic or context for question generation.")

with tab3:
    st.header("Settings")
    
    # Create a form for editing settings
    with st.form("settings_form"):
        new_settings = {}
        
        new_settings['API_KEY'] = st.text_input("API Key", value=settings.API_KEY, type="password")
        new_settings['LLM_MODEL'] = st.text_input("LLM Model", value=settings.LLM_MODEL)
        new_settings['EMBEDDING_MODEL'] = st.text_input("Embedding Model", value=settings.EMBEDDING_MODEL)
        new_settings['API_BASE'] = st.text_input("API Base", value=settings.API_BASE)
        new_settings['API_VERSION'] = st.text_input("API Version", value=settings.API_VERSION)
        new_settings['INPUT_DIR'] = st.text_input("Input Directory", value=settings.INPUT_DIR)
        new_settings['LANCEDB_URI'] = st.text_input("LanceDB URI", value=settings.LANCEDB_URI)
        new_settings['COMMUNITY_LEVEL'] = st.number_input("Community Level", value=settings.COMMUNITY_LEVEL, min_value=1, step=1)
        new_settings['MAX_TOKENS'] = st.number_input("Max Tokens", value=settings.MAX_TOKENS, min_value=1, step=1)
        
        submitted = st.form_submit_button("Save Settings")
        
        if submitted:
            # Update settings
            for key, value in new_settings.items():
                setattr(settings, key, value)
            st.success("Settings updated successfully!")

    # Display current settings
    st.subheader("Current Settings")
    settings_dict = {
        "API_KEY": "********" if settings.API_KEY != "default_api_key" else "Not set",
        "LLM_MODEL": settings.LLM_MODEL,
        "EMBEDDING_MODEL": settings.EMBEDDING_MODEL,
        "API_BASE": settings.API_BASE,
        "API_VERSION": settings.API_VERSION,
        "INPUT_DIR": settings.INPUT_DIR,
        "LANCEDB_URI": settings.LANCEDB_URI,
        "COMMUNITY_LEVEL": settings.COMMUNITY_LEVEL,
        "MAX_TOKENS": settings.MAX_TOKENS,
    }
    st.json(settings_dict)

    def is_default_value(value):
        if isinstance(value, str):
            return value.startswith("default_") or value == "Not set"
        return False

# Move this check before displaying the settings
if any(is_default_value(value) for value in settings_dict.values()):
    st.warning("Some settings are using default values. Please update them for full functionality.")

# Display current settings
st.subheader("Current Settings")
st.json(settings_dict)
