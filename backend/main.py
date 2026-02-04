from fastapi import FastAPI, HTTPException, Query
from crud import (
    get_operadoras,
    get_operadora,
    get_historico_despesas,
    get_estatisticas
)
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="API Operadoras ANS")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)



@app.get("/api/operadoras")
def listar_operadoras(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    data, total = get_operadoras(page, limit)
    return {
        "data": data,
        "total": total,
        "page": page,
        "limit": limit
    }


@app.get("/api/operadoras/{cnpj}")
def detalhe_operadora(cnpj: str):
    operadora = get_operadora(cnpj)
    if not operadora:
        raise HTTPException(status_code=404, detail="Operadora não encontrada")
    return operadora

@app.get("/api/operadoras/{cnpj}/despesas")
def listar_historico_despesas(cnpj: str):
    historico = get_historico_despesas(cnpj)
    if not historico:
        return [] 
    return historico

@app.get("/api/estatisticas")
def estatisticas():
    return get_estatisticas()
