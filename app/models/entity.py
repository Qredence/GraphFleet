from pydantic import BaseModel
from typing import Optional

class Entity(BaseModel):
    id: str
    title: str
    type: str
    description: Optional[str]
    source_id: str
    degree: int
    human_readable_id: str
    community: Optional[int]
    size: Optional[float]
    entity_type: Optional[str]
    top_level_node_id: str
    x: Optional[float]
    y: Optional[float]