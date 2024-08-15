# Overview
<div align="left">
<a href="https://pypi.org/project/graphfleet/">
   <img alt="Pepy Total Downlods" src="https://img.shields.io/pepy/dt/graphfleet">
   </a>
   <img alt="GitHub License" src="https://img.shields.io/github/license/qredence/graphfleet">
   <img alt="GitHub forks" src="https://img.shields.io/github/forks/qredence/graphfleet">
   <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/qredence/graphfleet">
   <img alt="X (formerly Twitter) Follow" src="https://img.shields.io/twitter/follow/agenticfleet">
   <img alt="Discord" src="https://img.shields.io/discord/1053300403149733969?style=flat&label=discord">


   

</div>


  
![image](https://github.com/user-attachments/assets/c3ca5ec8-1bbf-4a9c-988e-e7f5100ea5d5)
<img alt="X (formerly Twitter) Follow" src="https://img.shields.io/twitter/follow/agenticfleet">
   <img alt="Discord" src="https://img.shields.io/discord/1053300403149733969?style=for-the-badge&logo=discord">
GraphFleet is an advanced implementation of [GraphRAG from Microsoft](https://github.com/microsoft/graphrag), designed to enhance large language models' ability to reason about complex information and private datasets. It builds upon GraphRAG (Retrieval Augmented Generation using Graph structures) and will gradually adopt its own path to fulfill our roadmap at Qredence.

## GraphFleet

GraphFleet uses knowledge graphs to provide substantial improvements in question-and-answer performance when reasoning about complex information. It addresses limitations of traditional RAG approaches:


## Roadmap


- [ ] Provide a FleetUI Design Kit and a quicker way of starting GraphFleet locally.
- [ ] Provide a Toddle interface ready to use for GraphFleet
- [ ] Add integrations of Composio
- [ ] Add integrations of LangSmith
- [ ] Add few selfhosting  one click deploy solutions.
- [ ] Access GraphFleet through a secure and enterprise-ready Azure Cloud hosting version.
- [ ] And way more... 👀

## Key Features

- Structured, hierarchical approach to Retrieval Augmented Generation.
- Knowledge graph extraction from raw text.
- Community hierarchy building.
- Hierarchical summarization.
- Enhanced reasoning capabilities for LLMs on private datasets.

## Contribute

- Leave us a star ♥
- Fork and contribute to the project
- [![Join the discord](https://discord.gg/BD8MPgzEJc)

## Getting Started

### Prerequisites


- Python 3.10
- Poetry
- Make sure to have a virtual environment manager such as `virtualenv` installed


### Installation

1. Clone the repository:

``` bash
   git clone https://github.com/Qredence/GraphFleet.git
   cd GraphFleet
```


2. Simply run these in your terminal:

   ``` bash
   poetry shell
   poetry install
   ```



### Usage

1. Configuration:
Environment Variables: Set up your environment variables in a .env file (refer to the .env.example file for available options). Key variables include:

   ```sh
   export GRAPHRAG_API_KEY="fd7763c639184c20962857cacacd1a38"
   export GRAPHRAG_API_BASE="https://gpt-4o-fr.openai.azure.com"
   export GRAPHRAG_API_VERSION="2024-04-01-preview"
   export GRAPHRAG_LLM_MODEL="gpt-4"
   export GRAPHRAG_DEPLOYMENT_NAME="model name"
   export GRAPHRAG_EMBEDDING_MODEL="embedding model"
   ```

   settings.yaml: Customize GraphFleet's behavior further by modifying the settings.yaml file within the graphfleet directory.

1. Data Indexing:
Jupyter Notebook Guide: Follow the instructions provided in the get-started-graphfleet.ipynb notebook to learn how to index your data with GraphFleet. This notebook provides a hands-on experience for setting up your knowledge base.

1. Interacting with GraphFleet:
Jupyter Notebooks: Explore GraphFleet's capabilities with the provided notebooks:

   get-started-graphfleet.ipynb: A comprehensive guide to indexing your data and running basic queries.

   Local Search Notebook.ipynb: Demonstrates local search techniques.

   app.py (FastAPI Application): Run a Streamlit-powered web interface to interact with GraphFleet using a user-friendly chat-like interface.

### Start the application API only

``` bash
uvicorn graphfleet.api.api:app --host 0.0.0.0 --port 8001
```

Access the interface in your web browser at the provided URL  <http://0.0.0.0:8001/docs> .



1. Data Indexing:

Jupyter Notebook Guide: Follow the instructions provided in the get-started-graphfleet.ipynb notebook to learn how to index your data with GraphFleet. This notebook provides a hands-on experience for setting up your knowledge base.

3. Interacting with GraphFleet:
Jupyter Notebooks: Explore GraphFleet's capabilities with the provided notebooks:

get-started-graphfleet.ipynb: A comprehensive guide to indexing your data and running basic queries.
Local Search Notebook.ipynb: Demonstrates local search techniques.
[Add descriptions of other notebooks and their purpose here]
app.py (FastAPI Application): Run a Streamlit-powered web interface to interact with GraphFleet using a user-friendly chat-like interface:

### Running the API only

To run the API, save the code in a file named api.py and execute the following command in your terminal:

``` bash
uvicorn api:app --reload --port 8001
```

### Start the application

``` bash
streamlit run app.py # Access the interface in your web browser at the provided URL (usually http://localhost:8080).
```

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

## Security

[Security](SECURITY.md)

## License

[text](LICENSE)

## Star History
[![Star History Chart](https://api.star-history.com/svg?repos=Qredence/GraphFleet&type=Date)](https://star-history.com/#Qredence/GraphFleet&Date)
