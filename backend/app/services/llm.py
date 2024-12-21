from typing import Dict, List, Optional
import openai
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import Settings, get_settings

class LLMService:
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        openai.api_key = self.settings.openai_api_key
        self.model = self.settings.openai_model_name
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def generate_completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        top_p: float = 1.0,
        frequency_penalty: float = 0.0,
        presence_penalty: float = 0.0,
    ) -> str:
        """Generate a completion using OpenAI's API with retry logic."""
        try:
            response = await openai.ChatCompletion.acreate(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Error generating completion: {str(e)}")

    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using OpenAI's API."""
        try:
            response = await openai.Embedding.acreate(
                model="text-embedding-ada-002",
                input=texts
            )
            return [data.embedding for data in response.data]
        except Exception as e:
            raise Exception(f"Error generating embeddings: {str(e)}")

    async def analyze_similarity(self, text1: str, text2: str) -> float:
        """Analyze semantic similarity between two texts using embeddings."""
        embeddings = await self.generate_embeddings([text1, text2])
        # Calculate cosine similarity between embeddings
        similarity = self._cosine_similarity(embeddings[0], embeddings[1])
        return similarity

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        import numpy as np
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        return dot_product / (norm1 * norm2)
