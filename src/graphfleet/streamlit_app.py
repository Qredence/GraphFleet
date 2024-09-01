import os
import streamlit as st
import requests
import json
from streamlit_agraph import agraph, Node, Edge, Config

API_URL = os.getenv("API_URL", "http://localhost:8000")  # Use environment variable with a default

st.set_page_config(page_title="GraphFleet Interface", layout="wide")

st.title("GraphFleet Interface")

# Sidebar for different actions
action = st.sidebar.selectbox("Choose an action", [
    "Query", "Index File", "Index Documents", "Visualize Graph", "Search", 
    "Auto Prompt Tune", "Advanced Reasoning", "Generate Release Notes", 
    "Web-Enhanced Query", "Containerized Processing", "Self-Improve", "Monthy Scrape",
    "Ask Monty"  # Add this new option
])

# Add this to the sidebar
storage_backend = st.sidebar.selectbox("Select Storage Backend", [backend.value for backend in StorageBackend])
if st.sidebar.button("Set Storage Backend"):
    response = requests.post(f"{API_URL}/set-storage-backend", json=storage_backend)
    if response.status_code == 200:
        st.sidebar.success(f"Storage backend set to {storage_backend}")
    else:
        st.sidebar.error(f"Error: {response.json()['detail']}")

if action == "Query":
    st.header("Query the Knowledge Graph")
    query = st.text_input("Enter your question:")
    method = st.selectbox("Choose search method", ["global", "local"])
    if st.button("Submit Query"):
        response = requests.post(f"{API_URL}/query", json={"question": query, "method": method})
        if response.status_code == 200:
            result = response.json()
            st.success(f"Answer: {result['answer']}")
            st.info(f"Confidence: {result['confidence']:.2f}")
            if result['confidence'] < 0.7:
                st.warning("The AI is not very confident about this answer. You may want to verify it.")
        else:
            st.error(f"Error: {response.json()['detail']}")

elif action == "Index File":
    st.header("Index File")
    uploaded_file = st.file_uploader("Choose a file to index (PDF, JSON, HTML, or TXT)", type=["pdf", "json", "html", "htm", "txt"])
    if uploaded_file is not None:
        if st.button("Index File"):
            files = {"file": uploaded_file}
            response = requests.post(f"{API_URL}/index-file", files=files)
            if response.status_code == 200:
                st.success("File indexed successfully")
            else:
                st.error(f"Error: {response.json()['detail']}")

elif action == "Index Documents":
    st.header("Index Documents")
    uploaded_file = st.file_uploader("Choose a JSON file containing documents", type="json")
    if uploaded_file is not None:
        if st.button("Index Documents"):
            files = {"file": uploaded_file}
            response = requests.post(f"{API_URL}/index", files=files)
            if response.status_code == 200:
                st.success(f"Indexed {response.json()['indexed_count']} documents successfully")
            else:
                st.error(f"Error: {response.json()['detail']}")

elif action == "Visualize Graph":
    st.header("Visualize Knowledge Graph")
    if st.button("Generate Visualization"):
        response = requests.get(f"{API_URL}/visualize")
        if response.status_code == 200:
            # Assuming the API now returns the graph data instead of saving an image
            graph_data = response.json()
            
            nodes = [Node(id=node["id"], label=node["label"]) for node in graph_data["nodes"]]
            edges = [Edge(source=edge["source"], target=edge["target"]) for edge in graph_data["edges"]]
            
            config = Config(width=750, height=950, directed=True, physics=True, hierarchical=False)
            
            agraph(nodes=nodes, edges=edges, config=config)
        else:
            st.error(f"Error: {response.json()['detail']}")

elif action == "Search":
    st.header("Search Documents")
    search_query = st.text_input("Enter search query:")
    limit = st.slider("Number of results", min_value=1, max_value=100, value=10)
    offset = st.number_input("Offset", min_value=0, value=0)
    if st.button("Search"):
        response = requests.get(f"{API_URL}/search", params={"query": search_query, "limit": limit, "offset": offset})
        if response.status_code == 200:
            results = response.json()
            for doc in results:
                st.subheader(f"Document: {doc['metadata'].get('title', 'Untitled')}")
                st.write(doc['content'])
                st.json(doc['metadata'])
                st.markdown("---")
        else:
            st.error(f"Error: {response.json()['detail']}")

elif action == "Auto Prompt Tune":
    st.header("Auto Prompt Tune")
    if st.button("Start Auto Prompt Tune"):
        response = requests.post(f"{API_URL}/auto-prompt-tune")
        if response.status_code == 200:
            st.success("Auto prompt tuning started in the background")
            st.info("Check the API logs for progress and completion status")
        else:
            st.error(f"Error: {response.json()['detail']}")

elif action == "Advanced Reasoning":
    st.header("Advanced Reasoning")
    question = st.text_input("Enter your question for advanced reasoning:")
    if st.button("Submit"):
        response = requests.post(f"{API_URL}/advanced-reasoning", params={"question": question})
        if response.status_code == 200:
            st.success(f"Answer: {response.json()['answer']}")
        else:
            st.error(f"Error: {response.json()['detail']}")

elif action == "Generate Release Notes":
    st.header("Generate Release Notes")
    version = st.text_input("Enter version number:")
    changes = st.text_area("Enter changes (one per line):")
    if st.button("Generate"):
        changes_list = changes.split("\n")
        response = requests.post(f"{API_URL}/generate-release-notes", json={"version": version, "changes": changes_list})
        if response.status_code == 200:
            st.success("Release Notes:")
            st.text(response.json()['release_notes'])
        else:
            st.error(f"Error: {response.json()['detail']}")

elif action == "Web-Enhanced Query":
    st.header("Web-Enhanced Query")
    question = st.text_input("Enter your question for web-enhanced query:")
    if st.button("Submit"):
        response = requests.post(f"{API_URL}/web-enhanced-query", params={"question": question})
        if response.status_code == 200:
            st.success(f"Answer: {response.json()['answer']}")
        else:
            st.error(f"Error: {response.json()['detail']}")

elif action == "Containerized Processing":
    st.header("Containerized Processing")
    data = st.text_area("Enter JSON data for containerized processing:")
    if st.button("Process"):
        try:
            json_data = json.loads(data)
            response = requests.post(f"{API_URL}/containerized-processing", json=json_data)
            if response.status_code == 200:
                st.success("Processed Result:")
                st.json(response.json()['result'])
            else:
                st.error(f"Error: {response.json()['detail']}")
        except json.JSONDecodeError:
            st.error("Invalid JSON data")

elif action == "Self-Improve":
    st.header("Trigger Self-Improvement")
    if st.button("Start Self-Improvement"):
        response = requests.post(f"{API_URL}/self-improve")
        if response.status_code == 200:
            st.success("Self-improvement process completed")
        else:
            st.error(f"Error: {response.json()['detail']}")

elif action == "Monthy Scrape":
    st.header("Monthy Web Scraper")
    url = st.text_input("Enter the URL to scrape:")
    output_format = st.selectbox("Choose output format", ["text", "csv"])
    if st.button("Scrape"):
        response = requests.post(f"{API_URL}/monthy-scrape", json={"url": url, "output_format": output_format})
        if response.status_code == 200:
            st.success("Scraping completed successfully")
            content = response.json()['content']
            if output_format == "csv":
                st.download_button(
                    label="Download CSV",
                    data=content,
                    file_name="scraped_content.csv",
                    mime="text/csv"
                )
            else:
                st.text_area("Scraped Content", content, height=300)
        else:
            st.error(f"Error: {response.json()['detail']}")

# Add this new elif block for Ask Monty
elif action == "Ask Monty":
    st.header("Ask Monty")
    request = st.text_area("What would you like Monty to do?", height=150)
    if st.button("Submit Request"):
        response = requests.post(f"{API_URL}/ask-monty", params={"request": request})
        if response.status_code == 200:
            st.success("Monty's Response:")
            st.markdown(response.json()['response'])
        else:
            st.error(f"Error: {response.json()['detail']}")

# Display API info
st.sidebar.header("API Info")
info_response = requests.get(f"{API_URL}/info")
if info_response.status_code == 200:
    info = info_response.json()
    st.sidebar.text(f"API Base: {info['api_base']}")
    st.sidebar.text(f"API Version: {info['api_version']}")
    st.sidebar.text(f"Deployment: {info['deployment_name']}")
else:
    st.sidebar.error("Failed to fetch API info")

# Health Check
health_response = requests.get(f"{API_URL}/health")
if health_response.status_code == 200:
    st.sidebar.success("API Status: Healthy")
else:
    st.sidebar.error("API Status: Unhealthy")