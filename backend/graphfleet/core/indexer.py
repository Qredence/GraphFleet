"""Core indexing functionality for GraphFleet."""
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
import yaml
import json
from typing_extensions import TypedDict

from ..utils.chunker import chunk_text
from ..utils.prompt_generator import PromptGenerator
from ..utils.auto_prompt_tuning import AutoPromptTuner

logger = logging.getLogger(__name__)

class IndexConfig(TypedDict):
    """Configuration for indexing."""
    chunk_size: int
    chunk_overlap: int
    chunk_strategy: str

class GraphIndexer:
    """Implements GraphRAG's indexing pipeline."""
    
    def __init__(
        self,
        input_dir: Path,
        output_dir: Path,
        config_path: Optional[str] = None
    ):
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.config = self._load_config(config_path)
        self.prompt_generator = PromptGenerator()
        
    def _load_config(self, config_path: Optional[str]) -> Dict[str, IndexConfig]:
        """Load configuration from file or use defaults."""
        if config_path:
            with open(config_path) as f:
                config = yaml.safe_load(f)
                if not isinstance(config, dict) or "indexing" not in config:
                    raise ValueError("Invalid config format: missing 'indexing' section")
                return config
                
        return {
            "indexing": IndexConfig(
                chunk_size=1000,
                chunk_overlap=200,
                chunk_strategy="sentence"
            )
        }
        
    def _create_validation_data(self, sample_chunks: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Create validation data from sample chunks for prompt tuning."""
        validation_data: Dict[str, List[Dict[str, Any]]] = {}
        
        # Create tuner for base prompts
        entity_tuner = AutoPromptTuner(
            base_prompt=self.prompt_generator._load_prompt("entity_extraction.txt")
        )
        global_tuner = AutoPromptTuner(
            base_prompt=self.prompt_generator._load_prompt("global_search_map_system_prompt.txt")
        )
        
        # Entity extraction validation data
        entity_samples = []
        for chunk in sample_chunks[:3]:  # Use first 3 chunks
            # Generate completion using base prompt
            completion = entity_tuner._generate_completion(
                entity_tuner.base_prompt,
                chunk
            )
            if completion:
                try:
                    entity_samples.append({
                        "input": chunk,
                        "expected": json.loads(completion)
                    })
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in entity extraction completion: {completion}")
                    continue
                    
        validation_data["entity_extraction"] = entity_samples
        
        # Global search validation data
        global_samples = []
        for chunk in sample_chunks[:3]:  # Use first 3 chunks
            # Generate completion using base prompt
            completion = global_tuner._generate_completion(
                global_tuner.base_prompt,
                "Summarize the key points from this text."
            )
            if completion:
                try:
                    global_samples.append({
                        "input": "Summarize the key points from this text.",
                        "expected": json.loads(completion)
                    })
                except json.JSONDecodeError:
                    logger.warning(f"Invalid JSON in global search completion: {completion}")
                    continue
                    
        validation_data["global_search"] = global_samples
        
        return validation_data
        
    def _tune_prompts_for_content(self) -> None:
        """Dynamically tune prompts based on input content."""
        logger.info("Starting dynamic prompt tuning")
        
        # Collect sample chunks from input files
        sample_chunks: List[str] = []
        unique_content: Set[str] = set()
        
        for doc_path in self.input_dir.glob("**/*.*"):
            if not doc_path.is_file():
                continue
                
            # Read document
            text = doc_path.read_text()
            
            # Chunk text
            chunks = chunk_text(
                text=text,
                chunk_size=self.config["indexing"]["chunk_size"],
                overlap=self.config["indexing"]["chunk_overlap"],
                chunk_strategy=self.config["indexing"]["chunk_strategy"]
            )
            
            # Add unique chunks to samples
            for chunk in chunks:
                # Use a content hash to avoid duplicates
                content_hash = str(hash(chunk.strip()))
                if content_hash not in unique_content and len(sample_chunks) < 10:
                    sample_chunks.append(chunk)
                    unique_content.add(content_hash)
                    
            if len(sample_chunks) >= 10:
                break
                
        if not sample_chunks:
            logger.warning("No content found for prompt tuning")
            return
            
        # Create validation data from samples
        validation_data = self._create_validation_data(sample_chunks)
        
        # Tune prompts for each task type
        for task_type, task_validation_data in validation_data.items():
            if task_validation_data:
                logger.info(f"Tuning prompts for {task_type}")
                try:
                    self.prompt_generator.tune_prompts(
                        task_type=task_type,
                        validation_data=task_validation_data
                    )
                except Exception as e:
                    logger.error(f"Error tuning prompts for {task_type}: {str(e)}")
        
    def _process_document(self, doc_path: Path) -> List[Dict[str, Any]]:
        """Process a single document into chunks with metadata."""
        logger.info(f"Processing document: {doc_path}")
        
        # Read document
        text = doc_path.read_text()
        
        # Chunk text
        chunks = chunk_text(
            text=text,
            chunk_size=self.config["indexing"]["chunk_size"],
            overlap=self.config["indexing"]["chunk_overlap"],
            chunk_strategy=self.config["indexing"]["chunk_strategy"]
        )
        
        # Process chunks
        processed_chunks = []
        for i, chunk in enumerate(chunks):
            # Extract entities
            entities = self._extract_entities(chunk)
            
            # Extract relationships
            relationships = self._extract_relationships(chunk, entities)
            
            # Create chunk metadata
            chunk_data = {
                "text": chunk,
                "metadata": {
                    "source": str(doc_path),
                    "chunk_id": i,
                    "total_chunks": len(chunks)
                },
                "entities": entities,
                "relationships": relationships
            }
            processed_chunks.append(chunk_data)
            
        return processed_chunks
        
    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract entities from text using LLM."""
        prompt = self.prompt_generator.generate_entity_extraction_prompt(
            text=text,
            entity_types=["person", "organization", "location", "concept", "date"]
        )
        # TODO: Implement LLM call
        return []
        
    def _extract_relationships(
        self,
        text: str,
        entities: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Extract relationships between entities."""
        # TODO: Implement relationship extraction
        return []
        
    def _build_knowledge_graph(self, chunks: List[Dict[str, Any]]) -> None:
        """Build knowledge graph from processed chunks."""
        # TODO: Implement graph construction
        pass
        
    def _create_community_summaries(self) -> None:
        """Create summaries for graph communities."""
        # TODO: Implement community detection and summarization
        pass
        
    def run_pipeline(self) -> None:
        """Run the complete indexing pipeline."""
        logger.info("Starting indexing pipeline")
        
        # Dynamic prompt tuning based on input content
        self._tune_prompts_for_content()
        
        # Process all documents
        all_chunks = []
        for doc_path in self.input_dir.glob("**/*.*"):
            if doc_path.is_file():
                chunks = self._process_document(doc_path)
                all_chunks.extend(chunks)
                
        # Build knowledge graph
        logger.info("Building knowledge graph")
        self._build_knowledge_graph(all_chunks)
        
        # Create community summaries
        logger.info("Creating community summaries")
        self._create_community_summaries()
        
        # Save index
        logger.info("Saving index")
        self._save_index()
        
        logger.info("Indexing pipeline complete")
        
    def _save_index(self) -> None:
        """Save the index to disk."""
        # TODO: Implement index saving
        pass 