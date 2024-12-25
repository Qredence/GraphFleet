"""GraphFleet CLI for document processing and querying."""
import os
import click
from pathlib import Path
import logging
from typing import Optional

from .core.indexer import GraphIndexer
from .core.querying import QueryEngine
from .utils.prompt_generator import PromptGenerator
from .utils.chunker import chunk_text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """GraphFleet CLI for document processing and querying."""
    pass

@cli.command()
@click.option('--root', required=True, help='Root directory for the project')
@click.option('--config', default=None, help='Path to config file')
def index(root: str, config: Optional[str] = None):
    """Run the indexing pipeline on input documents."""
    root_path = Path(root)
    input_dir = root_path / "input"
    output_dir = root_path / "output"
    
    if not input_dir.exists():
        raise click.ClickException(f"Input directory not found: {input_dir}")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize indexer
    indexer = GraphIndexer(
        input_dir=input_dir,
        output_dir=output_dir,
        config_path=config
    )
    
    try:
        # Run indexing pipeline
        logger.info("Starting indexing pipeline...")
        indexer.run_pipeline()
        logger.info(f"Indexing complete. Output saved to {output_dir}")
    except Exception as e:
        raise click.ClickException(f"Indexing failed: {str(e)}")

@cli.command()
@click.option('--root', required=True, help='Root directory for the project')
@click.option('--method', type=click.Choice(['local', 'global', 'dynamic']), required=True, 
              help='Query method to use')
@click.option('--config', default=None, help='Path to config file')
@click.argument('query')
def query(root: str, method: str, query: str, config: Optional[str] = None):
    """Query the indexed documents."""
    root_path = Path(root)
    output_dir = root_path / "output"
    
    if not output_dir.exists():
        raise click.ClickException(f"Output directory not found: {output_dir}")
    
    # Initialize query engine
    engine = QueryEngine(
        index_dir=output_dir,
        config_path=config
    )
    
    try:
        # Execute query based on method
        if method == 'local':
            result = engine.local_search(query)
        elif method == 'global':
            result = engine.global_search(query)
        else:  # dynamic
            result = engine.dynamic_search(query)
            
        click.echo(result)
    except Exception as e:
        raise click.ClickException(f"Query failed: {str(e)}")

@cli.command()
@click.option('--root', required=True, help='Root directory for the project')
@click.option('--task-type', required=True, help='Type of task to tune prompts for')
@click.option('--config', default=None, help='Path to config file')
def tune(root: str, task_type: str, config: Optional[str] = None):
    """Tune prompts for specific tasks."""
    root_path = Path(root)
    prompts_dir = root_path / "prompts"
    
    if not prompts_dir.exists():
        prompts_dir.mkdir(parents=True)
    
    # Initialize prompt generator
    generator = PromptGenerator(prompt_dir=prompts_dir)
    
    try:
        # Run prompt tuning
        logger.info(f"Tuning prompts for task: {task_type}")
        generator.tune_prompts(task_type)
        logger.info("Prompt tuning complete")
    except Exception as e:
        raise click.ClickException(f"Prompt tuning failed: {str(e)}")

@cli.command()
@click.option('--root', required=True, help='Root directory for the project')
def init(root: str):
    """Initialize a new GraphFleet project."""
    root_path = Path(root)
    
    # Create project structure
    directories = [
        "input",      # For input documents
        "output",     # For indexed data
        "prompts",    # For prompt templates
        "config",     # For configuration files
        "cache"       # For caching
    ]
    
    try:
        for dir_name in directories:
            dir_path = root_path / dir_name
            dir_path.mkdir(parents=True, exist_ok=True)
            
        # Create default config
        config_path = root_path / "config" / "settings.yaml"
        if not config_path.exists():
            default_config = """
### GraphFleet Configuration ###
llm:
  type: azure_openai_chat
  model: gpt-4
  api_version: '2024-02-15-preview'

embeddings:
  type: azure_openai_embedding
  model: text-embedding-3-large

indexing:
  chunk_size: 1000
  chunk_overlap: 200
  chunk_strategy: sentence

query:
  local_search:
    max_hops: 2
    similarity_threshold: 0.7
  global_search:
    community_level: 1
    
storage:
  type: file
  base_dir: output
"""
            config_path.write_text(default_config)
            
        # Create .env template
        env_path = root_path / ".env.example"
        if not env_path.exists():
            env_template = """
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_key_here
AZURE_OPENAI_ENDPOINT=your_endpoint_here

# GraphRAG
GRAPHRAG_API_KEY=your_key_here

# Optional: Azure Storage
AZURE_STORAGE_CONNECTION_STRING=your_connection_string_here
"""
            env_path.write_text(env_template)
            
        logger.info(f"Initialized GraphFleet project in {root_path}")
        logger.info("Next steps:")
        logger.info("1. Copy .env.example to .env and fill in your API keys")
        logger.info("2. Place your documents in the input directory")
        logger.info("3. Run 'graphfleet index --root .' to index your documents")
        
    except Exception as e:
        raise click.ClickException(f"Project initialization failed: {str(e)}")

if __name__ == '__main__':
    cli()
