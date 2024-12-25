"""Prompt generation utilities for GraphFleet."""
from typing import Dict, List, Optional, Any, Tuple
from pathlib import Path
import json
import logging
from .auto_prompt_tuning import AutoPromptTuner, TuningConfig, TuningObjective

logger = logging.getLogger(__name__)

class PromptGenerator:
    """Generate prompts for different tasks."""
    
    def __init__(self, prompt_dir: str = "prompts"):
        self.prompt_dir = Path(prompt_dir)
        self._cache: Dict[str, str] = {}
        self.tuned_prompts_dir = self.prompt_dir / "tuned"
        self.tuned_prompts_dir.mkdir(parents=True, exist_ok=True)
        
    def _load_prompt(self, prompt_file: str) -> str:
        """Load a prompt template from file."""
        if prompt_file in self._cache:
            return self._cache[prompt_file]
            
        # Check for tuned version first
        tuned_path = self.tuned_prompts_dir / f"{prompt_file.replace('.txt', '_tuned.txt')}"
        if tuned_path.exists():
            prompt = tuned_path.read_text().strip()
            self._cache[prompt_file] = prompt
            return prompt
            
        # Fall back to base prompt
        prompt_path = self.prompt_dir / prompt_file
        if not prompt_path.exists():
            raise FileNotFoundError(f"Prompt file not found: {prompt_file}")
            
        prompt = prompt_path.read_text().strip()
        self._cache[prompt_file] = prompt
        return prompt
        
    def tune_prompts(
        self,
        task_type: str,
        validation_data: Optional[List[Dict[str, Any]]] = None,
        config: Optional[TuningConfig] = None
    ) -> Dict[str, Any]:
        """Tune prompts for a specific task type."""
        logger.info(f"Tuning prompts for task type: {task_type}")
        
        # Map task type to prompt files
        task_prompts = {
            "entity_extraction": ["entity_extraction.txt"],
            "local_search": ["local_search_system_prompt.txt"],
            "global_search": ["global_search_map_system_prompt.txt", "global_search_reduce_system_prompt.txt"],
            "summarization": ["summarize_descriptions.txt"],
            "drift_search": ["drift_search_system_prompt.txt"]
        }
        
        if task_type not in task_prompts:
            raise ValueError(f"Unknown task type: {task_type}")
            
        if validation_data is None:
            validation_data = self._load_validation_data(task_type)
            
        results = {}
        for prompt_file in task_prompts[task_type]:
            logger.info(f"Tuning prompt: {prompt_file}")
            
            # Load base prompt
            base_prompt = self._load_prompt(prompt_file)
            
            # Initialize tuner
            tuner = AutoPromptTuner(
                base_prompt=base_prompt,
                config=config,
                save_dir=self.tuned_prompts_dir
            )
            
            # Run tuning
            tuned_prompt, tuning_stats = tuner.tune(
                task_type=prompt_file.replace('.txt', ''),
                validation_data=validation_data
            )
            
            # Update cache with tuned prompt
            self._cache[prompt_file] = tuned_prompt
            
            results[prompt_file] = tuning_stats
            
        return results
        
    def _load_validation_data(self, task_type: str) -> List[Dict[str, Any]]:
        """Load validation data for a specific task type."""
        validation_path = self.prompt_dir / "validation" / f"{task_type}_validation.json"
        if not validation_path.exists():
            raise FileNotFoundError(
                f"Validation data not found for task type: {task_type}. "
                f"Expected at: {validation_path}"
            )
            
        with open(validation_path) as f:
            data: List[Dict[str, Any]] = json.load(f)
            return data
        
    def generate_local_search_prompt(
        self,
        query: str,
        context: Optional[Dict] = None
    ) -> str:
        """Generate prompt for local search."""
        template = self._load_prompt("local_search_system_prompt.txt")
        context = context or {}
        return template.format(query=query, **context)
        
    def generate_global_search_prompt(
        self,
        query: str,
        community_level: int = 1,
        context: Optional[Dict] = None
    ) -> str:
        """Generate prompt for global search."""
        template = self._load_prompt("global_search_map_system_prompt.txt")
        context = context or {}
        context.update({
            "community_level": community_level
        })
        return template.format(query=query, **context)
        
    def generate_drift_search_prompt(
        self,
        query: str,
        time_window: str,
        drift_threshold: float,
        context: Optional[Dict] = None
    ) -> str:
        """Generate prompt for drift search."""
        template = self._load_prompt("drift_search_system_prompt.txt")
        context = context or {}
        context.update({
            "time_window": time_window,
            "drift_threshold": drift_threshold
        })
        return template.format(query=query, **context)
        
    def generate_entity_extraction_prompt(
        self,
        text: str,
        entity_types: List[str],
        context: Optional[Dict] = None
    ) -> str:
        """Generate prompt for entity extraction."""
        template = self._load_prompt("entity_extraction.txt")
        context = context or {}
        context.update({
            "entity_types": ", ".join(entity_types)
        })
        return template.format(text=text, **context)
        
    def generate_summarization_prompt(
        self,
        text: str,
        max_length: int = 500,
        context: Optional[Dict] = None
    ) -> str:
        """Generate prompt for text summarization."""
        template = self._load_prompt("summarize_descriptions.txt")
        context = context or {}
        context.update({
            "max_length": max_length
        })
        return template.format(text=text, **context)
        
    def clear_cache(self) -> None:
        """Clear the prompt template cache."""
        self._cache.clear() 