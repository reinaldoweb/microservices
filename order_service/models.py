from sqlalchemy import Column, Integer, Float, String
# from database import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, nullable=False)
    pizza_nome = Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False)


class OrderRequest(Base):
    pizza_id: int
    quantidade: int


class OrderResponse(Base):
    pizza_nome: str
    quantidade: int
    valor_unitario: float
    valor_total: float

    class Config:
        orm_mode = True
