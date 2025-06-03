from pydantic import BaseModel


class Pizza(BaseModel):
    id: int
    nome: str
    preco: float