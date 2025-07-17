from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from config import API_KEY
from crud import (
        create_pizza,
        listar_pizzas,
        deletar_pizza,
        atualizar_pizza,
        buscar_pizza
        )
from database import get_db, engine, Base
from schemas import PizzaCreate, PizzaResponse, PizzaUpdate

app = FastAPI(title="Pizza Service")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Middleware de autenticação
api_key_header = APIKeyHeader(name="X-API-KEY")


def verify_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chave API inválilda"
        )


@app.post("/pizzas", response_model=PizzaResponse,
          status_code=status.HTTP_201_CREATED)
async def criar_pizza(
        pizza: PizzaCreate, db: AsyncSession = Depends(get_db)):
    return await create_pizza(db, pizza)


@app.get("/pizzas", response_model=list[PizzaResponse])
async def listar(db: AsyncSession = Depends(get_db)) -> any:
    pizzas = await listar_pizzas(db)
    return [PizzaResponse.from_orm(p) for p in pizzas]


# End point protegido
@app.get("/pizzas/{pizza_id}", response_model=PizzaResponse)
async def buscar(pizza_id: int, db: AsyncSession = Depends(get_db)):
    pizza = await buscar_pizza(db, pizza_id)
    if not pizza:
        raise HTTPException(status_code=404, detail="Pizza não encontrada")
    return PizzaResponse.from_orm(pizza)


@app.patch("/pizzas/{pizza_id}", response_model=PizzaResponse)
async def atualizar(
        pizza_id: int,
        dados: PizzaUpdate,
        db: AsyncSession = Depends(get_db)):
    pizza_up = await atualizar_pizza(db, pizza_id, dados)
    if not pizza_up:
        raise HTTPException(status_code=404, detail="Pizza não encontrada")
    return [PizzaResponse.from_orm(pizza_up)]


@app.delete("/pizzas/{pizza_id}")
async def deletar(pizza_id: int, db: AsyncSession = Depends(get_db)):
    pizza_deletar = await deletar_pizza(db, pizza_id)
    if not pizza_deletar:
        raise HTTPException(status_code=404, detail="Pizza não encontrada")
    return {"message": "Pizza removida com sucesso"}
