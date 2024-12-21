# Advanced Features Guide

This guide covers advanced features and best practices for using GraphFleet effectively.

## Custom Query Pipelines

GraphFleet allows you to create custom query pipelines that combine different retrieval strategies:

```python
from graphfleet import GraphFleet, QueryConfig, RetrievalType

# Initialize
graph_fleet = GraphFleet("./my_project")

# Custom hybrid pipeline
config = QueryConfig(
    retrieval_type=RetrievalType.HYBRID,
    vector_weight=0.7,
    keyword_weight=0.3,
    context_window=3
)

result = await graph_fleet.query(
    "How do neural networks work?",
    config=config
)
```

## Template Management

Create and manage custom prompt templates:

```python
from graphfleet import PromptGenerator

# Initialize
generator = PromptGenerator(model="gpt-4")

# Register custom template
generator.register_template(
    name="technical",
    template="""
    You are a technical expert. Based on the following documentation:
    {context}
    
    Please answer: {query}
    
    Format your answer as:
    1. Brief overview
    2. Technical details
    3. Examples
    """,
    metadata={
        "description": "Template for technical questions",
        "version": "1.0"
    }
)

# Generate prompts
prompts = await generator.generate_prompts(
    template_type="technical",
    context_window=3
)
```

## Query Optimization

Optimize query parameters for better results:

```python
from graphfleet import QueryOptimizer

# Initialize
optimizer = QueryOptimizer(
    evaluation_model="gpt-4",
    num_trials=5
)

# Define parameter space
param_space = {
    "temperature": (0.0, 1.0),
    "top_k": (3, 10),
    "threshold": (0.5, 0.9)
}

# Optimize
best_params = await optimizer.optimize(
    query="What is deep learning?",
    param_space=param_space
)

# Query with optimized parameters
result = await graph_fleet.query(
    "What is deep learning?",
    **best_params
)
```

## Advanced Indexing

Fine-tune your indexing strategy:

```python
from graphfleet import IndexConfig, IndexType

# Custom index configuration
config = IndexConfig(
    index_type=IndexType.LANCEDB,
    dimension=1536,
    metric="cosine",
    additional_config={
        "num_partitions": 8,
        "num_threads": 4
    }
)

# Create index
await graph_fleet.create_index(config=config)
```

## Batch Processing

Process multiple queries efficiently:

```python
# Prepare queries
queries = [
    "What is machine learning?",
    "How do neural networks work?",
    "What is deep learning?"
]

# Process in batch
async def batch_process(queries, batch_size=2):
    results = []
    for i in range(0, len(queries), batch_size):
        batch = queries[i:i + batch_size]
        batch_results = await graph_fleet.batch_query(
            queries=batch,
            max_tokens=1000
        )
        results.extend(batch_results)
    return results

# Run batch processing
results = await batch_process(queries)
```

## Performance Optimization

### 1. Chunking Strategy

Optimize document chunking:

```python
from graphfleet import TextProcessor

processor = TextProcessor(
    chunk_size=512,
    overlap=50,
    split_method="markdown"
)

# Process with metadata
chunks = processor.process_text(
    text="Your document content",
    metadata={
        "source": "technical_docs",
        "category": "machine_learning"
    }
)
```

### 2. Caching

Enable result caching:

```python
from graphfleet import GraphFleet

graph_fleet = GraphFleet(
    "./my_project",
    config={
        "enable_cache": True,
        "cache_size": 1000,
        "cache_ttl": 3600  # 1 hour
    }
)
```

### 3. Parallel Processing

Use parallel processing for large datasets:

```python
async def parallel_index(documents, max_workers=4):
    tasks = []
    for doc in documents:
        task = graph_fleet.add_document(doc)
        tasks.append(task)
        if len(tasks) >= max_workers:
            await asyncio.gather(*tasks)
            tasks = []
    
    if tasks:
        await asyncio.gather(*tasks)
```

## Best Practices

1. **Document Processing**
   - Use appropriate chunk sizes (256-1024 tokens)
   - Maintain context with proper overlap
   - Include relevant metadata

2. **Query Optimization**
   - Start with default parameters
   - Use optimization for important queries
   - Monitor and adjust based on results

3. **Template Management**
   - Create specific templates for different use cases
   - Include clear instructions
   - Version your templates

4. **Performance**
   - Use batch processing for multiple queries
   - Enable caching for frequent queries
   - Monitor resource usage

5. **Error Handling**
   - Implement proper error handling
   - Use appropriate timeouts
   - Handle rate limits gracefully

## Monitoring and Analysis

### 1. Query Analysis

```python
# Analyze query results
analysis = await graph_fleet.analyze_query(
    query="What is AI?",
    metrics=["relevance", "coherence"]
)

print(f"Relevance: {analysis.scores['relevance']}")
print(f"Coherence: {analysis.scores['coherence']}")
```

### 2. Performance Metrics

```python
# Get performance metrics
metrics = await graph_fleet.get_metrics()

print(f"Average query time: {metrics['avg_query_time']}ms")
print(f"Cache hit rate: {metrics['cache_hit_rate']}%")
```

## Advanced Configuration

### 1. Custom Storage Backend

```python
from graphfleet import GraphFleet
from your_storage import CustomStorage

graph_fleet = GraphFleet(
    "./my_project",
    config={
        "storage": {
            "backend": CustomStorage,
            "options": {
                "connection_string": "..."
            }
        }
    }
)
```

### 2. Custom Embeddings

```python
from graphfleet import GraphFleet
from your_embeddings import CustomEmbeddings

graph_fleet = GraphFleet(
    "./my_project",
    config={
        "embeddings": {
            "model": CustomEmbeddings,
            "options": {
                "model_path": "..."
            }
        }
    }
)
```

## Troubleshooting

1. **Query Issues**
   - Check query configuration
   - Verify index status
   - Review error messages

2. **Performance Issues**
   - Monitor resource usage
   - Check batch sizes
   - Review caching strategy

3. **Index Issues**
   - Verify document processing
   - Check storage backend
   - Review index configuration
