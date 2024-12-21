import asyncio
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
import pandas as pd
from dotenv import load_dotenv

from app.main import app
from app.services import initialize_llm, load_dataframes
from app.config import Settings

# Load environment variables
load_dotenv()

# Initialize test client
client = TestClient(app)

# Verify Azure OpenAI environment variables
required_vars = [
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_API_BASE",
    "AZURE_OPENAI_API_VERSION",
    "AZURE_OPENAI_DEPLOYMENT",
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
]

@pytest.fixture
def test_settings():
    """Fixture to provide test settings"""
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        pytest.skip(f"Missing required environment variables: {missing_vars}")
    
    return Settings()

@pytest.fixture
def test_data(test_settings):
    """Fixture to provide test data"""
    data = load_dataframes(test_settings)
    if not all(data.values()):
        pytest.skip("Test data not available")
    return data

def test_environment_variables(test_settings):
    """Test that all required environment variables are set"""
    for var in required_vars:
        assert os.getenv(var) is not None, f"Missing environment variable: {var}"
    
    assert test_settings.azure_openai_api_key == os.getenv("AZURE_OPENAI_API_KEY")
    assert test_settings.azure_openai_api_base == os.getenv("AZURE_OPENAI_API_BASE")

@pytest.mark.asyncio
async def test_llm_initialization(test_settings):
    """Test LLM initialization"""
    llm = await initialize_llm(test_settings)
    assert llm is not None

def test_global_search_endpoint(test_settings, test_data):
    """Test the global search endpoint"""
    response = client.post(
        "/search/global",
        json={
            "query": "What are the main topics?",
            "community_level": 1,
            "dynamic_community_selection": True
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    assert "context_data" in result

def test_local_search_endpoint(test_settings, test_data):
    """Test the local search endpoint"""
    response = client.post(
        "/search/local",
        json={
            "query": "What are the main topics?",
            "community_level": 1
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    assert "context_data" in result

def test_drift_search_endpoint(test_settings, test_data):
    """Test the drift search endpoint"""
    response = client.post(
        "/search/drift",
        json={
            "query": "What are the main topics?",
            "community_level": 1
        }
    )
    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    assert "context_data" in result

def test_error_handling():
    """Test error handling for invalid requests"""
    # Test missing query
    response = client.post("/search/global", json={})
    assert response.status_code == 422

    # Test invalid community level
    response = client.post(
        "/search/global",
        json={
            "query": "test",
            "community_level": -1
        }
    )
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
