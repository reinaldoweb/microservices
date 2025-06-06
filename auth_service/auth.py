from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, TokenResponse
from utils import hashed_password, verify_password, create_access_token


router = APIRouter()


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(
        User.username == user.username))
    if result.scalars():
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = User(
                    username=user.name,
                    hashed_password=hashed_password(user.password))
    db.add(new_user)
    await db.commit()
    return {"message": "Usuário registrado com sucesso"}


@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(
        User.username == user.username))
    db_user = result.scalars()
    if not db_user or not verify_password(
            user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    access_token = create_access_token(data={"sub": user.username})
    return {"acess_token": access_token, "token_type": "bearer"}
