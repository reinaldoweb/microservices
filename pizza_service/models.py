from sqlalchemy import Column, Integer, String, Float
from database import Base  # Certifique-se de importar corretamente o Base do database.py


class Pizza(Base):
    __tablename__ = "pizzas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    preco = Column(Float, nullable=False)
