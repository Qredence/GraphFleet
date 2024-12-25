"""Auto prompt tuning functionality for GraphFleet."""
from typing import Dict, List, Optional, Any, Tuple, cast, Callable
import json
import numpy as np
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum
import os
from openai import AzureOpenAI
from numpy.typing import NDArray

logger = logging.getLogger(__name__)

class TuningObjective(Enum):
    ACCURACY = "accuracy"
    DIVERSITY = "diversity"
    EFFICIENCY = "efficiency"

@dataclass
class TuningConfig:
    """Configuration for auto prompt tuning."""
    num_iterations: int = 10
    population_size: int = 5
    mutation_rate: float = 0.1
    crossover_rate: float = 0.8
    objective: TuningObjective = TuningObjective.ACCURACY
    
    # Validation parameters
    validation_size: int = 100
    validation_metric: str = "f1"
    
    # Early stopping
    patience: int = 3
    min_delta: float = 0.01
    
    # LLM parameters
    temperature: float = 0.7
    max_tokens: int = 1000
    top_p: float = 0.95

class AutoPromptTuner:
    """Implements GraphRAG's auto prompt tuning."""
    
    def __init__(
        self,
        base_prompt: str,
        config: Optional[TuningConfig] = None,
        save_dir: Optional[Path] = None
    ):
        self.base_prompt = base_prompt
        self.config = config or TuningConfig()
        self.save_dir = Path(save_dir) if save_dir else Path("prompts/tuned")
        self.save_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize Azure OpenAI client
        self.client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", "")
        )
        
    def _generate_prompt_variants(self, prompt: str, n: int = 5) -> List[str]:
        """Generate variations of a prompt using controlled perturbation."""
        variants = []
        for _ in range(n):
            # Apply random transformations
            variant = self._apply_transformations(prompt)
            variants.append(variant)
        return variants
        
    def _apply_transformations(self, prompt: str) -> str:
        """Apply random transformations to a prompt."""
        transformations: List[Callable[[str], str]] = [
            self._add_examples,
            self._modify_instructions,
            self._adjust_formatting,
            self._add_constraints
        ]
        
        # Randomly select and apply transformations
        num_transforms = int(np.random.randint(1, len(transformations) + 1))
        selected_transforms = cast(
            NDArray[np.object_],
            np.random.choice(transformations, size=num_transforms, replace=False)
        )
        
        result = prompt
        for transform in selected_transforms:
            result = cast(str, transform(result))
        return result
        
    def _add_examples(self, prompt: str) -> str:
        """Add few-shot examples to the prompt."""
        examples = [
            {
                "input": "Microsoft announced Windows 12 at their annual developer conference.",
                "output": {
                    "entities": [
                        {"text": "Microsoft", "type": "organization", "start": 0, "end": 9},
                        {"text": "Windows 12", "type": "product", "start": 20, "end": 30},
                        {"text": "annual developer conference", "type": "event", "start": 39, "end": 64}
                    ]
                }
            }
        ]
        
        # Add example before the main task
        example = examples[int(np.random.randint(len(examples)))]
        example_text = f"\nExample:\nInput: {example['input']}\nOutput: {json.dumps(example['output'], indent=2)}\n"
        
        # Insert before the final task
        parts = prompt.split("Now extract entities from this text:")
        return parts[0] + example_text + "\nNow extract entities from this text:" + parts[1]
        
    def _modify_instructions(self, prompt: str) -> str:
        """Modify the instruction part of the prompt."""
        modifications = [
            "Remember to be precise with character positions.",
            "Ensure all entity spans are exact matches from the text.",
            "Pay attention to nested entities and overlapping spans.",
            "Consider context when determining entity types."
        ]
        
        # Add a random modification
        modification = modifications[int(np.random.randint(len(modifications)))]
        
        # Insert after the initial instructions
        lines = prompt.split("\n")
        insert_idx = next(i for i, line in enumerate(lines) if line.strip() == "")
        lines.insert(insert_idx, modification)
        return "\n".join(lines)
        
    def _adjust_formatting(self, prompt: str) -> str:
        """Adjust the formatting of the prompt."""
        formatting_options: List[Callable[[str], str]] = [
            lambda p: p.replace("Example", "EXAMPLE"),
            lambda p: p.replace("Now extract", "TASK: Extract"),
            lambda p: p.replace("Format your response", "OUTPUT FORMAT")
        ]
        
        # Apply random formatting
        formatter = formatting_options[int(np.random.randint(len(formatting_options)))]
        return formatter(prompt)
        
    def _add_constraints(self, prompt: str) -> str:
        """Add additional constraints to the prompt."""
        constraints = [
            "- Do not include partial words or incomplete entities",
            "- Maintain case sensitivity in entity text",
            "- Include articles (a, an, the) only if they're part of proper nouns",
            "- Exclude punctuation from entity spans unless it's part of the entity"
        ]
        
        # Add 1-2 random constraints
        num_constraints = int(np.random.randint(1, 3))
        selected = cast(
            NDArray[np.str_],
            np.random.choice(constraints, size=num_constraints, replace=False)
        )
        
        # Add after format specifications
        lines = prompt.split("\n")
        format_end = next(i for i, line in enumerate(lines) if "}" in line)
        for constraint in selected:
            lines.insert(format_end + 1, str(constraint))
        return "\n".join(lines)
        
    def _generate_completion(self, prompt: str, input_text: str) -> str:
        """Generate completion using the LLM."""
        try:
            response = self.client.chat.completions.create(
                model=os.getenv("AZURE_OPENAI_MODEL", "gpt-4"),
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": input_text}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p
            )
            return str(response.choices[0].message.content or "")
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            return ""
        
    def _calculate_metrics(
        self,
        completion: str,
        expected: str,
        metric: str = "f1"
    ) -> float:
        """Calculate evaluation metrics."""
        try:
            # Parse completion and expected outputs
            completion_data = json.loads(completion)
            expected_data = json.loads(expected)
            
            # Extract entities
            pred_entities = set(
                (e["text"], e["type"], e["start"], e["end"])
                for e in completion_data["entities"]
            )
            true_entities = set(
                (e["text"], e["type"], e["start"], e["end"])
                for e in expected_data["entities"]
            )
            
            # Calculate metrics
            if metric == "f1":
                if not pred_entities and not true_entities:
                    return 1.0
                if not pred_entities or not true_entities:
                    return 0.0
                    
                tp = len(pred_entities & true_entities)
                fp = len(pred_entities - true_entities)
                fn = len(true_entities - pred_entities)
                
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                
                return 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
                
            elif metric == "accuracy":
                total = len(true_entities)
                if total == 0:
                    return 1.0 if not pred_entities else 0.0
                return len(pred_entities & true_entities) / total
                
            else:
                raise ValueError(f"Unsupported metric: {metric}")
                
        except Exception as e:
            logger.error(f"Error calculating metrics: {str(e)}")
            return 0.0
            
    def _evaluate_prompt(
        self,
        prompt: str,
        validation_data: List[Dict[str, Any]]
    ) -> float:
        """Evaluate a prompt variant using validation data."""
        scores = []
        for example in validation_data:
            # Generate completion using the prompt
            completion = self._generate_completion(prompt, example["input"])
            
            # Calculate metrics
            score = self._calculate_metrics(
                completion,
                json.dumps(example["expected"]),
                self.config.validation_metric
            )
            scores.append(score)
            
        return float(np.mean(scores))
        
    def tune(
        self,
        task_type: str,
        validation_data: List[Dict[str, Any]]
    ) -> Tuple[str, Dict[str, Any]]:
        """Run the auto prompt tuning process."""
        logger.info(f"Starting auto prompt tuning for task: {task_type}")
        
        best_prompt = self.base_prompt
        best_score = float('-inf')
        no_improvement = 0
        history = []
        
        for iteration in range(self.config.num_iterations):
            logger.info(f"Iteration {iteration + 1}/{self.config.num_iterations}")
            
            # Generate prompt variants
            variants = self._generate_prompt_variants(
                best_prompt,
                n=self.config.population_size
            )
            
            # Evaluate variants
            scores = []
            for variant in variants:
                score = self._evaluate_prompt(variant, validation_data)
                scores.append(score)
                
            # Update best prompt
            max_score = max(scores)
            if max_score > best_score + float(self.config.min_delta):
                best_score = max_score
                best_prompt = variants[scores.index(max_score)]
                no_improvement = 0
            else:
                no_improvement += 1
                
            # Record history
            history.append({
                "iteration": iteration,
                "best_score": best_score,
                "mean_score": float(np.mean(scores)),
                "std_score": float(np.std(scores))
            })
            
            # Early stopping
            if no_improvement >= self.config.patience:
                logger.info("Early stopping triggered")
                break
                
        # Save tuned prompt
        self._save_tuned_prompt(task_type, best_prompt, history)
        
        return best_prompt, {
            "task_type": task_type,
            "final_score": best_score,
            "history": history
        }
        
    def _save_tuned_prompt(
        self,
        task_type: str,
        prompt: str,
        history: List[Dict[str, Any]]
    ) -> None:
        """Save the tuned prompt and tuning history."""
        # Save prompt
        prompt_path = self.save_dir / f"{task_type}_tuned.txt"
        prompt_path.write_text(prompt)
        
        # Save history
        history_path = self.save_dir / f"{task_type}_history.json"
        with open(history_path, 'w') as f:
            json.dump(history, f, indent=2)
            
        logger.info(f"Saved tuned prompt to {prompt_path}") 