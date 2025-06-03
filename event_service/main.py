import asyncio
from consumer import listen_redis

if __name__ == "__main__":
    print("🚀 Iniciando serviço de eventos...")
    asyncio.run(listen_redis())
