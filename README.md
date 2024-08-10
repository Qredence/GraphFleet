# Overview

![image](https://github.com/user-attachments/assets/c3ca5ec8-1bbf-4a9c-988e-e7f5100ea5d5)

GraphFleet is an advanced implementation of [GraphRAG from Microsoft](https://github.com/microsoft/graphrag), designed to enhance large language models' ability to reason about complex information and private datasets. It builds upon GraphRAG (Retrieval Augmented Generation using Graph structures) and will gradually adopt its own path to fulfill our roadmap at Qredence.

## GraphFleet

GraphFleet uses knowledge graphs to provide substantial improvements in question-and-answer performance when reasoning about complex information. It addresses limitations of traditional RAG approaches:

- [x] Connecting disparate pieces of information through shared attributes.
- [x] Structured, hierarchical approach to Retrieval Augmented Generation.
- [x] Knowledge graph extraction from raw text.
- [x] Community hierarchy building.
- [x] Hierarchical summarization.
- [x] Enhanced reasoning capabilities for LLMs on private datasets.
- [ ] Improve the structure of the overall repository.
- [ ] Add dedicated prompts for indexing and querying, and more vector databases.
- [ ] Add more notebooks.
- [ ] Provide a FleetUI Design Kit and a quicker way of starting GraphFleet locally.
- [ ] Add integrations (Langchain, Flowise, Langflow, Microsoft Fabric, Composio, Neo4j, etc.).
- [ ] Access GraphFleet through a secure and enterprise-ready Azure Cloud hosting version. [Join the waitlist now](https://forms.office.com/e/9cHKxgrQgV).
- [ ] And way more... 👀

## Key Features

- Structured, hierarchical approach to Retrieval Augmented Generation.
- Knowledge graph extraction from raw text.
- Community hierarchy building.
- Hierarchical summarization.
- Enhanced reasoning capabilities for LLMs on private datasets.

## Getting Started

### Prerequisites

- Python 3.11 
- Make sure to have a virtual environment manager such as `virtualenv` installed 

### Installation

1. Clone the repository:

``` bash
   git clone https://github.com/Qredence/GraphFleet.git
   cd GraphFleet
```


2. Create a virtual environment and activate it:

``` bash
python3.11 -m venv gfleetenv
source gfleetenv/bin/activate
```

3. Install dependencies:

```
pip install -r requirements.txt
```

### Usage

1. Configuration:
Environment Variables: Set up your environment variables in a .env file (refer to the .env.example file for available options). Key variables include:

```
GRAPHRAG_API_KEY
GRAPHRAG_API_BASE (for Azure OpenAI)
GRAPHRAG_API_VERSION (for Azure OpenAI)
Other settings related to your LLM and embedding models.
settings.yaml: Customize GraphFleet's behavior further by modifying the settings.yaml file within the graphfleet directory.
```

2. Data Indexing:

Jupyter Notebook Guide: Follow the instructions provided in the get-started-graphfleet.ipynb notebook to learn how to index your data with GraphFleet. This notebook provides a hands-on experience for setting up your knowledge base.

3. Interacting with GraphFleet:
Jupyter Notebooks: Explore GraphFleet's capabilities with the provided notebooks:

get-started-graphfleet.ipynb: A comprehensive guide to indexing your data and running basic queries.
Local Search Notebook.ipynb: Demonstrates local search techniques.
[Add descriptions of other notebooks and their purpose here]
app.py (FastAPI Application): Run a Streamlit-powered web interface to interact with GraphFleet using a user-friendly chat-like interface:

### Start the application: 

```
streamlit run app.py
```
Access the interface in your web browser at the provided URL (usually http://localhost:8080).

``` bash
python -m graphrag.query --root ./graphfleet --method local "What are the key features of GraphRAG ??"
```

For Global query mode :

``` bash
python -m graphrag.query --root ./graphfleet --method global "What are the top main features of GraphRAG"
```
### Running the API only

To run the API, save the code in a file named api.py and execute the following command in your terminal:

``` bash
uvicorn api:app --reload --port 8001
```

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Qredence/GraphFleet&type=Date)](https://star-history.com/#Qredence/GraphFleet&Date)

