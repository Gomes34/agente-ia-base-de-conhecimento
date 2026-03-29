from pydantic import BaseModel
from typing import List, Optional

class KnowledgeItem(BaseModel):
    id: int
    titulo: str
    categoria: str
    perguntas_relacionadas: List[str]
    passos: List[str]
    observacoes: Optional[str] = ""

class ChatRequest(BaseModel):
    pergunta: str

class ChatResponse(BaseModel):
    resposta: str
    score: Optional[float] = None
    item_encontrado: Optional[str] = None
    fonte: Optional[str] = None