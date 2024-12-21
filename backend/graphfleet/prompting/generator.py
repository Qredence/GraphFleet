"""
Prompt generation functionality for GraphFleet.
"""

from typing import List, Optional, Dict, Any
from pathlib import Path
import yaml

from graphrag.prompting import PromptTemplate
from ..core.types import QueryType

class PromptGenerator:
    """
    Generate and manage prompts for different query types.
    
    Args:
        model: Model to use for prompt generation
        num_prompts: Number of prompts to generate
        temperature: Temperature for generation
        **kwargs: Additional configuration options
    """
    
    def __init__(
        self,
        model: str = "gpt-4",
        num_prompts: int = 5,
        temperature: float = 0.7,
        **kwargs
    ):
        self.model = model
        self.num_prompts = num_prompts
        self.temperature = temperature
        self.config = kwargs
        self._templates = {}
        
    async def generate_prompts(
        self,
        template_type: str = "standard",
        context_window: int = 5,
        **kwargs
    ) -> List[str]:
        """
        Generate prompts based on template and context.
        
        Args:
            template_type: Type of template to use
            context_window: Number of context chunks to consider
            **kwargs: Additional generation options
            
        Returns:
            List of generated prompts
        """
        template = self._get_template(template_type)
        prompts = await template.generate(
            num_prompts=self.num_prompts,
            context_window=context_window,
            temperature=self.temperature,
            model=self.model,
            **kwargs
        )
        return prompts
    
    def register_template(
        self,
        name: str,
        template: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a new prompt template.
        
        Args:
            name: Template name
            template: Template string
            metadata: Optional template metadata
        """
        self._templates[name] = PromptTemplate(
            template=template,
            metadata=metadata or {}
        )
    
    def load_templates(self, path: Path) -> None:
        """
        Load templates from a YAML file.
        
        Args:
            path: Path to templates file
        """
        with open(path) as f:
            templates = yaml.safe_load(f)
        
        for name, data in templates.items():
            self.register_template(
                name=name,
                template=data["template"],
                metadata=data.get("metadata")
            )
    
    def save_prompts(
        self,
        prompts: List[str],
        template_type: str,
        path: Path
    ) -> None:
        """
        Save generated prompts to a file.
        
        Args:
            prompts: List of prompts to save
            template_type: Type of template used
            path: Path to save file
        """
        data = {
            "template_type": template_type,
            "model": self.model,
            "temperature": self.temperature,
            "prompts": prompts
        }
        with open(path, "w") as f:
            yaml.dump(data, f)
    
    def _get_template(self, template_type: str) -> PromptTemplate:
        """Get a template by type."""
        if template_type not in self._templates:
            raise ValueError(f"Unknown template type: {template_type}")
        return self._templates[template_type]
