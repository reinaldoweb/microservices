# criar_db.py
import asyncio
from database import criar_tabelas

if __name__ == "__main__":
    asyncio.run(criar_tabelas())
