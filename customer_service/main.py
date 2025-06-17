from fastapi import FastAPI
from customer import router

app = FastAPI()
app.include_router(router)
