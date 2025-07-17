from sqlalchemy import Column, Integer, Float, String, DateTime, func
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    pizza_nome = Column(String(255), nullable=False)
    pizza_id = Column(Integer, nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_unitario = Column(Float, nullable=False)
    valor_total = Column(Float, nullable=False)
    cliente_id = Column(Integer, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())

