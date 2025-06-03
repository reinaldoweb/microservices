import pytest
import respx
from httpx import Response
from fastapi.testclient import TestClient

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from main import app

client = TestClient(app)

@pytest.fixture
def order_payload():
    return{
        "pizza_id": 1,
        "quantidade": 2
    }

@respx.mock
def test_create_order_success(order_payload):
    # Simula a resposta do pizza-service
    respx.get("http://localhost:8001/pizzas/1").mock(
    return_value=Response(200, json={"id":1, "nome": "Margherita", "preco": 30.0})
    )
    response = client.post("orders", json=order_payload)
    assert response.status_code == 200
    data = response.json()

    assert data["pizza_nome"] == "Margherita"
    assert data["preco_unitario"] == 30.0
    assert data["quantidade"] == 2
    assert data["preco_total"] == 60.0

@respx.mock
def test_create_order_pizza_not_found(order_payload):
    # Simula erro 404 no pizza_service
    respx.get("http://localhost:8001/pizzas/1").mock(
    return_value=Response(404, json={"detail": "Pizza não encontrada"})
    )

    response = client.post("/orders", json=order_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Pizza não encontrada"