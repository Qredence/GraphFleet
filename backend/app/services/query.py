from typing import List, Dict, Any, Optional
import asyncio
import logging
from pathlib import Path

from app.core.config import Settings
from app.services.llm import LLMService
from app.services.graph import GraphService
from app.services.prompt_tune import PromptTuneService
from app.schemas.search import SearchQuery, SearchResult
from app.utils.data_processing import format_query_result

logger = logging.getLogger(__name__)

class QueryService:
    def __init__(
        self,
        settings: Settings,
        llm_service: LLMService,
        graph_service: GraphService,
        prompt_tune_service: PromptTuneService,
    ):
        self.settings = settings
        self.llm = llm_service
        self.graph = graph_service
        self.prompt_tune = prompt_tune_service

    async def execute_query(
        self,
        query: str,
        method: str = "global",
        streaming: bool = False,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> SearchResult:
        """Execute a query using the specified method."""
        # Load tuned prompts
        prompts = await self.prompt_tune.load_prompts()
        
        # Get relevant subgraph based on query
        subgraph = await self.graph.get_relevant_subgraph(query, method)
        
        # Get community hierarchy if using global method
        if method == "global":
            communities = await self.graph.get_community_hierarchy(subgraph)
            context = await self._prepare_global_context(query, subgraph, communities)
        else:
            context = await self._prepare_local_context(query, subgraph)
        
        # Generate response using LLM
        response = await self.llm.generate_completion(
            prompt=self._format_query_prompt(query, context, prompts["query"]),
            max_tokens=max_tokens or self.settings.openai_max_tokens,
            temperature=temperature or self.settings.openai_temperature,
        )
        
        # Format and return result
        return format_query_result(
            query=query,
            response=response,
            context=context,
            method=method,
        )

    async def _prepare_global_context(
        self,
        query: str,
        subgraph: Dict[str, Any],
        communities: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Prepare context for global query method."""
        # Get community summaries
        summary_tasks = [
            self._summarize_community(community, subgraph)
            for community in communities
        ]
        summaries = await asyncio.gather(*summary_tasks)
        
        return {
            "query": query,
            "subgraph": subgraph,
            "communities": communities,
            "summaries": summaries,
        }

    async def _prepare_local_context(
        self,
        query: str,
        subgraph: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Prepare context for local query method."""
        return {
            "query": query,
            "subgraph": subgraph,
            "local_summary": await self._summarize_subgraph(subgraph),
        }

    async def _summarize_community(
        self,
        community: Dict[str, Any],
        subgraph: Dict[str, Any],
    ) -> str:
        """Summarize a community using the LLM."""
        prompts = await self.prompt_tune.load_prompts()
        system_prompt = prompts["summarize"]
        
        user_prompt = (
            f"Please summarize the following community of nodes:\n"
            f"{community}\n\n"
            f"Context from subgraph:\n{subgraph}"
        )
        
        return await self.llm.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=200,
        )

    async def _summarize_subgraph(self, subgraph: Dict[str, Any]) -> str:
        """Summarize a subgraph using the LLM."""
        prompts = await self.prompt_tune.load_prompts()
        system_prompt = prompts["summarize"]
        
        user_prompt = f"Please summarize the following subgraph:\n{subgraph}"
        
        return await self.llm.generate_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            max_tokens=200,
        )

    def _format_query_prompt(
        self,
        query: str,
        context: Dict[str, Any],
        base_prompt: str,
    ) -> str:
        """Format the query prompt with context."""
        if "communities" in context:
            # Global query format
            community_info = "\n".join(
                f"Community {i+1}:\n{summary}"
                for i, summary in enumerate(context["summaries"])
            )
            return (
                f"{base_prompt}\n\n"
                f"Query: {query}\n\n"
                f"Graph Context:\n{community_info}\n\n"
                "Please provide a comprehensive answer based on the graph structure and community information."
            )
        else:
            # Local query format
            return (
                f"{base_prompt}\n\n"
                f"Query: {query}\n\n"
                f"Local Context:\n{context['local_summary']}\n\n"
                "Please provide a focused answer based on the local graph structure."
            )
