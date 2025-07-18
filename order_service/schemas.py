from datetime import datetime
from pydantic import BaseModel


class OrderItem(BaseModel):
    id: int
    quantidade: int


class OrderBase(BaseModel):
    pizza_nome: str
    quantidade: int
    valor_unitario: float
    valor_total: float
    criado_em: datetime
    cliente_id: int


class OrderCreate(BaseModel):
    pizzas: List[OrderItem]
    bebidas: List[OrderItem]


class OrderResponse(OrderBase):
    id: int

    class config:
        orm_mode = True
