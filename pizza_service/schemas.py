from typing import Optional
from pydantic import BaseModel


class PizzaBase(BaseModel):
    nome: str
    descricao: str
    preco: float


class PizzaCreate(PizzaBase):
    pass


class PizzaUpdate(BaseModel):
    nome: str
    descricao: str
    preco: float


class PizzaResponse(PizzaBase):
    id: int

    class Config:
        from_attrributes = True
