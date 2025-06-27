from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models import Pizza
from schemas import PizzaCreate, PizzaResponse


async def create_pizza(db: AsyncSession, pizza: PizzaCreate):
    result = await db.execute(select(Pizza).where(Pizza.nome == pizza.nome))
    pizza_existe = result.scalar_one_or_none()
    if pizza_existe:
        raise HTTPException(status_code=400, detail="Pizza já cadastrada")
    nova_pizza = Pizza(**pizza.model_dump())
    db.add(nova_pizza)
    await db.commit()
    await db.refresh(nova_pizza)
    return nova_pizza


async def listar_pizzas(db: AsyncSession):
    result = await db.execute(select(Pizza))
    return result.scalars().all()


async def atualizar_pizza(db: AsyncSession, id: int, dados: PizzaResponse):
    pizza_update = await buscar_pizza(db, id)
    if pizza_update:
        for field, value in dados.model_dump().items():
            setattr(pizza_update, field, value)
        await db.commit()
        await db.refresh(pizza_update)
    return pizza_update


async def buscar_pizza(db: AsyncSession, id: int):
    result = await db.execute(select(Pizza).where(Pizza.id == id))
    buscar = result.scalar_one_or_none()
    if not buscar:
        raise HTTPException(status_code=404, detail="Pizza não encontrada")
    return buscar


async def deletar_pizza(db: AsyncSession, id: int):
    result = await db.execute(select(Pizza).where(Pizza.id == id))
    pizza_deletar = result.scalar_one_or_none()

    if not pizza_deletar:
        raise HTTPException(status_code=404, detail="Pizza não encontrada")
    await db.delete(pizza_deletar)
    await db.commit()
    return pizza_deletar