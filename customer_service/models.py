from sqlalchemy import Column, Integer, String
from .database import Base


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
