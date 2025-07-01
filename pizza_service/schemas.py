from pydantic import BaseModel


class PizzaBase(BaseModel):
    nome: str
    descricao: str
    preco: float


class PizzaCreate(PizzaBase):
    pass


class PizzaUpdate(PizzaBase):
    id: int


class PizzaResponse(PizzaBase):
    id: int

    class Config:
        orm_mode = True
