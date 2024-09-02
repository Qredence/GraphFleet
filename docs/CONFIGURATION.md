# Configuration

This document explains the configuration mechanisms within the GraphFleet project, encompassing both application-level and GraphRAG-specific settings. Think of configuration as setting up the rules and parameters for how GraphFleet operates.

## Configuration Files

- **app/config.py:** Defines application-level settings using Pydantic's `BaseSettings`. This file is like the general settings panel for the entire application.
- **graphfleet/settings.yaml:** Configures GraphRAG parameters, including LLM settings, embedding models, and data paths. This file is like the specialized settings panel for the GraphRAG engine itself.

## Application-Level Settings (app/config.py)

The `app/config.py` file manages settings related to the FastAPI application, such as:

- **API_KEY:** API key for accessing external services like OpenAI. This is like your login credential to use OpenAI's powerful language models.
- **LLM_MODEL:** Identifier for the LLM used for response generation. This is like choosing which "brain" you want GraphFleet to use - a more powerful one for complex tasks, or a smaller one for quicker responses.
- **EMBEDDING_MODEL:** Name of the embedding model used for text representation. This is like choosing the language that GraphFleet uses to understand and process text.
- **API_BASE:** Base URL for external API endpoints. This is like the address of the OpenAI service that GraphFleet communicates with.
- **API_VERSION:** Version of the external API being used. This ensures that GraphFleet is speaking the same language as the OpenAI service.
- **INPUT_DIR:** Directory containing input data for GraphRAG. This is like the library where GraphFleet gets all its information from.
- **LANCEDB_URI:** URI for connecting to the LanceDB instance. This is like the address of the database where GraphFleet stores its knowledge graph.
- **COMMUNITY_LEVEL:** Level of community detection in the knowledge graph. This is like setting the granularity for how GraphFleet groups related information together.
- **MAX_TOKENS:** Maximum number of tokens allowed for LLM responses. This is like setting a limit on how long GraphFleet's answers can be.

## GraphRAG Settings (graphfleet/settings.yaml)

The `graphfleet/settings.yaml` file configures the behavior of the GraphRAG implementation, including:

- **LLM Settings:** API keys, model names, temperature, top_p, and other parameters for LLM interaction. These settings fine-tune how GraphRAG interacts with the chosen language model.
- **Embedding Settings:** API keys, model names, and other parameters for embedding generation. These settings control how GraphFleet translates text into a format it can understand.
- **Data Input and Output:** Paths for input data sources, cache directories, and output artifacts. These settings tell GraphFleet where to find data, where to store temporary files, and where to save results.
- **Chunking:** Chunk size, overlap, and grouping criteria for dividing text data. These settings control how GraphFleet breaks down large pieces of text into smaller, more manageable chunks.
- **Entity and Relationship Extraction:** Prompt templates, entity types, and maximum gleanings for entity and relationship extraction. These settings fine-tune how GraphFleet identifies and extracts key information from text.
- **Knowledge Graph Storage:** Storage type (file or blob) and related parameters. These settings determine how and where GraphFleet stores its knowledge graph.
- **Local and Global Search:** Parameters controlling the behavior of local and global search operations. These settings fine-tune how GraphFleet searches for information within its knowledge graph.

## Environment Variables

Configuration values can be overridden using environment variables. The `app/config.py` file uses `python-dotenv` to load environment variables from a `.env` file. This allows you to easily switch between different configurations without modifying the code directly.

## Configuration Hierarchy

The configuration follows a hierarchical structure, with environment variables overriding values specified in `app/config.py`, which in turn override defaults defined in `graphfleet/settings.yaml`. This ensures that the most specific settings take precedence.

## Best Practices

- Store sensitive information, such as API keys, in environment variables. This keeps your sensitive data separate from your codebase.
- Use descriptive names for configuration parameters. This makes your configuration files easier to understand and maintain.
- Document configuration options clearly in the respective files. This helps you and others understand the purpose of each setting.
- Test configuration changes thoroughly to ensure desired behavior. Don't assume your changes will work as expected - always test them!