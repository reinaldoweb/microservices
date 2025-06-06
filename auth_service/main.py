from fastapi import FastAPI
from auth import router as auth_router

app = FastAPI(title="Auth Service")

app.include_router(auth_router)