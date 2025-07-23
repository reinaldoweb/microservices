from sqlalchemy import Column, Integer, String
from .database import Base
from pydantic import BaseModel, EmailStr


class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)


class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
