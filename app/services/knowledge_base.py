import time
import requests
from app.config import KNOWLEDGE_API_URL, CACHE_TTL_SECONDS, KNOWLEDGE_API_TIMEOUT

_cache = {
    "data": [],
    "timestamp": 0
}

def get_knowledge_base():
    global _cache

    now = time.time()
    if now - _cache["timestamp"] < CACHE_TTL_SECONDS and _cache["data"]:
        return _cache["data"]

    try:
        response = requests.get(KNOWLEDGE_API_URL, timeout=KNOWLEDGE_API_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            _cache["data"] = data
            _cache["timestamp"] = now
            return data

        return []
    except Exception:
        # fallback para o cache se houver algo
        return _cache["data"] if _cache["data"] else []