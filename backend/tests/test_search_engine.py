import pytest
from unittest.mock import patch, MagicMock
from graphrag.query.exceptions import GraphRAGError
from app.services.search_engine import create_search_engines
from app.config import Settings

@pytest.fixture
def mock_data():
    """Mock data for testing."""
    return {
        "nodes": MagicMock(),
        "community_reports": MagicMock(),
        "entities": MagicMock(),
        "relationships": MagicMock(),
        "text_units": MagicMock(),
    }

def test_create_search_engines_success(test_settings, mock_data):
    """Test successful creation of search engines."""
    with patch("pandas.read_parquet") as mock_read, \
         patch("app.utils.data_processing.read_indexer_entities") as mock_entities, \
         patch("app.utils.data_processing.read_indexer_reports") as mock_reports:
        
        # Configure mocks
        mock_read.return_value = mock_data["nodes"]
        mock_entities.return_value = mock_data["entities"]
        mock_reports.return_value = mock_data["reports"]
        
        # Create search engines
        local_search, global_search = create_search_engines()
        
        # Verify search engines were created
        assert local_search is not None
        assert global_search is not None
        
        # Verify data loading
        mock_read.assert_called()
        mock_entities.assert_called_once()
        mock_reports.assert_called_once()

def test_create_search_engines_missing_data(test_settings):
    """Test search engine creation with missing data."""
    with patch("pandas.read_parquet", side_effect=FileNotFoundError("Missing data")):
        with pytest.raises(GraphRAGError) as exc:
            create_search_engines()
        assert "Missing data" in str(exc.value)

@pytest.mark.parametrize("error_type", [
    ValueError("Invalid data format"),
    KeyError("Missing key"),
    Exception("Unknown error")
])
def test_create_search_engines_errors(test_settings, error_type):
    """Test search engine creation with various errors."""
    with patch("pandas.read_parquet", side_effect=error_type):
        with pytest.raises(GraphRAGError) as exc:
            create_search_engines()
        assert str(error_type) in str(exc.value)

def test_search_engine_configuration(test_settings, mock_data):
    """Test search engine configuration parameters."""
    with patch("pandas.read_parquet") as mock_read, \
         patch("app.utils.data_processing.read_indexer_entities") as mock_entities, \
         patch("app.utils.data_processing.read_indexer_reports") as mock_reports:
        
        # Configure mocks
        mock_read.return_value = mock_data["nodes"]
        mock_entities.return_value = mock_data["entities"]
        mock_reports.return_value = mock_data["reports"]
        
        # Create search engines
        local_search, global_search = create_search_engines()
        
        # Verify local search configuration
        assert local_search.llm_params["max_tokens"] == test_settings.llm.max_tokens
        assert local_search.llm_params["temperature"] == test_settings.llm.temperature
        assert local_search.llm_params["response_format"]["type"] == "text"
        
        # Verify global search configuration
        assert global_search.max_data_tokens == test_settings.llm.max_tokens
        assert global_search.map_llm_params["response_format"]["type"] == "json_object"
        assert global_search.reduce_llm_params["response_format"]["type"] == "text"
        assert global_search.concurrent_coroutines == test_settings.graphrag.max_concurrent_requests

@pytest.mark.asyncio
async def test_search_engine_responses(mock_search_engines):
    """Test search engine response formats."""
    local_search, global_search = mock_search_engines
    
    # Test local search
    local_result = await local_search.asearch("test query")
    assert local_result.response == "Test response"
    assert local_result.confidence_score == 0.95
    assert "entities" in local_result.context_data
    
    # Test global search
    global_result = await global_search.asearch("test query")
    assert global_result.response == "Test response"
    assert global_result.confidence_score == 0.95
    assert "entities" in global_result.context_data
    
    # Test streaming
    async for token in local_search.astream("test query"):
        if isinstance(token, dict):
            assert "finish_reason" in token
        else:
            assert isinstance(token, str)

@pytest.mark.asyncio
async def test_search_engine_streaming(mock_search_engines):
    """Test search engine streaming functionality."""
    local_search, global_search = mock_search_engines
    
    # Test local search streaming
    tokens = []
    async for token in local_search.astream("test query"):
        tokens.append(token)
    
    assert len(tokens) == 4  # "Test", "streaming", "response", and finish dict
    assert isinstance(tokens[-1], dict)
    assert tokens[-1]["finish_reason"] == "stop"
    
    # Test global search streaming
    tokens = []
    async for token in global_search.astream("test query"):
        tokens.append(token)
    
    assert len(tokens) == 4
    assert isinstance(tokens[-1], dict)
    assert tokens[-1]["finish_reason"] == "stop"

@pytest.mark.asyncio
async def test_search_engine_context_data(mock_search_engines):
    """Test search engine context data handling."""
    local_search, global_search = mock_search_engines
    
    # Test local search context data
    result = await local_search.asearch("test query")
    assert "entities" in result.context_data
    assert "relationships" in result.context_data
    assert len(result.context_data["entities"]) > 0
    assert isinstance(result.context_data["entities"][0], dict)
    assert "id" in result.context_data["entities"][0]
    
    # Test global search context data
    result = await global_search.asearch("test query")
    assert "entities" in result.context_data
    assert "relationships" in result.context_data
    assert len(result.context_data["entities"]) > 0
    assert isinstance(result.context_data["entities"][0], dict)
    assert "id" in result.context_data["entities"][0]

def test_search_engine_error_handling(mock_search_engines):
    """Test search engine error handling."""
    local_search, global_search = mock_search_engines
    
    # Test invalid query type
    with pytest.raises(ValueError):
        local_search.asearch(123)  # Non-string query
    
    # Test empty query
    with pytest.raises(ValueError):
        global_search.asearch("")
    
    # Test query too long
    long_query = "test " * 1000
    with pytest.raises(ValueError):
        local_search.asearch(long_query)

@pytest.mark.asyncio
async def test_search_engine_metadata(mock_search_engines):
    """Test search engine metadata handling."""
    local_search, global_search = mock_search_engines
    
    # Test local search metadata
    result = await local_search.asearch("test query")
    assert hasattr(result, "metadata")
    assert isinstance(result.metadata, dict)
    assert "source" in result.metadata
    
    # Test global search metadata
    result = await global_search.asearch("test query")
    assert hasattr(result, "metadata")
    assert isinstance(result.metadata, dict)
    assert "source" in result.metadata
