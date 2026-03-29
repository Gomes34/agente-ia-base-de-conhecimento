# main.py

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
from data import knowledge_base

app = FastAPI(
    title="Base de Conhecimento de Suporte Técnico",
    description="API simples com instruções fictícias de suporte técnico",
    version="1.0.0"
)

class KnowledgeItem(BaseModel):
    id: int
    titulo: str
    categoria: str
    perguntas_relacionadas: List[str]
    passos: List[str]
    observacoes: Optional[str] = None

@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo à API da Base de Conhecimento",
        "rotas": [
            "/itens",
            "/itens/{id}",
            "/buscar?termo=...",
            "/itens (POST)"
        ]
    }

@app.get("/itens", response_model=List[KnowledgeItem])
def listar_itens():
    return knowledge_base

@app.get("/itens/{item_id}", response_model=KnowledgeItem)
def buscar_item_por_id(item_id: int):
    for item in knowledge_base:
        if item["id"] == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item não encontrado")

@app.get("/buscar", response_model=List[KnowledgeItem])
def buscar_por_termo(termo: str = Query(..., min_length=2)):
    termo = termo.lower()
    resultados = []

    for item in knowledge_base:
        if termo in item["titulo"].lower():
            resultados.append(item)
            continue

        if termo in item["categoria"].lower():
            resultados.append(item)
            continue

        if any(termo in pergunta.lower() for pergunta in item["perguntas_relacionadas"]):
            resultados.append(item)
            continue

        if any(termo in passo.lower() for passo in item["passos"]):
            resultados.append(item)

    return resultados

@app.post("/itens", response_model=KnowledgeItem, status_code=201)
def adicionar_item(novo_item: KnowledgeItem):
    for item in knowledge_base:
        if item["id"] == novo_item.id:
            raise HTTPException(status_code=400, detail="Já existe um item com esse ID")

    knowledge_base.append(novo_item.dict())
    return novo_item