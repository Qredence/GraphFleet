"""
Query optimization functionality for GraphFleet.
"""

from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass

from graphrag.querying import QueryOptimization
from ..core.types import QueryConfig, QueryResult

@dataclass
class OptimizationResult:
    """Optimization result with parameters and scores."""
    parameters: Dict[str, Any]
    score: float
    metrics: Dict[str, float]

class QueryOptimizer:
    """
    Optimize query parameters for better results.
    
    Args:
        evaluation_model: Model to use for evaluation
        num_trials: Number of optimization trials
        **kwargs: Additional optimization options
    """
    
    def __init__(
        self,
        evaluation_model: str = "gpt-4",
        num_trials: int = 5,
        **kwargs
    ):
        self.evaluation_model = evaluation_model
        self.num_trials = num_trials
        self.config = kwargs
        self._optimizer = QueryOptimization()
    
    async def optimize(
        self,
        query: str,
        param_space: Dict[str, Tuple[float, float]],
        initial_config: Optional[QueryConfig] = None,
        **kwargs
    ) -> OptimizationResult:
        """
        Optimize query parameters.
        
        Args:
            query: Query to optimize for
            param_space: Parameter space to search
            initial_config: Initial configuration
            **kwargs: Additional optimization options
            
        Returns:
            Optimization result
        """
        config = initial_config or QueryConfig()
        
        result = await self._optimizer.optimize(
            query=query,
            param_space=param_space,
            initial_params=config.dict(),
            num_trials=self.num_trials,
            evaluation_model=self.evaluation_model,
            **kwargs
        )
        
        return OptimizationResult(
            parameters=result["best_params"],
            score=result["best_score"],
            metrics=result["metrics"]
        )
    
    def evaluate_query(
        self,
        query: str,
        result: QueryResult,
        metrics: Optional[Dict[str, Any]] = None
    ) -> Dict[str, float]:
        """
        Evaluate a query result.
        
        Args:
            query: Original query
            result: Query result to evaluate
            metrics: Metrics to evaluate
            
        Returns:
            Evaluation scores
        """
        metrics = metrics or {
            "relevance": True,
            "coherence": True,
            "conciseness": True
        }
        
        scores = self._optimizer.evaluate(
            query=query,
            result=result.dict(),
            metrics=metrics,
            model=self.evaluation_model
        )
        
        return scores
    
    def suggest_improvements(
        self,
        query: str,
        result: QueryResult,
        scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Suggest improvements based on evaluation.
        
        Args:
            query: Original query
            result: Query result
            scores: Evaluation scores
            
        Returns:
            Improvement suggestions
        """
        suggestions = self._optimizer.suggest_improvements(
            query=query,
            result=result.dict(),
            scores=scores,
            model=self.evaluation_model
        )
        
        return suggestions
