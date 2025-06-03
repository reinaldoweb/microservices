import pytest
import respx
import json
from httpx import AsyncClient, Response  # CORRETO
from main import app  # ou de onde vem seu FastAPI()


@pytest.fixture
def order_payload():
    return {"pizza_id": 1, "quantidade": 2}


@pytest.mark.asyncio
@respx.mock
async def test_create_order_success(order_payload):
    respx.get("http://localhost:8001/pizzas/1").mock(
        return_value=Response(
            status_code=200,
            content=json.dumps({"id": 1, "nome": "Calabresa", "preco": 35.0}),
            headers={"Content-Type": "application/json"}
        )
    )

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/orders", json=order_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["pizza_nome"] == "Calabresa"
    assert data["quantidade"] == 2
    assert data["preco_unitario"] == 35.0
    assert data["preco_total"] == 70


@pytest.mark.asyncio
@respx.mock
async def test_create_order_pizza_not_found(order_payload):
    respx.get("http://localhost:8001/pizzas/1").mock(
        return_value=Response(
            status_code=404,
            content=json.dumps({"detail": "Pizza não encontrada"}),
            headers={"Content-Type": "application/json"}
        )
    )

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.post("/orders", json=order_payload)

    assert response.status_code == 404
    assert response.json()["detail"] == "Pizza não encontrada"
