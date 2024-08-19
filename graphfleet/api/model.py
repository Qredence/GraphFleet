from pydantic import BaseModel, Field
from typing import List, Optional

class UploadFilesRequest(BaseModel):
    """No request body needed, files are sent in FormData"""
    pass

class BuildIndexRequest(BaseModel):
    """Request body for building a GraphRAG index."""
    storage_name: str = Field(..., description="Name of the data storage (e.g., directory name within 'data/').")
    index_name: str = Field(..., description="Unique name for the index.")
    entity_extraction_prompt_filepath: Optional[str] = Field(
        None, description="Optional path to a custom entity extraction prompt file."
    )
    community_prompt_filepath: Optional[str] = Field(
        None, description="Optional path to a custom community prompt file."
    )
    summarize_description_prompt_filepath: Optional[str] = Field(
        None, description="Optional path to a custom description summarization prompt file."
    )


class QueryRequest(BaseModel):
    """Request body for search queries."""
    index_name: str = Field(..., description="Name of the index to search.")
    query: str = Field(..., description="The search query.")


class SourceRequest(BaseModel):
    """Request body (if any) for retrieving a specific source."""
    index_name: str = Field(..., description="Name of the index.")
    source_id: str = Field(..., description="ID of the source to retrieve.")
    # You might need to adjust the type of 'source_id' (e.g., int) 
    # depending on how 'graphrag' structures source IDs.
