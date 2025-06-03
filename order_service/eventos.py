import redis.asyncio as redis
import json


redis_client = redis.Redis(host="redis", port=6379, decode_responses=True)


async def publicar_pedido_criado(pedido_id: int, cliente_id: int, total: float):
    evento = {
        "pedido_id": pedido_id,
        "cliente_id": cliente_id,
        "valor_total": total,
    }
    await redis_client.publish("pedido_criado", json.dumps(evento))
