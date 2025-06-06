import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from models import Base
# from models import Base

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@postgres:5432/microservices_db"
)

# Criação do engine de conexão assíncrona
engine = create_async_engine(DATABASE_URL, echo=True)

# Fábrica de sessões
AsyncSessionLocal = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False)


# Use apenas uma vez para criar a tabela no banco
async def criar_tabela():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Dependência para obter a sessão no FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
