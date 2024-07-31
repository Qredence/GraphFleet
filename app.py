import streamlit as st
import subprocess
import shlex

def process_query(query: str, search_method: str) -> str:
    cmd = [
        "python3", "-m", "graphrag.query",
        "--root", "./graphfleet",
        "--method", search_method,
    ]
    cmd.append(shlex.quote(query))

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        response = output.split(f"SUCCESS: {search_method.capitalize()} Search Response:", 1)[-1].strip()
        return response
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e.stderr}"

def display_chat_message(role: str, content: str):
    with st.chat_message(role):
        st.markdown(content)

def clear_chat_history():
    st.session_state.messages = []

def main():
    st.set_page_config(page_title="AI Chat Assistant", page_icon="🤖", layout="wide")
    st.title("AI Chat Assistant")

    st.markdown("""
    Welcome to the AI Chat Assistant! This app uses advanced natural language processing
    to answer your questions. Simply type your query in the chat input below and press Enter.
    """)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.header("Settings")
        search_method = st.selectbox("Search Method", ["local", "global"], index=0)
        if st.button("Clear Chat History"):
            clear_chat_history()

    for message in st.session_state.messages:
        display_chat_message(message["role"], message["content"])

    if prompt := st.chat_input("What's your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat_message("user", prompt)

        with st.spinner("Thinking..."):
            response = process_query(prompt, search_method)

        st.session_state.messages.append({"role": "assistant", "content": response})
        display_chat_message("assistant", response)

if __name__ == "__main__":
    main()