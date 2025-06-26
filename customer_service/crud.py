from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Cliente
from schemas import ClienteCreate, ClienteUpdate


async def criar_cliente(db: AsyncSession, cliente: ClienteCreate):
    result = await db.execute(select(Cliente).where(
        Cliente.email == cliente.email))
    cliente = result.scalar_one_or_none()
    if cliente:
        raise HTTPException(status_code=400, detail="Cliente já Cadastrado")
    novo_cliente = Cliente(**cliente.model_dump())
    db.add(novo_cliente)
    await db.commit()
    await db.refresh(novo_cliente)
    return novo_cliente


async def listar_clientes(db: AsyncSession):
    result = await db.execute(select(Cliente))
    return result.scalars().all()


async def atualizar_cliente(db: AsyncSession, id: int, dados: ClienteUpdate):
    cliente = await buscar_cliente(db, id)
    if cliente:
        for field, value in dados.model_dump().items():
            setattr(cliente, field, value)
        await db.commit()
        await db.refresh(cliente)
    return cliente


async def buscar_cliente(db: AsyncSession, id: int):
    result = await db.execute(select(Cliente).where(Cliente.id == id))
    cliente = result.scalar_one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cliente


async def deletar_cliente(db: AsyncSession, id: int):
    result = await db.execute(select(Cliente).where(Cliente.id == id))
    cliente = result.scalar_one_or_none()

    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    await db.delete(cliente)
    await db.commit()
    return {"detail": "Cliente deletado com sucesso"}
