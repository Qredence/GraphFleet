import pytest
from unittest.mock import Mock, patch
from src.graphfleet.graphfleet import GraphFleet


@pytest.fixture
def mock_storage():
    return Mock()


@pytest.fixture
def graph_fleet(mock_storage):
    with patch('src.graphfleet.graphfleet.LocalStorage', return_value=mock_storage):
        return GraphFleet()


def test_query(graph_fleet):
    question = "What is GraphRAG?"
    mock_answer = "GraphRAG is a graph-based retrieval augmented generation system."
    graph_fleet.graph_rag.query = Mock(return_value=(mock_answer, 0.9))
    
    answer, confidence = graph_fleet.query(question)
    assert answer == mock_answer
    assert confidence == 0.9
    graph_fleet.graph_rag.query.assert_called_once_with(question, method="global")

def test_index_documents(graph_fleet, mock_storage):
    documents = [{"content": "Test document", "metadata": {"source": "test"}}]
    graph_fleet.index_documents(documents)
    mock_storage.store_document.assert_called_once_with(documents[0])

def test_search(graph_fleet, mock_storage):
    query = "test"
    mock_results = [{"content": "Test result", "metadata": {"source": "test"}}]
    mock_storage.search_documents.return_value = mock_results
    
    results = graph_fleet.search(query)
    assert results == mock_results
    mock_storage.search_documents.assert_called_once_with(query, limit=10, offset=0)

def test_web_enhanced_query(graph_fleet):
    question = "What is the capital of France?"
    mock_answer = "The capital of France is Paris."
    graph_fleet.web_search.run = Mock(return_value={"content": f"{mock_answer} Confidence: 0.95"})
    
    answer, confidence = graph_fleet.web_enhanced_query(question)
    assert answer == mock_answer
    assert confidence == 0.95

def test_monthy_scrape(graph_fleet):
    url = "https://example.com"
    mock_content = "Scraped content"
    graph_fleet.web_scraper.run = Mock(return_value={"content": mock_content})
    
    result = graph_fleet.monthy_scrape(url)
    assert result == mock_content
    graph_fleet.web_scraper.run.assert_called_once()

# Add more tests for other methods...