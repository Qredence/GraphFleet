import os
import sys
import logging
import asyncio
from pathlib import Path
from graphfleet import GraphFleet
from graphfleet.app.services import ingest_documents, tune_prompts
from graphfleet.app.models import PromptTuningRequest, BuildIndexRequest

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Initialize GraphFleet
        project_dir = Path("data")  # Changed to match .env PROJECT_DIR
        logger.info(f"Initializing GraphFleet with project directory: {project_dir}")
        graph_fleet = GraphFleet(str(project_dir))
        logger.info("GraphFleet initialized successfully!")

        # Create sample document
        sample_doc = """
        GraphFleet is an advanced document processing system that uses graph-based representations
        for efficient information retrieval. It features automatic prompt tuning and intelligent
        indexing capabilities.

        Key Features:
        1. Graph-based document representation
        2. Auto-tuning of prompts
        3. Intelligent chunking and indexing
        4. Hybrid search capabilities
        
        The system processes documents by first chunking them into meaningful segments, then
        creating graph representations that preserve relationships between different parts of
        the content.
        """
        
        docs_dir = project_dir / "docs"
        docs_dir.mkdir(exist_ok=True)
        sample_doc_path = docs_dir / "sample.txt"
        sample_doc_path.write_text(sample_doc)
        logger.info(f"Created sample document at {sample_doc_path}")

        # Test auto-prompting
        logger.info("Starting auto-prompting test")
        prompt_request = PromptTuningRequest(
            task_type="query",
            sample_queries=[
                "What are the main features?",
                "How does the system work?",
                "Explain the document processing workflow"
            ],
            target_metrics=["accuracy", "relevance", "coherence"]
        )

        try:
            logger.info("Tuning prompts...")
            tuning_result = await tune_prompts(
                task_type=prompt_request.task_type,
                sample_queries=prompt_request.sample_queries,
                target_metrics=prompt_request.target_metrics,
                settings=graph_fleet.settings
            )
            logger.info("\nPrompt Tuning Results:")
            logger.info(f"- Success: {tuning_result.success}")
            logger.info("- Performance Metrics:")
            for metric, value in tuning_result.performance_metrics.items():
                logger.info(f"  {metric}: {value:.3f}")
        except Exception as e:
            logger.error(f"Error during prompt tuning: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {getattr(e, 'details', 'No details available')}")

        # Test indexing
        logger.info("Starting indexing test")
        try:
            logger.info("Creating index...")
            await graph_fleet.create_index()
            logger.info("Index created successfully!")
            
            # Test different query types
            queries = {
                "semantic": "What are the key features of the system?",
                "local": "How does document chunking work?",
                "global": "What is GraphFleet?"
            }
            
            for query_type, query_text in queries.items():
                logger.info(f"\nExecuting {query_type.upper()} QUERY: {query_text}")
                try:
                    result = await graph_fleet.query(
                        query_text=query_text,
                        query_type=query_type.lower()
                    )
                    logger.info(f"Answer: {result.get('answer', 'No answer found')}")
                    logger.info(f"Confidence: {result.get('confidence', 0):.2f}")
                except Exception as e:
                    logger.error(f"Error during {query_type} query: {str(e)}")
                    logger.error(f"Error type: {type(e).__name__}")
                    logger.error(f"Error details: {getattr(e, 'details', 'No details available')}")
                    
        except Exception as e:
            logger.error(f"Error building index: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            logger.error(f"Error details: {getattr(e, 'details', 'No details available')}")

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error details: {getattr(e, 'details', 'No details available')}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 