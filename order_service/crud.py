from fastapi import FastAPI, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Pedido
import httpx
from eventos import publicar_pedido_criado
from schemas import OrderResponse, OrderCreate, OrderBase
from dotenv import load_dotenv


app = FastAPI(debug=True)

load_dotenv()

PIZZA_SERVICE_URL = "http://pizza_service:8001"
API_KEY = "supersegredo123"


async def create_order(db: AsyncSession, order: OrderCreate, user_id: str):
    # Consulta os dados da pizza no serviço de pizza
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{PIZZA_SERVICE_URL}/pizzas/{order.pizza_id}",
                headers={"X-API-KEY": API_KEY},
            )
            response.raise_for_status()
            pizza = response.json()
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=404, detail="Pizza não encontrada")

    # Dados da pizza retornados do serviço externo
    valor_unitario = pizza["preco"]
    valor_total = valor_unitario * order.quantidade

    # Converte user_id (str) para int
    try:
        cliente_id = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="ID do usuário inválido"
        )

    # Cria e salva o pedido no banco de dados
    novo_pedido = Pedido(
        pizza_nome=order.pizza_nome,
        pizza_id=order.pizza_id,
        quantidade=order.quantidade,
        valor_unitario=valor_unitario,
        valor_total=valor_total,
        cliente_id=cliente_id,
    )
    db.add(novo_pedido)
    await db.commit()
    await db.refresh(novo_pedido)

    # Publica evento no Redis
    await publicar_pedido_criado(
        pedido_id=novo_pedido.id,
        cliente_id=cliente_id,
        total=valor_total,
    )

    # Retorna os dados do pedido criado (modelo de resposta)
    return novo_pedido


async def list_order(db: AsyncSession, user_id: int) -> OrderResponse:
    cliente_id = user_id
    result = await db.execute(select(Pedido).where(Pedido.cliente_id == cliente_id))
    return result.scalars().all()


async def delete_order(db: AsyncSession, id: int):
    result = await db.execute(select(Pedido).where(Pedido.id == id))
    pedido_del = result.scalar.one_or_none()

    if not pedido_del:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado"
        )
    await db.delete(pedido_del)
    await db.commit()
    return pedido_del
