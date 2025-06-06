from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt
import os
from datetime import datetime, timedelta
from database import get_db
from models import User
from schemas import UserCreate, UserLogin, TokenResponse
from utils import hashed_password, verify_password


router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "256"


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(
        User.username == user.username))
    if result.scalars().firt():
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
    db_user = result.scalars().first()
    if not db_user or not verify_password(
            user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token_data = {
        "sub": db_user.username,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"acess_token": token}