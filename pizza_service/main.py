from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from config import API_KEY

app = FastAPI()
# Mock de banco de dados
pizzas_db = {
                1:{"id": 1, "nome": "Pizza Margherita", "preco": 30.00},
                2:{"id": 2, "nome": "Pizza Pepperoni", "preco": 35.00},
                3:{"id": 3, "nome": "Pizza Calabresa", "preco": 40.00}
            }
# Middleware de autenticação
api_key_header = APIKeyHeader(name="X-API-KEY")


# class Pizza(BaseModel):
#     id: int
#     nome: str
#     preco: float


def verify_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Chave API inválilda")


# End point protegido
@app.get("/pizzas/{pizza_id}", dependencies=[Depends(verify_api_key)])
async def get_pizza(pizza_id: int):
    pizza = pizzas_db.get(pizza_id)
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza não encontrada")
    return pizza


# @app.get("/pizzas")
# async def get_pizzas():
#     return list(pizzas_db.values())
