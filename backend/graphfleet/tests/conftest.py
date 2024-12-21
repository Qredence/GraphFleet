"""
Test configuration and shared fixtures.
"""
import pytest
from pathlib import Path

@pytest.fixture(scope="session")
def test_data_dir():
    """Get the test data directory"""
    return Path(__file__).parent / "test_data"

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment(test_data_dir):
    """Set up the test environment"""
    # Ensure test data directory exists
    test_data_dir.mkdir(parents=True, exist_ok=True)
    
    # Add any other test environment setup here
    yield
    
    # Clean up after tests if needed
    # Note: Be careful with cleanup to not delete actual data
