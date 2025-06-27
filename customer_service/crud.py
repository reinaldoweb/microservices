from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Cliente
from schemas import ClienteCreate, ClienteResponse


async def criar_cliente(db: AsyncSession, cliente: ClienteCreate):
    result = await db.execute(select(Cliente).where(
        Cliente.email == cliente.email))
    cliente_existente = result.scalar_one_or_none()
    if cliente_existente:
        raise HTTPException(status_code=400, detail="Cliente já Cadastrado")

    novo_cliente = Cliente(**cliente.model_dump())
    db.add(novo_cliente)
    await db.commit()
    await db.refresh(novo_cliente)
    return novo_cliente


async def listar_clientes(db: AsyncSession):
    result = await db.execute(select(Cliente))
    return result.scalars().all()


async def atualizar_cliente(db: AsyncSession, id: int, dados: ClienteResponse):
    cliente_up = await buscar_cliente(db, id)
    if cliente_up:
        for field, value in dados.model_dump().items():
            setattr(cliente_up, field, value)
        await db.commit()
        await db.refresh(cliente_up)
    return cliente_up


async def buscar_cliente(db: AsyncSession, id: int):
    result = await db.execute(select(Cliente).where(Cliente.id == id))
    buscar = result.scalar_one_or_none()
    if not buscar:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return buscar


async def deletar_cliente(db: AsyncSession, id: int):
    result = await db.execute(select(Cliente).where(Cliente.id == id))
    cliente_deletar = result.scalar_one_or_none()

    if not cliente_deletar:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    await db.delete(cliente_deletar)
    await db.commit()
    return cliente_deletar
