"""
Example demonstrating performance optimization techniques in GraphFleet.
"""

import time
from typing import List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

from graphfleet import GraphFleet
from graphfleet.utils.profiling import profile, timer
from graphfleet.cache import cache_result

# Initialize GraphFleet with performance optimizations
gf = GraphFleet(
    config={
        "performance": {
            "cache": {
                "backend": "redis",
                "ttl": 3600
            },
            "batch": {
                "size": 1000,
                "workers": 4
            },
            "storage": {
                "compression": True,
                "compression_level": 6
            }
        }
    }
)

@profile
def batch_document_processing():
    """Demonstrate batch processing of documents."""
    # Generate sample documents
    documents = [
        {
            "content": f"Document {i} content",
            "metadata": {"id": i}
        }
        for i in range(10000)
    ]

    # Process in batches
    with timer("Batch Processing"):
        results = gf.process_documents(
            documents,
            batch_size=1000,
            parallel=True
        )

    print(f"Processed {len(results)} documents in batches")
    return results

@cache_result(ttl=3600)
def cached_computation(data: List[Dict[str, Any]]):
    """Demonstrate result caching for expensive computations."""
    # Simulate expensive computation
    time.sleep(1)
    return {
        "total": len(data),
        "processed": [item["id"] for item in data]
    }

def parallel_processing():
    """Demonstrate parallel processing strategies."""
    data = list(range(1000))

    # Thread pool for I/O-bound tasks
    with timer("Thread Pool"):
        with ThreadPoolExecutor(max_workers=4) as executor:
            results_thread = list(executor.map(
                lambda x: x * 2,
                data
            ))

    # Process pool for CPU-bound tasks
    with timer("Process Pool"):
        with ProcessPoolExecutor(max_workers=4) as executor:
            results_process = list(executor.map(
                lambda x: x ** 2,
                data
            ))

    print(f"Processed {len(data)} items in parallel")
    return results_thread, results_process

def optimized_queries():
    """Demonstrate query optimization techniques."""
    # Create sample graph
    graph = gf.create_graph(
        name="performance-demo",
        config={
            "index": {
                "type": "faiss",
                "dimension": 768,
                "metric": "cosine"
            },
            "cache": {
                "enabled": True,
                "max_size": "1G"
            }
        }
    )

    # Optimized query with hints
    with timer("Optimized Query"):
        results = graph.query(
            """
            MATCH (d:Document)-[:CONTAINS]->(c:Concept)
            WHERE c.type = 'technology'
            RETURN d.title, collect(c.name) as concepts
            """,
            hints={
                "use_index": True,
                "parallel": True,
                "cache": True
            }
        )

    print(f"Query returned {len(results)} results")
    return results

def memory_optimization():
    """Demonstrate memory optimization techniques."""
    # Configure memory limits
    gf.configure_memory(
        max_heap="8G",
        cache_size="2G",
        buffer_pool="1G"
    )

    # Stream large datasets
    with timer("Streaming Processing"):
        with gf.stream_documents("large_dataset.jsonl") as stream:
            for batch in stream.iter_batches(batch_size=1000):
                process_batch(batch)

def process_batch(batch):
    """Process a batch of documents."""
    # Simulate batch processing
    time.sleep(0.1)
    return len(batch)

def benchmark_operations():
    """Run performance benchmarks."""
    results = {}

    # Benchmark document indexing
    with timer("Document Indexing") as t:
        for _ in range(100):
            gf.index_document({
                "content": "Test document",
                "metadata": {"type": "test"}
            })
        results["indexing"] = t.elapsed

    # Benchmark search operations
    with timer("Search Operations") as t:
        for _ in range(100):
            gf.search("test query", limit=10)
        results["search"] = t.elapsed

    # Benchmark graph operations
    with timer("Graph Operations") as t:
        graph = gf.get_graph("performance-demo")
        for _ in range(100):
            graph.query(
                "MATCH (n) RETURN count(n)",
                cache=True
            )
        results["graph"] = t.elapsed

    print("\nBenchmark Results:")
    for op, time in results.items():
        print(f"- {op}: {time:.2f}s")

def monitor_resources():
    """Monitor system resource usage."""
    from graphfleet.utils.monitoring import ResourceMonitor

    monitor = ResourceMonitor()
    with monitor:
        # Run some operations
        batch_document_processing()
        parallel_processing()
        optimized_queries()

    print("\nResource Usage:")
    print(f"- Peak Memory: {monitor.peak_memory_mb:.2f} MB")
    print(f"- CPU Usage: {monitor.cpu_percent:.1f}%")
    print(f"- I/O Operations: {monitor.io_operations}")

def main():
    """Run the performance optimization examples."""
    print("1. Batch Processing...")
    batch_document_processing()

    print("\n2. Parallel Processing...")
    parallel_processing()

    print("\n3. Query Optimization...")
    optimized_queries()

    print("\n4. Memory Optimization...")
    memory_optimization()

    print("\n5. Performance Benchmarks...")
    benchmark_operations()

    print("\n6. Resource Monitoring...")
    monitor_resources()

if __name__ == "__main__":
    main() 