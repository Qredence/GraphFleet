"""
Script to run the FastAPI app locally with Azure OpenAI integration.
"""
import os
import logging
from pathlib import Path
import uvicorn
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if all required environment variables are set"""
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_API_BASE",
        "AZURE_OPENAI_API_VERSION",
        "AZURE_OPENAI_DEPLOYMENT",
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {missing}")

def check_data_directories():
    """Ensure all required data directories exist"""
    base_dir = Path(__file__).parent
    required_dirs = {
        'input': base_dir / 'input',
        'output': base_dir / 'output',
        'prompts': base_dir / 'prompts'
    }
    
    for name, path in required_dirs.items():
        if not path.exists():
            logger.info(f"Creating {name} directory at {path}")
            path.mkdir(parents=True, exist_ok=True)

def main():
    # Load environment variables
    env_file = Path(__file__).parent / '.env'
    if env_file.exists():
        logger.info(f"Loading environment from {env_file}")
        load_dotenv(env_file)
    else:
        logger.warning(f"No .env file found at {env_file}")
    
    try:
        # Check environment and directories
        check_environment()
        check_data_directories()
        
        # Get configuration from environment
        host = os.getenv("APP_HOST", "0.0.0.0")
        port = int(os.getenv("APP_PORT", "8000"))
        
        # Start the FastAPI app
        logger.info(f"Starting FastAPI app on http://{host}:{port}")
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=True,  # Enable auto-reload for development
            log_level="info"
        )
    
    except Exception as e:
        logger.error(f"Failed to start the application: {e}")
        raise

if __name__ == "__main__":
    main()
