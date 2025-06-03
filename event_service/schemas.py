from pydantic import BaseModel


class EventoPedidoSchema(BaseModel):
    pedido_id: int
    cliente_id: int
    valor_total: float

    class Config:
        orm_mode = True
