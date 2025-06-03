# customer_service/consumer.py
import asyncio
import redis.asyncio as redis
import json

async def listen_redis():
    r = redis.Redis(host="localhost", port=6379, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("pedido_criado")

    print("📡 Escutando canal 'pedido_criado'...")

    async for message in pubsub.listen():
        if message["type"] == "message":
            try:
                evento = json.loads(message["data"])
                print(f"📩 Evento recebido: Pedido #{evento['pedido_id']}, Cliente #{evento['cliente_id']}, Total: R${evento['valor_total']}")
                # Aqui você pode atualizar o cliente, salvar log, etc.
            except json.JSONDecodeError:
                print(f"⚠️ Evento malformado: {message['data']}")

if __name__ == "__main__":
    asyncio.run(listen_redis())
