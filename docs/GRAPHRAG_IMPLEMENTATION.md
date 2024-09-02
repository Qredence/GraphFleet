# GraphRAG Implementation

This document describes the core GraphRAG implementation within the GraphFleet project, located in the `graphfleet` directory. Think of GraphRAG as the brain of the operation - it's responsible for understanding information and answering your questions in a smart way.

## Functionality

The GraphRAG implementation is responsible for:

- **Knowledge Graph Construction:**
    - Indexes data from various sources into a knowledge graph using LanceDB. Imagine taking a giant library and organizing all the books and information into a structured, interconnected network of knowledge. That's what the knowledge graph is!
- **Query Processing:**
    - Translates user queries into knowledge graph traversals to retrieve relevant information. When you ask a question, GraphRAG figures out the best way to navigate that knowledge graph and find the answers you're looking for.
- **Response Generation:**
    - Leverages Large Language Models (LLMs) to generate comprehensive and contextually relevant responses based on the retrieved information. This is where the "magic" of AI comes in - LLMs are trained on massive amounts of text data and can generate human-like text to answer your questions in a comprehensive and informative way.

## Key Files and Directories

- **settings.yaml:** The primary configuration file for GraphRAG, defining parameters for LLM interaction, embedding models, data paths, and various pipeline stages. This is like the instruction manual for GraphRAG, telling it how to operate and what settings to use.

## Pipeline Stages

The GraphRAG implementation encompasses several key pipeline stages, like different steps in a recipe:

- **Data Ingestion:** Loads data from specified sources, such as text files or CSV files. This is like gathering all the ingredients you need before you start cooking.
- **Chunking:** Divides input data into manageable chunks for processing and embedding. This is like chopping up vegetables into bite-sized pieces.
- **Entity Extraction:** Identifies and extracts entities from text chunks using LLMs and predefined entity types. This is like identifying the different ingredients in your recipe - carrots, onions, etc.
- **Relationship Extraction:** Detects relationships between extracted entities to construct the knowledge graph. This is like understanding how the ingredients in your recipe are related - carrots are chopped, onions are diced, and they're both sautéed together.
- **Embedding Generation:** Generates embeddings for text chunks and entities using specified embedding models. This is like translating your recipe into a different language that a computer can understand.
- **Knowledge Graph Storage:** Stores the constructed knowledge graph, including entities, relationships, and embeddings, in LanceDB. This is like storing your finished recipe in a cookbook for later use.
- **Query Processing and Response Generation:** Handles incoming user queries, translates them into knowledge graph traversals, retrieves relevant information, and utilizes LLMs to generate responses. This is like using your cookbook to find a specific recipe and then following the instructions to cook a delicious meal.

## Configuration

The `settings.yaml` file plays a crucial role in configuring the GraphRAG pipeline. It allows customization of:

- LLM settings (API keys, models, parameters) - This is like choosing which AI chef you want to help you cook.
- Embedding model selection - This is like choosing the language you want to translate your recipe into.
- Data input and output paths - This is like deciding where to get your ingredients and where to store your finished dishes.
- Chunking parameters - This is like deciding how big or small to chop your vegetables.
- Entity and relationship extraction settings - This is like fine-tuning your ability to identify and understand the ingredients in your recipes.
- Knowledge graph storage options - This is like choosing whether to store your recipes in a physical cookbook or a digital app.
- Local and global search parameters - This is like deciding whether to search for a recipe in a specific section of your cookbook or across the entire book.

## Interaction with Other Components

The GraphRAG implementation interacts with:

- **FastAPI Application (app):** Provides the API endpoints for accessing GraphRAG functionality. This is like the kitchen counter where you interact with your AI chef.
- **Configuration (app/config.py):** Loads application-level settings. This is like having a pantry where you store your cooking utensils and spices.
- **External Data Sources:** Reads data from specified input sources. This is like going to the grocery store to buy ingredients.
- **LanceDB:** Utilizes LanceDB for efficient knowledge graph storage and retrieval. This is like having a well-organized refrigerator to store your ingredients and leftovers.

## Further Information

For detailed information on GraphRAG concepts, configuration options, and usage, refer to the GraphRAG documentation.