import pytest
from fastapi import status
from graphrag.query.exceptions import GraphRAGError, ContextBuilderError

pytestmark = pytest.mark.asyncio

async def test_global_search_success(test_client):
    """Test successful global search."""
    response = test_client.post("/search/global", json={"query": "test query"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["response"] == "Test response"
    assert data["confidence_score"] == 0.95
    assert data["metadata"] == {"source": "test"}
    
    # Check context data
    context = data["context_data"]
    assert len(context["entities"]) == 1
    assert context["entities"][0]["id"] == "e1"
    assert len(context["relationships"]) == 1
    assert context["relationships"][0]["source_id"] == "e1"

async def test_global_search_error(test_client, mock_search_engines):
    """Test global search with GraphRAG error."""
    mock_search_engines[1].asearch.side_effect = GraphRAGError("Test error")
    
    response = test_client.post("/search/global", json={"query": "test query"})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    
    error = response.json()
    assert error["detail"]["message"] == "Test error"
    assert error["detail"]["code"] == "GRAPHRAG_ERROR"

async def test_local_search_success(test_client):
    """Test successful local search."""
    response = test_client.post("/search/local", json={"query": "test query"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    assert data["response"] == "Test response"
    assert data["confidence_score"] == 0.95
    assert data["metadata"] == {"source": "test"}
    
    # Check context data
    context = data["context_data"]
    assert len(context["entities"]) == 1
    assert context["entities"][0]["name"] == "Entity 1"
    assert len(context["relationships"]) == 1
    assert context["relationships"][0]["weight"] == 0.8

async def test_local_search_context_error(test_client, mock_search_engines):
    """Test local search with context builder error."""
    mock_search_engines[0].asearch.side_effect = ContextBuilderError("Context error")
    
    response = test_client.post("/search/local", json={"query": "test query"})
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    
    error = response.json()
    assert error["detail"]["message"] == "Context error"
    assert error["detail"]["code"] == "CONTEXTBUILDERERROR"

@pytest.mark.parametrize("endpoint", ["/search/global/stream", "/search/local/stream"])
async def test_streaming_search(test_client, endpoint):
    """Test streaming search endpoints."""
    with test_client.websocket_connect(f"{endpoint}?query=test") as websocket:
        # Receive streaming tokens
        data = websocket.receive_json()
        assert data["token"] == "Test"
        
        data = websocket.receive_json()
        assert data["token"] == "streaming"
        
        data = websocket.receive_json()
        assert data["token"] == "response"
        
        # Receive finish message
        data = websocket.receive_json()
        assert data["finish_reason"] == "stop"
        assert data["token"] == ""

@pytest.mark.parametrize("endpoint", ["/search/global/stream", "/search/local/stream"])
async def test_streaming_search_error(test_client, endpoint, mock_search_engines):
    """Test streaming search with errors."""
    # Configure error for streaming
    async def mock_stream_error(*args, **kwargs):
        raise GraphRAGError("Streaming error")
    
    if "global" in endpoint:
        mock_search_engines[1].astream = mock_stream_error
    else:
        mock_search_engines[0].astream = mock_stream_error
    
    with pytest.raises(GraphRAGError) as exc:
        with test_client.websocket_connect(f"{endpoint}?query=test"):
            pass
    
    assert str(exc.value) == "Streaming error"
