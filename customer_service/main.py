from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ClienteCreate, ClienteResponse, ClienteUpdate
from .crud import (
    criar_cliente,
    listar_clientes,
    buscar_cliente,
    atualizar_cliente,
    deletar_cliente,
)
from .database import get_db


app = FastAPI(title="Customer Service")


@app.post("/clientes", response_model=ClienteResponse, status_code=200)
async def create_cliente(
        cliente: ClienteCreate,
        db: AsyncSession = Depends(get_db)):
    return await criar_cliente(db, cliente)


@app.get("/clientes", response_model=list[ClienteResponse])
async def listar(
    db: AsyncSession = Depends(get_db)
        ):
    return await listar_clientes(db)


@app.get("/clientes/{id}", response_model=ClienteResponse)
async def buscar(
        id: int,
        db: AsyncSession = Depends(get_db)):
    get_cliente = await buscar_cliente(db, id)
    if not get_cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return get_cliente


@app.patch("/clientes/{id}", response_model=ClienteResponse)
async def atualizar(
        id: int, dados: ClienteUpdate, db: AsyncSession = Depends(get_db)):
    cliente = await atualizar_cliente(db, id, dados)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


@app.delete("/cliente/{id}")
async def remover(id: int, db: AsyncSession = Depends(get_db)):
    cliente = await deletar_cliente(db, id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return {"message": "Cliente removido com sucesso!!"}
