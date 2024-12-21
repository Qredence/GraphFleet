from typing import Any, Dict, AsyncGenerator
from graphrag.llm.exceptions import GraphRAGError
from graphrag.query.structured_search.local_search.search import LocalSearch
from graphrag.query.structured_search.global_search.search import GlobalSearch

from app.core.config import Settings
from app.schemas.search import SearchResult, ContextData, EntityInfo, RelationshipInfo


class SearchService:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.local_search = self._create_local_search()
        self.global_search = self._create_global_search()

    def _create_local_search(self) -> LocalSearch:
        return LocalSearch(
            llm_params={
                "model": self.settings.OPENAI_MODEL,
                "max_tokens": self.settings.OPENAI_MAX_TOKENS,
                "temperature": self.settings.OPENAI_TEMPERATURE,
                "response_format": {"type": "text"},
            }
        )

    def _create_global_search(self) -> GlobalSearch:
        return GlobalSearch(
            max_data_tokens=self.settings.OPENAI_MAX_TOKENS,
            concurrent_coroutines=self.settings.GRAPHRAG_MAX_CONCURRENT_REQUESTS,
            map_llm_params={
                "model": self.settings.OPENAI_MODEL,
                "response_format": {"type": "json_object"},
            },
            reduce_llm_params={
                "model": self.settings.OPENAI_MODEL,
                "response_format": {"type": "text"},
            },
        )

    def _format_context_data(self, raw_context: Dict[str, Any]) -> ContextData:
        """Format raw context data into structured ContextData model."""
        return ContextData(
            entities=[
                EntityInfo(
                    id=entity["id"],
                    name=entity["name"],
                    type=entity["type"],
                    community_id=entity.get("community_id"),
                    rank=entity.get("rank"),
                )
                for entity in raw_context.get("entities", [])
            ],
            relationships=[
                RelationshipInfo(
                    source_id=rel["source_id"],
                    target_id=rel["target_id"],
                    type=rel["type"],
                    weight=rel.get("weight"),
                )
                for rel in raw_context.get("relationships", [])
            ],
            text_units=raw_context.get("text_units", []),
            community_reports=raw_context.get("community_reports", []),
            claims=raw_context.get("claims", []),
        )

    async def search(self, query: str) -> SearchResult:
        """Perform a search query using GraphRAG."""
        try:
            result = await self.global_search.asearch(query)
            return SearchResult(
                response=result.response,
                context_data=self._format_context_data(result.context_data),
                confidence_score=result.confidence_score,
                metadata=result.metadata,
            )
        except Exception as e:
            raise GraphRAGError(f"Search failed: {str(e)}")

    async def search_stream(self, query: str) -> AsyncGenerator[Dict[str, Any], None]:
        """Perform a streaming search query using GraphRAG."""
        try:
            async for token in self.global_search.astream(query):
                if isinstance(token, dict):
                    yield {"type": "finish", "data": token}
                else:
                    yield {"type": "token", "data": token}
        except Exception as e:
            raise GraphRAGError(f"Streaming search failed: {str(e)}")
