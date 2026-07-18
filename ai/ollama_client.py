import httpx
import asyncio
import time
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class OllamaResponse:
    success: bool = False
    text: str = ""
    error: str = ""

class OllamaClient:
    def __init__(self, model: str = "qwen2.5:latest"):
        self.url = "http://127.0.0.1:11434/api/generate"
        self.model = model

    async def generate(self, prompt: str, system_prompt: str = "") -> OllamaResponse:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "format": "json"
        }
        
        # Async HTTP Request
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(self.url, json=payload)
                response.raise_for_status()
                data = response.json()
                return OllamaResponse(success=True, text=data.get("response", ""))
            except Exception as e:
                return OllamaResponse(success=False, error=str(e))