from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException
from models import OrderRequest, OrderResponse
import httpx
from eventos import publicar_pedido_criado
from dependecies import get_current_user
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

app = FastAPI(debug=True)

load_dotenv()

PIZZA_SERVICE_URL = "http://pizza_service:8001"
API_KEY = "minha-chave-super-secreta"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@app.post("/orders", response_model=OrderResponse)
async def create_order(
        order: OrderRequest,
        user_id: str = Depends(get_current_user)):
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

    # Calcula o valor do pedido
    valor_unitario = pizza["preco"]
    valor_total = valor_unitario * order.quantidade

    # Simula dados do pedido no banco de dados
    pedido_id = str(uuid4())
    cliente_id = user_id

    # Publica evento no Redis
    await publicar_pedido_criado(
        pedido_id=pedido_id,
        cliente_id=cliente_id,
        total=valor_total,
    )

    # Retorna os dados do pedido criado
    return OrderResponse(
        pizza_nome=pizza["nome"],
        quantidade=order.quantidade,
        valor_unitario=valor_unitario,
        valor_total=valor_total,
    )


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Order Service API",
        version="1.0.0",
        description="API para criar pedidos de pizza com autenticação JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
