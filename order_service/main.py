from fastapi import Depends, FastAPI, HTTPException
from models import OrderRequest, OrderResponse
import httpx
from eventos import publicar_pedido_criado
from auth import verifica_usuario

app = FastAPI(debug=True)

PIZZA_SERVICE_URL = "http://pizza_service:8001"
API_KEY = "minha-chave-super-secreta"


@app.post("/orders", response_model=OrderResponse, dependencies=[
    Depends(verifica_usuario)])
async def create_order(order: OrderRequest):
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

    valor_unitario = pizza["preco"]
    valor_total = valor_unitario * order.quantidade

    # Id ficticio gerado para exemplo
    pedido_id = 123
    cliente_id = 1

    # Publica evento no Redis
    await publicar_pedido_criado(
        pedido_id=pedido_id,
        cliente_id=cliente_id,
        total=valor_total
        )

    return OrderResponse(
        pizza_nome=pizza["nome"],
        quantidade=order.quantidade,
        valor_unitario=valor_unitario,
        valor_total=valor_total,
    )
