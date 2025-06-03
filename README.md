# Projeto de Microserviços com Python, FastAPI, Redis e PostgreSQL

Este repositório contém uma aplicação distribuída baseada em microserviços, implementada com Python e FastAPI. O projeto é ideal para estudos de arquitetura de microsserviços, comunicação assíncrona e persistência de dados.

## 📦 Estrutura dos Serviços

- **pizza_service**: API que gerencia pizzas disponíveis.
- **order_service**: Recebe pedidos e publica eventos no Redis.
- **event_service**: Escuta eventos no canal Redis e grava os dados no banco.
- **customer_service**: CRUD completo de clientes com PostgreSQL.
- **notifier_service** (em construção): Futuro consumidor de notificações via HTTP.
- **postgres**: Banco de dados PostgreSQL para persistência.
- **redis**: Sistema de mensageria assíncrono entre os serviços.

## 🧪 Tecnologias Utilizadas

- Python 3.10+
- FastAPI
- SQLAlchemy (assíncrico)
- PostgreSQL
- Redis
- Docker + Docker Compose

## 🚀 Como executar o projeto

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/microservices-python.git
cd microservices-python
```

2. Suba os containers:

```bash
docker-compose up --build
```

3. Teste a criação de pedidos com o PowerShell:

```powershell
curl -X POST http://localhost:8000/orders `
  -H "Content-Type: application/json" `
  -d '{ "pizza_id": 1, "quantidade": 2 }'
```

## 🔁 Comunicação entre Serviços

- `order_service` publica um evento no Redis ao criar um pedido.
- `event_service` escuta o canal `pedido_criado`, processa o evento e grava no banco de dados.
- `notifier_service` (em breve) receberá notificações HTTP para alertas ou integração com clientes.

## 🗃️ Banco de Dados

- Tabelas criadas automaticamente com `SQLAlchemy`.
- Comando para criação (executado dentro do container):
```bash
docker exec -it event_service python criar_db.py
```

## ✅ Status

✔️ pizza_service, order_service, event_service e customer_service funcionando com Docker.
🛠️ notifier_service em fase de construção.

## 👨‍💻 Autor

Reinaldo de Jesus Santos
[LinkedIn](https://www.linkedin.com/in/dev-reinaldo)
