import httpx
import json
from typing import List, Dict, Any, Optional
from config.settings import settings

class LLMService:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.default_model = settings.DEFAULT_MODEL

    def generate_completion(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        model: Optional[str] = None, 
        temperature: float = 0.2,
        max_tokens: int = 1000
    ) -> str:
        if not self.api_key:
            print("Warning: No OPENROUTER_API_KEY found. Returning mock response.")
            return "This is a mock response because no API key was provided."

        target_model = model or self.default_model
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/AgentiQuo/Niche-Realtor", # Optional, for OpenRouter rankings
            "X-Title": "Niche Realtor", # Optional, for OpenRouter rankings
        }

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling OpenRouter: {e}")
            return f"Error: {str(e)}"

    def get_available_models(self) -> List[Dict[str, Any]]:
        """
        Returns a list of commonly used models on OpenRouter for quick reference.
        """
        return [
            {"id": "anthropic/claude-3.5-sonnet", "name": "Claude 3.5 Sonnet", "type": "High Intelligence"},
            {"id": "anthropic/claude-3-haiku", "name": "Claude 3 Haiku", "type": "Fast & Cheap"},
            {"id": "google/gemini-flash-1.5", "name": "Gemini 1.5 Flash", "type": "Fast & Large Context"},
            {"id": "google/gemini-pro-1.5", "name": "Gemini 1.5 Pro", "type": "High Intelligence"},
            {"id": "meta-llama/llama-3.1-70b-instruct", "name": "Llama 3.1 70B", "type": "Strong Open Source"},
            {"id": "meta-llama/llama-3.1-405b", "name": "Llama 3.1 405B", "type": "SOTA Open Source"},
            {"id": "openai/gpt-4o", "name": "GPT-4o", "type": "Flagship OpenAI"},
            {"id": "openai/gpt-4o-mini", "name": "GPT-4o mini", "type": "Cheap OpenAI"},
            {"id": "mistralai/mixtral-8x22b-instruct", "name": "Mixtral 8x22B", "type": "Efficient MoE"},
            {"id": "deepseek/deepseek-chat", "name": "DeepSeek Chat", "type": "Budget Friendly"},
            {"id": "qwen/qwen-2.5-72b-instruct", "name": "Qwen 2.5 72B", "type": "Strong Coding/Math"},
        ]

llm_service_instance = LLMService()
