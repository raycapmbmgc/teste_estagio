from pydantic import BaseModel
from typing import List

class Operadora(BaseModel):
    razao_social: str
    total_despesas: float
    media_despesas: float

class OperadorasResponse(BaseModel):
    data: List[Operadora]
    total: int
    page: int
    limit: int

class EstatisticaItem(BaseModel):
    razao_social: str
    total_despesas: float

class EstatisticasResponse(BaseModel):
    total_despesas: float
    media_despesas: float
    top_5_operadoras: List[EstatisticaItem]
