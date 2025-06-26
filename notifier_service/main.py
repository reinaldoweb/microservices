import asyncio
from consumer import listen_notifications

if __name__ == "__main__":
    print("✅ Iniciando notifier_service...")
    asyncio.run(listen_notifications())
