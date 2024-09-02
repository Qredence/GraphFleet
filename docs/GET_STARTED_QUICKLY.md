# Get Started Quickly

This guide provides a quick and easy way to get started with GraphFleet.

## Prerequisites

- **Python 3.11:** Ensure you have Python 3.11 installed on your system.
- **Poetry:** We recommend using Poetry for dependency management. Install it using `pip install poetry`.

## Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Qredence/GraphFleet.git
   cd GraphFleet
   ```

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   poetry install
   ```

## Configuration

1. **API Keys:**
   - Obtain API keys for any external services you plan to use (e.g., OpenAI).
   - Create a `.env` file in the project root and store your API keys there:
     ```
     OPENAI_API_KEY=your_openai_api_key
     ```

2. **Settings:**
   - Review the default settings in `graphfleet/settings.yaml` and customize them as needed.

## Running GraphFleet

1. **Start the FastAPI Application:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Access the Streamlit UI:**
   - Open your web browser and navigate to `http://localhost:8000`.

## Next Steps

- Explore the Streamlit UI to perform searches, generate questions, and manage settings.
- Refer to the documentation for more advanced configuration options and usage examples.