from app.config import MIN_SCORE, DIRECT_RESPONSE_SCORE
from app.services.knowledge_base import get_knowledge_base
from app.services.matcher import find_best_match
from app.services.ollama_client import ask_ollama

def format_direct_response(item: dict) -> str:
    lines = [f"{item.get('titulo', 'Informação encontrada')}:"]

    passos = item.get("passos", [])
    for i, passo in enumerate(passos, start=1):
        lines.append(f"{i}. {passo}")

    observacoes = item.get("observacoes")
    if observacoes:
        lines.append(f"Observação: {observacoes}")

    return "\n".join(lines)

def answer_question(pergunta: str) -> dict:
    knowledge_items = get_knowledge_base()

    if not knowledge_items:
        return {
            "resposta": "Não foi possível acessar a base de conhecimento no momento.",
            "score": None,
            "item_encontrado": None,
            "fonte": "sistema"
        }

    best_item, score = find_best_match(pergunta, knowledge_items)

    if not best_item or score < MIN_SCORE:
        return {
            "resposta": "Não encontrei essa informação na base de conhecimento.",
            "score": score,
            "item_encontrado": None,
            "fonte": "base"
        }

    # resposta direta para ficar mais rápido
    if score >= DIRECT_RESPONSE_SCORE:
        return {
            "resposta": format_direct_response(best_item),
            "score": score,
            "item_encontrado": best_item.get("titulo"),
            "fonte": "base_direta"
        }

    # usa o modelo apenas quando necessário
    try:
        llm_response = ask_ollama(pergunta, best_item)

        if not llm_response:
            llm_response = "Não encontrei essa informação na base de conhecimento."

        return {
            "resposta": llm_response,
            "score": score,
            "item_encontrado": best_item.get("titulo"),
            "fonte": "ollama"
        }
    except Exception:
        return {
            "resposta": format_direct_response(best_item),
            "score": score,
            "item_encontrado": best_item.get("titulo"),
            "fonte": "fallback_base_direta"
        }