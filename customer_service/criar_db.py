import asyncio
from database import engine, Base


async def criar_tabela():
    async with engine.bnegin() as conn:
        await conn.execute(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.run(criar_tabela())