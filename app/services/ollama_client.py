import requests
from app.config import OLLAMA_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT

def build_prompt(pergunta: str, item: dict) -> str:
    passos = "\n".join([f"- {p}" for p in item.get("passos", [])])

    contexto = f"""
ID: {item.get("id")}
Título: {item.get("titulo")}
Categoria: {item.get("categoria")}
Perguntas relacionadas: {", ".join(item.get("perguntas_relacionadas", []))}
Passos:
{passos}
Observações: {item.get("observacoes", "")}
""".strip()

    prompt = f"""
Você é um assistente de suporte técnico.

Responda SOMENTE com base no CONTEXTO abaixo.

Regras:
- Use apenas o conteúdo do CONTEXTO.
- Não invente informações.
- Não use conhecimento externo.
- Se a resposta não estiver no contexto, responda exatamente:
"Não encontrei essa informação na base de conhecimento."
- Responda em português do Brasil.
- Seja claro, objetivo e breve.

CONTEXTO:
{contexto}

PERGUNTA DO USUÁRIO:
{pergunta}

RESPOSTA:
""".strip()

    return prompt

def ask_ollama(pergunta: str, item: dict) -> str:
    prompt = build_prompt(pergunta, item)

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 180
        }
    }

    response = requests.post(OLLAMA_URL, json=payload, timeout=OLLAMA_TIMEOUT)
    response.raise_for_status()

    data = response.json()
    return (data.get("response") or "").strip()