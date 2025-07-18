from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from schemas import OrderCreate, OrderResponse
from dependencies import get_current_user
from fastapi.openapi.utils import get_openapi

from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud import create_order, list_order, delete_order
from fastapi.responses import Response


app = FastAPI(title="Service Order", debug=True)


@app.post(
        "/orders",
        response_model=OrderCreate,
        status_code=status.HTTP_201_CREATED)
async def create_order_handler(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    return await create_order(db, order, user_id)


@app.get("/orders", response_model=List[OrderResponse])
async def listar_orders_handler(
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user)
):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado!"
        )

    pedidos = await list_order(db, user_id)

    if not pedidos:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return pedidos


@app.delete("/orders/{id}")
async def delete_order_handler(id: int, db: AsyncSession = Depends(get_db)):
    order_del = await delete_order(db, id)
    if not order_del:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail="Pedido não encontado")
    return {"message": "Pedido removido com sucesso"}


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
