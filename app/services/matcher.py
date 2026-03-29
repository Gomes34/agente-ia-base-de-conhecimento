from rapidfuzz import fuzz

def normalize(text: str) -> str:
    return (text or "").strip().lower()

def calculate_score(user_question: str, item: dict) -> float:
    question = normalize(user_question)
    scores = []

    titulo = normalize(item.get("titulo", ""))
    categoria = normalize(item.get("categoria", ""))

    if titulo:
        scores.append(fuzz.token_set_ratio(question, titulo))

    if categoria:
        scores.append(fuzz.token_set_ratio(question, categoria))

    for related in item.get("perguntas_relacionadas", []):
        related_norm = normalize(related)
        if related_norm:
            scores.append(fuzz.token_set_ratio(question, related_norm))

    # bônus leve se alguma palavra da pergunta aparecer no título
    title_words = set(titulo.split())
    question_words = set(question.split())
    common_words = title_words.intersection(question_words)

    base_score = max(scores) if scores else 0
    bonus = min(len(common_words) * 2, 10)

    return min(base_score + bonus, 100)

def find_best_match(user_question: str, knowledge_items: list):
    best_item = None
    best_score = 0

    for item in knowledge_items:
        score = calculate_score(user_question, item)
        if score > best_score:
            best_score = score
            best_item = item

    return best_item, best_score