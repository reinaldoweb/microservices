import httpx
import redis.asyncio as redis
import json
from database import AsyncSessionLocal
from models import EventoPedido
from schemas import EventoPedidoSchema
from dotenv import load_dotenv

load_dotenv()


async def listen_redis():
    r = redis.Redis(host="redis", port=6379, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("pedido_criado")

    print("Escutando eventos no canal 'pedido_criado'...")

    async for message in pubsub.listen():
        if message["type"] == "message":
            try:
                evento_data = EventoPedidoSchema.parse_raw(message["data"])
                print(f"📩 Evento recebido: {evento_data}")

                # 1. Salva no banco
                async with AsyncSessionLocal() as db:
                    novo_evento = EventoPedido(
                        pedido_id=evento_data.pedido_id,
                        cliente_id=evento_data.cliente_id,
                        valor_total=evento_data.valor_total,
                    )
                    db.add(novo_evento)
                    await db.commit()
                    print("✅ Evento salvo no banco!")

                # 2. Notifica outro serviço via HTTP
                cliente_id = evento_data.cliente_id
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"http://customer_service:8003/clientes/{cliente_id}")
                        response.raise_for_status()
                        cliente_info = response.json()
                        print(f"Cliente encontrado: {cliente_info['nome']}")
                except httpx.HTTPStatusError:
                    print("Cliente não encontrado")

            except json.JSONDecodeError:
                print(f"Evento malformado: {message['data']}")
            except Exception as e:
                print(f"Erro ao processar evento: {e}")
