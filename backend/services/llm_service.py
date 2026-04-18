import httpx
import json
import logging
import random
import time
from typing import List, Dict, Any, Optional

from config.settings import settings

logger = logging.getLogger(__name__)

# HTTP status codes that are transient and worth retrying
_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}

# HTTP status codes that indicate a permanent failure — do NOT retry
_FATAL_STATUS_CODES = {400, 401, 403, 404, 422}


class LLMService:
    def __init__(
        self,
        max_retries: int = 4,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        timeout: float = 60.0,
    ):
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = settings.OPENROUTER_BASE_URL
        self.default_model = settings.DEFAULT_MODEL
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.2,
        max_tokens: int = 1000,
    ) -> str:
        """
        Send a chat completion request to OpenRouter.

        Retries on transient errors (429, 5xx) with exponential backoff + jitter.
        Raises immediately on permanent errors (401, 403, 422, etc.).
        Returns the model's text response, or an error string prefixed with 'Error:'.
        """
        if not self.api_key:
            logger.warning("No OPENROUTER_API_KEY found. Returning mock response.")
            return "This is a mock response because no API key was provided."

        target_model = model or self.default_model

        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/AgentiQuo/Niche-Realtor",
            "X-Title": "Niche Realtor",
        }

        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries + 1):
            try:
                logger.debug(
                    "[LLMService] attempt=%d model=%s prompt_len=%d",
                    attempt + 1,
                    target_model,
                    len(prompt),
                )
                with httpx.Client(timeout=self.timeout) as client:
                    response = client.post(
                        f"{self.base_url}/chat/completions",
                        headers=headers,
                        json=payload,
                    )

                # Handle HTTP-level errors with smart routing
                if response.status_code in _FATAL_STATUS_CODES:
                    logger.error(
                        "[LLMService] Fatal HTTP %d — not retrying. Body: %s",
                        response.status_code,
                        response.text[:400],
                    )
                    return f"Error: HTTP {response.status_code} — {response.text[:200]}"

                if response.status_code in _RETRYABLE_STATUS_CODES:
                    logger.warning(
                        "[LLMService] Transient HTTP %d on attempt %d/%d.",
                        response.status_code,
                        attempt + 1,
                        self.max_retries + 1,
                    )
                    last_error = httpx.HTTPStatusError(
                        f"HTTP {response.status_code}",
                        request=response.request,
                        response=response,
                    )
                    self._sleep_with_backoff(attempt, response)
                    continue

                response.raise_for_status()

                content = response.json()["choices"][0]["message"]["content"]
                if attempt > 0:
                    logger.info(
                        "[LLMService] Succeeded on attempt %d after retries.", attempt + 1
                    )
                return content

            except httpx.TimeoutException as exc:
                logger.warning(
                    "[LLMService] Timeout on attempt %d/%d: %s",
                    attempt + 1,
                    self.max_retries + 1,
                    exc,
                )
                last_error = exc
                self._sleep_with_backoff(attempt)

            except httpx.HTTPStatusError as exc:
                # Already handled above for known codes, but catch anything else
                logger.error("[LLMService] Unhandled HTTP error: %s", exc)
                return f"Error: {exc}"

            except Exception as exc:
                logger.error("[LLMService] Unexpected error: %s", exc, exc_info=True)
                return f"Error: {exc}"

        logger.error(
            "[LLMService] All %d attempts exhausted. Last error: %s",
            self.max_retries + 1,
            last_error,
        )
        return f"Error: Max retries exceeded — {last_error}"

    # ------------------------------------------------------------------
    # Utility / introspection
    # ------------------------------------------------------------------

    def get_available_models(self) -> List[Dict[str, Any]]:
        """Returns a quick-reference list of well-known OpenRouter models."""
        return [
            {"id": "anthropic/claude-3.5-sonnet",         "name": "Claude 3.5 Sonnet",  "type": "High Intelligence"},
            {"id": "anthropic/claude-3-haiku",             "name": "Claude 3 Haiku",     "type": "Fast & Cheap"},
            {"id": "google/gemini-flash-1.5",              "name": "Gemini 1.5 Flash",   "type": "Fast & Large Context"},
            {"id": "google/gemini-pro-1.5",                "name": "Gemini 1.5 Pro",     "type": "High Intelligence"},
            {"id": "meta-llama/llama-3.1-70b-instruct",   "name": "Llama 3.1 70B",      "type": "Strong Open Source"},
            {"id": "meta-llama/llama-3.1-405b",           "name": "Llama 3.1 405B",     "type": "SOTA Open Source"},
            {"id": "openai/gpt-4o",                        "name": "GPT-4o",             "type": "Flagship OpenAI"},
            {"id": "openai/gpt-4o-mini",                   "name": "GPT-4o mini",        "type": "Cheap OpenAI"},
            {"id": "mistralai/mixtral-8x22b-instruct",     "name": "Mixtral 8x22B",      "type": "Efficient MoE"},
            {"id": "deepseek/deepseek-chat",               "name": "DeepSeek Chat",      "type": "Budget Friendly"},
            {"id": "qwen/qwen-2.5-72b-instruct",          "name": "Qwen 2.5 72B",       "type": "Strong Coding/Math"},
        ]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _sleep_with_backoff(
        self, attempt: int, response: Optional[httpx.Response] = None
    ) -> None:
        """
        Sleep for an exponentially growing interval with ±25% jitter.

        If the server returned a 'Retry-After' header (common with 429s),
        that value takes precedence over the calculated delay.
        """
        # Honour server-side Retry-After if present
        if response is not None:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                try:
                    delay = float(retry_after)
                    logger.info("[LLMService] Honouring Retry-After: %.1fs", delay)
                    time.sleep(delay)
                    return
                except ValueError:
                    pass  # Header value wasn't a number; fall through to backoff

        # Exponential backoff: 1s, 2s, 4s, 8s … capped at max_delay
        base = min(self.base_delay * (2 ** attempt), self.max_delay)
        # Add ±25% jitter to avoid thundering-herd when many requests retry together
        jitter = base * 0.25 * (random.random() * 2 - 1)
        delay = max(0.0, base + jitter)
        logger.info("[LLMService] Backing off %.2fs before attempt %d.", delay, attempt + 2)
        time.sleep(delay)


# Singleton instance — imported by agents
llm_service_instance = LLMService()
