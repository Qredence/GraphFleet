# Overview
![image](https://github.com/user-attachments/assets/c3ca5ec8-1bbf-4a9c-988e-e7f5100ea5d5)

GraphFleet is based for now from the great  [GraphRAG from Microsoft](https://github.com/microsoft/graphrag) is an advanced implementation of GraphRAG (Retrieval Augmented Generation using Graph structures), designed to enhance large language models' ability to reason about complex information and private datasets. GraphFleet will gradually adopts its own path to fullfilled our roadmap at Qredence.

## GraphFleet

GraphFleet uses knowledge graphs to provide substantial improvements in question-and-answer performance when reasoning about complex information. It addresses limitations of traditional RAG approaches by:

1. Connecting disparate pieces of information through shared attributes.
2. Structured, hierarchical approach to Retrieval Augmented Generation
3. Knowledge graph extraction from raw text
4. Community hierarchy building
5. Hierarchical summarization
6. Enhanced reasoning capabilities for LLMs on private datasets
3. (Soon) Improve the structure of the overall repository.
4. (Soon) Add our dedicated prompts for the indexing & queriying, more vectordatabase
5. (Soon) Add pull requests features
6. (Soon) Provide an User Interface and a quicker way of starting GraphFleet locally
7. (Soon) Access GraphFleet among our set of solution through a secure and enterprise ready Azure Cloud hosting version. [Join the waitlist now](https://forms.office.com/e/9cHKxgrQgV)
8. And way more... 👀

## Key Features

- Structured, hierarchical approach to Retrieval Augmented Generation
- Knowledge graph extraction from raw text
- Community hierarchy building
- Hierarchical summarization
- Enhanced reasoning capabilities for LLMs on private datasets

## Getting Started

### Prerequisites

- Python 3.10+
- Poetry (for dependency management)

### Installation

1. Clone the repository:
```
git clone https://github.com/Qredence/GraphFleet.git
cd GraphFleet
```


2. Install dependencies using Poetry:

```
poetry shell
```

```
poetry install
```

### Usage

1. Setting up your settings:

```
cd graphfleet
```

- Set up the necessary environment variables in the `.env.example` file and change the name to .env.
The required ones being :

```
# Base LLM Settings
GRAPHRAG_API_KEY="your_api_key"
GRAPHRAG_API_BASE="http://<domain>.openai.azure.com" # For Azure OpenAI Users
GRAPHRAG_API_VERSION="api_version" # For Azure OpenAI Users

# Text Generation Settings
GRAPHRAG_LLM_TYPE="azure_openai_chat" # or openai_chat
GRAPHRAG_LLM_DEPLOYMENT_NAME="gpt-4-turbo-preview"
GRAPHRAG_LLM_MODEL_SUPPORTS_JSON=True

# Text Embedding Settings
GRAPHRAG_EMBEDDING_TYPE="azure_openai_embedding" # or openai_embedding
GRAPHRAG_LLM_DEPLOYMENT_NAME="text-embedding-3-small"

# Data Mapping Settings
GRAPHRAG_INPUT_TYPE="text"
```


- Open `settings.yaml` and fill the parameter you wish to fill according to your needs.


2. Run the indexing process:

```
python -m graphrag.index --root ./graphfleet
```


3. Perform queries in local mode or global mode depending on your usecase learn more in the [GraphRAG documentation](https://microsoft.github.io/graphrag/posts/query/overview/):
For local query mode :

```
python -m graphrag.query --root ./graphfleet --method local "What are the key features of GraphRAG ??"
```

For Global query mode :

```
python -m graphrag.query --root ./graphfleet --method global "What are the top main features of GraphRAG"
```
