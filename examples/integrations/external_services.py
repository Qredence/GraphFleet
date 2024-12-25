"""
Example demonstrating GraphFleet integration with external services.
"""

import os
from pathlib import Path
from typing import List, Dict, Any

from graphfleet import GraphFleet
from graphfleet.integrations import (
    S3Storage,
    ElasticsearchIndex,
    HuggingFaceModel
)

# Initialize GraphFleet with external services
gf = GraphFleet(
    config={
        "storage": {
            "type": "s3",
            "bucket": "graphfleet-demo",
            "prefix": "documents"
        },
        "search": {
            "type": "elasticsearch",
            "hosts": ["localhost:9200"],
            "index_prefix": "graphfleet"
        },
        "ml": {
            "type": "huggingface",
            "model_id": "sentence-transformers/all-mpnet-base-v2"
        }
    }
)

def setup_storage():
    """Configure S3 storage backend."""
    storage = S3Storage(
        bucket="graphfleet-demo",
        prefix="documents",
        config={
            "region": "us-west-2",
            "endpoint_url": "http://localhost:4566"  # For LocalStack
        }
    )

    # Upload sample documents
    documents = [
        {
            "content": "Sample document 1",
            "metadata": {"type": "text"}
        },
        {
            "content": "Sample document 2",
            "metadata": {"type": "text"}
        }
    ]

    # Store documents
    doc_ids = storage.store_documents(documents)
    print(f"Stored {len(doc_ids)} documents in S3")
    return storage, doc_ids

def setup_search():
    """Configure Elasticsearch search backend."""
    search = ElasticsearchIndex(
        hosts=["localhost:9200"],
        index_prefix="graphfleet",
        config={
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    )

    # Create index mappings
    search.create_index_mappings({
        "content": {
            "type": "text",
            "analyzer": "standard"
        },
        "embedding": {
            "type": "dense_vector",
            "dims": 768
        },
        "metadata": {
            "type": "object"
        }
    })

    print("Configured Elasticsearch index")
    return search

def setup_ml_model():
    """Configure HuggingFace model for embeddings."""
    model = HuggingFaceModel(
        model_id="sentence-transformers/all-mpnet-base-v2",
        config={
            "device": "cuda" if os.environ.get("USE_GPU") else "cpu",
            "batch_size": 32
        }
    )
    print("Loaded ML model")
    return model

def process_documents(
    storage: S3Storage,
    search: ElasticsearchIndex,
    model: HuggingFaceModel,
    doc_ids: List[str]
):
    """Process documents through the pipeline."""
    # Load documents from S3
    documents = storage.load_documents(doc_ids)

    # Generate embeddings
    embeddings = model.encode_documents(
        [doc["content"] for doc in documents]
    )

    # Index documents with embeddings
    for doc, embedding in zip(documents, embeddings):
        doc["embedding"] = embedding.tolist()
        search.index_document(doc)

    print("Processed and indexed documents")

def search_documents(
    search: ElasticsearchIndex,
    model: HuggingFaceModel,
    query: str
):
    """Search documents using hybrid search."""
    # Generate query embedding
    query_embedding = model.encode_text(query)

    # Hybrid search (combining semantic and keyword search)
    results = search.hybrid_search(
        query=query,
        embedding=query_embedding,
        weights={
            "semantic": 0.7,
            "keyword": 0.3
        },
        size=5
    )

    print(f"\nSearch results for '{query}':")
    for hit in results:
        print(f"- Score: {hit['_score']:.2f}, Content: {hit['_source']['content'][:100]}...")

def custom_pipeline():
    """Demonstrate custom processing pipeline."""
    # Define pipeline stages
    pipeline = gf.create_pipeline([
        {
            "name": "document_loader",
            "type": "s3",
            "config": {
                "bucket": "graphfleet-demo"
            }
        },
        {
            "name": "text_processor",
            "type": "custom",
            "function": lambda doc: {
                **doc,
                "word_count": len(doc["content"].split())
            }
        },
        {
            "name": "embedder",
            "type": "huggingface",
            "config": {
                "model_id": "sentence-transformers/all-mpnet-base-v2"
            }
        },
        {
            "name": "indexer",
            "type": "elasticsearch",
            "config": {
                "index": "processed-docs"
            }
        }
    ])

    # Process documents through pipeline
    results = pipeline.process([
        {"id": "doc1", "content": "Sample document for pipeline"},
        {"id": "doc2", "content": "Another document for testing"}
    ])

    print("\nPipeline processing results:")
    for doc_id, status in results.items():
        print(f"- {doc_id}: {status}")

def cleanup(search: ElasticsearchIndex):
    """Clean up resources."""
    # Delete indices
    search.delete_indices()
    print("\nCleaned up resources")

def main():
    """Run the example."""
    print("1. Setting up storage...")
    storage, doc_ids = setup_storage()

    print("\n2. Setting up search...")
    search = setup_search()

    print("\n3. Setting up ML model...")
    model = setup_ml_model()

    print("\n4. Processing documents...")
    process_documents(storage, search, model, doc_ids)

    print("\n5. Searching documents...")
    search_documents(search, model, "sample document")

    print("\n6. Running custom pipeline...")
    custom_pipeline()

    print("\n7. Cleaning up...")
    cleanup(search)

if __name__ == "__main__":
    main() 