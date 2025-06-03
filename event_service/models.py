from sqlalchemy import Column, Float, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EventoPedido(Base):
    __tablename__ = "eventos_pedidos"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, nullable=False)
    cliente_id = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
