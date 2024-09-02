# Streamlit UI

This document outlines the Streamlit UI component of the GraphFleet project, implemented in `app/streamlit_app.py`. Think of the Streamlit UI as the user-friendly "face" of GraphFleet. It's what you interact with directly to ask questions, get answers, and customize your experience.

## Functionality

The Streamlit UI provides a user-friendly web interface for interacting with the GraphFleet API, enabling users to:

- **Perform Searches:**
    - Execute local and global searches using a text input field. Imagine typing your question into a search bar, just like you would on Google.
    - Choose between standard and streaming response modes. Standard mode gives you all the results at once, while streaming mode shows you results as they're found, which can be helpful for long searches.
- **Generate Questions:**
    - Input a topic or context to generate relevant questions. This is helpful if you're not sure what to ask or want to explore a topic more deeply.
- **View and Modify Settings:**
    - Access and update application settings through an intuitive form. This allows you to customize things like the AI model used, the maximum response length, and more.

## Key Features

- **Interactive Search:** Users can input search queries and view results directly within the UI. It's a seamless and intuitive search experience.
- **Streaming Responses:** The UI supports streaming responses for both local and global searches, providing real-time updates as the search progresses. This means you don't have to wait for the entire search to finish before seeing results.
- **Question Generation:** Facilitates question exploration by generating questions based on user-provided topics. This helps you delve deeper into a subject and uncover new insights.
- **Settings Management:** Allows users to configure API keys, model parameters, data paths, and other settings through a user-friendly form. You're in control of how GraphFleet works for you.
- **Data Visualization:** Presents search results and context data in an organized and readable format using Streamlit's built-in data visualization capabilities. Charts, graphs, and tables make it easy to understand and analyze the information.

## Structure and Layout

The UI is structured using Streamlit's intuitive layout components, including tabs, sidebars, and expander widgets, to organize functionality and information effectively. It's designed to be clean, uncluttered, and easy to navigate.

## Interaction with Other Components

The Streamlit UI interacts with:

- **FastAPI Application (app):** Sends requests to the API endpoints for search, question generation, and settings management. It's like the messenger between you and the "brains" of the operation.
- **Configuration (app/config.py):** Displays and updates application settings. It's like the settings menu for the UI, allowing you to customize your experience.

## Usage

To launch the Streamlit UI, run the `streamlit_app.py` script. The UI will be accessible through a web browser at the specified address and port. It's as simple as that!