from typing import List, Optional, Dict, Any
import asyncio
import logging
from pathlib import Path

from app.core.config import Settings
from app.services.llm import LLMService
from app.services.graph import GraphService
from app.utils.data_processing import load_yaml, save_yaml

logger = logging.getLogger(__name__)

class PromptTuneService:
    def __init__(
        self,
        settings: Settings,
        llm_service: LLMService,
        graph_service: GraphService,
    ):
        self.settings = settings
        self.llm = llm_service
        self.graph = graph_service
        self.prompts_dir = Path(settings.PROMPTS_DIR)
        self.prompts_dir.mkdir(parents=True, exist_ok=True)

    async def tune_prompts(
        self,
        root_dir: Path,
        config: Dict[str, Any],
        no_entity_types: bool = False,
        output_dir: Optional[Path] = None,
    ) -> Dict[str, str]:
        """Tune prompts for different components of the system."""
        output_dir = output_dir or self.prompts_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        # Load base prompts
        base_prompts = load_yaml(root_dir / "prompts" / "base_prompts.yaml")
        
        # Initialize tuned prompts with base prompts
        tuned_prompts = base_prompts.copy()

        # Get graph statistics
        graph_stats = await self.graph.get_statistics()
        
        # Tune each prompt type
        tasks = [
            self._tune_prompt("query", base_prompts["query"], graph_stats, no_entity_types),
            self._tune_prompt("summarize", base_prompts["summarize"], graph_stats, no_entity_types),
            self._tune_prompt("extract", base_prompts["extract"], graph_stats, no_entity_types),
        ]
        
        results = await asyncio.gather(*tasks)
        
        # Update tuned prompts with results
        for prompt_type, tuned_prompt in zip(["query", "summarize", "extract"], results):
            tuned_prompts[prompt_type] = tuned_prompt

        # Save tuned prompts
        save_yaml(output_dir / "tuned_prompts.yaml", tuned_prompts)
        
        return tuned_prompts

    async def _tune_prompt(
        self,
        prompt_type: str,
        base_prompt: str,
        graph_stats: Dict[str, Any],
        no_entity_types: bool,
    ) -> str:
        """Tune a specific prompt type using the LLM."""
        # Create context for prompt tuning
        context = {
            "prompt_type": prompt_type,
            "graph_stats": graph_stats,
            "no_entity_types": no_entity_types,
        }
        
        # Get tuned prompt from LLM
        response = await self.llm.generate_completion(
            prompt=(
                f"Please optimize this {prompt_type} prompt for a graph with the following statistics:\n"
                f"{graph_stats}\n\n"
                f"Base prompt:\n{base_prompt}\n\n"
                f"Requirements:\n"
                f"- {'Ignore entity types' if no_entity_types else 'Consider entity types'}\n"
                f"- Maintain clarity and specificity\n"
                f"- Ensure consistency with graph structure"
            ),
            temperature=0.7,
            max_tokens=1000,
        )
        
        return response.strip()

    async def load_prompts(self) -> Dict[str, str]:
        """Load tuned prompts from file."""
        prompts_file = self.prompts_dir / "tuned_prompts.yaml"
        if not prompts_file.exists():
            # If tuned prompts don't exist, load and return base prompts
            return load_yaml(self.prompts_dir / "base_prompts.yaml")
        return load_yaml(prompts_file)
