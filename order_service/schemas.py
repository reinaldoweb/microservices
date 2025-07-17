from datetime import datetime
from pydantic import BaseModel


class OrderBase(BaseModel):
    pizza_nome: str
    quantidade: int
    valor_unitario: float
    valor_total: float
    data_pedido: datetime
    cliente_id: int


class OrderCreate(BaseModel):
    pizza_id: int
    quantidade: int
    cliente_id: int


class OrderResponse(OrderBase):
    id: int

    class config:
        from_attributes = True
