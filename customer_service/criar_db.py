import asyncio
from database import engine, Base
from models import Cliente


async def criar_tabela():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(criar_tabela())