# backend/services/llama_service.py

import requests

def query_llama(prompt: str) -> str:
    try:
        response = requests.post(
            "http://orbiton-ollama:11434/api/generate",  # docker-compose 내부 주소
            json={"model": "llama3", "prompt": prompt},
            timeout=30
        )
        response.raise_for_status()
        return response.json().get("response", "No response")
    except Exception as e:
        return f"Error: {str(e)}"
