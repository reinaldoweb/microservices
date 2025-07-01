from sqlalchemy import Column, Integer, String, Float
from database import Base


class Pizza(Base):
    __tablename__ = "pizzas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(150), nullable=False)
    descricao = Column(String(255), nullable=False)
    preco = Column(Float, nullable=False)
