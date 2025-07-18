from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from models import Drink
from schemas import DrinkCreate


async def create_drink(db: AsyncSession, drink: DrinkCreate):
    result = await db.execute(select(Drink).where(Drink.nome == drink.nome))
    drink_existe = result.scalar_one_or_none()
    if drink_existe:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Drink já cadastrado!"
                            )
    novo_drink = Drink(**drink.dict())
    db.add(novo_drink)
    await db.commit()
    await db.refresh(novo_drink)
    return novo_drink


async def list_drink(db: AsyncSession):
    result = await db.execute(select(Drink))
    return result.scalars().all()


async def get_drink_by_id(db: AsyncSession, drink_id: int):
    result = await db.execute(select(Drink).where(Drink.id == drink_id))
    drink = result.scalar_one_or_none()
    if not drink:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Drink não encontrado")
    return drink


async def buscar_drink(db: AsyncSession, drink_id: int):
    result = await db.execute(select(Drink).where(Drink.id == drink_id))
    buscar = result.scalar_one_or_none()
    if not buscar:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Drink não encontrado"
                            )
    return buscar