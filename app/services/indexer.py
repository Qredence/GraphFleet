import asyncio
from app.config import settings
from app.utils.logging import logger

async def run_indexer(verbose: bool = True):
    try:
        cmd = [
            "python", "-m", "graphrag.index",
            "--root", settings.INPUT_DIR,
            "--config", f"{settings.INPUT_DIR}/settings.yaml"
        ]
        if verbose:
            cmd.append("--verbose")

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            logger.info("Indexing completed successfully")
            return stdout.decode()
        else:
            logger.error(f"Indexing failed: {stderr.decode()}")
            raise RuntimeError("Indexing process failed")
    except Exception as e:
        logger.error(f"Error during indexing: {str(e)}")
        raise

async def run_prompt_tuning(no_entity_types: bool = True):
    try:
        cmd = [
            "python", "-m", "graphrag.prompt_tune",
            "--config", f"{settings.INPUT_DIR}/settings.yaml",
            "--root", settings.INPUT_DIR,
            "--output", f"{settings.INPUT_DIR}/prompts"
        ]
        if no_entity_types:
            cmd.append("--no-entity-types")

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            logger.info("Prompt tuning completed successfully")
            return stdout.decode()
        else:
            logger.error(f"Prompt tuning failed: {stderr.decode()}")
            raise RuntimeError("Prompt tuning process failed")
    except Exception as e:
        logger.error(f"Error during prompt tuning: {str(e)}")
        raise