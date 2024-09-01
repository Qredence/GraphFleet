import os
import streamlit as st
import requests
from requests.exceptions import ConnectionError, Timeout
import time

API_URL = os.getenv("API_URL", "http://localhost:8000")
MAX_RETRIES = 3
RETRY_DELAY = 2

def make_api_request(method, endpoint, **kwargs):
    for attempt in range(MAX_RETRIES):
        try:
            if method.lower() == 'get':
                response = requests.get(f"{API_URL}{endpoint}", **kwargs, timeout=10)
            elif method.lower() == 'post':
                response = requests.post(f"{API_URL}{endpoint}", **kwargs, timeout=10)
            else:
                st.error(f"Unsupported HTTP method: {method}")
                return None

            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                return None

        except (ConnectionError, Timeout) as e:
            if attempt < MAX_RETRIES - 1:
                st.warning(f"Connection attempt {attempt + 1} failed. Retrying in {RETRY_DELAY} seconds...")
                time.sleep(RETRY_DELAY)
            else:
                st.error(f"Failed to connect to the API after {MAX_RETRIES} attempts. Please check if the server is running.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
            return None

    return None

st.set_page_config(page_title="GraphFleet Interface", layout="wide")

st.title("GraphFleet Interface")

def handle_error(response):
    if response.status_code != 200:
        st.error(f"Error: {response.json().get('detail', 'An unknown error occurred')}")
        return True
    return False

action = st.sidebar.selectbox("Choose an action", [
    "Query", "Index File", "Search", "Monthy Scrape", "Ask Monty"
])

if action == "Query":
    st.header("Query the Knowledge Graph")
    question = st.text_input("Enter your question:")
    method = st.selectbox("Choose search method", ["global", "local"])
    if st.button("Submit Query"):
        result = make_api_request('post', "/graphfleet/query", json={"question": question, "method": method})
        if result:
            st.success(f"Answer: {result['answer']}")
            st.info(f"Confidence: {result['confidence']:.2f}")

elif action == "Index File":
    st.header("Index File")
    uploaded_file = st.file_uploader("Choose a file to index (JSON)", type=["json"])
    if uploaded_file is not None and st.button("Index File"):
        files = {"file": uploaded_file}
        result = make_api_request('post', "/graphfleet/index", files=files)
        if result:
            st.success(f"Indexed {result['indexed_count']} documents successfully")

elif action == "Search":
    st.header("Search Documents")
    search_query = st.text_input("Enter search query:")
    limit = st.slider("Number of results", min_value=1, max_value=100, value=10)
    offset = st.number_input("Offset", min_value=0, value=0)
    if st.button("Search"):
        result = make_api_request('get', "/graphfleet/search", params={"query": search_query, "limit": limit, "offset": offset})
        if result:
            results = result
            for doc in results:
                st.subheader(f"Document: {doc['metadata'].get('title', 'Untitled')}")
                st.write(doc['content'])
                st.json(doc['metadata'])
                st.markdown("---")

elif action == "Monthy Scrape":
    st.header("Monthy Web Scraper")
    url = st.text_input("Enter the URL to scrape:")
    output_format = st.selectbox("Choose output format", ["text", "csv"])
    if st.button("Scrape"):
        result = make_api_request('post', "/graphfleet/monthy-scrape", json={"url": url, "output_format": output_format})
        if result:
            st.success("Scraping completed successfully")
            st.text_area("Scraped Content", result['content'], height=300)

elif action == "Ask Monty":
    st.header("Ask Monty")
    request = st.text_area("What would you like Monty to do?", height=150)
    if st.button("Submit Request"):
        result = make_api_request('post', "/graphfleet/ask-monty", params={"request": request})
        if result:
            st.success("Monty's Response:")
            st.markdown(result['response'])

st.sidebar.header("API Info")
info_response = requests.get(f"{API_URL}")
if not handle_error(info_response):
    info = info_response.json()
    st.sidebar.text(f"API Version: {info['version']}")
    st.sidebar.text(f"Docs URL: {info['docs_url']}")