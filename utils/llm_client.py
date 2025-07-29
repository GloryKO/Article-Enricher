# utils/llm_client.py
from dotenv import load_dotenv
load_dotenv()

import httpx
import os
from utils.logger import get_logger
logger = get_logger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

DEFAULT_MODEL = "openai/gpt-3.5-turbo"


def call_llm(prompt, model=DEFAULT_MODEL):
    url = "https://openrouter.ai/api/v1/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that edits markdown articles based on instructions."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    try:
        response = httpx.post(url, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()

        return response.json()["choices"][0]["message"]["content"]

    except httpx.RequestError as exc:
        logger.error(f"Request error: {exc}")
    except Exception as e:
        logger.error(f"Unexpected LLM error: {e}")

    return None
