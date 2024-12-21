"""
GraphFleet configuration module that extends GraphRAG configuration functionality.
"""

from pathlib import Path
from typing import Any, Dict

from graphrag.config.load_config import load_config as graphrag_load_config
from graphrag.config.resolve_path import resolve_paths as graphrag_resolve_paths

def load_config(config_path: Path) -> Dict[str, Any]:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration directory containing settings.yml
        
    Returns:
        Dict containing the configuration
    """
    return graphrag_load_config(config_path)

def resolve_paths(config: Dict[str, Any]) -> None:
    """
    Resolve all paths in the configuration relative to the base directory.
    
    Args:
        config: Configuration dictionary
    """
    graphrag_resolve_paths(config)
