from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from crud import create_drink, list_drinks, get_drink_by_id
from database import get_db
from schemas import DrinkCreate, DrinkResponse
from typing import List


app = FastAPI(title="Drink Service")


@app.post(
            "/drinks", response_model=DrinkResponse,
            status_code=status.HTTP_201_CREATED
            )
async def criar_drink(drink: DrinkCreate, db: AsyncSession = Depends(get_db)):
    return await create_drink(db, drink)


@app.get("/drinks", response_model=List[DrinkResponse])
async def listar(db: AsyncSession = Depends(get_db)) -> any:
    drinks = await list_drinks(db)
    return drinks


@app.get("/drinks/{drink_id}", response_model=DrinkResponse)
async def buscar_drink(drink_id: int, db: AsyncSession = Depends(get_db)):
    drink = await get_drink_by_id(db, drink_id)
    if not drink:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Drink não encontrado"
                            )
    return drink