import redis.asyncio as redis
import json


async def listen_notifications():
    client = redis.Redis(host="localhost", port=6379, decode_responses=True)
    pubsub = client.pubsub()
    await pubsub.subscribe("pedido_criado")

    print("Notifier Escutando o canal 'pedido_criado'...")

    async for message in pubsub.listen():
        if message[type] == "message":
            try:
                evento = json.loads(message["data"])
                print(
                    f"Notificando cliente {evento['cliente_id']} "
                    f"sobre o pedido {evento['pedido_id']}, "
                    f"total R${evento['valor_total']}"
                )
            except Exception as e:
                print(f"Erro ao processar notificação: {str(e)}")
