from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models import User
from database import get_db
from schemas import TokenResponse, UserCreate, UserLogin, Token
from utils import create_access_token, hashed_password, verify_password
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()


@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(
        User.username == user.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe")

    new_user = User(
                    username=user.username,
                    password=hashed_password(user.password))
    db.add(new_user)
    await db.commit()
    return {"message": "Usuário registrado com sucesso"}


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(
        User.username == user.username))
    db_user = result.scalar_one_or_none()
    if not db_user or not verify_password(
            user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    token = create_access_token(data={"sub": str(db_user.id)})
    return TokenResponse(access_token=token, token_type="bearer")
