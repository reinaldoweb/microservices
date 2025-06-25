from fastapi import FastAPI
from customer import router as cliente_router

app = FastAPI()
app.include_router(cliente_router, prefix="/clientes", tags=["clientes"])
