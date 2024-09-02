# FastAPI Application

This document details the FastAPI application within the GraphFleet project, residing in the `app` directory. Think of this as the engine of a car - it handles the core functionality and makes everything work, but you interact with it through a more user-friendly interface (like the car's dashboard).

## Functionality

The FastAPI application serves as the backend API, providing endpoints for:

- **Search:**
    - Performs local and global searches powered by the GraphRAG engine. Imagine this as searching for information within a specific document (local) or across your entire library (global).
    - Offers both standard and streaming response modes. Standard is like getting all the search results at once, while streaming is like seeing them appear one by one as they're found.
- **Question Generation:**
    - Generates questions based on a provided topic or context. This is like having a study buddy who can come up with insightful questions to help you learn.
- **Settings Management:**
    - Allows viewing and updating application settings through the Streamlit UI. This is like adjusting the settings on your phone to customize your experience.

## Key Files

- **api.py:** Defines the core API logic for search, question generation, and data reformatting. This is where the "magic" happens behind the scenes.
- **config.py:** Manages application settings and configuration loading from environment variables. Think of this as the control panel for the application.
- **main.py:** Initializes the FastAPI application, defines routes, and handles error logging. This is like the engine's control unit, making sure everything runs smoothly.
- **streamlit_app.py:** Implements the Streamlit UI for user interaction with the API. This is like the car's dashboard, providing a user-friendly way to interact with the engine.
- **utils.py:** Provides utility functions for data conversion and processing. These are like the tools in a mechanic's toolbox, used to perform specific tasks.

## Endpoints

The API exposes the following endpoints, which are like specific buttons or controls on the dashboard:

- `/search/local`: Performs a local search within a specific context.
- `/search/global`: Performs a global search across the entire knowledge base.
- `/search/local/stream`: Performs a local search with streaming responses.
- `/search/global/stream`: Performs a global search with streaming responses.
- `/generate_questions`: Generates questions based on a given topic.

## Error Handling

The application integrates with Sentry for error tracking and logging, ensuring robust error handling and reporting. This is like having a built-in diagnostic system that alerts you to any issues and helps you troubleshoot them.

## Interaction with Other Components

The FastAPI application interacts closely with:

- **GraphRAG Implementation (graphfleet):** Utilizes the GraphRAG engine for search and question generation. This is like the engine using the car's transmission to transfer power to the wheels.
- **Streamlit UI (app/streamlit_app.py):** Provides the frontend interface for user interaction. This is like the dashboard displaying information from the engine and allowing the driver to control it.
- **Configuration (app/config.py, graphfleet/settings.yaml):** Loads and applies configuration settings. This is like using the car's settings to adjust things like seat position and climate control.

## Further Information

For detailed API specifications and usage examples, refer to the project's API documentation.