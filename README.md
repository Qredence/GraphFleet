# Overview

<div align="left">
<a href="https://pypi.org/project/graphfleet/">
   <img alt="Pepy Total Downlods" src="https://img.shields.io/pepy/dt/graphfleet">
   </a>
   <img alt="GitHub License" src="https://img.shields.io/github/license/qredence/graphfleet">
   <img alt="GitHub forks" src="https://img.shields.io/github/forks/qredence/graphfleet">
   <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/qredence/graphfleet">

</div>

![GraphFleet_Query](https://github.com/user-attachments/assets/cf32f463-d52f-4568-a795-1f869f33d07f)

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
- <a href="https://discord.gg/BD8MPgzEJc">
    <img alt="Discord" src="https://img.shields.io/discord/1053300403149733969?style=for-the-badge&logo=discord">
   </a>
   <img alt="X (formerly Twitter) Follow" src="https://img.shields.io/twitter/follow/agenticfleet?style=for-the-badge&logo=x&logoColor=white&labelColor=blue&link=https%3A%2F%2Fx.com%2Fagenticfleet">

## Getting Started

### Prerequisites

- Python 3.11

- Poetry
- Make sure to have a virtual environment manager such as `virtualenv` installed

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Qredence/GraphFleet.git
   cd GraphFleet
   ```

2. Install the dependencies:

   ```bash
   poetry shell
   poetry install
   ```

### Usage

1. Configuration:
Environment Variables: Set up your environment variables in a .env file (refer to the .env.example file for available options). Key variables include:

Fill in the .env file in the root folder and the one in the graphfleet folder.

 ```sh
export GRAPHRAG_API_KEY="your_api_key_here"
export GRAPHRAG_API_BASE="<https://your-azure-openai-resource.openai.azure.com/>"
export GRAPHRAG_API_VERSION=""
export GRAPHRAG_DEPLOYMENT_NAME="your_deployment_name"
export GRAPHRAG_API_TYPE="azure_openai"
export GRAPHRAG_EMBEDDING_MODEL="text-embedding-ada-002"
export GRAPHRAG_LLM_MODEL="gpt-4"
export GRAPHRAG_DATA_PATH="./your_data_directory"
export GRAPHRAG_EMBEDDING_TYPE="azure_openai_embedding"
export GRAPHRAG_EMBEDDING_KEY="your_embedding_key_here"
export GRAPHRAG_EMBEDDING_ENDPOINT="<https://your-azure-openai-embedding-resource.openai.azure.com/>"
export GRAPHRAG_EMBEDDING_DEPLOYMENT_NAME="your_embedding_deployment_name"

```

   settings.yaml: Customize GraphFleet's behavior further by modifying the settings.yaml file within the graphfleet directory.

1. Data Indexing:
Jupyter Notebook Guide: Follow the instructions provided in the get-started-graphfleet.ipynb notebook to learn how to index your data with GraphFleet. This notebook provides a hands-on experience for setting up your knowledge base.

1. Interacting with GraphFleet:
Jupyter Notebooks: Explore GraphFleet's capabilities with the provided notebooks:

   get-started-graphfleet.ipynb: A comprehensive guide to indexing your data and running basic queries.

   Local Search Notebook.ipynb: Demonstrates local search techniques.

   app.py (FastAPI Application): Run a Streamlit-powered web interface to interact with GraphFleet using a user-friendly chat-like interface.

### Add your text files in ./graphfleet/input/ and run the auto_prompt function

``` bash
!python -m graphrag.prompt_tune \
    --config ./graphfleet/settings.yaml \
    --root ./graphfleet \
    --no-entity-types \
    --output ./graphfleet/prompts
```



### Data Indexing:

Jupyter Notebook Guide: Follow the instructions provided in the get-started-graphfleet.ipynb notebook to learn how to index your data with GraphFleet. This notebook provides a hands-on experience for setting up your knowledge base.

``` bash
! python -m graphrag.index \
    --verbose \
    --root ./graphfleet \
    --config ./graphfleet/settings.yaml
```


## Interacting with GraphFleet:
Jupyter Notebooks: Explore GraphFleet's capabilities with the provided notebooks:

get-started-graphfleet.ipynb: A comprehensive guide to indexing your data and running basic queries.
Local Search Notebook.ipynb: Demonstrates local search techniques.
[Add descriptions of other notebooks and their purpose here]
app.py (FastAPI Application): Run a Streamlit-powered web interface to interact with GraphFleet using a user-friendly chat-like interface:

### Running the API only (or run CLI commands for local search or global search)

To run the API, save the code in a file named api.py and execute the following command in your terminal:

``` bash
## uvicorn app:main --reload --port 8001 
```

### Run the CLI commands to query the graph (Follow the get-started-graphfleet.ipynb notebook)

``` bash
! python -m graphrag.query \
--root ./graphfleet \
--method global \
--streaming \ #stream the response
"Language Agent Tree Search?"
```

``` bash
! python -m graphrag.query \
--root ./graphfleet \
--method global \
--streaming \ #stream the response
"What are the key features of GraphRAG ??"
```

### Running the API only

To run the API, save the code in a file named api.py and execute the following command in your terminal:

``` bash
## uvicorn api:app --reload --port 8001 SOON
```


## Security

For details about our security policy, please see [Security](SECURITY.md) or [Security](docs/SECURITY.md).

## License

This project is licensed under the Apache License 2.0. For the full license text, please see [License](LICENSE) or [License](docs/LICENSE).

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Qredence/GraphFleet&type=Date)](https://star-history.com/#Qredence/GraphFleet&Date)
