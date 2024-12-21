import os
import pytest
from fastapi.testclient import TestClient
import pandas as pd
from unittest.mock import MagicMock, patch
from graphrag.query.llm.oai.chat_openai import ChatOpenAI
from graphrag.query.structured_search.local_search.search import LocalSearch
from graphrag.query.structured_search.global_search.search import GlobalSearch

from app.main import create_app
from app.config import Settings

@pytest.fixture
def test_settings():
    """Test settings with mock values."""
    return Settings(
        llm={"api_key": "test-key", "model": "test-model"},
        embedding={"model": "test-embedding-model"},
        graphrag={
            "input_dir": "tests/fixtures/data",
            "community_level": 2,
            "max_concurrent_requests": 1
        }
    )

@pytest.fixture
def mock_llm():
    """Mock LLM for testing."""
    llm = MagicMock(spec=ChatOpenAI)
    llm.asearch.return_value = MagicMock(
        response="Test response",
        context_data={
            "entities": [
                {
                    "id": "e1",
                    "name": "Entity 1",
                    "type": "test",
                    "community_id": "c1",
                    "rank": 0.9
                }
            ],
            "relationships": [
                {
                    "source_id": "e1",
                    "target_id": "e2",
                    "type": "related_to",
                    "weight": 0.8
                }
            ],
            "text_units": [],
            "community_reports": [],
            "claims": []
        },
        confidence_score=0.95,
        metadata={"source": "test"}
    )
    return llm

@pytest.fixture
def mock_search_engines(mock_llm):
    """Mock search engines for testing."""
    local_search = MagicMock(spec=LocalSearch)
    global_search = MagicMock(spec=GlobalSearch)
    
    # Configure mock responses
    local_search.asearch.return_value = mock_llm.asearch.return_value
    global_search.asearch.return_value = mock_llm.asearch.return_value
    
    # Configure streaming responses
    async def mock_stream(*args, **kwargs):
        yield "Test"
        yield "streaming"
        yield "response"
        yield {"finish_reason": "stop"}
    
    local_search.astream = mock_stream
    global_search.astream = mock_stream
    
    return local_search, global_search

@pytest.fixture
def test_app(test_settings, mock_search_engines):
    """Test FastAPI application."""
    with patch("app.services.search_engine.local_search_engine", mock_search_engines[0]), \
         patch("app.services.search_engine.global_search_engine", mock_search_engines[1]):
        app = create_app(test_settings)
        yield app

@pytest.fixture
def test_client(test_app):
    """Test client for making requests."""
    return TestClient(test_app)

@pytest.fixture
def sample_data():
    """Sample test data."""
    return {
        "entities": pd.DataFrame({
            "id": ["e1", "e2"],
            "name": ["Entity 1", "Entity 2"],
            "type": ["test", "test"],
            "community_id": ["c1", "c1"],
            "rank": [0.9, 0.8]
        }),
        "relationships": pd.DataFrame({
            "source_id": ["e1"],
            "target_id": ["e2"],
            "type": ["related_to"],
            "weight": [0.8]
        })
    }
