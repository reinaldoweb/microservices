from pydantic import BaseModel
from typing import Optional


class DrinkBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    preco: float


class DrinkCreate(DrinkBase):
    pass


class DrinkResponse(DrinkBase):
    id: int

    class Config:
        orm_mode = True
