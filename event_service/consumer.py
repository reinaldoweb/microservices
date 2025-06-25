import redis.asyncio as redis
import json
import httpx
from database import AsyncSessionLocal
from models import EventoPedido

# 🚀 URL interna do customer_service no Docker
CUSTOMER_SERVICE_URL = "http://customer_service:8003"


async def listen_redis():
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("pedido_criado")

    print("📡 Escutando eventos no canal 'pedido_criado'...")

    async for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            evento = json.loads(message["data"])
            print(f"📦 Evento recebido: {evento}")

            # ✅ Validação: verifica se o cliente existe via customer_service
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{CUSTOMER_SERVICE_URL}/clientes/{evento['cliente_id']}")
                if response.status_code != 200:
                    print(f"❌ Cliente {evento['cliente_id']} não encontrado. Evento ignorado.")
                    continue

            # 💾 Persiste o evento no banco de dados
            async with AsyncSessionLocal() as db:
                novo_evento = EventoPedido(
                    pedido_id=evento["pedido_id"],
                    cliente_id=evento["cliente_id"],
                    valor_total=evento["valor_total"],
                )
                db.add(novo_evento)
                await db.commit()
                print("✅ Evento salvo com sucesso.")

        except json.JSONDecodeError:
            print(f"❌ Evento malformado: {message['data']}")
        except Exception as e:
            print(f"❌ Erro ao processar evento: {e}")
