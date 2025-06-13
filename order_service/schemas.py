from pydantic import BaseModel


class OrderRequest(BaseModel):
    pizza_id: int
    quantidade: int


class OrderResponse(BaseModel):
    pizza_nome: str
    quantidade: int
    valor_unitario: float
    valor_total: float
 